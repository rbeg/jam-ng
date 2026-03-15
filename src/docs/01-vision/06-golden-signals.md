---
id: golden-signals
title: Les Golden Signals
sidebar_label: Golden Signals
sidebar_position: 6
---

# Les Golden Signals

## Origine

Le concept des Golden Signals vient du livre **Site Reliability Engineering** de Google.
Il part d'un constat simple : dans un système distribué complexe, on ne peut pas tout
surveiller. Il faut choisir les indicateurs qui donnent la vision la plus fidèle possible
de l'état d'un service, avec le minimum de bruit.

Google en a identifié quatre. Ce sont les **quatre questions fondamentales** auxquelles
on doit pouvoir répondre sur n'importe quel service en production, à tout moment.

## Les quatre signaux

### ⏱️ Latence — *"Est-ce que c'est rapide ?"*

Le temps nécessaire pour traiter une requête. On distingue la latence des requêtes
réussies de celle des requêtes en erreur — une distinction importante : une requête
qui échoue immédiatement peut afficher une latence très faible et masquer un problème
réel si on ne sépare pas les deux.

**Ce qu'on surveille** : p50, p95, p99 — pas uniquement la moyenne, qui lisse les pics
et donne une fausse impression de stabilité.

:::warning
Une moyenne à 200ms peut cacher un p99 à 4 secondes. Ce sont ces 1% d'utilisateurs
qui appellent le support.
:::

### 🚦 Trafic — *"Quelle est la charge ?"*

Le volume de demandes que reçoit le service. Selon le type de service, cela peut être
des requêtes HTTP par seconde, des messages consommés par seconde, ou des transactions
métier par minute.

Le trafic est le **signal de contexte**. Une latence qui monte sans augmentation de
trafic n'a pas la même cause qu'une latence qui monte pendant un pic de charge.

### ❌ Taux d'erreur — *"Est-ce que ça fonctionne ?"*

La proportion de requêtes qui se terminent en erreur. On distingue :

- Les erreurs **explicites** : codes HTTP 5xx, exceptions non gérées
- Les erreurs **implicites** : codes HTTP 2xx mais réponse métier en échec
  *(ex : `{"status": "KO"}` retourné avec un 200)*

:::warning
Les erreurs implicites sont souvent les plus dangereuses car elles ne déclenchent pas
les alertes classiques. C'est là que les labels métier et les logs d'événements business
prennent toute leur valeur.
:::

### 📊 Saturation — *"Est-ce que ça tient ?"*

Le niveau d'utilisation des ressources du service : CPU, mémoire, threads, connexions
à la base de données, queue de messages. La saturation est un signal **prédictif** :
un service peut encore fonctionner correctement à 85% de saturation, mais c'est le
moment d'agir — pas à 100%.

## Pourquoi ces quatre signaux ?

| Signal | Question | Nature |
|---|---|---|
| Latence | Est-ce que c'est rapide ? | Symptôme ressenti par l'utilisateur |
| Trafic | Quelle est la charge ? | Signal de contexte |
| Taux d'erreur | Est-ce que ça fonctionne ? | Symptôme ressenti par l'utilisateur |
| Saturation | Est-ce que ça tient ? | Signal prédictif |

Ensemble, ils couvrent les deux dimensions essentielles de la fiabilité :
**ce que ressent l'utilisateur** (latence, erreurs) et **ce que vit le système**
(trafic, saturation).

## Application sur la plateforme

Sur notre plateforme, les Golden Signals sont le **fil conducteur** de la construction
des dashboards et des règles d'alerting :

- Tout dashboard de supervision d'un service doit exposer ces quatre signaux
- Les alertes critiques doivent a minima couvrir le taux d'erreur et la latence
- L'APM calcule automatiquement latence et taux d'erreur à partir des traces —
  raison supplémentaire pour laquelle l'agent APM est obligatoire

:::note Références croisées
La section [Standards — Dashboards](../02-standards/05-dashboards) détaille comment
construire un dashboard autour des Golden Signals.

La section [Standards — Alerting](../02-standards/04-alerting) explique comment
définir des seuils pertinents sur ces quatre signaux.
:::

## Pour aller plus loin

Les Golden Signals sont documentés dans le chapitre 6 du livre *Site Reliability
Engineering* de Google, disponible gratuitement en ligne :
[sre.google/sre-book — Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)
