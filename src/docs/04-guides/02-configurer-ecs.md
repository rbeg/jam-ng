---
id: configurer-ecs
title: Configurer les logs au format ECS
sidebar_label: Configurer ECS
sidebar_position: 2
---

# Configurer les logs au format ECS

## Prérequis

- Service Spring Boot 3.x
- Java 17 ou supérieur
- Logback (inclus par défaut dans Spring Boot)

---

## Étape 1 — Ajouter la dépendance Maven

```xml
<dependency>
  <groupId>co.elastic.logging</groupId>
  <artifactId>logback-ecs-encoder</artifactId>
  <version>1.5.0</version>
</dependency>
```

:::note
La version est gérée via le BOM Spring Boot si la dépendance y est référencée.
Vérifier la compatibilité avec la version de Spring Boot utilisée sur le projet.
:::

---

## Étape 2 — Configurer Logback

Créer ou modifier le fichier `src/main/resources/logback-spring.xml` :

```xml
<configuration>

  <springProperty name="APP_NAME"
                  source="spring.application.name"
                  defaultValue="unknown-service"/>
  <springProperty name="APP_VERSION"
                  source="spring.application.version"
                  defaultValue="unknown"/>
  <springProperty name="APP_ENV"
                  source="spring.profiles.active"
                  defaultValue="local"/>

  <appender name="ECS_CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
    <encoder class="co.elastic.logging.logback.EcsEncoder">
      <serviceName>${APP_NAME}</serviceName>
      <serviceVersion>${APP_VERSION}</serviceVersion>
      <serviceEnvironment>${APP_ENV}</serviceEnvironment>
      <includeOrigin>false</includeOrigin>
    </encoder>
  </appender>

  <!-- Profil local : format lisible en développement -->
  <springProfile name="local">
    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
      <encoder>
        <pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
      </encoder>
    </appender>
    <root level="DEBUG">
      <appender-ref ref="CONSOLE"/>
    </root>
  </springProfile>

  <!-- Tous les autres profils : format ECS JSON -->
  <springProfile name="!local">
    <root level="INFO">
      <appender-ref ref="ECS_CONSOLE"/>
    </root>
  </springProfile>

</configuration>
```

:::tip
Le profil `local` conserve un format lisible en développement. Le format ECS JSON
ne s'active qu'en dehors de l'environnement local, ce qui évite de rendre les logs
illisibles pour les développeurs au quotidien.
:::

---

## Étape 3 — Vérifier la configuration Spring Boot

Dans `application.yml`, s'assurer que les propriétés sont correctement déclarées :

```yaml
spring:
  application:
    name: payment-service
    version: '@project.version@'
  profiles:
    active: ${SPRING_PROFILES_ACTIVE:local}
```

La notation `'@project.version@'` permet à Maven de substituer automatiquement
la version du projet définie dans le `pom.xml`.

---

## Étape 4 — Vérifier localement

Démarrer l'application avec le profil `staging` ou `production` pour activer
l'encodage ECS :

```bash
java -jar target/payment-service.jar --spring.profiles.active=staging
```

Les logs doivent apparaître en JSON sur la sortie standard :

```json
{
  "@timestamp": "2024-11-15T10:23:45.123Z",
  "log.level": "INFO",
  "message": "Application démarrée",
  "service.name": "payment-service",
  "service.version": "2.3.1",
  "service.environment": "staging"
}
```

---

## Bonnes pratiques sur le contenu des messages

Un log conforme ECS structure les données. Un bon message de log rend l'investigation
possible. Les deux sont nécessaires.

```java
// ❌ À éviter
log.error("Erreur");
log.info("Traitement effectué");

// ✅ À privilégier
log.error("Échec traitement paiement — order.id: {}, motif: {}",
    order.getId(), e.getMessage(), e);

log.info("Paiement validé — order.id: {}, amount: {} {}",
    order.getId(), order.getAmount(), order.getCurrency());
```

Pour ajouter des champs structurés supplémentaires sans polluer le message :

```java
// Via MDC — les champs sont ajoutés au document ECS
MDC.put("order.id", order.getId());
MDC.put("user.id", userId);
try {
    log.info("Validation commande en cours");
    // ...
} finally {
    MDC.remove("order.id");
    MDC.remove("user.id");
}
```

---

## Pour aller plus loin

- [Standards › Logs ECS](../02-standards/01-logs-ecs)
- [logback-ecs-encoder — GitHub](https://github.com/elastic/ecs-logging-java)
- [ECS — Référence des champs](https://www.elastic.co/guide/en/ecs/current/ecs-field-reference.html)
