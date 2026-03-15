---
id: apm
title: APM — Agent et configuration
sidebar_label: APM
sidebar_position: 2
---

# APM — Agent et configuration

## ⛔ Obligatoire

L'agent APM Elastic est **obligatoire** sur tous les services Spring Boot de la
plateforme. Il est la source principale des traces distribuées et des métriques
de performance.

## Ce que l'agent APM fait automatiquement

Sans une ligne de code supplémentaire, l'agent APM capture et publie :

- toutes les **transactions HTTP** entrantes : méthode, path, status, durée, outcome
- tous les **appels sortants** : HTTP vers d'autres services, requêtes JDBC,
  opérations Kafka
- les **exceptions** non gérées
- les **métriques JVM** : heap, garbage collection, threads
- les champs de corrélation **`trace.id`** et **`transaction.id`** injectés
  automatiquement dans les logs ECS

:::note
La corrélation logs ↔ traces est automatique dès lors que `log_correlation: true`
est activé dans la configuration de l'agent et que les logs sont au format ECS.
Aucun code applicatif n'est nécessaire pour ces champs.
:::

---

## Configuration

### Dépendance Maven

```xml
<dependency>
  <groupId>co.elastic.apm</groupId>
  <artifactId>apm-agent-attach</artifactId>
  <version>1.44.0</version>
</dependency>
```

### `application.yml`

```yaml
elastic:
  apm:
    service_name: ${spring.application.name}
    service_version: ${spring.application.version}
    environment: ${spring.profiles.active}
    server_url: https://apm-server.plateforme.interne
    log_correlation: true
```

:::warning
`service_name` doit être **identique** à la valeur de `service.name` déclarée dans
`logback-spring.xml`. Une incohérence entre les deux rend la corrélation logs ↔ APM
impossible dans Kibana.
:::

---

## Ce que les équipes doivent configurer

L'agent fait le plus gros du travail automatiquement. Il reste deux champs à configurer
explicitement, car l'agent ne peut pas les inférer seul.

### `user.id` — Recommandé ✅

L'agent APM ne connaît pas l'identité de l'utilisateur. Pour l'associer aux
transactions et permettre de suivre un parcours utilisateur lors d'une investigation,
il faut l'injecter manuellement — idéalement dans un filtre HTTP global :

```java
import co.elastic.apm.api.ElasticApm;
import jakarta.servlet.*;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;

@Component
public class ApmUserContextFilter implements Filter {

    @Override
    public void doFilter(ServletRequest request,
                         ServletResponse response,
                         FilterChain chain)
                         throws IOException, ServletException {

        var authentication = SecurityContextHolder
            .getContext()
            .getAuthentication();

        if (authentication != null && authentication.isAuthenticated()) {
            ElasticApm.currentTransaction()
                .setUser(authentication.getName(), null, null);
        }

        chain.doFilter(request, response);
    }
}
```

### Labels métier — Recommandé ✅

Les labels métier (`business_use_case`, `business_criticality`, `business_domain`)
sont à poser sur les transactions concernées. Voir la page dédiée :
[Labels métier](./03-labels-metier).

---

## Vérifier que le service est visible dans APM

Dans **Kibana › APM › Services**, rechercher le nom du service. S'il n'apparaît pas
dans les minutes suivant le démarrage de l'application :

1. Vérifier que la dépendance Maven est présente et que la version est correcte
2. Vérifier que `server_url` pointe vers le bon APM Server
3. Vérifier les logs de démarrage — l'agent APM logue son initialisation au niveau `INFO`
4. Vérifier que `service_name` ne contient pas d'espaces ni de caractères spéciaux

:::tip Référence croisée
Le guide pas à pas de configuration de l'agent APM est disponible dans
[Guides › Configurer APM](../04-guides/03-configurer-apm).
:::

---

## Pour aller plus loin

- [Agent APM Java — Documentation officielle](https://www.elastic.co/guide/en/apm/agent/java/current/index.html)
- [Agent APM Java — Configuration complète](https://www.elastic.co/guide/en/apm/agent/java/current/configuration.html)
- [API publique de l'agent APM Java](https://www.elastic.co/guide/en/apm/agent/java/current/public-api.html)
