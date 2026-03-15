---
id: kibana-dashboards
title: Kibana › Dashboards
sidebar_label: Dashboards
sidebar_position: 3
---

# Kibana › Dashboards — Naviguer et interpréter

## Accéder aux dashboards

**Kibana › Dashboards**

Les dashboards sont organisés par convention de nommage :
`[Domaine] — [Service ou périmètre] — [Type]`

Utiliser la barre de recherche pour trouver un dashboard par domaine ou par service.

:::tip
Avant d'investiguer manuellement dans Discover ou APM, vérifier si un dashboard
couvre déjà le besoin. Les dashboards socles et technologiques sont documentés dans
le [Catalogue des assets](../06-catalogue/index).
:::

---

## Utiliser les filtres

La plupart des dashboards plateforme exposent des filtres paramétrables en haut de
page :

- **`service.name`** : filtrer sur un service spécifique
- **`service.environment`** : isoler production, staging…
- **`labels.business_use_case`** : restreindre à un parcours métier

Modifier ces filtres sans éditer le dashboard : utiliser la barre de filtres Kibana
en haut de l'interface (`Add filter`).

---

## Interpréter les visualisations

### Séries chronologiques

Les courbes temporelles montrent l'évolution d'une métrique sur la période
sélectionnée. Points d'attention :

- Une **rupture de pente** indique un changement de comportement — souvent corrélé
  avec un déploiement ou un événement infrastructure
- Un **pic isolé** est souvent moins préoccupant qu'une **tendance à la hausse**
  progressive
- Comparer toujours avec la période précédente pour contextualiser

### Jauges et valeurs instantanées

Les jauges affichent la valeur courante d'une métrique. Elles sont utiles pour
un état des lieux rapide mais insuffisantes seules — toujours les lire en complément
d'une série chronologique.

### Tables

Les tables listent des événements ou des agrégats. Dans les dashboards plateforme,
elles servent typiquement à afficher les erreurs récentes, les transactions les plus
lentes, ou les services les plus dégradés.

---

## Modifier la période

Le sélecteur de période en haut à droite s'applique à toutes les visualisations
du dashboard. Périodes recommandées selon le contexte :

| Contexte | Période recommandée |
|---|---|
| Investigation d'un incident en cours | Last 15 min / Last 1 hour |
| Analyse post-incident | Période personnalisée autour de l'incident |
| Revue hebdomadaire | Last 7 days |
| Revue mensuelle | Last 30 days |

---

## Pour aller plus loin

- [Catalogue des assets](../06-catalogue/index)
- [Kibana Dashboards — Documentation officielle](https://www.elastic.co/guide/en/kibana/current/dashboard.html)
