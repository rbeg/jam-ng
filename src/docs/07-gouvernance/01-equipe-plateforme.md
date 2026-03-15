---
id: equipe-plateforme
title: Équipe plateforme
sidebar_label: Équipe plateforme
sidebar_position: 1
---

# Équipe plateforme — Périmètre et responsabilités

## Ce que l'équipe plateforme maintient

L'équipe plateforme est responsable du cadre d'observabilité commun. Concrètement,
cela couvre :

**Infrastructure et pipelines**
- Pipeline de collecte des logs Kubernetes (Logging Flows)
- APM Server et sa disponibilité
- Index Elasticsearch et leur cycle de vie (ILM)
- Data Views Kibana

**Standards et documentation**
- Ce cadre de référence
- Les standards ECS, APM, labels métier
- Les conventions de nommage

**Assets transverses**
- Dashboards socles (niveau 1)
- Dashboards technologiques (niveau 2)
- Alertes socles

---

## Ce qui est de la responsabilité des équipes produit

L'équipe plateforme n'est pas responsable de :

- L'instrumentation des services applicatifs (ECS, agent APM, labels métier)
- Les dashboards de niveau 3 spécifiques à un domaine
- Les alertes spécifiques à un service
- La qualité du contenu des logs (messages, niveautage)

:::warning
L'équipe plateforme n'est pas un helpdesk. Ce cadre de référence et les guides
associés sont conçus pour permettre aux équipes d'être autonomes. Les demandes
d'aide doivent être accompagnées d'une description précise du problème et des
vérifications déjà effectuées.
:::

---

## Comment contacter l'équipe plateforme

| Canal | Usage |
|---|---|
| Canal Slack `#plateforme-observabilite` | Questions, discussions, retours |
| Ticket Jira — projet `PLAT` | Demandes formelles, incidents plateforme |
| Revue trimestrielle | Présentation des évolutions, recueil des besoins |
