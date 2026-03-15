---
id: logs-ecs
title: Logs — Format ECS
sidebar_label: Logs ECS
sidebar_position: 1
---

# Logs — Format ECS Layout

## ⛔ Obligatoire

Le format ECS (Elastic Common Schema) est le format de logs **obligatoire** sur tous
les services de la plateforme, sans exception.

## Pourquoi ECS ?

Dans une plateforme partagée, les logs de dizaines de services coexistent dans les
mêmes index Elasticsearch. Sans format commun :

- les recherches inter-services sont impossibles
- les dashboards ne peuvent pas agréger des données hétérogènes
- la corrélation avec les traces APM est perdue
- le temps d'investigation en incident est considérablement allongé

ECS garantit une structure cohérente, une corrélation automatique avec les traces APM,
et une compatibilité native avec Kibana.

:::note
Les champs de corrélation APM (`trace.id`, `transaction.id`) sont injectés
**automatiquement** dans les logs ECS par l'agent APM, à condition que
`log_correlation: true` soit activé dans sa configuration. Il n'y a rien à faire
manuellement pour ces champs.
:::

---

## Champs à configurer

### Champs obligatoires

Ces champs doivent être présents dans tous les logs. La plupart sont portés
automatiquement par l'encodeur ECS à partir de la configuration Spring Boot —
il suffit de les déclarer correctement dans `logback-spring.xml`.

| Champ | Description | Exemple |
|---|---|---|
| `@timestamp` | Horodatage ISO 8601 en UTC — géré automatiquement par l'encodeur | `2024-11-15T10:23:45.123Z` |
| `log.level` | Niveau de log en majuscules — géré automatiquement | `INFO`, `ERROR`, `WARN` |
| `message` | Message lisible et contextualisé — **à soigner** | `"Échec paiement commande #98765"` |
| `service.name` | Nom du service, stable, sans espace ni majuscule | `payment-service` |
| `service.environment` | Environnement de déploiement | `production`, `staging` |

### Champs recommandés

Ces champs enrichissent les logs et permettent des investigations plus précises.

| Champ | Description | Exemple |
|---|---|---|
| `service.version` | Version déployée — permet de corréler un incident avec une livraison | `2.3.1` |
| `user.id` | Identifiant de l'utilisateur connecté | `usr_44821` |
| `http.response.status_code` | Code HTTP de la réponse | `200`, `500` |
| `url.path` | Chemin de la requête | `/api/v1/payments` |
| `error.type` | Type d'exception Java en cas d'erreur | `PaymentGatewayException` |
| `error.message` | Message de l'exception | `Timeout après 3000ms` |

---

## Configuration Spring Boot

**`pom.xml`**
```xml
<dependency>
  <groupId>co.elastic.logging</groupId>
  <artifactId>logback-ecs-encoder</artifactId>
  <version>1.5.0</version>
</dependency>
```

**`logback-spring.xml`**
```xml
<configuration>
  <appender name="ECS_JSON" class="ch.qos.logback.core.ConsoleAppender">
    <encoder class="co.elastic.logging.logback.EcsEncoder">
      <serviceName>${spring.application.name}</serviceName>
      <serviceVersion>${spring.application.version}</serviceVersion>
      <serviceEnvironment>${spring.profiles.active}</serviceEnvironment>
    </encoder>
  </appender>

  <root level="INFO">
    <appender-ref ref="ECS_JSON" />
  </root>
</configuration>
```

:::tip
`service.name` doit être **identique** à la valeur configurée dans l'agent APM.
C'est ce qui permet de naviguer sans rupture entre les logs dans Discover et les
traces dans APM.
:::

---

## Bonnes pratiques sur le contenu des logs

La conformité ECS couvre la structure. Elle ne garantit pas la qualité du contenu.
Un log bien structuré mais sans contexte utile n'aide pas à investiguer.

:::danger À éviter
```java
log.error("Erreur inattendue");
log.warn("Problème");
log.info("OK");
```
Ces messages sont inutilisables en production.
:::

:::tip À privilégier
```java
log.error("Échec validation commande — order.id: {}, motif: {}",
    order.getId(), e.getMessage());

log.warn("Délai de réponse élevé — service: {}, duration_ms: {}",
    serviceName, duration);

log.info("Commande validée — order.id: {}, amount: {}, currency: {}",
    order.getId(), order.getAmount(), order.getCurrency());
```
Chaque log doit permettre de répondre à : *quoi, sur quoi, pourquoi.*
:::

### Règles de niveautage

| Niveau | Usage |
|---|---|
| `ERROR` | Erreur non récupérée, impact utilisateur avéré ou probable |
| `WARN` | Situation anormale récupérée, dégradation possible |
| `INFO` | Événement métier significatif (commande créée, paiement validé…) |
| `DEBUG` | Information technique utile en développement — désactivé en production |

:::warning
Ne pas logger à `ERROR` une exception métier attendue (ex : validation échouée,
ressource non trouvée). Cela fausse les taux d'erreur et génère du bruit dans
les alertes.
:::

---

## Vérifier la conformité de ses logs

Dans **Kibana › Discover**, sélectionner la Data View `logs-*` et filtrer :

```
service.name: "mon-service" AND NOT _exists_: "log.level"
```

Si des résultats remontent, des logs ne sont pas conformes ECS.

---

## Pour aller plus loin

- [Elastic Common Schema — Référence complète](https://www.elastic.co/guide/en/ecs/current/index.html)
- [logback-ecs-encoder — GitHub](https://github.com/elastic/ecs-logging-java)
