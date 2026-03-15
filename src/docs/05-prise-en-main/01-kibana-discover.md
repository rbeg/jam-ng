---
id: kibana-discover
title: Kibana › Discover — Explorer ses logs
sidebar_label: Discover
sidebar_position: 1
---

# Kibana › Discover — Explorer ses logs

## À quoi sert Discover ?

Discover est l'interface de Kibana pour **interroger et explorer les données brutes**
stockées dans Elasticsearch. C'est l'outil principal pour investiguer des logs,
rechercher des événements précis, et construire des requêtes avant de les intégrer
dans un dashboard.

---

## Sélectionner la bonne Data View

La première étape est de choisir la Data View correspondant aux données à explorer.

| Data View | Contenu |
|---|---|
| `Logs applicatifs` | Logs ECS de tous les services |
| `APM Traces` | Transactions, spans, errors APM |
| `APM Metrics` | Métriques JVM et système |

Pour les logs applicatifs, utiliser **`Logs applicatifs`** qui couvre les index `logs-*`.

---

## Filtres essentiels

### Filtrer par service

```
service.name: "payment-service"
```

### Filtrer par niveau de log

```
log.level: "ERROR"
```

### Filtrer par environnement

```
service.environment: "production"
```

### Combiner des filtres

```
service.name: "payment-service"
AND service.environment: "production"
AND log.level: "ERROR"
```

### Filtrer sur une période

Utiliser le sélecteur de période en haut à droite de Kibana. Les intervalles les
plus utiles en investigation : **Last 15 minutes**, **Last 1 hour**, **Last 24 hours**.

---

## Colonnes recommandées

Par défaut, Discover affiche peu de colonnes. Ajouter les colonnes suivantes pour
une vue plus exploitable :

- `log.level`
- `service.name`
- `message`
- `error.type` (pour les erreurs)
- `trace.id` (pour la corrélation APM)

Les colonnes sont configurables via le panneau de gauche en cliquant sur les champs.

---

## Requêtes utiles

### Logs en erreur d'un service sur les dernières heures

```
service.name: "payment-service"
AND log.level: "ERROR"
AND service.environment: "production"
```

### Logs sans champ ECS `log.level` (non conformes)

```
service.name: "mon-service" AND NOT _exists_: "log.level"
```

### Logs liés à une trace APM spécifique

```
trace.id: "4bf92f3577b34da6a3ce929d0e0e4736"
```

### Logs d'un parcours métier

```
labels.business_use_case: "checkout"
AND log.level: "ERROR"
```

---

## Pour aller plus loin

- [Kibana Discover — Documentation officielle](https://www.elastic.co/guide/en/kibana/current/discover.html)
- [KQL — Kibana Query Language](https://www.elastic.co/guide/en/kibana/current/kuery-query.html)
