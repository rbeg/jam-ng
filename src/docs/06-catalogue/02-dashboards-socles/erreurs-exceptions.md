---
id: erreurs-exceptions
title: Erreurs et exceptions
sidebar_label: Erreurs & exceptions
sidebar_position: 3
---

# Dashboard — Erreurs et exceptions

## Fiche synthèse

| | |
|---|---|
| **Nom Kibana** | `Plateforme — Erreurs — Vue générale` |
| **Niveau** | 1 — Socle |
| **Maintenu par** | Équipe plateforme |
| **Index utilisés** | `traces-apm-*`, `logs-*` |
| **Audience** | Développeurs, tech leads, ops |

---

## Objectif

Centraliser la vue des erreurs et exceptions sur la plateforme. Ce dashboard est
le point de départ pour analyser la fréquence, la distribution et l'évolution des
erreurs applicatives, sans avoir à naviguer service par service dans APM.

---

## Contenu

### En-tête — Métriques globales

- Nombre total d'erreurs sur la période
- Taux d'erreur global
- Nombre de types d'erreurs distincts (`error.grouping_key`)

### Top types d'erreurs

Table des types d'erreurs les plus fréquents :

- `error.exception.type`
- Nombre d'occurrences
- Service(s) concerné(s)
- Première et dernière occurrence
- Lien vers un exemple de trace APM

### Évolution temporelle

Série chronologique du nombre d'erreurs par service, pour détecter une augmentation
soudaine ou progressive.

### Distribution par service

Camembert ou tableau de la répartition des erreurs par `service.name`.

### Erreurs récentes

Table des dernières erreurs avec :

- `@timestamp`
- `error.exception.type`
- `error.exception.message`
- `service.name`
- `trace.id`

---

## Filtres disponibles

| Filtre | Description |
|---|---|
| `service.name` | Restreindre à un ou plusieurs services |
| `service.environment` | Isoler un environnement |
| `error.exception.type` | Filtrer par type d'exception |
| `labels.business_criticality` | Prioriser les erreurs sur les parcours critiques |
| Période | Sélecteur de période Kibana |
