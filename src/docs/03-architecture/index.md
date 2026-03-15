---
id: architecture
title: Architecture de la plateforme
sidebar_label: Vue d'ensemble
sidebar_position: 3
---

# Architecture de la plateforme

Cette section décrit comment les données d'observabilité circulent sur la plateforme :
depuis les applications et l'infrastructure jusqu'à leur restitution dans Kibana.

Comprendre cette architecture permet de savoir **où chercher une information**, pourquoi
certaines données apparaissent dans un index et pas dans un autre, et comment les
différents pipelines coexistent sans interférer.

## Dans cette section

- [Pipeline des logs applicatifs](./01-pipeline-logs)
- [Pipeline APM](./02-pipeline-apm)
- [Pipeline des indicateurs métier](./03-pipeline-metier)
- [Index et Data Views](./04-index-et-data-views)
- [Corrélation entre les données](./05-correlation)
