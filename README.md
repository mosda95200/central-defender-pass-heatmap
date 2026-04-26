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

## Résultat final

| field | value |
| --- | --- |
| Data source | StatsBomb Open Data |
| Competition | UEFA Euro |
| Country | Europe |
| Season | 2024 |
| Match | Spain 2 - 1 England |
| Match date | 2024-07-14 |
| Competition stage | Final |
| Team | Spain |
| Player | Robin Aime Robert Le Normand |
| Position | Right Center Back |
| Event type | Pass |
| Analysis type | Pass start location heatmap |
| Output file | ../outputs/robin_aime_robert_le_normand_pass_heatmap.png |


## Cas analysé

| metric | value |
| --- | --- |
| Player | Robin Aime Robert Le Normand |
| Team | Spain |
| Match | Spain 2 - 1 England |
| Match date | 2024-07-14 |
| Total passes | 84 |
| Completed passes | 80 |
| Completion rate | 95.2% |
| Forward passes | 65 |
| Forward pass share | 77.4% |
| Long passes | 11 |
| Long pass share | 13.1% |
| Average pass length | 21.9 |

## Analyse

La heatmap montre que le joueur concentre principalement ses passes dans une zone basse et axiale du terrain. Cette distribution suggère un rôle important dans la première phase de construction, avec une implication régulière dans la relance depuis la ligne défensive.

Le taux de réussite élevé indique un profil relativement sécurisant à la passe. La part de passes vers l’avant permet cependant d’évaluer si cette sécurité s’accompagne d’une volonté de progression ou si le joueur privilégie principalement la conservation.

## Livrables

Le projet contient actuellement :

- un notebook d’exploration : `notebooks/01_data_exploration.ipynb` ;
- un module Python réutilisable : `src/pass_heatmap.py` ;
- une heatmap exportée : `outputs/robin_aime_robert_le_normand_pass_heatmap.png` ;
- un README documentant le projet, la méthode et les résultats.

## Reproduire le projet

### 1. Cloner le dépôt

```bash
git clone https://github.com/mosda95200/central-defender-pass-heatmap.git
cd central-defender-pass-heatmap