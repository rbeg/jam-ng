---
id: glossaire
title: Glossaire
sidebar_label: Glossaire
sidebar_position: 8
---

# Glossaire

## Observabilité & architecture

| Terme | Définition |
|---|---|
| **ECS** | Elastic Common Schema — format de structuration des logs défini par Elastic |
| **APM** | Application Performance Monitoring — agent Elastic qui capture automatiquement les traces et métriques d'un service |
| **Trace** | Représentation du chemin complet d'une requête à travers un ou plusieurs services |
| **Transaction** | Unité de travail dans APM (ex : traitement d'une requête HTTP entrante) |
| **Span** | Sous-opération d'une transaction (ex : appel SQL, appel HTTP sortant, opération Kafka) |
| **Logging Flow** | Pipeline de collecte et routage des logs depuis les pods Kubernetes vers Elasticsearch |
| **ECS Layout** | Implémentation Java/Logback du format ECS pour les applications Spring Boot |
| **SIEM** | Security Information and Event Management — outil de centralisation et d'analyse des événements de sécurité |
| **SRE** | Site Reliability Engineering — discipline visant à maintenir la fiabilité des systèmes en production |
| **Definition of Done** | Ensemble des critères qu'une story doit satisfaire pour être considérée comme terminée |
| **Golden Signals** | Les 4 métriques fondamentales de supervision d'un service : latence, trafic, taux d'erreur, saturation |
| **Business Label** | Label métier ajouté dans les logs et traces pour contextualiser un événement technique (`labels.business_use_case`, `labels.business_criticality`…) |

## Elasticsearch & Kibana

| Terme | Définition |
|---|---|
| **Index** | Unité de stockage dans Elasticsearch — regroupe des documents de même nature (ex : tous les logs applicatifs) |
| **Data View** | Vue Kibana sur un ou plusieurs index, permet d'interroger et de visualiser les données |
| **Mapping** | Schéma d'un index Elasticsearch — définit le type de chaque champ (keyword, text, date, integer…) |
| **Shard** | Subdivision d'un index Elasticsearch — permet la distribution et la parallélisation des requêtes |
| **Pipeline d'ingestion** | Séquence de transformations appliquées aux documents avant leur indexation dans Elasticsearch |

## Métriques & mesure

| Terme | Définition |
|---|---|
| **Percentile** | Valeur en dessous de laquelle se trouve un certain pourcentage des observations. Contrairement à la moyenne, les percentiles révèlent la distribution réelle des valeurs et ne sont pas affectés par les valeurs extrêmes. |
| **p50 (médiane)** | 50% des requêtes sont traitées en moins de cette durée. Représente l'expérience du cas "normal". Ex : p50 = 120ms signifie que la moitié des requêtes répondent en moins de 120ms. |
| **p95** | 95% des requêtes sont traitées en moins de cette durée. Représente l'expérience de la grande majorité des utilisateurs. C'est souvent le percentile de référence pour les SLO. |
| **p99** | 99% des requêtes sont traitées en moins de cette durée. Représente les cas les plus lents — le "pire cas fréquent". Un p99 élevé signifie que certains utilisateurs vivent une expérience très dégradée, même si la moyenne semble correcte. |
| **Moyenne (avg)** | Somme des valeurs divisée par le nombre d'observations. **Trompeuse pour la latence** : une moyenne à 150ms peut masquer un p99 à 4 secondes si la majorité des requêtes sont rapides. |
| **Taux d'erreur** | Proportion de requêtes en erreur sur le total des requêtes. Exprimé en pourcentage. |
| **Saturation** | Niveau d'utilisation d'une ressource par rapport à sa capacité maximale. Une saturation à 80% est un signal d'alerte, pas encore une panne. |
| **SLO** | Service Level Objective — objectif de niveau de service défini pour un indicateur donné. Ex : "p95 de latence inférieur à 500ms sur 30 jours". |
| **SLI** | Service Level Indicator — la mesure concrète utilisée pour évaluer un SLO. Ex : le p95 de latence mesuré par APM. |
| **SLA** | Service Level Agreement — engagement contractuel ou organisationnel basé sur un ou plusieurs SLO. |
