---
id: ajouter-labels-metier
title: Ajouter les labels métier
sidebar_label: Labels métier
sidebar_position: 4
---

# Ajouter les labels métier

## Prérequis

- Agent APM configuré (voir [Configurer APM](./03-configurer-apm))
- Logs au format ECS configurés (voir [Configurer ECS](./02-configurer-ecs))
- Valeurs de labels définies et validées avec les autres services du domaine

---

## Étape 1 — Définir les valeurs

Avant d'implémenter, définir les valeurs en cohérence avec les autres services
du même domaine fonctionnel. Des valeurs incohérentes entre services rendent
l'agrégation impossible.

| Label | Ma valeur | Valeurs utilisées dans le domaine |
|---|---|---|
| `business_use_case` | ex : `checkout` | `checkout`, `cart`, `catalog`… |
| `business_criticality` | ex : `high` | `low`, `medium`, `high`, `critical` |
| `business_domain` | ex : `payment` | `payment`, `catalog`, `identity`… |

---

## Étape 2 — Implémenter un filtre global

La pose des labels dans un filtre HTTP centralisé est l'approche recommandée.
Elle évite la duplication dans chaque contrôleur et garantit la présence des labels
sur toute la transaction.

```java
import co.elastic.apm.api.ElasticApm;
import jakarta.servlet.*;
import jakarta.servlet.http.HttpServletRequest;
import org.slf4j.MDC;
import org.springframework.stereotype.Component;

@Component
public class ApmBusinessContextFilter implements Filter {

    @Override
    public void doFilter(ServletRequest request,
                         ServletResponse response,
                         FilterChain chain)
                         throws IOException, ServletException {

        HttpServletRequest httpRequest = (HttpServletRequest) request;

        String useCase     = resolveUseCase(httpRequest);
        String criticality = resolveCriticality(useCase);
        String domain      = "payment"; // fixe pour ce service

        // Labels sur la transaction APM
        ElasticApm.currentTransaction()
            .addLabel("business_use_case",   useCase)
            .addLabel("business_criticality", criticality)
            .addLabel("business_domain",      domain);

        // Labels dans les logs via MDC
        MDC.put("labels.business_use_case",    useCase);
        MDC.put("labels.business_criticality", criticality);
        MDC.put("labels.business_domain",      domain);

        try {
            chain.doFilter(request, response);
        } finally {
            MDC.remove("labels.business_use_case");
            MDC.remove("labels.business_criticality");
            MDC.remove("labels.business_domain");
        }
    }

    private String resolveUseCase(HttpServletRequest request) {
        String path = request.getRequestURI();
        if (path.startsWith("/api/v1/payments")) return "checkout";
        if (path.startsWith("/api/v1/refunds"))  return "refund";
        return "unknown";
    }

    private String resolveCriticality(String useCase) {
        return switch (useCase) {
            case "checkout" -> "critical";
            case "refund"   -> "high";
            default         -> "low";
        };
    }
}
```

:::warning
Toujours nettoyer le MDC dans un bloc `finally`. Sans cela, les labels peuvent
contaminer les logs des requêtes suivantes traitées par le même thread du pool.
:::

---

## Étape 3 — Cas des consommateurs Kafka

Pour les services qui consomment des messages Kafka, les labels doivent être posés
dans le listener, car il n'y a pas de filtre HTTP :

```java
@KafkaListener(topics = "payment.requested")
public void onPaymentRequested(PaymentRequestedEvent event) {

    ElasticApm.currentTransaction()
        .addLabel("business_use_case",    "checkout")
        .addLabel("business_criticality", "critical")
        .addLabel("business_domain",      "payment");

    MDC.put("labels.business_use_case",    "checkout");
    MDC.put("labels.business_criticality", "critical");
    MDC.put("labels.business_domain",      "payment");

    try {
        paymentService.process(event);
    } finally {
        MDC.remove("labels.business_use_case");
        MDC.remove("labels.business_criticality");
        MDC.remove("labels.business_domain");
    }
}
```

---

## Pour aller plus loin

- [Standards › Labels métier](../02-standards/03-labels-metier)
- [API publique de l'agent APM Java](https://www.elastic.co/guide/en/apm/agent/java/current/public-api.html)
