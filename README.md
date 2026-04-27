# Central Defender Pass Analysis

## Présentation du projet

Ce projet est le premier projet d’un portfolio personnel dédié à l’analyse de données appliquée au football.

L’objectif est d’analyser les passes de défenseurs centraux à partir de données événementielles StatsBomb Open Data, puis de générer automatiquement plusieurs livrables analytiques :

1. une **pass density heatmap** pour visualiser les zones depuis lesquelles un joueur initie ses passes ;
2. une **pass map** avec flèches pour visualiser la direction, la longueur et la réussite des passes ;
3. un fichier de **métriques individuelles** par joueur ;
4. un fichier de **comparaison globale** entre défenseurs centraux ;
5. des graphiques comparatifs pour interpréter les profils de relance.

Le projet a d’abord été construit dans des notebooks d’exploration, puis transformé en pipeline automatisé avec des scripts Python et des fichiers de configuration JSON.

---

## Objectif principal

L’objectif principal est de répondre à la question suivante :

> Comment un défenseur central participe-t-il à la construction du jeu à travers ses passes ?

Le projet cherche à analyser :

- les zones de départ des passes ;
- le volume de passes ;
- le taux de réussite ;
- la direction des passes ;
- les passes vers l’avant ;
- les passes longues ;
- la longueur moyenne des passes ;
- les différences de profil entre défenseurs centraux.

---

## Objectif long terme

À terme, l’objectif est d’appliquer cette méthode à plusieurs défenseurs centraux, sur différents matchs ou compétitions, afin de comparer leurs profils de relance.

Le cas d’usage cible initial est l’analyse des défenseurs centraux de Manchester United lors de la saison 2025/2026 de Premier League, sous réserve de disponibilité d’une source de données événementielles compatible.

Cette première version utilise StatsBomb Open Data afin de construire une méthode reproductible, documentée et exploitable dans un portfolio.

---

## Cas analysé dans cette version

Cette version porte sur la finale de l’Euro 2024 entre l’Espagne et l’Angleterre.

| Élément | Valeur |
|---|---|
| Source | StatsBomb Open Data |
| Competition ID | 55 |
| Season ID | 282 |
| Match ID | 3943043 |
| Match | Spain 2 - 1 England |
| Date | 2024-07-14 |
| Événement analysé | Passes |
| Population analysée | Défenseurs centraux ayant participé au match |
| Visualisations générées | Pass density heatmap, pass map, graphiques comparatifs |

---

## Joueurs analysés

Les défenseurs centraux récupérés à partir des lineups StatsBomb sont :

| Joueur | Équipe | Poste |
|---|---|---|
| John Stones | England | Right Center Back |
| Marc Guéhi | England | Left Center Back |
| Aymeric Laporte | Spain | Left Center Back |
| José Ignacio Fernández Iglesias | Spain | Right Center Back |
| Robin Aime Robert Le Normand | Spain | Right Center Back |

Pour la comparaison principale, un filtre de volume minimum est appliqué afin d’éviter les échantillons trop faibles.

Dans cette version, seuls les joueurs ayant effectué au moins 20 passes sont conservés dans la comparaison principale.

---

## Visualisations générées

### Pass density heatmap

La pass density heatmap représente les zones du terrain depuis lesquelles le joueur effectue le plus souvent ses passes.

Elle utilise les coordonnées de départ des passes :

```text
x, y = point de départ de la passe
```

Les fichiers sont générés dans :

```text
outputs/heatmaps/
```

Exemple :

```text
outputs/heatmaps/robin_aime_robert_le_normand_pass_density_heatmap.png
```

---

### Pass map

La pass map représente chaque passe individuellement avec une flèche.

- Les passes réussies sont affichées en vert.
- Les passes ratées sont affichées en rouge.
- Chaque flèche va du point de départ au point d’arrivée de la passe.

Les fichiers sont générés dans :

```text
outputs/passmaps/
```

Exemple :

```text
outputs/passmaps/robin_aime_robert_le_normand_pass_map.png
```

---

### Graphiques comparatifs

Les graphiques comparatifs sont générés à partir du fichier global de métriques.

Ils permettent de comparer les défenseurs centraux selon plusieurs dimensions :

- volume total de passes ;
- taux de réussite ;
- part des passes vers l’avant ;
- part des passes longues ;
- longueur moyenne des passes.

Les fichiers sont générés dans :

```text
outputs/comparison_charts/
```

Exemples :

```text
outputs/comparison_charts/total_passes_comparison.png
outputs/comparison_charts/completion_rate_comparison.png
outputs/comparison_charts/forward_pass_share_comparison.png
outputs/comparison_charts/long_pass_share_comparison.png
outputs/comparison_charts/average_pass_length_comparison.png
```

---

## Métriques calculées

Le projet calcule automatiquement les métriques suivantes pour chaque joueur :

| Métrique | Description |
|---|---|
| `total_passes` | Nombre total de passes tentées |
| `completed_passes` | Nombre de passes réussies |
| `incomplete_passes` | Nombre de passes non réussies |
| `completion_rate` | Taux de réussite des passes |
| `forward_passes` | Nombre de passes vers l’avant |
| `forward_pass_share` | Part des passes vers l’avant |
| `long_passes` | Nombre de passes longues |
| `long_pass_share` | Part des passes longues |
| `average_pass_length` | Longueur moyenne des passes |

Les métriques individuelles sont exportées dans :

```text
outputs/metrics/
```

Exemple :

```text
outputs/metrics/robin_aime_robert_le_normand_metrics.csv
```

Le fichier de comparaison global est exporté dans :

```text
outputs/metrics/euro_2024_final_centre_backs_comparison.csv
```

Une version filtrée est également produite pour la comparaison principale :

```text
outputs/metrics/euro_2024_final_centre_backs_comparison_filtered.csv
```

---

## Résultats de comparaison

Après filtrage des joueurs ayant effectué au moins 20 passes, la comparaison principale porte sur :

| Joueur | Équipe | Total passes | Completed passes | Completion rate | Forward pass share | Long pass share | Average pass length |
|---|---|---:|---:|---:|---:|---:|---:|
| Robin Aime Robert Le Normand | Spain | 84 | 80 | 95.2% | 77.4% | 13.1% | 21.9 |
| Aymeric Laporte | Spain | 83 | 80 | 96.4% | 60.2% | 22.9% | 22.3 |
| John Stones | England | 35 | 30 | 85.7% | 65.7% | 31.4% | 27.7 |
| Marc Guéhi | England | 26 | 23 | 88.5% | 65.4% | 15.4% | 18.9 |

José Ignacio Fernández Iglesias est bien présent dans les données, mais il n’est pas conservé dans la comparaison principale car son volume de passes est trop faible.

---

## Première lecture analytique

Robin Aime Robert Le Normand et Aymeric Laporte sont les deux défenseurs centraux les plus impliqués dans la circulation du ballon lors de ce match, avec respectivement 84 et 83 passes.

Robin Le Normand présente le volume de passes le plus élevé et la plus forte part de passes vers l’avant parmi les joueurs conservés dans la comparaison. Cela suggère une forte implication dans la progression du jeu espagnol.

Aymeric Laporte affiche le meilleur taux de réussite parmi les défenseurs centraux principaux, tout en conservant un volume de passes très élevé. Son profil apparaît donc plus sécurisé, avec une forte fiabilité dans la première relance.

John Stones présente la plus forte part de passes longues et la longueur moyenne de passe la plus élevée. Cela peut indiquer un profil plus direct dans ce match, avec davantage de passes longues ou de changements d’orientation.

Marc Guéhi présente un volume de passes plus faible, ce qui peut refléter une moindre possession anglaise ou un rôle plus limité dans la construction depuis l’arrière.

---

## Stack technique

### Langage

```text
Python
```

### Bibliothèques principales

```text
pandas
numpy
matplotlib
mplsoccer
statsbombpy
jupyterlab
ipykernel
```

### Rôle des bibliothèques

| Bibliothèque | Rôle |
|---|---|
| pandas | Chargement, filtrage et transformation des données |
| numpy | Calculs numériques et gestion des coordonnées |
| matplotlib | Création et personnalisation des visualisations |
| mplsoccer | Dessin du terrain et visualisations football |
| statsbombpy | Chargement des données StatsBomb Open Data |
| jupyterlab | Exploration et prototypage dans les notebooks |

---

## Structure du dépôt

```text
central-defender-pass-heatmap/
│
├── configs/
│   ├── robin_le_normand.json
│   │
│   └── generated/
│       └── euro_2024_final/
│           ├── england_john_stones.json
│           ├── england_marc_guehi.json
│           ├── spain_aymeric_laporte.json
│           ├── spain_jose_ignacio_fernandez_iglesias.json
│           └── spain_robin_aime_robert_le_normand.json
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_pass_density_heatmap.ipynb
│   ├── 03_pass_map.ipynb
│   └── 04_centre_back_comparison.ipynb
│
├── outputs/
│   ├── heatmaps/
│   ├── passmaps/
│   ├── metrics/
│   └── comparison_charts/
│
├── scripts/
│   ├── generate_player_pass_analysis.py
│   ├── generate_configs_from_lineups.py
│   ├── run_all_configs.py
│   └── build_metrics_comparison.py
│
├── src/
│   ├── __init__.py
│   ├── data_preparation.py
│   ├── utils.py
│   └── visualizations.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Description des dossiers

### `configs/`

Ce dossier contient les fichiers de configuration JSON utilisés pour automatiser les analyses.

Chaque fichier définit :

- la compétition ;
- la saison ;
- le match ;
- le joueur ;
- les visualisations à générer.

Exemple :

```json
{
  "competition_id": 55,
  "season_id": 282,
  "match_id": 3943043,
  "player_name": "Robin Aime Robert Le Normand",
  "data_source": "StatsBomb Open Data",
  "event_type": "Pass",
  "analysis_type": "Pass density heatmap and pass map",
  "generate_heatmap": true,
  "generate_passmap": true
}
```

---

### `notebooks/`

Ce dossier contient les notebooks d’exploration et d’analyse.

| Notebook | Rôle |
|---|---|
| `01_data_exploration.ipynb` | Exploration initiale et préparation des données |
| `02_pass_density_heatmap.ipynb` | Prototypage de la heatmap de densité |
| `03_pass_map.ipynb` | Prototypage de la pass map avec flèches |
| `04_centre_back_comparison.ipynb` | Comparaison des défenseurs centraux |

---

### `src/`

Ce dossier contient le code Python réutilisable du projet.

#### `data_preparation.py`

Contient les fonctions de chargement, nettoyage et transformation des données :

- chargement du contexte de match ;
- chargement des événements StatsBomb ;
- filtrage des passes ;
- extraction des coordonnées ;
- création des features ;
- calcul des métriques ;
- création du DataFrame de métriques.

#### `visualizations.py`

Contient les fonctions de visualisation :

- `plot_pass_density_heatmap()`
- `plot_pass_map()`

#### `utils.py`

Contient les fonctions utilitaires :

- chargement des fichiers JSON ;
- création de slugs pour les noms de fichiers ;
- création automatique des dossiers de sortie.

---

### `scripts/`

Ce dossier contient les scripts d’automatisation.

#### `generate_player_pass_analysis.py`

Génère automatiquement les visualisations et les métriques pour un joueur à partir d’un fichier JSON.

Commande :

```bash
python scripts/generate_player_pass_analysis.py --config configs/robin_le_normand.json
```

#### `generate_configs_from_lineups.py`

Génère automatiquement les fichiers JSON des joueurs à partir des lineups StatsBomb.

Commande pour générer les configs des défenseurs centraux de la finale :

```bash
python scripts/generate_configs_from_lineups.py --competition-id 55 --season-id 282 --match-id 3943043 --position-filter "Center Back"
```

#### `run_all_configs.py`

Exécute automatiquement toutes les configurations JSON trouvées dans un dossier.

Commande :

```bash
python scripts/run_all_configs.py
```

Commande pour exécuter uniquement les configs générées pour la finale :

```bash
python scripts/run_all_configs.py --config-dir configs/generated/euro_2024_final
```

#### `build_metrics_comparison.py`

Agrège les fichiers de métriques individuels dans un fichier global de comparaison.

Commande :

```bash
python scripts/build_metrics_comparison.py
```

---

## Installation du projet

### 1. Cloner le dépôt

```bash
git clone https://github.com/TON-UTILISATEUR/central-defender-pass-heatmap.git
cd central-defender-pass-heatmap
```

### 2. Créer un environnement virtuel

```bash
python -m venv .venv
```

### 3. Activer l’environnement virtuel

Sur Windows :

```bash
.venv\Scripts\activate
```

Sur macOS ou Linux :

```bash
source .venv/bin/activate
```

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## Utilisation du projet

### Générer l’analyse pour un joueur

```bash
python scripts/generate_player_pass_analysis.py --config configs/robin_le_normand.json
```

---

### Générer les fichiers de configuration depuis les lineups

```bash
python scripts/generate_configs_from_lineups.py --competition-id 55 --season-id 282 --match-id 3943043 --position-filter "Center Back"
```

---

### Générer les analyses pour tous les joueurs configurés

```bash
python scripts/run_all_configs.py --config-dir configs/generated/euro_2024_final
```

---

### Construire le fichier global de comparaison

```bash
python scripts/build_metrics_comparison.py
```

---

## Pipeline complet

Le pipeline complet se lance dans cet ordre :

```bash
python scripts/generate_configs_from_lineups.py --competition-id 55 --season-id 282 --match-id 3943043 --position-filter "Center Back"

python scripts/run_all_configs.py --config-dir configs/generated/euro_2024_final

python scripts/build_metrics_comparison.py
```

Ensuite, le notebook suivant permet d’explorer et d’interpréter les résultats :

```text
notebooks/04_centre_back_comparison.ipynb
```

---

## Méthodologie

### 1. Chargement des données

Les données sont chargées avec `statsbombpy` à partir des identifiants :

```text
competition_id
season_id
match_id
```

### 2. Récupération des joueurs

Les joueurs sont récupérés via les lineups du match :

```python
sb.lineups(match_id=match_id)
```

### 3. Filtrage des défenseurs centraux

Les joueurs sont filtrés sur la position :

```text
Center Back
```

### 4. Filtrage des passes

Les événements sont filtrés pour conserver uniquement :

```python
events[events["type"] == "Pass"]
```

### 5. Sélection du joueur

Les passes sont ensuite filtrées sur le nom exact du joueur :

```python
passes[passes["player"] == player_name]
```

### 6. Préparation des coordonnées

Les coordonnées StatsBomb sont transformées en colonnes exploitables :

```text
location           -> x, y
pass_end_location  -> end_x, end_y
```

### 7. Création des features

Le projet ajoute plusieurs variables :

```text
is_completed
x_progression
y_progression
is_forward_pass
is_long_pass
```

### 8. Calcul des métriques

Les métriques principales sont calculées à partir du DataFrame préparé.

### 9. Génération des visualisations

Deux visualisations sont générées automatiquement :

- pass density heatmap ;
- pass map.

### 10. Comparaison entre joueurs

Les métriques individuelles sont agrégées dans un fichier global, puis utilisées pour comparer les défenseurs centraux.

---

## Limites actuelles

Cette version du projet présente plusieurs limites :

- l’analyse porte sur un seul match ;
- les conclusions ne doivent pas être généralisées à toute une saison ;
- les passes longues sont définies avec un seuil simple de `pass_length >= 30` ;
- les passes vers l’avant sont approximées avec `end_x > x` ;
- le contexte tactique global du match n’est pas encore intégré ;
- le volume de passes varie fortement selon le temps de jeu et le scénario du match ;
- la comparaison principale exclut les joueurs avec un volume de passes trop faible.

---

## Prochaines évolutions prévues

Les prochaines évolutions possibles sont :

1. ajouter un vrai calcul de passes progressives ;
2. intégrer le temps de jeu pour normaliser les métriques ;
3. comparer les métriques par 90 minutes ;
4. automatiser la génération d’un rapport Markdown ;
5. améliorer les graphiques comparatifs ;
6. ajouter une analyse par zones du terrain ;
7. appliquer le pipeline à plusieurs matchs ;
8. appliquer le pipeline à une compétition entière ;
9. adapter le projet à une future source de données Manchester United.

---

## Statut du projet

```text
Statut : pipeline automatisé fonctionnel
Source : StatsBomb Open Data
Match analysé : Finale Euro 2024, Espagne 2 - 1 Angleterre
Population : défenseurs centraux
Visualisations : heatmap, pass map, graphiques comparatifs
Automatisation : fichiers JSON + scripts Python
Comparaison : fichier global de métriques + notebook dédié
```

---

## Commandes utiles

### Lancer Jupyter Lab

```bash
jupyter lab
```

### Lancer l’analyse d’un joueur

```bash
python scripts/generate_player_pass_analysis.py --config configs/robin_le_normand.json
```

### Générer les configs depuis les lineups

```bash
python scripts/generate_configs_from_lineups.py --competition-id 55 --season-id 282 --match-id 3943043 --position-filter "Center Back"
```

### Lancer toutes les analyses

```bash
python scripts/run_all_configs.py --config-dir configs/generated/euro_2024_final
```

### Créer le fichier de comparaison

```bash
python scripts/build_metrics_comparison.py
```

### Vérifier l’état Git

```bash
git status
```

### Ajouter les changements

```bash
git add -A
```

### Créer un commit

```bash
git commit -m "Update README with centre-back comparison workflow"
```

### Envoyer sur GitHub

```bash
git push
```