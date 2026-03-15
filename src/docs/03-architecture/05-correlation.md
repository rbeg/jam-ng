---
id: correlation
title: Corrélation entre les données
sidebar_label: Corrélation
sidebar_position: 5
---

# Corrélation entre les données

## Le principe

Les logs, les traces APM et les métriques sont stockés dans des index distincts.
Ce qui les relie, ce sont deux champs partagés, injectés automatiquement par l'agent
APM dans tous les documents produits pendant une transaction :

```
trace.id          →  Identifie une trace complète de bout en bout,
                     potentiellement sur plusieurs services
transaction.id    →  Identifie une transaction spécifique à l'intérieur
                     d'une trace
```

Ces deux champs sont la **colonne vertébrale de l'investigation** sur la plateforme.
Ils permettent de naviguer sans rupture entre les logs dans Discover et les traces
dans APM.

---

## Schéma de corrélation

```
┌─────────────────────────────────────────────────────────────────────┐
│  trace.id: 4bf92f3577b34da6a                                        │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  payment-service                                            │   │
│  │  Transaction: POST /api/v1/payments                         │   │
│  │  transaction.id: 00f067aa0ba902b7                           │   │
│  │                                                             │   │
│  │  ├── Span: SELECT FROM accounts      (postgresql)          │   │
│  │  ├── Span: POST /risk-evaluation     (http → risk-service) │   │
│  │  └── Span: SEND payment.processed    (kafka)               │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  risk-service  (appelé en tant que dépendance)              │   │
│  │  Transaction: POST /risk-evaluation                         │   │
│  │  transaction.id: a1b2c3d4e5f60001                           │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  Logs ECS (index logs-*)                                            │
│  ─────────────────────────────────────────────────────────────      │
│  Tous les logs produits pendant cette trace portent                 │
│  trace.id: 4bf92f3577b34da6a → navigation directe depuis APM       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Navigation dans Kibana

### Depuis APM vers les logs

Dans **Kibana › APM**, sélectionner une transaction puis cliquer sur
**"View logs"** ou **"Investigate in Discover"**. Kibana filtre automatiquement
sur le `trace.id` de la transaction sélectionnée et affiche tous les logs
correspondants.

### Depuis les logs vers APM

Dans **Kibana › Discover**, identifier un log portant un `trace.id`. Cliquer sur
la valeur du champ pour filtrer, ou utiliser le lien **"View in APM"** si configuré
dans la Data View.

### Recherche directe par trace

Dans Discover, sur la Data View `logs-*` ou `traces-apm-*` :

```
trace.id: "4bf92f3577b34da6a3ce929d0e0e4736"
```

Cette requête remonte tous les documents — logs et traces — liés à cette opération.

---

## Prérequis pour que la corrélation fonctionne

La corrélation est automatique à condition que trois éléments soient en place :

- [x] L'agent APM est configuré avec `log_correlation: true`
- [x] Les logs sont au format ECS (encodeur `logback-ecs-encoder`)
- [x] `service.name` est **identique** dans la configuration de l'agent APM
      et dans `logback-spring.xml`

:::warning
Si `service.name` diffère entre APM et les logs, Kibana ne peut pas proposer
la navigation directe entre les deux. C'est l'erreur de configuration la plus
fréquente sur la plateforme.
:::
