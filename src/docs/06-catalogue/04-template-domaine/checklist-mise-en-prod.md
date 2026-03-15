---
id: checklist-mise-en-prod
title: Checklist mise en production
sidebar_label: Checklist mise en production
sidebar_position: 3
---

# Checklist — Mise en production d'un dashboard

À compléter avant toute mise en production d'un dashboard de niveau 3.

---

## Conception

- [ ] Le besoin a été défini avec les trois questions préalables (audience, questions,
      contexte d'utilisation)
- [ ] Le besoin n'est pas couvert par un dashboard socle ou technologique existant
- [ ] Les visualisations répondent à des questions précises et identifiées

## Structure

- [ ] Les Golden Signals (taux d'erreur, latence, trafic) sont visibles en en-tête
- [ ] Les visualisations utilisent des séries chronologiques (pas uniquement des
      valeurs instantanées)
- [ ] Aucune valeur n'est filtrée en dur dans les visualisations (tout passe par
      des filtres paramétrables)

## Nommage et filtres

- [ ] Le nom respecte la convention `[Domaine] — [Service ou périmètre] — [Type]`
- [ ] Les filtres `service.name` et `service.environment` sont paramétrables
- [ ] Le filtre `labels.business_use_case` est exposé si le dashboard couvre un
      parcours métier

## Documentation

- [ ] Une fiche de documentation a été rédigée (voir
      [Guide de construction](./guide-construction))
- [ ] La fiche a été ajoutée au catalogue des assets

## Validation

- [ ] Le dashboard a été testé sur au moins deux environnements (`staging`,
      `production`)
- [ ] L'équipe plateforme a été informée avant la mise en production (voir
      [Faire une demande](../../07-gouvernance/03-demandes))
- [ ] Un responsable de maintenance est identifié dans l'équipe

---

:::warning
Un dashboard mis en production sans passer par cette checklist pourra être retiré
par l'équipe plateforme lors du cycle de revue trimestriel.
:::
