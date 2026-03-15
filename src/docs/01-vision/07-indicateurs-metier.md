---
id: indicateurs-metier
title: Indicateurs métier
sidebar_label: Indicateurs métier
sidebar_position: 7
---

# L'observabilité métier

## Un périmètre distinct

L'observabilité ne se limite pas aux applications et à leur infrastructure. Elle couvre
également les **indicateurs métier** — taux de conversion, volumes de transactions, KPIs
business, suivi de parcours utilisateur — que les équipes métier et produit ont besoin
de suivre au quotidien.

Sur notre plateforme, ce périmètre est géré de façon **entièrement séparée** de
l'observabilité applicative couverte par ce cadre de référence, y compris au niveau
des instances ELK — chaque périmètre dispose de sa propre instance Elasticsearch
et Kibana.

## Architecture dédiée

Chaque périmètre métier dispose de son propre pipeline et de sa propre instance ELK,
indépendants du pipeline de logs applicatifs et d'APM :

```
                  Observabilité applicative        Observabilité métier
                  (ce cadre de référence)          (périmètre distinct)

Sources       →   Pods Kubernetes              →   Bases de données
              →   Applications Spring Boot     →   Topics Kafka
              →   Agents APM                   →   Autres sources métier

Pipeline      →   Logging Flows                →   Logstash (par périmètre)

Stockage      →   Elasticsearch (instance A)   →   Elasticsearch (instance B)

Restitution   →   Kibana (instance A)          →   Kibana (instance B)
                  Logs, APM, Dashboards             Dashboards métier
```

Cette séparation est intentionnelle. Elle garantit l'isolation des données métier
vis-à-vis des données techniques, une gouvernance par périmètre fonctionnel avec ses
propres règles d'accès et d'habilitation, et une scalabilité indépendante de chaque
pipeline.

:::note
Pour accéder aux dashboards métier d'un périmètre, se rapprocher de l'équipe
responsable de ce périmètre pour obtenir les accès nécessaires. Ce cadre de référence
ne couvre pas la configuration ni la gouvernance des pipelines métier.
:::

## Le lien avec l'observabilité applicative

Les deux périmètres sont complémentaires, même s'ils sont techniquement séparés.

Un pic d'abandons détecté dans un dashboard métier peut s'expliquer par une dégradation
visible dans APM sur l'instance applicative. Inversement, une alerte technique sur un
parcours critique prend tout son sens quand on connaît son impact business mesuré côté
métier.

C'est pourquoi les **labels métier** dans les logs et traces applicatifs
(`labels.business_use_case`, `labels.business_criticality`) sont recommandés sur la
plateforme : ils créent un **langage commun** entre les deux mondes et facilitent la
corrélation lors des investigations, même lorsque les outils sont distincts.

:::tip Référence croisée
La définition et l'implémentation des labels métier sont détaillées dans
[Standards — Labels métier](../02-standards/03-labels-metier).
:::
