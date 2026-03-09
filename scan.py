# #!/usr/bin/env python3
“””
dep-observatory/scanner/scan.py

Scanne tous les projets GitLab d’une instance pour extraire les versions
de dépendances Maven (pom.xml) et npm (package.json).
Enrichit ensuite avec les dernières versions disponibles (Maven Central + npm registry).
Produit un fichier deps.json consommé par le dashboard.

Variables d’environnement requises :
GITLAB_URL        ex: https://gitlab.monentreprise.fr
GITLAB_TOKEN      Personal Access Token (scope: read_api)
GITLAB_GROUPS     (optionnel) IDs/noms de groupes séparés par virgule. Si absent → tous les projets accessibles.
TARGET_LIBS_MAVEN (optionnel) Liste de artifactId à surveiller, séparés par virgule.
Si absent → toutes les dépendances directes du pom.xml.
TARGET_LIBS_NPM   (optionnel) Idem pour npm.
MAX_WORKERS       (optionnel, défaut=10) Parallélisme HTTP.
“””

import os
import sys
import json
import logging
import hashlib
import time
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import xml.etree.ElementTree as ET

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ─── Logging ──────────────────────────────────────────────────────────────────

logging.basicConfig(
level=logging.INFO,
format=”%(asctime)s [%(levelname)s] %(message)s”,
datefmt=”%H:%M:%S”,
)
log = logging.getLogger(**name**)

# ─── Config ───────────────────────────────────────────────────────────────────

GITLAB_URL    = os.environ[“GITLAB_URL”].rstrip(”/”)
GITLAB_TOKEN  = os.environ[“GITLAB_TOKEN”]
GITLAB_GROUPS = [g.strip() for g in os.environ.get(“GITLAB_GROUPS”, “”).split(”,”) if g.strip()]
MAX_WORKERS   = int(os.environ.get(“MAX_WORKERS”, “10”))
OUTPUT_FILE   = os.environ.get(“OUTPUT_FILE”, “deps.json”)

# Librairies Maven à surveiller (si vide → toutes)

TARGET_MAVEN_RAW = os.environ.get(“TARGET_LIBS_MAVEN”, “”)
TARGET_MAVEN = set(x.strip() for x in TARGET_MAVEN_RAW.split(”,”) if x.strip()) if TARGET_MAVEN_RAW else set()

# Librairies npm à surveiller (si vide → toutes sauf @types/*)

TARGET_NPM_RAW = os.environ.get(“TARGET_LIBS_NPM”, “”)
TARGET_NPM = set(x.strip() for x in TARGET_NPM_RAW.split(”,”) if x.strip()) if TARGET_NPM_RAW else set()

# Mapping groupId Maven pour une meilleure lisibilité

KNOWN_GROUP_IDS = {
“spring-boot-starter-parent”: “org.springframework.boot”,
“spring-boot”:                “org.springframework.boot”,
“spring-cloud-dependencies”:  “org.springframework.cloud”,
“kafka-clients”:              “org.apache.kafka”,
“kafka-streams”:              “org.apache.kafka”,
“avro”:                       “org.apache.avro”,
“lombok”:                     “org.projectlombok”,
“junit-jupiter”:              “org.junit.jupiter”,
“junit-jupiter-api”:          “org.junit.jupiter”,
“micrometer-core”:            “io.micrometer”,
“log4j-core”:                 “org.apache.logging.log4j”,
“jackson-databind”:           “com.fasterxml.jackson.core”,
“hibernate-core”:             “org.hibernate.orm”,
“flyway-core”:                “org.flywaydb”,
“liquibase-core”:             “org.liquibase”,
“testcontainers”:             “org.testcontainers”,
“resilience4j-spring-boot2”:  “io.github.resilience4j”,
“resilience4j-spring-boot3”:  “io.github.resilience4j”,
“opentelemetry-api”:          “io.opentelemetry”,
}

# ─── HTTP Session avec retry ──────────────────────────────────────────────────

def make_session(token: str | None = None) -> requests.Session:
session = requests.Session()
retry = Retry(
total=4,
backoff_factor=1.0,
status_forcelist=[429, 500, 502, 503, 504],
allowed_methods=[“GET”],
)
adapter = HTTPAdapter(max_retries=retry)
session.mount(“https://”, adapter)
session.mount(“http://”, adapter)
if token:
session.headers.update({“PRIVATE-TOKEN”: token})
session.headers.update({“Accept”: “application/json”})
return session

gl_session = make_session(GITLAB_TOKEN)
ext_session = make_session()  # pas de token pour Maven Central / npm

# ─── GitLab API helpers ───────────────────────────────────────────────────────

def gitlab_get(path: str, params: dict | None = None) -> dict | list:
url = f”{GITLAB_URL}/api/v4{path}”
r = gl_session.get(url, params=params, timeout=15)
r.raise_for_status()
return r.json()

def gitlab_paginate(path: str, params: dict | None = None) -> list:
“”“Récupère toutes les pages d’un endpoint GitLab paginé.”””
params = dict(params or {})
params.setdefault(“per_page”, 100)
page = 1
results = []
while True:
params[“page”] = page
r = gl_session.get(f”{GITLAB_URL}/api/v4{path}”, params=params, timeout=20)
r.raise_for_status()
data = r.json()
if not data:
break
results.extend(data)
total_pages = int(r.headers.get(“X-Total-Pages”, 1))
if page >= total_pages:
break
page += 1
return results

def get_file_content(project_id: int, file_path: str, ref: str = “HEAD”) -> str | None:
“”“Récupère le contenu brut d’un fichier dans un projet GitLab.”””
import urllib.parse
encoded = urllib.parse.quote(file_path, safe=””)
try:
r = gl_session.get(
f”{GITLAB_URL}/api/v4/projects/{project_id}/repository/files/{encoded}/raw”,
params={“ref”: ref},
timeout=15,
)
if r.status_code == 404:
return None
r.raise_for_status()
return r.text
except Exception as e:
log.debug(f”  [{project_id}] {file_path} → {e}”)
return None

# ─── Collecte des projets ─────────────────────────────────────────────────────

def get_all_projects() -> list[dict]:
“”“Retourne tous les projets accessibles (filtrés par groupe si configuré).”””
projects = []
if GITLAB_GROUPS:
for group in GITLAB_GROUPS:
log.info(f”Récupération des projets du groupe : {group}”)
try:
# Essai par ID numérique d’abord, puis par nom encodé
import urllib.parse
path = f”/groups/{urllib.parse.quote(str(group), safe=’’)}/projects”
grp_projects = gitlab_paginate(path, {
“include_subgroups”: “true”,
“archived”: “false”,
“with_programming_language”: “”,
})
projects.extend(grp_projects)
log.info(f”  → {len(grp_projects)} projets trouvés dans {group}”)
except Exception as e:
log.warning(f”Groupe {group} inaccessible : {e}”)
else:
log.info(“Récupération de tous les projets accessibles…”)
projects = gitlab_paginate(”/projects”, {
“membership”: “true”,
“archived”: “false”,
“order_by”: “last_activity_at”,
})
log.info(f”  → {len(projects)} projets trouvés au total”)

```
# Dédoublonnage par ID
seen = set()
unique = []
for p in projects:
    if p["id"] not in seen:
        seen.add(p["id"])
        unique.append(p)
return unique
```

# ─── Parsing pom.xml ──────────────────────────────────────────────────────────

NS = {“m”: “http://maven.apache.org/POM/4.0.0”}

def _resolve_property(value: str, props: dict) -> str:
“”“Résout les références ${property} dans les versions Maven.”””
if not value or not value.startswith(”${”):
return value
key = value[2:-1]  # enlève ${ et }
return props.get(key, value)

def parse_pom(content: str) -> list[dict]:
“””
Parse un pom.xml et retourne la liste des dépendances avec leur version.
Gère : parent, properties, dependencies, dependencyManagement.
“””
deps = []
try:
root = ET.fromstring(content)
except ET.ParseError as e:
log.debug(f”ParseError pom.xml : {e}”)
return deps

```
def tag(name):
    return f"{{{NS['m']}}}{name}" if "{" not in root.tag else name

# Détecter si le namespace est présent
has_ns = "{http://maven.apache.org/POM/4.0.0}" in root.tag

def find(el, path):
    if has_ns:
        parts = path.split("/")
        return el.find("/".join(f"{{{NS['m']}}}{p}" for p in parts))
    return el.find(path)

def findall(el, path):
    if has_ns:
        parts = path.split("/")
        return el.findall("/".join(f"{{{NS['m']}}}{p}" for p in parts))
    return el.findall(path)

def text(el, path):
    node = find(el, path)
    return node.text.strip() if node is not None and node.text else None

# 1. Collecte des properties
props = {}
props_node = find(root, "properties")
if props_node is not None:
    for child in props_node:
        local = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        if child.text:
            props[local] = child.text.strip()

# Ajoute java.version et project.* comme properties courantes
java_ver = props.get("java.version", props.get("maven.compiler.source", ""))
if java_ver:
    props["java.version"] = java_ver

# 2. Parent
parent = find(root, "parent")
if parent is not None:
    artifact = text(parent, "artifactId")
    version  = text(parent, "version")
    group    = text(parent, "groupId")
    if artifact and version:
        deps.append({
            "artifactId": artifact,
            "groupId": group or KNOWN_GROUP_IDS.get(artifact, ""),
            "version": _resolve_property(version, props),
            "scope": "parent",
        })

# 3. Dépendances directes + dependencyManagement
for section_path in ["dependencies/dependency", "dependencyManagement/dependencies/dependency"]:
    for dep in findall(root, section_path):
        artifact = text(dep, "artifactId")
        group    = text(dep, "groupId")
        version  = text(dep, "version")
        scope    = text(dep, "scope") or "compile"
        if artifact and version:
            resolved = _resolve_property(version, props)
            if resolved and not resolved.startswith("${"):
                deps.append({
                    "artifactId": artifact,
                    "groupId": group or KNOWN_GROUP_IDS.get(artifact, ""),
                    "version": resolved,
                    "scope": scope,
                })

# Dédoublonnage par artifactId (garde la première occurrence = plus spécifique)
seen = set()
unique = []
for d in deps:
    if d["artifactId"] not in seen:
        seen.add(d["artifactId"])
        unique.append(d)

# Filtrage si TARGET_MAVEN configuré
if TARGET_MAVEN:
    unique = [d for d in unique if d["artifactId"] in TARGET_MAVEN]

return unique
```

# ─── Parsing package.json ─────────────────────────────────────────────────────

def parse_package_json(content: str) -> list[dict]:
“”“Parse un package.json et retourne les dépendances avec version.”””
deps = []
try:
pkg = json.loads(content)
except json.JSONDecodeError:
return deps

```
# On prend dependencies + devDependencies (Angular est souvent en devDep)
all_deps = {}
all_deps.update(pkg.get("dependencies", {}))
all_deps.update(pkg.get("devDependencies", {}))

for name, version in all_deps.items():
    # Ignore les packages @types, les liens locaux et les wildcards purs
    if name.startswith("@types/"):
        continue
    if version.startswith(("file:", "link:", "github:", "git+")):
        continue
    # Nettoie les préfixes semver (^, ~, >=, etc.)
    clean_version = version.lstrip("^~>=<").split(" ")[0].split("-")[0]
    if not clean_version or clean_version == "*":
        continue

    if TARGET_NPM and name not in TARGET_NPM:
        continue

    deps.append({
        "name": name,
        "version": clean_version,
        "raw_version": version,
    })

return deps
```

# ─── Scan d’un projet ─────────────────────────────────────────────────────────

def scan_project(project: dict) -> dict | None:
“””
Scanne un projet GitLab : cherche pom.xml et/ou package.json à la racine
(et dans les sous-modules Maven classiques).
Retourne un dict avec les dépendances trouvées, ou None si rien d’intéressant.
“””
pid    = project[“id”]
name   = project[“path_with_namespace”]
branch = project.get(“default_branch”) or “HEAD”

```
found_deps = []

# ── Maven : pom.xml ──
pom_content = get_file_content(pid, "pom.xml", branch)
if pom_content:
    maven_deps = parse_pom(pom_content)
    for d in maven_deps:
        found_deps.append({
            "ecosystem": "maven",
            "lib":       d["artifactId"],
            "groupId":   d.get("groupId", ""),
            "version":   d["version"],
            "scope":     d.get("scope", "compile"),
        })
    log.debug(f"  {name} → {len(maven_deps)} dépendances Maven")

# ── npm : package.json ──
pkg_content = get_file_content(pid, "package.json", branch)
if pkg_content:
    npm_deps = parse_package_json(pkg_content)
    for d in npm_deps:
        found_deps.append({
            "ecosystem": "npm",
            "lib":       d["name"],
            "groupId":   "",
            "version":   d["version"],
            "scope":     "dependencies",
        })
    log.debug(f"  {name} → {len(npm_deps)} dépendances npm")

if not found_deps:
    return None

# Récupère le namespace/groupe pour enrichir les métadonnées
namespace = project.get("namespace", {})

return {
    "project_id":   pid,
    "project":      project["path"],
    "namespace":    name,
    "team":         namespace.get("name", ""),
    "web_url":      project.get("web_url", ""),
    "last_activity": project.get("last_activity_at", ""),
    "dependencies": found_deps,
}
```

# ─── Enrichissement : version latest ─────────────────────────────────────────

_latest_cache: dict[str, str | None] = {}

def get_latest_maven(artifact_id: str, group_id: str) -> str | None:
“”“Interroge Maven Central pour la dernière version stable.”””
cache_key = f”maven:{group_id}:{artifact_id}”
if cache_key in _latest_cache:
return _latest_cache[cache_key]

```
# Stratégie 1 : groupId + artifactId
queries = []
if group_id:
    queries.append(f"g:{group_id}+AND+a:{artifact_id}")
queries.append(f"a:{artifact_id}")

for q in queries:
    try:
        r = ext_session.get(
            "https://search.maven.org/solrsearch/select",
            params={"q": q, "rows": "5", "wt": "json", "core": "gav"},
            timeout=10,
        )
        if r.status_code == 200:
            data = r.json()
            docs = data.get("response", {}).get("docs", [])
            # Filtre les versions stables (pas de -SNAPSHOT, -alpha, -beta, -RC)
            stable = [
                d["v"] for d in docs
                if not any(x in d.get("v","").lower() for x in
                           ["snapshot","alpha","beta","-rc",".rc","milestone","m1","m2","m3"])
            ]
            if stable:
                _latest_cache[cache_key] = stable[0]
                return stable[0]
    except Exception as e:
        log.debug(f"Maven Central error for {artifact_id}: {e}")
    time.sleep(0.1)  # rate limit doux

_latest_cache[cache_key] = None
return None
```

def get_latest_npm(package_name: str) -> str | None:
“”“Interroge le registry npm pour la dernière version stable.”””
cache_key = f”npm:{package_name}”
if cache_key in _latest_cache:
return _latest_cache[cache_key]

```
try:
    import urllib.parse
    encoded = urllib.parse.quote(package_name, safe="@/")
    r = ext_session.get(
        f"https://registry.npmjs.org/{encoded}/latest",
        timeout=10,
    )
    if r.status_code == 200:
        data = r.json()
        version = data.get("version")
        _latest_cache[cache_key] = version
        return version
    elif r.status_code == 404:
        # Essai avec le endpoint principal (dist-tags)
        r2 = ext_session.get(
            f"https://registry.npmjs.org/{encoded}",
            timeout=10,
        )
        if r2.status_code == 200:
            data = r2.json()
            version = data.get("dist-tags", {}).get("latest")
            _latest_cache[cache_key] = version
            return version
except Exception as e:
    log.debug(f"npm registry error for {package_name}: {e}")

_latest_cache[cache_key] = None
return None
```

# ─── Calcul du score d’obsolescence ──────────────────────────────────────────

def parse_semver(v: str) -> tuple[int, int, int]:
“”“Parse une version semver en tuple (major, minor, patch).”””
if not v:
return (0, 0, 0)
# Nettoie les suffixes non numériques
clean = v.split(”-”)[0].split(”+”)[0]
parts = clean.split(”.”)
try:
major = int(parts[0]) if len(parts) > 0 else 0
minor = int(parts[1]) if len(parts) > 1 else 0
patch = int(parts[2]) if len(parts) > 2 else 0
return (major, minor, patch)
except (ValueError, IndexError):
return (0, 0, 0)

def compute_obsolescence(current: str, latest: str) -> dict:
“””
Calcule le score d’obsolescence (0-100) et les métriques de retard.
Score = min(100, majors_lag * 30 + minors_lag * 5 + patches_lag * 1)
Statut :
0-20  → ok
21-45 → minor
46-75 → major
76+   → critical
“””
if not latest:
return {“score”: 0, “status”: “unknown”, “majors_lag”: 0, “minors_lag”: 0, “patches_lag”: 0}

```
c = parse_semver(current)
l = parse_semver(latest)

majors_lag  = max(0, l[0] - c[0])
minors_lag  = max(0, l[1] - c[1]) if majors_lag == 0 else 0
patches_lag = max(0, l[2] - c[2]) if majors_lag == 0 and minors_lag == 0 else 0

score = min(100, majors_lag * 30 + minors_lag * 5 + patches_lag * 1)

if score >= 76:
    status = "critical"
elif score >= 46:
    status = "major"
elif score >= 21:
    status = "minor"
else:
    status = "ok"

return {
    "score":       score,
    "status":      status,
    "majors_lag":  majors_lag,
    "minors_lag":  minors_lag,
    "patches_lag": patches_lag,
}
```

# ─── Enrichissement batch ─────────────────────────────────────────────────────

def enrich_with_latest(all_projects: list[dict]) -> list[dict]:
“””
Pour chaque dépendance de chaque projet, récupère la version latest
et calcule le score d’obsolescence.
Utilise un cache pour ne pas appeler N fois la même lib.
“””
# 1. Collecte des libs uniques à enrichir
unique_libs: dict[str, dict] = {}  # clé → {ecosystem, lib, groupId}
for proj in all_projects:
for dep in proj.get(“dependencies”, []):
key = f”{dep[‘ecosystem’]}:{dep[‘lib’]}”
if key not in unique_libs:
unique_libs[key] = {
“ecosystem”: dep[“ecosystem”],
“lib”:       dep[“lib”],
“groupId”:   dep.get(“groupId”, “”),
}

```
log.info(f"Enrichissement de {len(unique_libs)} librairies uniques...")

# 2. Fetch latest en parallèle
latest_versions: dict[str, str | None] = {}

def fetch_latest(key: str, meta: dict) -> tuple[str, str | None]:
    if meta["ecosystem"] == "maven":
        v = get_latest_maven(meta["lib"], meta["groupId"])
    else:
        v = get_latest_npm(meta["lib"])
    return key, v

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
    futures = {pool.submit(fetch_latest, k, v): k for k, v in unique_libs.items()}
    done = 0
    for fut in as_completed(futures):
        key, version = fut.result()
        latest_versions[key] = version
        done += 1
        if done % 20 == 0:
            log.info(f"  {done}/{len(unique_libs)} librairies enrichies...")

log.info(f"  ✓ {len(latest_versions)} librairies enrichies")

# 3. Injection dans les projets
for proj in all_projects:
    for dep in proj.get("dependencies", []):
        key = f"{dep['ecosystem']}:{dep['lib']}"
        latest = latest_versions.get(key)
        dep["latest"] = latest or dep["version"]  # fallback sur current si inconnu
        dep["latest_found"] = latest is not None
        obs = compute_obsolescence(dep["version"], dep["latest"])
        dep.update(obs)

return all_projects
```

# ─── Statistiques globales ────────────────────────────────────────────────────

def compute_summary(all_projects: list[dict]) -> dict:
all_deps = [dep for proj in all_projects for dep in proj.get(“dependencies”, [])]

```
by_status = {"ok": 0, "minor": 0, "major": 0, "critical": 0, "unknown": 0}
for dep in all_deps:
    by_status[dep.get("status", "unknown")] += 1

critical_projects = set(
    proj["project"]
    for proj in all_projects
    for dep in proj.get("dependencies", [])
    if dep.get("status") == "critical"
)

return {
    "total_projects":   len(all_projects),
    "total_deps":       len(all_deps),
    "by_status":        by_status,
    "critical_projects_count": len(critical_projects),
    "critical_projects": sorted(critical_projects),
    "scan_date": datetime.now(timezone.utc).isoformat(),
}
```

# ─── Main ──────────────────────────────────────────────────────────────────────

def main():
log.info(”=” * 60)
log.info(“DEP-OBSERVATORY — Scan démarré”)
log.info(f”  GitLab : {GITLAB_URL}”)
log.info(f”  Groupes : {GITLAB_GROUPS or ‘tous’}”)
log.info(f”  Libs Maven ciblées : {TARGET_MAVEN or ‘toutes’}”)
log.info(f”  Libs npm ciblées : {TARGET_NPM or ‘toutes’}”)
log.info(”=” * 60)

```
# 1. Récupère tous les projets
projects_meta = get_all_projects()
log.info(f"→ {len(projects_meta)} projets à scanner")

# 2. Scan en parallèle
scanned = []
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
    futures = {pool.submit(scan_project, p): p for p in projects_meta}
    done = 0
    for fut in as_completed(futures):
        result = fut.result()
        if result:
            scanned.append(result)
        done += 1
        if done % 20 == 0:
            log.info(f"  {done}/{len(projects_meta)} projets scannés ({len(scanned)} avec dépendances)...")

log.info(f"→ {len(scanned)} projets avec dépendances détectées")

# 3. Enrichissement avec les versions latest
scanned = enrich_with_latest(scanned)

# 4. Calcul du summary
summary = compute_summary(scanned)

# 5. Sortie JSON
output = {
    "summary":  summary,
    "projects": scanned,
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

log.info(f"✓ Résultats écrits dans {OUTPUT_FILE}")
log.info(f"  {summary['total_projects']} projets · {summary['total_deps']} dépendances")
log.info(f"  🔴 Critiques : {summary['by_status']['critical']}")
log.info(f"  🟠 Majeures  : {summary['by_status']['major']}")
log.info(f"  🟡 Mineures  : {summary['by_status']['minor']}")
log.info(f"  🟢 À jour    : {summary['by_status']['ok']}")
log.info("=" * 60)
```

if **name** == “**main**”:
main()