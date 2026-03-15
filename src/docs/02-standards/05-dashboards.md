---
id: dashboards
title: Dashboards
sidebar_label: Dashboards
sidebar_position: 5
---

# Standards de construction des dashboards

## Principes généraux

Un dashboard n'est pas une collection de visualisations. C'est un **outil de décision**
qui répond à des questions précises, pour une audience identifiée, dans un contexte
d'utilisation défini.

Avant de créer un dashboard, trois questions préalables :

> *À qui est-il destiné ?*
>
> *Quelles questions doit-il permettre de répondre ?*
>
> *Dans quel contexte sera-t-il consulté ?*

:::tip
Avant de créer un nouveau dashboard, vérifier que le besoin n'est pas déjà couvert
par un dashboard socle existant, éventuellement filtrable sur le service ou le domaine
concerné. Voir le [Catalogue des assets](../06-catalogue/index).
:::

---

## Les trois niveaux de dashboards

La plateforme distingue trois niveaux de dashboards, avec des règles de gouvernance
distinctes pour chacun :

| Niveau | Description | Maintenu par |
|---|---|---|
| **Niveau 1 — Socles** | Universels, paramétrables, couvrent les Golden Signals pour tous les services | Équipe plateforme |
| **Niveau 2 — Technologiques** | Par brique technique transverse (Kafka, batch…), filtrables par équipe | Équipe plateforme |
| **Niveau 3 — Domaine** | Spécifiques à un périmètre métier ou fonctionnel, construits sur le template plateforme | Équipes produit |

:::note
Les équipes produit sont **responsables** de leurs dashboards de niveau 3. L'équipe
plateforme fournit le template, les conventions de nommage, et la checklist de mise
en production — pas le contenu.
:::

---

## Structure recommandée

Tout dashboard de supervision d'un service doit suivre cette structure, inspirée
des [Golden Signals](../01-vision/06-golden-signals) :

```
┌──────────────────────────────────────────────────────────────────┐
│  En-tête : nom du service, environnement, période de temps       │
├──────────────────┬───────────────────┬───────────────────────────┤
│  Taux d'erreur   │  Latence p95/p99  │  Trafic (req/min)         │
├──────────────────┴───────────────────┴───────────────────────────┤
│  Évolution temporelle — séries chronologiques                    │
├──────────────────────────────────────────────────────────────────┤
│  Détail par endpoint ou par parcours métier                      │
├──────────────────────────────────────────────────────────────────┤
│  Erreurs récentes — table avec message, type, trace.id           │
└──────────────────────────────────────────────────────────────────┘
```

---

## Convention de nommage

Une convention de nommage uniforme est obligatoire pour que les dashboards restent
identifiables dans Kibana, quelle que soit l'équipe qui les a créés.

```
[Domaine] — [Service ou périmètre] — [Type]
```

Exemples :

```
Payment — payment-service — Supervision
Checkout — Parcours complet — Vue métier
Plateforme — APM Overview — Tous services
Kafka — Connecteurs — Monitoring
```

---

## Recommandations de construction

### Exposer les Golden Signals en en-tête

Tout dashboard de supervision doit exposer en premier plan les quatre Golden Signals :
taux d'erreur, latence (p95 minimum), trafic, et saturation si applicable. Ce sont
les premiers indicateurs consultés lors d'une investigation.

### Utiliser des filtres dynamiques

Utiliser des filtres Kibana sur `service.name`, `service.environment` et
`labels.business_use_case` pour rendre le dashboard réutilisable sans duplication.
Un dashboard paramétrable vaut mieux que cinq dashboards identiques filtrés en dur.

### Préférer les séries chronologiques

Une valeur instantanée ne permet pas de décider. Une série chronologique montre la
tendance, les pics, la corrélation avec un événement (déploiement, pic de trafic).
Toujours privilégier la dimension temporelle pour les métriques de supervision.

### Documenter le dashboard

Tout dashboard mis en production doit être décrit dans le
[Catalogue des assets](../06-catalogue/index) avec au minimum :
son objectif, son audience cible, les index utilisés, et les filtres disponibles.

### Ne pas multiplier les dashboards

Un dashboard exhaustif vaut mieux que plusieurs dashboards partiels qui se chevauchent.
En cas de doute, enrichir un dashboard existant plutôt qu'en créer un nouveau.

---

## Checklist avant mise en production

- [ ] Le dashboard respecte la convention de nommage
- [ ] Les quatre Golden Signals sont visibles en en-tête
- [ ] Les filtres `service.name` et `service.environment` sont paramétrables
- [ ] Les visualisations utilisent des séries chronologiques
- [ ] Le dashboard est documenté dans le catalogue des assets
- [ ] L'équipe plateforme a été informée de l'ajout

:::tip Référence croisée
Le template Kibana exportable et le guide de construction pour les dashboards de
niveau 3 sont disponibles dans
[Catalogue › Template domaine](../06-catalogue/04-template-domaine/guide-construction).
:::
