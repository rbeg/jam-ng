---
id: pipeline-logs
title: Pipeline des logs applicatifs
sidebar_label: Pipeline logs
sidebar_position: 1
---

# Pipeline des logs applicatifs

## Vue d'ensemble

Les logs de tous les services Spring Boot déployés sur Kubernetes sont collectés,
routés et indexés dans Elasticsearch de façon **entièrement automatique**. Les équipes
n'ont pas à gérer ce pipeline — il est industrialisé et maintenu par l'équipe
plateforme.

La responsabilité des équipes se limite à produire des logs **au bon format** (ECS)
sur la sortie standard du conteneur. Le reste est pris en charge.

```
Application Spring Boot
        │
        │  stdout (format ECS JSON)
        ▼
  Pod Kubernetes
        │
        │  collecte automatique
        ▼
  Logging Flow
  (agent de collecte sur chaque nœud)
        │
        │  routage et enrichissement
        ▼
  Elasticsearch
  (index logs-*)
        │
        ▼
  Kibana › Discover
  Kibana › Dashboards
```

---

## Étapes du pipeline

### 1. Production des logs

L'application écrit ses logs sur `stdout` au format JSON ECS. C'est la seule
responsabilité de l'équipe de développement dans ce pipeline.

:::warning
Ne jamais écrire les logs dans un fichier à l'intérieur du conteneur. Kubernetes
ne collecte que la sortie standard (`stdout` / `stderr`). Un log écrit dans un fichier
est un log perdu.
:::

### 2. Collecte par le Logging Flow

Un agent de collecte tourne sur chaque nœud Kubernetes. Il capture automatiquement
la sortie standard de tous les pods en cours d'exécution et la transmet au pipeline
d'ingestion.

Les logs sont enrichis à ce niveau avec des métadonnées Kubernetes :
`kubernetes.namespace`, `kubernetes.pod.name`, `kubernetes.node.name`, etc.

### 3. Indexation dans Elasticsearch

Les logs sont indexés dans Elasticsearch sous la convention `logs-*`. L'index de
destination peut varier selon le namespace Kubernetes ou l'environnement.

### 4. Restitution dans Kibana

Les logs sont consultables dans **Kibana › Discover** via les Data Views configurées
sur les index `logs-*`.

---

## Ce que le pipeline ajoute automatiquement

En plus du contenu ECS produit par l'application, le pipeline enrichit chaque document
avec des métadonnées d'infrastructure :

| Champ | Description |
|---|---|
| `kubernetes.namespace` | Namespace Kubernetes du pod |
| `kubernetes.pod.name` | Nom du pod |
| `kubernetes.node.name` | Nœud Kubernetes sur lequel tourne le pod |
| `kubernetes.labels.*` | Labels Kubernetes du pod |
| `host.name` | Nom de l'hôte |

Ces champs sont disponibles dans Discover et peuvent être utilisés pour filtrer
les logs par namespace ou par pod lors d'une investigation infrastructure.

---

## Pour aller plus loin

- [Index et Data Views](./04-index-et-data-views)
- [Corrélation entre les données](./05-correlation)
- [Kibana › Discover — Prise en main](../05-prise-en-main/01-kibana-discover)
