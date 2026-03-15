---
id: pourquoi-observabilite
title: Pourquoi l'observabilité ?
sidebar_label: Pourquoi l'observabilité ?
sidebar_position: 1
---

# Pourquoi l'observabilité ?

:::info Note de l'auteur
Ce cadre de référence n'est pas né d'une décision de comité. Il est le résultat
d'années passées à investiguer des incidents en production, à chercher des informations
qui n'existaient pas, à reconstruire des timelines à partir de logs illisibles.

Il est porté par une conviction forgée sur le terrain : l'observabilité n'est pas
une option, ni une bonne pratique parmi d'autres. C'est ce qui fait la différence
entre une équipe qui subit sa production et une équipe qui la maîtrise.
:::

## Le vrai coût d'un incident mal instrumenté

Un incident en production a toujours un coût. Ce coût dépend de deux facteurs :
sa durée et son impact métier.

Sur la durée, l'observabilité est le levier le plus direct. Les études sectorielles
sont convergentes : **le temps moyen de détection et de résolution d'un incident est
3 à 5 fois plus long sur des services non instrumentés** que sur des services
correctement observés.

Concrètement, la différence entre 6 minutes et 36 minutes d'investigation tient
souvent à trois choses :

- des logs structurés qui permettent de filtrer immédiatement sur la bonne
  transaction, le bon utilisateur, le bon code d'erreur
- un agent APM qui expose la trace distribuée et identifie la dépendance en cause
- des labels métier qui permettent de qualifier immédiatement l'impact business —
  quel parcours, quelle criticité

Sans ces trois éléments, l'investigation se fait à l'aveugle. Avec eux, elle devient
méthodique et rapide — et accessible à n'importe quel membre de l'équipe, pas
seulement à celui qui connaît le service par cœur.

## Pourquoi c'est particulièrement critique sur notre plateforme

Nos services ne fonctionnent pas en silo. Ils s'appellent mutuellement, dépendent
d'APIs externes, partagent des ressources communes, et tournent sur une infrastructure
Kubernetes partagée.

Dans ce contexte, un problème n'a presque jamais une cause unique et évidente.
Il faut pouvoir :

- corréler un symptôme utilisateur avec un événement technique précis
- remonter une chaîne d'appels inter-services pour identifier le composant en cause
- distinguer une erreur ponctuelle d'une dégradation progressive
- qualifier l'impact métier d'un incident technique en temps réel

Ces capacités ne s'improvisent pas au moment de l'incident. Elles se construisent
en amont, dès la conception du service.

## Ce que ce cadre de référence couvre

Ce document définit le **cadre d'observabilité de la plateforme**. Il s'adresse à
toutes les équipes qui développent, opèrent ou maintiennent des services :

- Les **développeurs** qui instrumentent leurs services
- Les **tech leads** qui définissent les standards de leur équipe
- Les **ops et SRE** qui maintiennent la plateforme en condition opérationnelle
- Les **product managers** qui veulent suivre la santé de leurs parcours métier

Il répond à trois questions :

> *Qu'est-ce qui est attendu de mon service ?*
>
> *Comment mettre en œuvre ces attentes concrètement ?*
>
> *Comment exploiter ce que la plateforme met à disposition ?*

## Par où commencer ?

Comprendre le cadre global avant de se lancer :
→ [Les trois piliers](./02-trois-piliers) et [Nos principes directeurs](./03-principes-directeurs)

Intégrer un nouveau service et savoir quoi faire concrètement :
→ [Guide d'onboarding](../04-guides/01-onboarding)

Comprendre pourquoi les labels métier sont demandés :
→ [Observabilité by design](./04-observabilite-by-design)

Investiguer un incident en cours :
→ [Recettes du quotidien](../05-prise-en-main/05-recettes)
