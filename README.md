# Data

Ce dossier documente les données utilisées dans le projet.

## Source principale

La première version du projet utilise StatsBomb Open Data.

Les données seront chargées directement depuis Python avec la bibliothèque `statsbombpy`.

## Données brutes

Les données brutes ne sont pas stockées dans ce dépôt.

Raisons :

- elles sont accessibles publiquement via StatsBomb Open Data ;
- cela évite d’alourdir le dépôt GitHub ;
- cela permet de garder le projet reproductible ;
- cela respecte une bonne pratique de séparation entre code et données.

## Données transformées

Les données transformées pourront être stockées localement dans :

```text
data/processed/