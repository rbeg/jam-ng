---
id: demandes
title: Faire une demande
sidebar_label: Faire une demande
sidebar_position: 3
---

# Faire une demande

Pour tout besoin qui sort du périmètre couvert par ce cadre de référence, voici
comment formuler une demande à l'équipe plateforme.

---

## Demande de nouveau dashboard socle ou technologique

**Canal** : Ticket Jira — projet `PLAT`, type `Demande`

**Informations à fournir :**

- Besoin décrit en une phrase (quelle question le dashboard doit-il répondre ?)
- Audience cible
- Services ou composants concernés
- Index de données nécessaires
- Nombre d'équipes qui bénéficieraient de ce dashboard

:::note
Les dashboards socles et technologiques sont créés par l'équipe plateforme uniquement
si le besoin est **transverse** — c'est-à-dire partagé par au moins deux équipes.
Un besoin spécifique à une seule équipe relève d'un dashboard de niveau 3.
:::

---

## Demande de nouvelle alerte socle

**Canal** : Ticket Jira — projet `PLAT`, type `Demande`

**Informations à fournir :**

- Service(s) concerné(s)
- Signal à surveiller (taux d'erreur, latence, disponibilité…)
- Condition de déclenchement (seuil, fenêtre de temps)
- Sévérité souhaitée
- Destinataires (canal Slack, email…)
- Runbook associé (au moins une ébauche)

---

## Demande de dérogation à un standard

**Canal** : Ticket Jira — projet `PLAT`, type `Dérogation`

**Informations à fournir :**

- Standard concerné (ECS, APM, nommage…)
- Raison de la dérogation
- Solution alternative proposée
- Durée prévue (dérogation temporaire ou permanente)

Les dérogations sont examinées lors de la prochaine revue de l'équipe plateforme.

---

## Signalement d'une anomalie sur la plateforme

**Canal** : Canal Slack `#plateforme-observabilite` pour une anomalie en cours,
ticket Jira pour un dysfonctionnement récurrent.

**Informations à fournir :**

- Description du problème observé
- Service ou composant concerné
- Environnement
- Étapes déjà effectuées pour diagnostiquer
