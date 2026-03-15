---
id: recettes
title: Recettes du quotidien
sidebar_label: Recettes
sidebar_position: 5
---

# Recettes du quotidien

Des procédures pas à pas pour les situations les plus fréquentes. Chaque recette
indique les outils à utiliser et les étapes dans l'ordre.

---

## 🔍 Trouver les erreurs d'un service sur les dernières heures

**Outils** : Kibana › APM ou Kibana › Discover

### Via APM

1. Ouvrir **Kibana › APM › Services › [mon-service]**
2. Sélectionner la période (Last 1 hour, Last 4 hours…)
3. Consulter le graphique **Failed transactions rate**
4. Aller dans l'onglet **Errors** pour voir les erreurs regroupées par type
5. Cliquer sur un groupe d'erreurs pour accéder à un exemple de trace

### Via Discover

```
service.name: "mon-service"
AND log.level: "ERROR"
AND service.environment: "production"
```

Trier par `@timestamp` décroissant pour voir les erreurs les plus récentes en premier.

---

## ⏱️ Analyser la latence d'un parcours métier

**Outils** : Kibana › APM

1. Ouvrir **Kibana › APM › Services › [mon-service] › Transactions**
2. Filtrer sur `labels.business_use_case: "checkout"` dans la barre de filtres
3. Trier les transactions par **Impact**
4. Identifier les transactions avec la latence p95 la plus élevée
5. Cliquer sur une transaction pour accéder à la timeline

:::tip
Comparer la latence p95 sur deux périodes (avant / après un déploiement) pour
détecter une régression introduite par une livraison.
:::

---

## 🔗 Suivre un appel de bout en bout

**Outils** : Kibana › APM › Traces

1. Obtenir le `trace.id` — depuis un log en erreur dans Discover, ou depuis
   une notification d'incident
2. Ouvrir **Kibana › APM › Traces**
3. Rechercher par `trace.id`
4. La timeline affiche l'ensemble des services traversés et leurs spans
5. Identifier le span le plus long ou celui en erreur
6. Cliquer sur le span pour accéder au détail (durée, ressource, outcome)

---

## 🚨 Investiguer une alerte déclenchée

**Outils** : Kibana › Alerting, APM, Discover

1. Ouvrir **Kibana › Observability › Alerts**
2. Identifier l'alerte active — noter le service, le signal, et la valeur observée
3. Consulter le **runbook** lié à l'alerte (lien dans le détail de l'alerte)
4. Depuis l'alerte, cliquer sur **"View in APM"** pour ouvrir le service
   sur la période de déclenchement
5. Analyser le taux d'erreur et la latence sur cette période
6. Remonter une trace en erreur via l'onglet **Errors**
7. Si nécessaire, basculer sur **Discover** pour explorer les logs bruts
   sur la même fenêtre temporelle

---

## 📉 Identifier un service dégradé

**Outils** : Kibana › APM

1. Ouvrir **Kibana › APM › Services**
2. Trier par **Failed transactions rate** décroissant
3. Identifier les services avec un taux d'erreur anormal
4. Vérifier si la dégradation est corrélée avec un déploiement récent
   (filtre `service.version`)
5. Ouvrir le service et analyser les transactions et erreurs

---

## 🗓️ Vérifier qu'un déploiement n'a pas introduit de régression

**Outils** : Kibana › APM

1. Ouvrir **Kibana › APM › Services › [mon-service] › Transactions**
2. Sélectionner une période couvrant avant et après le déploiement
3. Filtrer sur `service.version: "nouvelle-version"`
4. Comparer la latence p95 et le taux d'erreur avec la version précédente
   (ajouter un second filtre sur `service.version: "ancienne-version"`)

---

## 📋 Vérifier qu'un service est bien instrumenté

**Outils** : Kibana › APM, Kibana › Discover

1. Vérifier la présence dans **APM › Services** — le service doit apparaître
2. Dans **Discover**, filtrer `service.name: "mon-service"` — des logs doivent remonter
3. Vérifier la présence du champ `log.level` sur les logs
4. Vérifier la présence du champ `trace.id` sur les logs produits pendant une requête
5. Depuis une transaction APM, tester le lien **"View logs"** vers Discover

→ Guide complet : [Vérifier l'instrumentation dans Kibana](../04-guides/05-verifier-instrumentation)
