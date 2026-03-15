---
id: logs-applicatifs
title: Logs applicatifs
sidebar_label: Logs applicatifs
sidebar_position: 2
---

# Dashboard — Logs applicatifs

## Fiche synthèse

| | |
|---|---|
| **Nom Kibana** | `Plateforme — Logs — Vue générale` |
| **Niveau** | 1 — Socle |
| **Maintenu par** | Équipe plateforme |
| **Index utilisés** | `logs-*` |
| **Audience** | Développeurs, ops |

---

## Objectif

Donner une vue agrégée des logs applicatifs sur la plateforme, filtrables par service
et par environnement. Permet de suivre le volume de logs par niveau, de détecter une
augmentation anormale d'erreurs, et d'accéder rapidement aux logs récents.

---

## Contenu

### En-tête — Distribution par niveau

- Répartition des logs par `log.level` sur la période (INFO, WARN, ERROR, DEBUG)
- Évolution temporelle du volume de logs ERROR

### Volume par service

Histogramme empilé du volume de logs par service, coloré par `log.level`.
Permet de détecter un service qui génère un volume anormal de logs ERROR ou WARN.

### Logs récents

Table des derniers logs avec les colonnes :

- `@timestamp`
- `log.level`
- `service.name`
- `message`
- `trace.id` (cliquable vers APM)

### Conformité ECS

Indicateur du pourcentage de logs conformes ECS (possédant le champ `log.level`)
sur la période. Permet de détecter des services non conformes.

---

## Filtres disponibles

| Filtre | Description |
|---|---|
| `service.name` | Restreindre à un ou plusieurs services |
| `service.environment` | Isoler un environnement |
| `log.level` | Filtrer par niveau de log |
| `labels.business_use_case` | Restreindre à un parcours métier |
| Période | Sélecteur de période Kibana |
