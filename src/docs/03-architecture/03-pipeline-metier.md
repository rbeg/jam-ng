---
id: pipeline-metier
title: Pipeline des indicateurs métier
sidebar_label: Pipeline métier
sidebar_position: 3
---

# Pipeline des indicateurs métier

## Un pipeline distinct

Les indicateurs métier — volumes de transactions, KPIs business, suivi de parcours
utilisateur — sont alimentés par un pipeline **entièrement séparé** du pipeline de
logs applicatifs et d'APM. Ce pipeline ne fait pas partie du périmètre de ce cadre
de référence, mais il coexiste sur la même infrastructure.

:::note
Ce pipeline est géré par périmètre fonctionnel, avec ses propres règles d'accès et
d'habilitation. Pour obtenir un accès aux dashboards métier, se rapprocher de l'équipe
responsable du périmètre concerné.
:::

---

## Architecture

Chaque périmètre métier dispose de son propre pipeline Logstash et de sa propre
instance ELK, indépendants de l'instance applicative :

```
Sources métier                 Pipeline dédié          Instance ELK métier
──────────────────────────────────────────────────────────────────────────
Bases de données          →                       →
Topics Kafka              →   Logstash             →   Elasticsearch (B)
Autres sources métier     →   (par périmètre)     →   → Kibana (B)
```

Cette séparation garantit :

- l'**isolation** des données métier vis-à-vis des données techniques
- une **gouvernance autonome** par périmètre, avec ses propres règles d'accès
- la **scalabilité indépendante** de chaque pipeline

---

## Lien avec l'observabilité applicative

Même si les deux instances ELK sont distinctes, les deux périmètres sont
complémentaires. Un pic d'abandons détecté dans un dashboard métier peut s'expliquer
par une dégradation visible dans APM. Les **labels métier** dans les traces et les
logs applicatifs (`labels.business_use_case`, `labels.business_criticality`) servent
précisément à maintenir ce lien sémantique entre les deux mondes.
