---
id: kibana-alerting
title: Kibana › Alerting — Consulter les alertes
sidebar_label: Alerting
sidebar_position: 4
---

# Kibana › Alerting — Consulter les alertes

## À quoi sert cette section ?

Cette page explique comment **consulter et interpréter** les alertes existantes sur
la plateforme. La création et la configuration d'alertes sont du ressort de l'équipe
plateforme — voir [Gouvernance › Faire une demande](../07-gouvernance/03-demandes).

---

## Accéder aux alertes actives

**Kibana › Stack Management › Rules** ou **Kibana › Observability › Alerts**

La vue Alerts liste tous les événements d'alerte déclenchés sur la période sélectionnée,
avec leur sévérité, leur statut, et le service concerné.

---

## Lire une alerte

Chaque alerte affiche :

| Champ | Description |
|---|---|
| **Nom** | Suit la convention `[service] — [signal] — [condition]` |
| **Sévérité** | `critical`, `high`, `medium`, `low` |
| **Statut** | `Active` (toujours en cours), `Recovered` (revenue à la normale) |
| **Durée** | Depuis combien de temps l'alerte est active |
| **Valeur observée** | La valeur du signal au moment du déclenchement |

---

## Naviguer depuis une alerte vers les données

Depuis une alerte, plusieurs chemins d'investigation sont possibles :

- **"View in APM"** — ouvre directement le service concerné dans APM avec la période
  de l'alerte
- **"View in Discover"** — ouvre Discover filtré sur le service et la période
- **Lien vers le runbook** — procédure d'investigation associée à cette alerte

:::tip
Le runbook est le premier réflexe à consulter lors du déclenchement d'une alerte.
Il documente les causes les plus fréquentes et les étapes d'investigation recommandées.
:::

---

## Consulter l'historique d'une règle

**Kibana › Stack Management › Rules › [nom de la règle] › Execution history**

L'historique d'exécution montre :

- les déclenchements passés avec leur timestamp
- la valeur observée à chaque déclenchement
- la durée de chaque période d'alerte active

Utile pour distinguer une alerte récurrente (problème structurel) d'une alerte
ponctuelle (pic transitoire).

---

## Catalogue des alertes socles

Les alertes maintenues par l'équipe plateforme sont listées dans le
[Catalogue des assets › Alertes socles](../06-catalogue/05-alertes-socles/catalogue-alertes).

---

## Pour aller plus loin

- [Standards › Alerting](../02-standards/04-alerting)
- [Kibana Alerting — Documentation officielle](https://www.elastic.co/guide/en/kibana/current/alerting-getting-started.html)
