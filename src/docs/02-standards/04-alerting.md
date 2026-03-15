---
id: alerting
title: Alerting
sidebar_label: Alerting
sidebar_position: 4
---

# Standards d'alerting

## Principes généraux

Une alerte qui se déclenche trop souvent est ignorée. Une alerte qui ne se déclenche
pas assez est inutile. L'objectif d'une alerte est de **signaler un état anormal qui
nécessite une action humaine** — pas d'informer, pas de logger.

:::warning
Une alerte sans runbook associé génère du stress sans générer d'action utile.
Toute alerte mise en production doit référencer une procédure d'investigation.
:::

---

## Niveaux de sévérité

| Niveau | Signification | Réponse attendue |
|---|---|---|
| `critical` | Impact utilisateur avéré, service dégradé ou indisponible | Intervention immédiate, 24h/24 |
| `high` | Dégradation significative, risque d'impact imminent | Intervention dans l'heure |
| `medium` | Anomalie détectée, pas encore d'impact utilisateur | Traitement dans la journée |
| `low` | Signal faible, à surveiller | Traitement dans la semaine |

---

## Convention de nommage

Une alerte doit être identifiable sans avoir à l'ouvrir. La convention suivante
est obligatoire sur la plateforme :

```
[service-name] — [signal] — [condition]
```

Exemples :

```
payment-service — error-rate — above 5%
order-service — latency-p95 — above 2s
identity-service — availability — below 99%
kafka-connector — consumer-lag — above 10000
```

---

## Ce qu'une alerte doit documenter

Toute alerte mise en production doit renseigner les éléments suivants :

| Élément | Description |
|---|---|
| **Condition de déclenchement** | Quel seuil, sur quelle fenêtre de temps, avec quel opérateur |
| **Sévérité** | Selon la grille ci-dessus |
| **Impact potentiel** | Quel service, quel parcours métier, quelle population d'utilisateurs |
| **Destinataires** | Qui est notifié, par quel canal (Slack, email, PagerDuty…) |
| **Runbook** | Lien vers la procédure d'investigation associée |

---

## Recommandations

### Alerter sur les symptômes, pas sur les causes

Préférer des alertes sur ce que ressent l'utilisateur — taux d'erreur, latence —
plutôt que sur les ressources système — CPU, mémoire. Une alerte CPU à 80% ne dit
pas si les utilisateurs sont impactés. Une alerte taux d'erreur à 5% si.

### Utiliser les percentiles

Définir les seuils sur les **percentiles** (p95, p99) plutôt que sur les moyennes.
Une moyenne stable peut masquer des pics importants qui dégradent l'expérience d'une
partie des utilisateurs.

### Contextualiser avec les labels métier

Quand c'est possible, restreindre les alertes critiques aux parcours
`labels.business_criticality: critical` ou `high`. Une dégradation sur un parcours
secondaire n'a pas la même priorité qu'une dégradation sur le checkout.

### Définir des fenêtres de temps adaptées

Une alerte trop courte génère du bruit sur des pics transitoires. Une alerte trop
longue détecte les problèmes trop tard. En règle générale :

| Type de signal | Fenêtre recommandée |
|---|---|
| Taux d'erreur | 5 minutes |
| Latence p95 | 5 à 10 minutes |
| Disponibilité | 1 minute |
| Consumer lag Kafka | 10 minutes |

### Revoir régulièrement les seuils

Un seuil pertinent à J+30 après la mise en prod ne l'est peut-être plus à J+180.
Planifier une revue des alertes au moins une fois par trimestre.

---

## Catalogue des alertes socles

Les alertes maintenues par l'équipe plateforme sont documentées dans le
[Catalogue des assets › Alertes socles](../06-catalogue/05-alertes-socles/catalogue-alertes).
