---
id: trois-piliers
title: Les trois piliers
sidebar_label: Les trois piliers
sidebar_position: 2
---

# Les trois piliers : Logs, Métriques, Traces

L'observabilité repose sur trois sources de données complémentaires.
Sur notre plateforme, chacune a un rôle précis et des outils dédiés.

## 📄 Logs

Les logs capturent les **événements discrets** de la vie d'un service : une requête
reçue, une erreur levée, une règle métier franchie. Bien structurés au format ECS,
ils permettent de reconstituer précisément ce qui s'est passé, quand, et dans quel
contexte.

- **Outil principal** : Kibana › Discover
- **Stockage** : Elasticsearch
- **Format obligatoire** : ECS Layout

> *Les logs répondent à : "Qu'est-ce qui s'est passé ?"*

## 📈 Métriques

Les métriques mesurent l'**état continu** d'un système : taux d'erreur, latence,
saturation CPU, nombre de transactions. Elles sont la base des dashboards de
supervision et des alertes.

- **Outil principal** : Kibana › Dashboards, APM
- **Compléments** : Grafana (métriques infrastructure), Zabbix (disponibilité)

> *Les métriques répondent à : "Est-ce que ça va ?"*

## 🔍 Traces

Les traces reconstituent le **chemin complet d'une requête** à travers les services.
Elles permettent d'identifier précisément quel service, quelle opération, quelle
dépendance est responsable d'une latence ou d'une erreur dans un appel distribué.
Sur notre plateforme, elles sont prises en charge automatiquement par les agents APM.

- **Outil principal** : Kibana › APM
- **Instrumentation** : Agent APM Elastic (obligatoire sur tous les services)

> *Les traces répondent à : "Où est le problème ?"*

## La complémentarité des trois piliers

Les trois piliers ne s'utilisent pas en silo. Une investigation typique suit ce chemin :

1. Une **alerte** se déclenche → une métrique dépasse un seuil
2. On ouvre **APM** → on identifie le service et la transaction dégradée
3. On remonte aux **logs** → on comprend précisément l'erreur, avec son contexte métier
4. On corrèle avec les **traces** → on identifie la dépendance en cause

:::tip
C'est la corrélation entre les trois piliers — rendue possible par les champs communs
`trace.id` et `transaction.id` — qui donne toute sa puissance à la plateforme.
Un agent APM correctement configuré injecte ces champs automatiquement dans les logs.
:::
