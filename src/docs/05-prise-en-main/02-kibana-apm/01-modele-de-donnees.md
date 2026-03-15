---
id: apm-modele-de-donnees
title: Modèle de données APM
sidebar_label: Modèle de données
sidebar_position: 1
---

# Modèle de données APM

## Comprendre la structure avant d'explorer

Kibana APM propose une interface de haut niveau — services, transactions, traces —
qui masque la structure sous-jacente. Cette abstraction est utile au quotidien, mais
elle devient un obstacle dès qu'on veut construire un dashboard personnalisé, écrire
une requête dans Discover, ou comprendre pourquoi une donnée attendue n'apparaît pas.

Cette page décrit la structure réelle des données APM dans Elasticsearch : quels index,
quels types de documents, quels champs clés.

:::note
La maîtrise de ce modèle de données est le prérequis pour construire des dashboards
APM personnalisés ou pour investiguer directement dans Kibana Discover sur les index
`traces-apm-*` et `metrics-apm-*`.
:::

---

## Vue d'ensemble des index APM

L'agent APM Elastic génère plusieurs types de documents, stockés dans des index
distincts. Sur notre plateforme, ces index suivent la convention de nommage
`traces-apm-*`, `metrics-apm-*` et `logs-apm-*`.

```
┌─────────────────────────────────────────────────────────────────┐
│                        Index APM                                │
├───────────────────────┬─────────────────────────────────────────┤
│  traces-apm-*         │  Transactions, Spans, Errors            │
├───────────────────────┼─────────────────────────────────────────┤
│  metrics-apm-*        │  Métriques JVM, système, custom         │
├───────────────────────┼─────────────────────────────────────────┤
│  logs-apm-*           │  Logs corrélés via trace.id             │
└───────────────────────┴─────────────────────────────────────────┘
```

---

## Les types de documents

### 📌 Transaction

La transaction est l'**unité de travail principale** dans APM. Elle représente une
opération de bout en bout du point de vue d'un service : le traitement d'une requête
HTTP entrante, la consommation d'un message Kafka, l'exécution d'un job planifié.

**Index** : `traces-apm-*` — **Champ discriminant** : `processor.event: transaction`

| Champ | Description | Exemple |
|---|---|---|
| `transaction.id` | Identifiant unique de la transaction | `00f067aa0ba902b7` |
| `trace.id` | Identifiant de la trace parente | `4bf92f3577b34da6a` |
| `transaction.name` | Nom de la transaction | `POST /api/v1/payments` |
| `transaction.type` | Type de transaction | `request`, `messaging`, `scheduled` |
| `transaction.duration.us` | Durée en microsecondes | `145230` |
| `transaction.result` | Résultat HTTP | `HTTP 2xx`, `HTTP 5xx` |
| `transaction.outcome` | Succès ou échec | `success`, `failure`, `unknown` |
| `service.name` | Service ayant traité la transaction | `payment-service` |
| `service.version` | Version du service | `2.3.1` |
| `service.environment` | Environnement | `production` |
| `labels.*` | Labels custom dont les labels métier | `labels.business_use_case` |

---

### 📌 Span

Un span représente une **sous-opération** à l'intérieur d'une transaction : un appel
SQL, un appel HTTP sortant vers un autre service, un accès cache, une opération Kafka.
Une transaction contient zéro ou plusieurs spans.

**Index** : `traces-apm-*` — **Champ discriminant** : `processor.event: span`

| Champ | Description | Exemple |
|---|---|---|
| `span.id` | Identifiant unique du span | `a2fb4a1d1a96d312` |
| `transaction.id` | Transaction parente | `00f067aa0ba902b7` |
| `trace.id` | Trace parente | `4bf92f3577b34da6a` |
| `span.name` | Nom de l'opération | `SELECT FROM orders` |
| `span.type` | Type de span | `db`, `external`, `messaging` |
| `span.subtype` | Sous-type | `postgresql`, `http`, `kafka` |
| `span.duration.us` | Durée en microsecondes | `23400` |
| `span.outcome` | Succès ou échec | `success`, `failure` |
| `destination.service.name` | Service ou ressource appelée | `postgresql` |

---

### 📌 Error

Un document error est créé à chaque **exception capturée** par l'agent APM, qu'elle
soit gérée ou non. Il est systématiquement corrélé à la transaction en cours.

**Index** : `traces-apm-*` — **Champ discriminant** : `processor.event: error`

| Champ | Description | Exemple |
|---|---|---|
| `error.id` | Identifiant unique de l'erreur | `5f4e3d2c1b0a9876` |
| `error.grouping_key` | Clé de regroupement des erreurs similaires | hash |
| `error.exception.type` | Type d'exception Java | `PaymentGatewayException` |
| `error.exception.message` | Message de l'exception | `Timeout après 3000ms` |
| `error.exception.stacktrace` | Stack trace complète | `…` |
| `transaction.id` | Transaction dans laquelle l'erreur s'est produite | `00f067aa0ba902b7` |
| `trace.id` | Trace parente | `4bf92f3577b34da6a` |

---

### 📌 Metric

Les documents metric contiennent les **métriques collectées en continu** par l'agent
APM : métriques JVM, métriques système, et métriques custom si définies.

**Index** : `metrics-apm-*` — **Champ discriminant** : `processor.event: metric`

**Métriques JVM**

| Champ | Description |
|---|---|
| `jvm.memory.heap.used` | Heap utilisée en bytes |
| `jvm.memory.heap.max` | Heap maximale en bytes |
| `jvm.gc.time` | Temps passé en garbage collection |
| `jvm.thread.count` | Nombre de threads actifs |

**Métriques système**

| Champ | Description |
|---|---|
| `system.cpu.total.norm.pct` | Utilisation CPU normalisée (0 à 1) |
| `system.memory.actual.used.bytes` | Mémoire système utilisée |

**Agrégats de transactions** (précalculés par l'agent)

| Champ | Description |
|---|---|
| `transaction.duration.histogram` | Distribution des durées de transaction |
| `span.destination.service.response_time.sum.us` | Temps de réponse cumulé vers une dépendance |

---

## Le modèle de corrélation

C'est le point le plus important à comprendre. Tous les documents APM — transactions,
spans, errors, metrics — partagent deux champs communs qui permettent de les relier
entre eux **et** avec les logs applicatifs :

```
trace.id          →  Identifie une trace complète de bout en bout
transaction.id    →  Identifie une transaction spécifique dans la trace
```

```
┌──────────────────────────────────────────────────────────────┐
│  trace.id: 4bf92f3577b34da6a                                 │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Transaction: POST /api/v1/payments                  │   │
│  │  transaction.id: 00f067aa0ba902b7                    │   │
│  │                                                      │   │
│  │  ├── Span: SELECT FROM accounts  (postgresql)       │   │
│  │  ├── Span: POST /risk-check      (http)             │   │
│  │  ├── Span: SEND payment.processed (kafka)           │   │
│  │  └── Error: PaymentGatewayException                 │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  Logs applicatifs corrélés (index logs-*)                    │
│  via les champs trace.id + transaction.id                    │
└──────────────────────────────────────────────────────────────┘
```

:::tip
Ce modèle permet depuis n'importe quel point d'entrée — un log, une transaction,
une erreur — de naviguer vers tous les autres documents liés à la même opération.
C'est la raison pour laquelle `log_correlation: true` est obligatoire dans la
configuration de l'agent APM.
:::

---

## Les types de transactions courants

Sur nos services Spring Boot, les types de transactions les plus fréquents sont :

| `transaction.type` | Contexte | Exemple |
|---|---|---|
| `request` | Requête HTTP entrante | `POST /api/v1/payments` |
| `messaging` | Consommation d'un message Kafka | `RECEIVE payment.requested` |
| `scheduled` | Job planifié Spring `@Scheduled` | `processExpiredOrders` |
| `backgroundjob` | Tâche asynchrone | `CompletableFuture` |

---

## Interroger les données APM dans Discover

Il est tout à fait possible d'interroger les index APM directement dans
**Kibana › Discover**, en sélectionnant la Data View `traces-apm-*` ou `metrics-apm-*`.

Quelques filtres utiles pour commencer :

```
# Toutes les transactions en erreur d'un service
processor.event: "transaction"
AND service.name: "payment-service"
AND transaction.outcome: "failure"

# Tous les spans vers PostgreSQL de plus de 500ms
processor.event: "span"
AND span.subtype: "postgresql"
AND span.duration.us > 500000

# Toutes les erreurs d'un type donné
processor.event: "error"
AND error.exception.type: "PaymentGatewayException"

# Retrouver tous les documents d'une trace
trace.id: "4bf92f3577b34da6a3ce929d0e0e4736"
```

:::note
Les durées dans APM sont exprimées en **microsecondes** (`us`).
500ms = 500 000µs, 1s = 1 000 000µs.
:::

---

## Pour aller plus loin

La documentation officielle Elastic couvre le schéma complet des données APM
et les fonctionnalités avancées :

- [Data Model — Vue d'ensemble](https://www.elastic.co/guide/en/apm/guide/current/data-model.html)
- [Data Model — Transactions](https://www.elastic.co/guide/en/apm/guide/current/data-model-transactions.html)
- [Data Model — Spans](https://www.elastic.co/guide/en/apm/guide/current/data-model-spans.html)
- [Data Model — Errors](https://www.elastic.co/guide/en/apm/guide/current/data-model-errors.html)
- [Data Model — Metrics](https://www.elastic.co/guide/en/apm/guide/current/data-model-metrics.html)
- [Corrélation logs et traces — Agent Java](https://www.elastic.co/guide/en/apm/agent/java/current/log-correlation.html)
- [Configuration de l'agent APM Java](https://www.elastic.co/guide/en/apm/agent/java/current/configuration.html)
