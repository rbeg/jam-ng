---
id: verifier-instrumentation
title: Vérifier l'instrumentation dans Kibana
sidebar_label: Vérifier l'instrumentation
sidebar_position: 5
---

# Vérifier l'instrumentation dans Kibana

Une fois le service configuré et déployé en staging, ces vérifications permettent
de s'assurer que tout remonte correctement avant la mise en production.

---

## 1. Vérifier la présence dans APM

**Kibana › APM › Services**

Le service doit apparaître dans la liste avec son nom exact (`service.name`).

Si le service n'apparaît pas après quelques minutes :

- Vérifier que la dépendance `apm-agent-attach` est bien présente dans le `pom.xml`
- Vérifier les logs de démarrage de l'application — l'agent logue son initialisation
- Vérifier que `server_url` pointe vers le bon APM Server
- Vérifier que le service a bien reçu des requêtes depuis son démarrage

---

## 2. Vérifier les transactions

**Kibana › APM › Services › [mon-service] › Transactions**

- Les transactions doivent être visibles avec le bon type (`request`, `messaging`…)
- Le nom des transactions doit être lisible (`POST /api/v1/payments` et non
  `transaction_0` ou équivalent)
- Le taux d'erreur et la latence doivent être cohérents avec l'activité du service

---

## 3. Vérifier les logs

**Kibana › Discover** — Data View `Logs applicatifs`

Filtrer sur le service :

```
service.name: "mon-service"
```

Vérifier que :

- [ ] Les documents remontent bien
- [ ] Le champ `log.level` est présent et en majuscules (`INFO`, `ERROR`…)
- [ ] Le champ `service.environment` correspond au bon environnement
- [ ] Le champ `trace.id` est présent sur les logs produits pendant une transaction

Pour détecter des logs non conformes ECS :

```
service.name: "mon-service" AND NOT _exists_: "log.level"
```

Si des résultats remontent, des logs ne passent pas par l'encodeur ECS.

---

## 4. Vérifier la corrélation logs ↔ APM

**Kibana › APM › Services › [mon-service] › Transactions**

Sélectionner une transaction, puis cliquer sur **"View logs"** ou
**"Investigate in Discover"**. Kibana doit afficher les logs filtrés sur le
`trace.id` de cette transaction.

Si aucun log n'apparaît :

- Vérifier que `log_correlation: true` est bien activé dans la configuration APM
- Vérifier que `service.name` dans APM et dans Logback sont **strictement identiques**

---

## 5. Vérifier les labels métier

**Kibana › Discover** — Data View `Logs applicatifs`

```
service.name: "mon-service" AND _exists_: "labels.business_use_case"
```

Si aucun résultat ne remonte, les labels ne sont pas posés ou le MDC n'est pas
correctement configuré.

**Kibana › APM › Services › [mon-service] › Transactions**

Ouvrir une transaction et vérifier dans l'onglet **"Labels"** que les labels métier
sont présents.

---

## Récapitulatif des vérifications

| Vérification | Où | Résultat attendu |
|---|---|---|
| Service visible | APM › Services | Service présent dans la liste |
| Transactions | APM › Services › Transactions | Transactions typées et nommées correctement |
| Logs présents | Discover › `logs-*` | Documents avec champs ECS complets |
| Corrélation | APM › Transaction › View logs | Logs filtrés sur `trace.id` |
| Labels métier | Discover + APM › Labels | Labels visibles dans les deux sources |

:::tip
En cas de doute sur un résultat, ne pas hésiter à contacter l'équipe plateforme
avant la mise en production. Voir [Gouvernance › Faire une demande](../07-gouvernance/03-demandes).
:::
