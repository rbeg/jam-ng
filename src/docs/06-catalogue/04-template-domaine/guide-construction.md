---
id: guide-construction
title: Guide de construction — Dashboard domaine
sidebar_label: Guide de construction
sidebar_position: 1
---

# Guide de construction — Dashboard domaine (niveau 3)

Ce guide s'adresse aux équipes qui souhaitent créer un dashboard spécifique à leur
périmètre métier ou fonctionnel. Il définit ce qu'un dashboard de niveau 3 doit
contenir, comment le construire, et les règles à respecter avant sa mise en production.

:::note
Avant de créer un dashboard de niveau 3, vérifier que le besoin n'est pas déjà
couvert par un [dashboard socle](../02-dashboards-socles/index) ou un
[dashboard technologique](../03-dashboards-technologiques/index).
:::

---

## Étape 1 — Définir le besoin

Avant d'ouvrir Kibana, répondre à ces trois questions :

> *À qui est destiné ce dashboard ?*
> *(développeurs, ops, product manager, équipe métier)*
>
> *Quelles questions doit-il permettre de répondre ?*
> *(3 à 5 questions précises, pas plus)*
>
> *Dans quel contexte sera-t-il consulté ?*
> *(supervision quotidienne, investigation d'incident, revue hebdomadaire)*

Un dashboard qui ne répond pas à des questions précises finit par ne servir à personne.

---

## Étape 2 — Respecter la structure de base

Tout dashboard de niveau 3 doit inclure en en-tête les **Golden Signals** du ou des
services concernés. Le reste du dashboard est libre selon le besoin métier.

Structure minimale attendue :

```
┌──────────────────────────────────────────────────────────────────┐
│  En-tête : nom du service / domaine, environnement, période      │
├──────────────────┬───────────────────┬───────────────────────────┤
│  Taux d'erreur   │  Latence p95/p99  │  Trafic (req/min)         │
├──────────────────┴───────────────────┴───────────────────────────┤
│  [Visualisations spécifiques au domaine]                         │
│  ex : taux de conversion, endpoints critiques, données métier    │
└──────────────────────────────────────────────────────────────────┘
```

---

## Étape 3 — Utiliser les filtres dynamiques

Les dashboards de niveau 3 doivent utiliser des **filtres Kibana paramétrables**
plutôt que des valeurs en dur. Cela permet de réutiliser le dashboard sur plusieurs
environnements sans avoir à le dupliquer.

Filtres recommandés à exposer :

- `service.name`
- `service.environment`
- `labels.business_use_case` si applicable

---

## Étape 4 — Respecter la convention de nommage

```
[Domaine] — [Service ou périmètre] — [Type]

Exemples :
Payment — payment-service — Supervision
Checkout — Parcours complet — Vue métier
Identity — Authentification — Erreurs
```

Voir [Conventions de nommage](./conventions-nommage) pour le détail.

---

## Étape 5 — Documenter le dashboard

Tout dashboard de niveau 3 doit être documenté dans ce catalogue. La fiche de
documentation doit inclure :

- Nom Kibana exact
- Objectif en une phrase
- Audience cible
- Index utilisés
- Filtres disponibles
- Utilisation typique

Utiliser le modèle de fiche ci-dessous.

---

## Modèle de fiche de documentation

```markdown
## Fiche synthèse

| | |
|---|---|
| **Nom Kibana** | `[Domaine] — [Service] — [Type]` |
| **Niveau** | 3 — Domaine |
| **Maintenu par** | [Équipe] |
| **Index utilisés** | `traces-apm-*`, `logs-*` |
| **Audience** | [Développeurs / Ops / Product] |

## Objectif

[Une phrase décrivant ce que ce dashboard permet de faire.]

## Contenu

[Description des sections et visualisations principales.]

## Filtres disponibles

| Filtre | Description |
|---|---|
| `service.name` | … |
| `service.environment` | … |

## Utilisation typique

[2-3 cas d'usage concrets.]
```

---

## Checklist avant mise en production

- [ ] Les Golden Signals sont visibles en en-tête
- [ ] Le nommage respecte la convention plateforme
- [ ] Les filtres `service.name` et `service.environment` sont paramétrables
- [ ] Le dashboard est documenté dans le catalogue
- [ ] L'équipe plateforme a été informée (voir [Faire une demande](../../07-gouvernance/03-demandes))

:::tip Référence croisée
La checklist complète est également disponible dans
[Checklist mise en production](./checklist-mise-en-prod).
:::
