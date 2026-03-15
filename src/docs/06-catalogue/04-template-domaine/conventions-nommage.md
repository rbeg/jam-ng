---
id: conventions-nommage
title: Conventions de nommage
sidebar_label: Conventions de nommage
sidebar_position: 2
---

# Conventions de nommage des dashboards

Une convention de nommage uniforme est obligatoire sur la plateforme. Elle garantit
que les dashboards restent identifiables dans Kibana par n'importe quelle équipe,
quelle que soit leur origine.

---

## Format

```
[Domaine] — [Service ou périmètre] — [Type]
```

Les trois segments sont séparés par des tirets longs (`—`), pas des tirets courts.

---

## Segment 1 — Domaine

Le domaine fonctionnel ou technique du dashboard. Doit correspondre à une valeur
de `labels.business_domain` ou à une brique technique reconnue.

| Valeur | Usage |
|---|---|
| `Payment` | Services du domaine paiement |
| `Catalog` | Services du domaine catalogue |
| `Identity` | Services du domaine identité et authentification |
| `Kafka` | Dashboards liés aux composants Kafka |
| `Plateforme` | Dashboards transverses maintenus par l'équipe plateforme |
| `[Votre domaine]` | À définir en cohérence avec les autres équipes |

---

## Segment 2 — Service ou périmètre

Le service ou le périmètre fonctionnel couvert par le dashboard.

Exemples :

- `payment-service` — un service spécifique
- `Parcours checkout` — un parcours multi-services
- `Connecteurs` — un ensemble de composants techniques
- `Tous services` — périmètre global

---

## Segment 3 — Type

Le type de dashboard, qui indique son usage principal.

| Valeur | Usage |
|---|---|
| `Supervision` | Vue de santé Golden Signals |
| `Vue métier` | Indicateurs orientés business / produit |
| `Erreurs` | Focus sur les erreurs et exceptions |
| `Monitoring` | Surveillance d'une brique technique |
| `Investigation` | Outil d'analyse approfondie |

---

## Exemples valides

```
Payment — payment-service — Supervision
Checkout — Parcours complet — Vue métier
Identity — auth-service — Erreurs
Kafka — Connecteurs — Monitoring
Plateforme — APM Overview — Tous services
```

## Exemples non valides

```
Dashboard payment          ❌ format non respecté
payment service errors     ❌ pas de majuscules, pas de séparateur
Mon dashboard custom       ❌ non identifiable
```
