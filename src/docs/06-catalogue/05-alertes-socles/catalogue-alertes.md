---
id: catalogue-alertes
title: Catalogue des alertes socles
sidebar_label: Catalogue des alertes
sidebar_position: 1
---

# Catalogue des alertes socles

Les alertes listées ici sont **maintenues par l'équipe plateforme** et actives sur
tous les services instrumentés par APM. Elles couvrent les signaux fondamentaux et
ne nécessitent aucune configuration spécifique de la part des équipes.

Des alertes supplémentaires peuvent être demandées via
[Gouvernance › Faire une demande](../../07-gouvernance/03-demandes).

---

## Alertes de taux d'erreur

### `[service] — error-rate — above 5% (production)`

| | |
|---|---|
| **Signal** | Taux de transactions en erreur (`transaction.outcome: failure`) |
| **Condition** | Taux > 5% sur une fenêtre glissante de 5 minutes |
| **Sévérité** | `high` |
| **Environnement** | `production` uniquement |
| **Destinataires** | Canal Slack de l'équipe propriétaire du service |
| **Runbook** | Ouvrir APM › service concerné › Errors — identifier le type d'erreur dominant |

### `[service] — error-rate — above 10% (production)`

| | |
|---|---|
| **Signal** | Taux de transactions en erreur |
| **Condition** | Taux > 10% sur une fenêtre glissante de 5 minutes |
| **Sévérité** | `critical` |
| **Environnement** | `production` uniquement |
| **Destinataires** | Canal Slack de l'équipe + canal plateforme |
| **Runbook** | Ouvrir APM › service concerné › Errors — déclencher la procédure d'incident |

---

## Alertes de latence

### `[service] — latency-p95 — above 2s (production)`

| | |
|---|---|
| **Signal** | Latence p95 des transactions `request` |
| **Condition** | p95 > 2 000ms sur une fenêtre glissante de 10 minutes |
| **Sévérité** | `high` |
| **Environnement** | `production` uniquement |
| **Destinataires** | Canal Slack de l'équipe propriétaire du service |
| **Runbook** | Ouvrir APM › service concerné › Transactions — trier par impact — identifier les transactions lentes |

---

## Alertes de disponibilité

### `[service] — availability — below 99% (production)`

| | |
|---|---|
| **Signal** | Pourcentage de transactions avec `transaction.outcome: success` |
| **Condition** | Taux de succès < 99% sur une fenêtre glissante de 1 minute |
| **Sévérité** | `critical` |
| **Environnement** | `production` uniquement |
| **Destinataires** | Canal Slack de l'équipe + canal plateforme |
| **Runbook** | Vérifier dans APM si le service répond — vérifier les logs de démarrage — alerter l'équipe infrastructure si le pod est indisponible |

---

## Alertes Kafka

### `kafka-connector — status — FAILED`

| | |
|---|---|
| **Signal** | Statut d'un connecteur Kafka |
| **Condition** | Statut `FAILED` détecté dans les logs du connecteur |
| **Sévérité** | `high` |
| **Environnement** | Tous environnements |
| **Destinataires** | Canal Slack de l'équipe propriétaire du connecteur |
| **Runbook** | Ouvrir le dashboard [Kafka Connectors](../03-dashboards-technologiques/kafka-connectors) — identifier les erreurs — redémarrer le connecteur si applicable |

---

## Demander une nouvelle alerte

Pour demander une alerte spécifique à un service ou un parcours métier, voir
[Gouvernance › Faire une demande](../../07-gouvernance/03-demandes).

Toute demande doit préciser : le signal, la condition de déclenchement, la sévérité,
les destinataires, et le runbook associé.
