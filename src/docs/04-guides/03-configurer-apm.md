---
id: configurer-apm
title: Configurer l'agent APM
sidebar_label: Configurer APM
sidebar_position: 3
---

# Configurer l'agent APM

## Prérequis

- Service Spring Boot 3.x
- Java 17 ou supérieur
- Logs configurés au format ECS (voir [Configurer ECS](./02-configurer-ecs))

---

## Étape 1 — Ajouter la dépendance Maven

```xml
<dependency>
  <groupId>co.elastic.apm</groupId>
  <artifactId>apm-agent-attach</artifactId>
  <version>1.44.0</version>
</dependency>
```

---

## Étape 2 — Configurer l'agent

Dans `application.yml` :

```yaml
elastic:
  apm:
    service_name: ${spring.application.name}
    service_version: ${spring.application.version}
    environment: ${spring.profiles.active}
    server_url: https://apm-server.plateforme.interne
    log_correlation: true
    capture_body: off
    transaction_sample_rate: 1.0
```

| Propriété | Description |
|---|---|
| `service_name` | Doit être **identique** au `service.name` dans Logback |
| `service_version` | Permet de corréler un incident avec une livraison |
| `environment` | Permet de filtrer par environnement dans APM |
| `server_url` | URL de l'APM Server de la plateforme |
| `log_correlation` | Active l'injection de `trace.id` dans les logs ECS — **ne pas désactiver** |
| `capture_body` | Désactivé par défaut pour éviter de capturer des données sensibles |
| `transaction_sample_rate` | 1.0 = 100% des transactions sont tracées |

:::warning
`service_name` doit être **strictement identique** à la valeur de `service.name`
déclarée dans `logback-spring.xml`. Une incohérence casse la corrélation logs ↔ APM
dans Kibana.
:::

---

## Étape 3 — Ajouter le contexte utilisateur

L'agent APM ne connaît pas l'identité de l'utilisateur. L'injecter dans un filtre
HTTP global :

```java
import co.elastic.apm.api.ElasticApm;
import jakarta.servlet.*;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;

@Component
public class ApmUserContextFilter implements Filter {

    @Override
    public void doFilter(ServletRequest request,
                         ServletResponse response,
                         FilterChain chain)
                         throws IOException, ServletException {

        Authentication auth = SecurityContextHolder
            .getContext()
            .getAuthentication();

        if (auth != null && auth.isAuthenticated()
                && !"anonymousUser".equals(auth.getPrincipal())) {
            ElasticApm.currentTransaction()
                .setUser(auth.getName(), null, null);
        }

        chain.doFilter(request, response);
    }
}
```

---

## Étape 4 — Configurer par environnement

Il est recommandé de surcharger la configuration APM par profil Spring Boot pour
adapter le `server_url` à chaque environnement :

**`application-staging.yml`**
```yaml
elastic:
  apm:
    server_url: https://apm-server-staging.plateforme.interne
    transaction_sample_rate: 1.0
```

**`application-production.yml`**
```yaml
elastic:
  apm:
    server_url: https://apm-server-prod.plateforme.interne
    transaction_sample_rate: 0.1
```

:::tip
En production, un taux d'échantillonnage de 10% (`0.1`) est souvent suffisant
pour les services à fort trafic, afin de réduire le volume de données APM.
Sur les services à faible trafic ou les parcours critiques, conserver `1.0`.
:::

---

## Pour aller plus loin

- [Standards › APM](../02-standards/02-apm)
- [Agent APM Java — Documentation officielle](https://www.elastic.co/guide/en/apm/agent/java/current/index.html)
- [Agent APM Java — Configuration complète](https://www.elastic.co/guide/en/apm/agent/java/current/configuration.html)
