---
id: onboarding
title: Checklist d'onboarding nouveau service
sidebar_label: Checklist onboarding
sidebar_position: 1
---

# Checklist d'onboarding nouveau service

Cette checklist couvre tout ce qu'un nouveau service Spring Boot doit mettre en place
pour être conforme aux standards d'observabilité de la plateforme. Elle peut être
utilisée comme critère d'acceptance lors de la mise en production.

---

## 1. Logs ECS

- [ ] La dépendance `logback-ecs-encoder` est présente dans le `pom.xml`
- [ ] `logback-spring.xml` est configuré avec `EcsEncoder`
- [ ] `service.name` est déclaré et cohérent avec le nom APM
- [ ] `service.version` est déclaré et valorisé depuis `${spring.application.version}`
- [ ] `service.environment` est déclaré et valorisé depuis `${spring.profiles.active}`
- [ ] Les messages de logs sont contextualisés (identifiants métier, causes d'erreur)
- [ ] Le niveautage ERROR / WARN / INFO est correct et ne génère pas de bruit

→ Guide détaillé : [Configurer les logs au format ECS](./02-configurer-ecs)

---

## 2. Agent APM

- [ ] La dépendance `apm-agent-attach` est présente dans le `pom.xml`
- [ ] `application.yml` contient la configuration APM complète
- [ ] `service_name` est identique au `service.name` déclaré dans Logback
- [ ] `log_correlation: true` est activé
- [ ] `server_url` pointe vers le bon APM Server de l'environnement
- [ ] Le filtre `user.id` est implémenté si le service authentifie des utilisateurs

→ Guide détaillé : [Configurer l'agent APM](./03-configurer-apm)

---

## 3. Labels métier

- [ ] Les parcours métier couverts par le service sont identifiés
- [ ] Les valeurs de `business_use_case`, `business_criticality` et `business_domain`
      sont définies et cohérentes avec les autres services du domaine
- [ ] Les labels sont posés sur les transactions APM concernées
- [ ] Les labels sont propagés dans les logs via MDC

→ Guide détaillé : [Ajouter les labels métier](./04-ajouter-labels-metier)

---

## 4. Vérification dans Kibana

- [ ] Le service apparaît dans **Kibana › APM › Services**
- [ ] Les transactions sont visibles et correctement typées (`request`, `messaging`…)
- [ ] Les logs apparaissent dans **Kibana › Discover** avec les champs ECS attendus
- [ ] La corrélation logs ↔ traces fonctionne (lien "View logs" depuis APM)
- [ ] Les labels métier sont visibles dans les transactions et les logs

→ Guide détaillé : [Vérifier l'instrumentation dans Kibana](./05-verifier-instrumentation)

---

## 5. Dashboards et alertes

- [ ] Les dashboards socles existants couvrent-ils le besoin ? (vérifier le catalogue)
- [ ] Si un dashboard spécifique est nécessaire, le template niveau 3 est utilisé
- [ ] Le dashboard est nommé selon la convention plateforme
- [ ] Le dashboard est documenté dans le catalogue des assets

→ Voir : [Catalogue des assets](../06-catalogue/index)

:::tip
En cas de doute sur l'une des étapes, contacter l'équipe plateforme avant la mise en
production plutôt qu'après. Voir [Gouvernance › Faire une demande](../07-gouvernance/03-demandes).
:::
