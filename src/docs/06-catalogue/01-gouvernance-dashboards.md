---
id: gouvernance-dashboards
title: Gouvernance des dashboards
sidebar_label: Gouvernance
sidebar_position: 1
---

# Gouvernance des dashboards

## Les trois niveaux

La plateforme distingue trois niveaux de dashboards avec des règles de gouvernance
distinctes. Cette organisation évite la prolifération de dashboards redondants,
maintient une cohérence visuelle et sémantique, et clarifie les responsabilités
de maintenance.

---

### Niveau 1 — Dashboards socles

**Maintenus par : équipe plateforme**

Dashboards universels, paramétrables, qui couvrent les Golden Signals pour tous les
services sans distinction. Un seul dashboard suffit pour l'ensemble des équipes —
le filtre `service.name` permet de l'adapter à n'importe quel service.

Ces dashboards constituent le **socle minimal** attendu sur tout service en production.
Ils sont créés et maintenus exclusivement par l'équipe plateforme.

Exemples : APM Overview, Logs applicatifs, Erreurs et exceptions.

---

### Niveau 2 — Dashboards technologiques

**Maintenus par : équipe plateforme**

Dashboards dédiés à une brique technique transverse utilisée par plusieurs équipes.
Filtrables par équipe ou par composant. Évitent que chaque équipe crée son propre
dashboard Kafka, son propre dashboard batch, etc.

Ces dashboards sont proposés par l'équipe plateforme lorsqu'un besoin transverse
est identifié sur plusieurs équipes.

Exemples : Kafka Connectors, Jobs batch, API Gateway.

---

### Niveau 3 — Dashboards domaine

**Maintenus par : équipes produit**

Dashboards spécifiques à un périmètre métier ou fonctionnel. Ils couvrent des besoins
qui ne peuvent pas être généralisés à toute la plateforme : endpoints spécifiques,
champs métier propres à un domaine, visualisations fonctionnelles.

Les équipes produit sont **responsables** de la création, de la maintenance et de
la documentation de ces dashboards. L'équipe plateforme fournit le template de départ
et les conventions à respecter.

:::warning
Un dashboard de niveau 3 ne doit pas dupliquer ce qui est déjà couvert par un
dashboard socle. Il doit le **compléter**, pas le remplacer.
:::

---

## Tableau de synthèse

| | Niveau 1 — Socles | Niveau 2 — Technologiques | Niveau 3 — Domaine |
|---|---|---|---|
| **Périmètre** | Tous les services | Par brique technique | Par domaine métier |
| **Créé par** | Équipe plateforme | Équipe plateforme | Équipe produit |
| **Maintenu par** | Équipe plateforme | Équipe plateforme | Équipe produit |
| **Documenté dans** | Ce catalogue | Ce catalogue | Ce catalogue (fiche synthèse) |
| **Template** | N/A | N/A | Obligatoire |
| **Revue** | Équipe plateforme | Équipe plateforme | Équipe produit + plateforme |

---

## Règles communes à tous les niveaux

Tout dashboard mis en production sur la plateforme doit respecter ces règles :

- [ ] Nommage conforme à la convention `[Domaine] — [Périmètre] — [Type]`
- [ ] Filtres dynamiques sur `service.name` et `service.environment`
- [ ] Golden Signals visibles en en-tête (niveaux 1 et 2) ou référencés (niveau 3)
- [ ] Documenté dans ce catalogue
- [ ] Équipe plateforme informée avant mise en production

:::tip Référence croisée
Le template Kibana exportable pour les dashboards de niveau 3 est disponible dans
[Template domaine](./04-template-domaine/guide-construction).
:::
