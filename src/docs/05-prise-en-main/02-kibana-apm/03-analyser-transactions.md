---
id: analyser-transactions
title: Analyser les transactions
sidebar_label: Analyser les transactions
sidebar_position: 3
---

# Analyser les transactions

## Vue d'ensemble d'un service

**Kibana › APM › Services › [mon-service]**

La page d'un service affiche les Golden Signals sur la période sélectionnée :

- **Throughput** : volume de transactions par minute
- **Latency** : latence moyenne, p95 et p99
- **Failed transactions** : taux de transactions en erreur

Ces trois métriques sont calculées automatiquement à partir des traces APM. Elles
constituent la vue de santé de référence pour un service.

---

## Analyser par type de transaction

**Kibana › APM › Services › [mon-service] › Transactions**

Les transactions sont regroupées par nom. Pour chaque groupe :

- volume moyen (transactions par minute)
- latence p95
- taux d'impact (proportion des transactions lentes ou en erreur)

:::tip
Trier par **"Impact"** plutôt que par volume ou latence seule. L'impact combine les
deux dimensions et remonte en priorité les transactions qui dégradent le plus
l'expérience utilisateur.
:::

---

## Filtrer les transactions

Le sélecteur de filtres en haut de la page APM permet de restreindre l'analyse :

| Filtre | Utilisation |
|---|---|
| `service.environment` | Isoler production, staging, etc. |
| `transaction.result` | Filtrer sur `HTTP 5xx`, `HTTP 4xx`… |
| `labels.business_use_case` | Restreindre à un parcours métier |
| `service.version` | Comparer deux versions déployées |

---

## Comparer deux versions

Après un déploiement, comparer les métriques entre l'ancienne et la nouvelle version :

1. Sélectionner la période couvrant les deux versions
2. Utiliser le filtre `service.version` pour isoler chaque version
3. Comparer latence p95 et taux d'erreur entre les deux

Cette comparaison est particulièrement utile pour valider qu'un déploiement n'a pas
introduit de régression de performance.

---

## Analyser les erreurs

**Kibana › APM › Services › [mon-service] › Errors**

La vue des erreurs regroupe les exceptions par type (`error.grouping_key`).
Pour chaque groupe :

- nombre d'occurrences sur la période
- dernière occurrence
- lien vers un exemple de trace

**Questions clés lors de l'analyse :**

- L'erreur est-elle apparue après un déploiement récent ?
- Est-elle associée à un type de transaction spécifique ?
- Est-elle ponctuelle ou systématique ?
- Le taux d'erreur est-il en augmentation ?

---

## Consulter les métriques JVM

**Kibana › APM › Services › [mon-service] › JVM**

La vue JVM affiche les métriques collectées en continu par l'agent :

- **Heap memory** : used vs max — surveiller une tendance à la hausse (memory leak)
- **Garbage collection** : fréquence et durée des GC — un GC fréquent peut expliquer
  des pics de latence
- **Thread count** : nombre de threads actifs — une saturation du pool de threads
  bloque les nouvelles requêtes

:::note
Les métriques JVM sont collectées toutes les 30 secondes par défaut. Elles ne sont
pas adaptées à la détection d'événements très courts (spike de quelques secondes).
:::

---

## Pour aller plus loin

- [Lire une trace distribuée](./02-lire-une-trace)
- [Modèle de données APM](./01-modele-de-donnees)
- [Kibana APM — Documentation officielle](https://www.elastic.co/guide/en/kibana/current/apm.html)
