---
id: ecosysteme
title: Un écosystème plus large
sidebar_label: Écosystème
sidebar_position: 5
---

# Un écosystème plus large que les seules applications

## Au-delà de ce cadre de référence

Ce document se concentre sur l'observabilité **applicative** — logs, traces et métriques
des services Spring Boot, via Elasticsearch, Kibana et les agents APM. C'est le périmètre
que l'équipe plateforme définit, maintient et standardise.

Mais l'observabilité dans l'entreprise ne s'arrête pas là.

## D'autres outils, d'autres équipes

D'autres équipes socles mettent à disposition des ressources complémentaires que les
équipes peuvent — et doivent — exploiter dans leurs investigations :

| Outil | Usage principal | Maintenu par |
|---|---|---|
| **Zabbix** | Supervision infrastructure, disponibilité des hôtes, sondes réseau | Équipe infrastructure |
| **Grafana** | Dashboards métriques système, Kubernetes, ressources | Équipe infrastructure / SRE |
| **Elastic SIEM** | Logs de sécurité, détection d'anomalies, audit | Équipe sécurité |
| **Kibana CI/CD** | Logs et métriques des pipelines de déploiement | Équipe DevOps |

:::tip
Avant de construire un dashboard ou une alerte, il convient de vérifier ce qui existe
déjà. Une métrique infrastructure sur la saturation d'un nœud Kubernetes peut expliquer
une dégradation applicative — et elle est peut-être déjà visible dans Grafana.
:::

## L'observabilité couvre bien plus que les applications

L'observabilité est transverse à toute la plateforme. Elle adresse de nombreux domaines
au-delà des seules applications :

- **Obsolescence** — suivi des versions de librairies, runtimes et composants en fin
  de support
- **Sécurité** — détection d'accès anormaux, audit des actions sensibles, conformité
- **CI/CD** — durée des pipelines, taux d'échec des déploiements, fréquence de livraison
- **Gestion des incidents** — corrélation des alertes, timeline des événements,
  post-mortems
- **Surveillance infrastructure** — disponibilité, capacité, saturation des ressources
  Kubernetes
- **Expérience utilisateur** — erreurs frontend, temps de chargement, taux d'abandon
  sur un parcours

Chacun de ces domaines a ses propres outils, ses propres équipes référentes, et
potentiellement sa propre documentation. Ce cadre de référence ne les couvre pas, mais
**ils font partie du même écosystème** et peuvent être mobilisés conjointement lors
d'une investigation.

## Savoir à qui s'adresser

| Domaine | Équipe référente |
|---|---|
| Infrastructure & réseau | Équipe infrastructure |
| Sécurité & conformité | Équipe sécurité |
| CI/CD & déploiement | Équipe DevOps |
| Observabilité applicative | Équipe plateforme *(ce cadre de référence)* |
| Expérience utilisateur | Équipe frontend / produit |
