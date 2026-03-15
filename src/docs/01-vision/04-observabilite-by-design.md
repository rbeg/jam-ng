---
id: observabilite-by-design
title: Observabilité by design
sidebar_label: Observabilité by design
sidebar_position: 4
---

# L'observabilité ne s'improvise pas en production

## Le piège classique

Le scénario est connu de toutes les équipes. Le service est livré en production.
Une anomalie est détectée quelques jours plus tard. On ouvre Kibana. Les logs sont
absents, ou illisibles, ou pas au bon format. APM ne connaît pas le service. On ne
sait pas ce qui se passe, depuis quand, ni pourquoi.

Ce n'est pas un problème d'outillage. C'est un problème de **timing**. L'observabilité
a été traitée comme une tâche post-livraison, alors qu'elle aurait dû être pensée
dès le début.

:::warning
L'observabilité ajoutée après la mise en production coûte systématiquement plus cher
que l'observabilité pensée dès le raffinage — en temps, en stress, et en impact
utilisateur subi.
:::

## Intégrer l'observabilité dans chaque phase

### 🔎 Raffinage & cadrage

C'est ici que se posent les **bonnes questions métier** :

- Quels sont les parcours critiques de cette fonctionnalité ?
- Quels événements business faut-il absolument tracer ?
  *(commande passée, paiement échoué, utilisateur bloqué…)*
- Quelle est la criticité métier ? (`labels.business_criticality`)
- Quel `labels.business_use_case` rattacher à cette fonctionnalité ?
- Comment saura-t-on que ça fonctionne correctement en production ?

:::tip
Si l'équipe n'est pas capable de répondre à "comment saura-t-on que ça marche en
production ?", le raffinage n'est pas terminé.
:::

### 🏗️ Conception & design technique

C'est ici que se définissent les **choix d'instrumentation** :

- Quels logs produire, à quel niveau, avec quels champs ?
- Quelles métriques custom sont nécessaires en plus de ce qu'APM capture
  automatiquement ?
- Y a-t-il des appels inter-services à tracer particulièrement ?
- Les labels métier sont-ils définis et cohérents avec les autres services du domaine ?

Un schéma des logs attendus, même sommaire, évite les mauvaises surprises au moment
de l'intégration.

### 💻 Développement

C'est ici que l'instrumentation est **implémentée et vérifiée** :

- Les logs respectent le format ECS dès le premier commit
- L'agent APM est configuré avec `service.name`, `service.version`,
  `service.environment`
- Les labels métier sont posés sur les transactions et logs concernés
- Les logs sont **relus comme du code** : sont-ils lisibles ? utiles ?
  correctement niveautés ?

:::danger Mauvaise pratique
```
log.error("Erreur inattendue")
```
Un message sans contexte ne permet aucune investigation en production.
:::

:::tip Bonne pratique
```java
log.error("Échec validation commande — order.id: {}, reason: {}",
    order.getId(), e.getMessage());
```
Ce log permet d'identifier immédiatement la commande concernée et la cause de l'erreur.
:::

### ✅ Definition of Done

L'observabilité fait partie de la **Definition of Done** au même titre que les tests
ou la revue de code. Une story n'est pas terminée si :

- [ ] Les logs ne sont pas au format ECS
- [ ] L'agent APM n'est pas configuré sur le service
- [ ] Les événements métier critiques ne sont pas tracés
- [ ] Les labels `labels.business_use_case` et `labels.business_criticality`
      ne sont pas renseignés sur les parcours concernés
- [ ] Aucune vérification n'a été faite dans Kibana en environnement de dev ou staging

### 🚀 Mise en production

Si les étapes précédentes ont été respectées, la mise en production ne réserve
aucune surprise :

- Les logs arrivent correctement dans Elasticsearch
- APM reconnaît le service et ses transactions
- Les dashboards plateforme affichent déjà les golden signals du service
- En cas d'anomalie, l'équipe est **immédiatement autonome** pour investiguer

## Ce que ça change concrètement

| Sans anticipation | Avec anticipation |
|---|---|
| Les manques se découvrent en prod, sous pression | Les manques sont détectés en dev, sans urgence |
| Les logs sont illisibles ou absents | Les logs sont exploitables dès J+1 en prod |
| L'investigation prend des heures | L'investigation prend des minutes |
| L'équipe plateforme est sollicitée en urgence | L'équipe est autonome |
| Les dashboards sont construits après l'incident | Les dashboards existent avant le premier incident |

---

> *"Observable by design, not by accident."*
