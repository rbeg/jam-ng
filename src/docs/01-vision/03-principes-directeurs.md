---
id: principes-directeurs
title: Principes directeurs
sidebar_label: Principes directeurs
sidebar_position: 3
---

# Nos principes directeurs

## 1. L'observabilité est intégrée, pas ajoutée après coup

Instrumenter un service ne se fait pas en fin de sprint. Les logs, les labels métier,
la configuration APM font partie de la **Definition of Done** d'une fonctionnalité.

Voir la section [Observabilité by design](./04-observabilite-by-design) pour le détail
de ce qui est attendu à chaque phase du cycle de développement.

## 2. Les standards existent pour être partagés

Un log qui ne respecte pas ECS est un log qu'on ne peut pas corréler avec les autres.
Un service sans `service.name` cohérent est un service invisible dans APM. Les standards
de la plateforme ne sont pas des contraintes bureaucratiques — ils sont la condition
pour que **tout le monde puisse s'y retrouver**, quelle que soit l'équipe.

## 3. L'observabilité est orientée business, pas seulement technique

Un taux d'erreur HTTP à 2% ne dit rien si on ne sait pas qu'il concerne le parcours
de paiement en production. Les **labels métier** (`labels.business_use_case`,
`labels.business_criticality`) sont là pour donner du contexte aux signaux techniques
et permettre aux équipes produit de s'approprier les données d'observabilité.

## 4. La plateforme fait le maximum, les équipes font le reste

Le pipeline de collecte des logs Kubernetes, l'indexation dans Elasticsearch, les
dashboards socles — tout cela est industrialisé et maintenu par l'équipe plateforme.
Ce qui reste à la charge des équipes produit, c'est l'**instrumentation de leurs
services** : format ECS, agent APM, labels métier. La frontière est claire.

:::note
En cas de doute sur la frontière de responsabilité, consulter la section
[Gouvernance](../07-gouvernance/01-equipe-plateforme).
:::

## 5. Autonomie et appropriation

Ce cadre de référence existe pour que chaque développeur soit **autonome** sur la
plateforme d'observabilité. Savoir où chercher une information, comprendre ce qu'on
lit dans Kibana, être capable d'investiguer soi-même une anomalie — c'est l'objectif.
L'équipe plateforme n'est pas un helpdesk.
