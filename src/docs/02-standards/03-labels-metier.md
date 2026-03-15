---
id: labels-metier
title: Labels métier
sidebar_label: Labels métier
sidebar_position: 3
---

# Labels métier

## ✅ Recommandé — ⛔ Obligatoire sur les parcours critiques

Les labels métier sont **fortement recommandés** sur tout service participant à un
parcours utilisateur identifié. Ils sont **obligatoires** sur les services dont
`business_criticality` est `high` ou `critical`.

## Pourquoi des labels métier ?

Un taux d'erreur de 2% ne dit rien sans contexte. S'il concerne le parcours de
paiement en période de forte activité, c'est un incident critique. S'il concerne
une API de consultation de catalogue en staging, ce n'est pas la même urgence.

Les labels métier permettent de **donner du sens aux signaux techniques** : construire
des dashboards par domaine fonctionnel, contextualiser les alertes, corréler une
dégradation technique avec un impact utilisateur.

---

## Labels disponibles

:::warning Note technique ECS
Le champ `labels` dans ECS est à plat — il n'accepte pas de sous-objets imbriqués.
Les labels métier utilisent la convention `business_*` avec un underscore.
`labels.business_use_case` est correct. `labels.business.use_case` ne l'est pas
et sera rejeté par le mapping Elasticsearch.
:::

| Label | Valeurs attendues | Description |
|---|---|---|
| `labels.business_use_case` | `checkout`, `onboarding`, `search`… | Parcours ou cas d'usage métier |
| `labels.business_criticality` | `low`, `medium`, `high`, `critical` | Criticité métier de l'opération |
| `labels.business_domain` | `payment`, `catalog`, `identity`… | Domaine fonctionnel |

:::tip
Les valeurs de ces labels doivent être **cohérentes entre tous les services d'un même
domaine**. Un parcours `checkout` instrumenté différemment selon les services rend
l'agrégation impossible. Concerter les valeurs au niveau du domaine fonctionnel avant
de les implémenter.
:::

---

## Implémentation

Les labels doivent être posés à la fois sur les **transactions APM** et dans les
**logs via MDC**, pour garantir leur présence dans les deux sources de données.

### Sur les transactions APM

```java
import co.elastic.apm.api.ElasticApm;

// À poser le plus tôt possible dans le traitement de la requête
// idéalement dans le contrôleur ou un filtre dédié
ElasticApm.currentTransaction()
    .addLabel("business_use_case", "checkout")
    .addLabel("business_criticality", "high")
    .addLabel("business_domain", "payment");
```

### Dans les logs via MDC

```java
import org.slf4j.MDC;

try {
    MDC.put("labels.business_use_case", "checkout");
    MDC.put("labels.business_criticality", "high");
    MDC.put("labels.business_domain", "payment");

    // traitement métier...

} finally {
    MDC.remove("labels.business_use_case");
    MDC.remove("labels.business_criticality");
    MDC.remove("labels.business_domain");
}
```

:::warning
Toujours nettoyer le MDC dans un bloc `finally`. Un MDC non nettoyé peut contaminer
les logs des requêtes suivantes traitées par le même thread.
:::

### Avec un filtre global

Pour éviter la duplication dans chaque contrôleur, il est recommandé de centraliser
la pose des labels dans un filtre HTTP, aux côtés du filtre `user.id` :

```java
@Component
public class ApmBusinessContextFilter implements Filter {

    @Override
    public void doFilter(ServletRequest request,
                         ServletResponse response,
                         FilterChain chain)
                         throws IOException, ServletException {

        // Résolution du contexte métier selon la requête entrante
        String useCase = resolveUseCase((HttpServletRequest) request);
        String criticality = resolveCriticality(useCase);
        String domain = resolveDomain((HttpServletRequest) request);

        ElasticApm.currentTransaction()
            .addLabel("business_use_case", useCase)
            .addLabel("business_criticality", criticality)
            .addLabel("business_domain", domain);

        MDC.put("labels.business_use_case", useCase);
        MDC.put("labels.business_criticality", criticality);
        MDC.put("labels.business_domain", domain);

        try {
            chain.doFilter(request, response);
        } finally {
            MDC.remove("labels.business_use_case");
            MDC.remove("labels.business_criticality");
            MDC.remove("labels.business_domain");
        }
    }
}
```

---

## Ce que ça permet dans Kibana

Avec ces labels en place, il devient possible de construire des visualisations
directement orientées business :

- taux d'erreur par `labels.business_use_case`
- latence p95 par `labels.business_domain`
- volume de transactions par parcours et par environnement
- alertes déclenchées uniquement sur les parcours `critical`

:::tip Référence croisée
Le guide d'implémentation pas à pas est disponible dans
[Guides › Ajouter les labels métier](../04-guides/04-ajouter-labels-metier).
:::
