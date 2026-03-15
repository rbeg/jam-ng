---
id: index-et-data-views
title: Index et Data Views
sidebar_label: Index & Data Views
sidebar_position: 4
---

# Index et Data Views

## Qu'est-ce qu'un index Elasticsearch ?

Un index est l'unité de stockage d'Elasticsearch. Il regroupe des documents de même
nature — tous les logs applicatifs, toutes les traces APM, toutes les métriques JVM.
Chaque index a un **mapping** qui définit le type de chaque champ (keyword, text,
date, integer…).

## Qu'est-ce qu'une Data View Kibana ?

Une Data View est une vue Kibana sur un ou plusieurs index. Elle est nécessaire pour
interroger des données dans Discover ou les utiliser dans une visualisation. Une
Data View peut couvrir plusieurs index via un pattern avec wildcard (`logs-*`).

---

## Cartographie des index de la plateforme

### Index applicatifs

| Index | Contenu | Data View Kibana |
|---|---|---|
| `logs-*` | Logs ECS de tous les services | `Logs applicatifs` |
| `traces-apm-*` | Transactions, spans, errors APM | `APM Traces` |
| `metrics-apm-*` | Métriques JVM, système, agrégats | `APM Metrics` |

### Index infrastructure (gérés par l'équipe infrastructure)

| Index | Contenu |
|---|---|
| `metrics-kubernetes-*` | Métriques des pods et nœuds Kubernetes |
| `logs-kubernetes-*` | Logs système Kubernetes |

:::note
Les index métier (pipeline Logstash dédié) sont sur une instance Elasticsearch
distincte et ne sont pas listés ici. Se rapprocher de l'équipe responsable du
périmètre pour y accéder.
:::

---

## Quel index pour quelle question ?

| Question | Où chercher |
|---|---|
| Mes logs sont-ils bien formatés ECS ? | `logs-*` › Discover |
| Mon service est-il visible dans APM ? | `traces-apm-*` › Kibana APM |
| Quelle est la latence p95 de mon service ? | `traces-apm-*` › Kibana APM ou Dashboard |
| Quelle exception s'est produite sur cette trace ? | `traces-apm-*` › `processor.event: error` |
| Quel est l'état de la heap JVM de mon service ? | `metrics-apm-*` › Kibana APM › JVM |
| Quelle est la consommation CPU du pod ? | `metrics-kubernetes-*` › Grafana |
| Quel est le taux d'erreur sur le parcours checkout ? | `traces-apm-*` filtré sur `labels.business_use_case: checkout` |

---

## Conventions de nommage des index

Les index suivent les conventions Elastic Data Streams :

```
{type}-{dataset}-{namespace}

Exemples :
logs-payment-service-production
traces-apm-default
metrics-apm-default
```

Le champ `data_stream.dataset` dans chaque document permet d'identifier précisément
la source d'un document.

---

## Pour aller plus loin

- [Elastic — Data Streams](https://www.elastic.co/guide/en/elasticsearch/reference/current/data-streams.html)
- [Kibana — Data Views](https://www.elastic.co/guide/en/kibana/current/data-views.html)
