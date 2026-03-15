---
id: apm-overview
title: APM Overview
sidebar_label: APM Overview
sidebar_position: 1
---

# Dashboard — APM Overview

## Fiche synthèse

| | |
|---|---|
| **Nom Kibana** | `Plateforme — APM Overview — Tous services` |
| **Niveau** | 1 — Socle |
| **Maintenu par** | Équipe plateforme |
| **Index utilisés** | `traces-apm-*`, `metrics-apm-*` |
| **Audience** | Développeurs, tech leads, ops |

---

## Objectif

Offrir une vue de santé transversale sur l'ensemble des services instrumentés par
APM. Ce dashboard est le **premier tableau de bord à consulter** lors d'une
investigation ou d'une revue de santé de la plateforme.

---

## Contenu

### En-tête — Vue globale

- Nombre de services actifs sur la période
- Taux d'erreur global (toutes transactions confondues)
- Latence p95 globale
- Volume de transactions par minute

### Section Golden Signals par service

Tableau récapitulatif avec pour chaque service :

- `service.name`
- `service.environment`
- Throughput (transactions/min)
- Latence p95
- Taux d'erreur (%)

Permet d'identifier d'un coup d'œil les services dégradés.

### Évolution temporelle

Séries chronologiques sur la période sélectionnée :

- Taux d'erreur global
- Latence p95 globale
- Volume de transactions

### Top erreurs

Table des types d'erreurs les plus fréquents sur la période, avec le service
concerné et le nombre d'occurrences.

---

## Filtres disponibles

| Filtre | Description |
|---|---|
| `service.name` | Restreindre à un ou plusieurs services |
| `service.environment` | Isoler un environnement |
| `transaction.type` | Filtrer par type (`request`, `messaging`…) |
| Période | Sélecteur de période Kibana |

---

## Utilisation typique

- **Revue quotidienne** : détecter en un coup d'œil un service dégradé
- **Après un déploiement** : vérifier que le service est stable
- **Lors d'une alerte** : identifier rapidement le service et le signal concernés
