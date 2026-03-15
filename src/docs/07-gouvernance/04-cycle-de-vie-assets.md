---
id: cycle-de-vie-assets
title: Cycle de vie des assets
sidebar_label: Cycle de vie des assets
sidebar_position: 4
---

# Cycle de vie des assets

Cette page décrit comment les dashboards et alertes sont créés, maintenus, revus,
et éventuellement dépréciés sur la plateforme.

---

## Création

Tout nouvel asset (dashboard ou alerte) suit ce processus avant d'être considéré
comme actif :

1. **Besoin identifié** — question à laquelle l'asset doit répondre
2. **Validation du niveau** — socle, technologique ou domaine
3. **Construction** — en respect des standards et conventions
4. **Documentation** — fiche dans le catalogue des assets
5. **Revue** — par l'équipe plateforme (niveaux 1 et 2) ou l'équipe produit +
   plateforme (niveau 3)
6. **Mise en production** — après validation de la checklist

---

## Maintenance

| Niveau | Responsable de maintenance | Fréquence de revue |
|---|---|---|
| 1 — Socles | Équipe plateforme | Trimestrielle |
| 2 — Technologiques | Équipe plateforme | Trimestrielle |
| 3 — Domaine | Équipe produit | À la charge de l'équipe |

Lors de chaque revue, les points vérifiés sont :

- L'asset répond-il toujours à un besoin actif ?
- Les seuils et filtres sont-ils toujours pertinents ?
- La documentation est-elle à jour ?
- Le responsable de maintenance est-il toujours identifié ?

---

## Dépréciation

Un asset est déprécié lorsqu'il ne répond plus à un besoin actif, qu'il est dupliqué
par un asset plus récent, ou que le service qu'il couvre est décommissionné.

**Processus de dépréciation :**

1. L'équipe plateforme (ou l'équipe produit pour le niveau 3) signale l'asset comme
   déprécié sur le canal `#plateforme-observabilite`
2. Un délai de 30 jours est accordé pour les éventuelles objections
3. Sans objection, l'asset est archivé dans Kibana et sa fiche est retirée du catalogue

:::warning
Un dashboard ou une alerte non maintenu et non documenté dans le catalogue peut être
déprécié sans délai lors du cycle de revue trimestriel.
:::

---

## Suppression

La suppression définitive d'un asset ne peut être effectuée que par l'équipe plateforme,
après archivage. Un asset archivé reste accessible en lecture seule pendant 90 jours
avant suppression définitive.
