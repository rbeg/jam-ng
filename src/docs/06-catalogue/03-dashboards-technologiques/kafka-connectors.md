---
id: kafka-connectors
title: Kafka Connectors
sidebar_label: Kafka Connectors
sidebar_position: 1
---

# Dashboard — Kafka Connectors

## Fiche synthèse

| | |
|---|---|
| **Nom Kibana** | `Kafka — Connecteurs — Monitoring` |
| **Niveau** | 2 — Technologique |
| **Maintenu par** | Équipe plateforme |
| **Index utilisés** | `logs-*` (logs des connecteurs Kafka) |
| **Audience** | Développeurs, ops, tech leads |

---

## Objectif

Surveiller l'état et l'activité des connecteurs Kafka déployés sur la plateforme.
Ce dashboard permet de détecter rapidement un connecteur en erreur, de suivre
le volume de messages traités, et d'identifier des anomalies de consommation
sans avoir à interroger manuellement les logs.

---

## Contenu

### En-tête — État global

- Nombre de connecteurs actifs
- Nombre de connecteurs en erreur sur la période
- Volume total de messages traités (lignes) sur la période

### État des connecteurs

Table listant tous les connecteurs avec :

- Nom du connecteur
- Statut (`RUNNING`, `FAILED`, `PAUSED`)
- Nombre de messages traités sur la période
- Dernière erreur détectée (type + timestamp)

Permet d'identifier en un coup d'œil les connecteurs qui ne consomment plus
ou qui sont en erreur.

### Connecteurs en erreur

Liste filtrée sur les connecteurs avec au moins une erreur sur la période,
avec le message d'erreur et le timestamp.

### Volume de traitement par connecteur

Série chronologique du nombre de lignes traitées par connecteur. Permet de détecter :

- Un connecteur qui s'arrête de consommer (courbe qui tombe à zéro)
- Un connecteur dont le débit diminue progressivement
- Un pic de volume anormal

### Erreurs par connecteur

Histogramme du nombre d'erreurs par connecteur sur la période, pour identifier
les connecteurs les plus instables.

---

## Filtres disponibles

| Filtre | Description |
|---|---|
| Nom du connecteur | Restreindre à un ou plusieurs connecteurs |
| Statut | Filtrer sur `FAILED`, `RUNNING`, `PAUSED` |
| Équipe / namespace | Restreindre au périmètre d'une équipe |
| Période | Sélecteur de période Kibana |

---

## Utilisation typique

- **Surveillance quotidienne** : vérifier qu'aucun connecteur n'est en erreur
- **Après un déploiement** : s'assurer que les connecteurs redémarrent correctement
- **Investigation d'un retard de traitement** : identifier le connecteur dont le
  débit a chuté et remonter les logs d'erreur associés

---

## Investiguer un connecteur en erreur

1. Identifier le connecteur en erreur dans la table d'état
2. Filtrer les logs sur le nom du connecteur dans **Kibana › Discover**
3. Rechercher les logs `log.level: "ERROR"` sur la période concernée
4. Identifier le type d'erreur et la cause (problème réseau, schéma incompatible,
   topic inexistant…)
5. Vérifier dans APM si des transactions liées à ce connecteur sont également
   en erreur
