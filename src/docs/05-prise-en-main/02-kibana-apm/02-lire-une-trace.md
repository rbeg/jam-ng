---
id: lire-une-trace
title: Lire une trace distribuée
sidebar_label: Lire une trace
sidebar_position: 2
---

# Lire une trace distribuée

## Qu'est-ce qu'une trace ?

Une trace représente le **chemin complet d'une requête** à travers un ou plusieurs
services. Elle regroupe toutes les opérations — transactions et spans — liées à un
même identifiant `trace.id`.

Dans une architecture microservices, une trace peut traverser plusieurs services :
le service appelant crée une transaction, qui produit un span vers le service suivant,
qui crée à son tour sa propre transaction, et ainsi de suite.

---

## Accéder à une trace

### Depuis la liste des transactions

**Kibana › APM › Services › [mon-service] › Transactions**

Sélectionner une transaction dans la liste. La page détail s'ouvre avec la timeline
de la trace.

### Par recherche directe

**Kibana › APM › Traces**

Rechercher par `trace.id`, `transaction.name`, ou filtrer par service et période.

### Depuis un log

Dans **Kibana › Discover**, cliquer sur la valeur du champ `trace.id` dans un log,
puis utiliser le lien **"View in APM"** si disponible, ou copier le `trace.id` et
le rechercher dans APM Traces.

---

## Lire la timeline d'une trace

La timeline (waterfall) est la représentation principale d'une trace. Elle affiche
toutes les opérations dans l'ordre chronologique, avec leur durée respective.

```
Trace: POST /api/v1/payments                           145ms
│
├── payment-service: POST /api/v1/payments             145ms
│   ├── postgresql: SELECT FROM accounts                 8ms
│   ├── http: POST /risk-evaluation → risk-service      92ms
│   │   └── risk-service: POST /risk-evaluation         90ms
│   │       └── postgresql: SELECT FROM rules            5ms
│   └── kafka: SEND payment.processed                    3ms
```

**Lecture de la timeline :**

- La **largeur** de chaque barre représente la durée relative de l'opération
- Le **décalage horizontal** représente le moment de démarrage de l'opération
- Les **couleurs** distinguent les types de spans (db, http, messaging…)
- Les opérations imbriquées sont les spans fils d'une transaction parente

---

## Identifier le goulot d'étranglement

Dans la timeline, la ou les opérations les plus larges sont les candidates prioritaires
à l'investigation. Dans l'exemple ci-dessus, l'appel vers `risk-service` représente
63% de la durée totale.

Cliquer sur un span pour obtenir le détail :

- Durée exacte
- Nom de la ressource appelée (URL, nom de table, topic Kafka…)
- Outcome (`success`, `failure`)
- Champs ECS associés

---

## Lire les erreurs dans une trace

Les erreurs apparaissent dans la timeline signalées par une icône distincte. Cliquer
sur l'erreur pour afficher :

- Le type d'exception (`error.exception.type`)
- Le message (`error.exception.message`)
- La stack trace complète
- Le lien vers les autres erreurs du même type (`error.grouping_key`)

:::tip
Le regroupement par `error.grouping_key` permet de savoir combien de fois une même
erreur s'est produite sur une période donnée, et de distinguer une erreur ponctuelle
d'une erreur systématique.
:::

---

## Naviguer vers les logs de la trace

Depuis la page détail d'une transaction, cliquer sur **"View logs"** ou
**"Investigate in Discover"** pour afficher tous les logs portant ce `trace.id`.

Cette navigation est disponible uniquement si `log_correlation: true` est activé
dans l'agent APM et que les logs sont au format ECS.

---

## Pour aller plus loin

- [Modèle de données APM](./01-modele-de-donnees)
- [Kibana APM — Documentation officielle](https://www.elastic.co/guide/en/kibana/current/apm.html)
