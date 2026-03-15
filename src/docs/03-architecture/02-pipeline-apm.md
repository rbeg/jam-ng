---
id: pipeline-apm
title: Pipeline APM
sidebar_label: Pipeline APM
sidebar_position: 2
---

# Pipeline APM

## Vue d'ensemble

L'agent APM embarqué dans chaque service Spring Boot collecte en continu les traces,
les métriques et les erreurs, et les transmet à l'APM Server de la plateforme. Ce
pipeline est distinct du pipeline de logs, mais les deux sont corrélés via les champs
`trace.id` et `transaction.id`.

```
Application Spring Boot
+ Agent APM (embarqué)
        │
        │  traces, spans, errors, métriques JVM
        ▼
  APM Server
  (plateforme)
        │
        │  traitement et enrichissement
        ▼
  Elasticsearch
  (index traces-apm-*, metrics-apm-*)
        │
        ▼
  Kibana › APM
  Kibana › Dashboards
```

---

## Responsabilités

| Qui | Quoi |
|---|---|
| **Équipe plateforme** | APM Server, configuration de l'ingestion, index, Data Views |
| **Équipes produit** | Configuration de l'agent dans l'application, `service.name`, `service.version`, `user.id`, labels métier |

---

## Ce que l'agent collecte

L'agent APM Java fonctionne par instrumentation automatique. Il intercepte les appels
entrants et sortants sans modification du code applicatif :

- **Transactions** : toute requête HTTP entrante, tout message Kafka consommé,
  tout job `@Scheduled`
- **Spans** : appels SQL (JDBC), appels HTTP sortants (RestTemplate, WebClient),
  opérations Kafka produites
- **Errors** : toute exception non gérée, et les exceptions gérées si explicitement
  capturées via l'API publique
- **Métriques JVM** : heap, GC, threads — collectées toutes les 30 secondes par défaut

:::note
Le modèle de données complet (transactions, spans, errors, metrics) est documenté
dans [Prise en main › Modèle de données APM](../05-prise-en-main/02-kibana-apm/01-modele-de-donnees).
:::

---

## Flux de corrélation avec les logs

Quand `log_correlation: true` est activé dans la configuration de l'agent, celui-ci
injecte automatiquement `trace.id` et `transaction.id` dans le contexte de chaque
log produit pendant une transaction. Ces champs apparaissent dans les logs ECS et
permettent de naviguer depuis un log vers sa trace APM, et inversement.

```
Log ECS (index logs-*)          Trace APM (index traces-apm-*)
─────────────────────           ──────────────────────────────
trace.id: 4bf92f3577b3   ────►  trace.id: 4bf92f3577b3
transaction.id: 00f067   ────►  transaction.id: 00f067
```

Cette corrélation est le fondement de l'investigation multi-sources sur la plateforme.

---

## Pour aller plus loin

- [Standards › APM — Configuration](../02-standards/02-apm)
- [Modèle de données APM](../05-prise-en-main/02-kibana-apm/01-modele-de-donnees)
- [Corrélation entre les données](./05-correlation)
