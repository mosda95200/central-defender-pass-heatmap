# Central Defender Pass Analysis

## Présentation du projet

Ce projet est le premier projet d’un portfolio personnel dédié à l’analyse de données appliquée au football.

L’objectif est d’analyser les passes d’un défenseur central à partir de données événementielles StatsBomb Open Data, puis de produire automatiquement deux visualisations :

1. une **pass density heatmap** pour identifier les zones depuis lesquelles le joueur initie ses passes ;
2. une **pass map** avec flèches pour visualiser la direction, la longueur et la réussite des passes.

Le projet a été construit progressivement à partir de notebooks d’exploration, puis transformé en pipeline automatisé grâce à des scripts Python et des fichiers de configuration JSON.

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
- le rôle du joueur dans la première phase de construction.

---

## Objectif long terme

À terme, l’objectif est d’appliquer cette méthode à plusieurs défenseurs centraux afin de comparer leurs profils de relance.

Le cas d’usage cible initial est l’analyse des défenseurs centraux de Manchester United lors de la saison 2025/2026 de Premier League, sous réserve de disponibilité d’une source de données événementielles compatible.

Cette première version utilise StatsBomb Open Data afin de construire une méthode reproductible, documentée et exploitable dans un portfolio.

---

## Cas analysé dans cette version

Le premier cas automatisé porte sur :

| Élément | Valeur |
|---|---|
| Joueur | Robin Aime Robert Le Normand |
| Source | StatsBomb Open Data |
| Competition ID | 52 |
| Season ID | 282 |
| Match ID | 3943043 |
| Événement analysé | Passes |
| Visualisations générées | Pass density heatmap, pass map |

Les informations détaillées du match, de la compétition, de l’équipe et du score sont récupérées automatiquement depuis StatsBomb Open Data au moment de l’exécution du script.

---

## Visualisations générées

### Pass density heatmap

La pass density heatmap représente les zones du terrain depuis lesquelles le joueur effectue le plus souvent ses passes.

Cette visualisation utilise les coordonnées de départ des passes.

```text
x, y = point de départ de la passe
```

Fichier généré :

```text
outputs/heatmaps/robin_aime_robert_le_normand_pass_density_heatmap.png
```

### Pass map

La pass map représente chaque passe individuellement avec une flèche.

- Les passes réussies sont affichées en vert.
- Les passes ratées sont affichées en rouge.
- Chaque flèche va du point de départ au point d’arrivée de la passe.

Fichier généré :

```text
outputs/passmaps/robin_aime_robert_le_normand_pass_map.png
```

---

## Métriques calculées

Le projet calcule automatiquement plusieurs métriques de passes :

| Métrique | Description |
|---|---|
| Total passes | Nombre total de passes tentées |
| Completed passes | Nombre de passes réussies |
| Incomplete passes | Nombre de passes non réussies |
| Completion rate | Taux de réussite des passes |
| Forward passes | Nombre de passes vers l’avant |
| Forward pass share | Part des passes vers l’avant |
| Long passes | Nombre de passes longues |
| Long pass share | Part des passes longues |
| Average pass length | Longueur moyenne des passes |

Ces métriques sont affichées dans le terminal lors de l’exécution du script.

---

## Stack technique

Le projet utilise Python et plusieurs bibliothèques spécialisées dans l’analyse de données et la visualisation football.

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
│   └── robin_le_normand.json
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_pass_density_heatmap.ipynb
│   └── 03_pass_map.ipynb
│
├── outputs/
│   ├── heatmaps/
│   │   └── robin_aime_robert_le_normand_pass_density_heatmap.png
│   │
│   └── passmaps/
│       └── robin_aime_robert_le_normand_pass_map.png
│
├── scripts/
│   ├── generate_player_pass_analysis.py
│   └── run_all_configs.py
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

Chaque fichier de configuration définit :

- la compétition ;
- la saison ;
- le match ;
- le joueur ;
- les visualisations à générer.

Exemple :

```json
{
  "competition_id": 52,
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

Ce dossier contient les notebooks d’exploration.

| Notebook | Rôle |
|---|---|
| `01_data_exploration.ipynb` | Exploration initiale et préparation des données |
| `02_pass_density_heatmap.ipynb` | Prototypage de la heatmap de densité |
| `03_pass_map.ipynb` | Prototypage de la pass map avec flèches |

Les notebooks servent à comprendre, tester et valider les étapes avant de les intégrer dans le pipeline automatisé.

---

### `src/`

Ce dossier contient le code Python réutilisable du projet.

#### `data_preparation.py`

Contient les fonctions de chargement et de préparation des données :

- chargement du contexte de match ;
- chargement des événements StatsBomb ;
- filtrage des passes ;
- extraction des coordonnées ;
- création des features ;
- calcul des métriques.

#### `visualizations.py`

Contient les fonctions de visualisation :

- `plot_pass_density_heatmap()`
- `plot_pass_map()`

Ces fonctions génèrent les deux visualisations principales du projet.

#### `utils.py`

Contient les fonctions utilitaires :

- chargement des fichiers JSON ;
- création de slugs pour les noms de fichiers ;
- création automatique des dossiers de sortie.

---

### `scripts/`

Ce dossier contient les scripts d’exécution automatique.

#### `generate_player_pass_analysis.py`

Script principal permettant de générer automatiquement les visualisations pour un joueur à partir d’un fichier de configuration JSON.

Exemple d’exécution :

```bash
python scripts/generate_player_pass_analysis.py --config configs/robin_le_normand.json
```

#### `run_all_configs.py`

Script permettant d’exécuter automatiquement toutes les configurations présentes dans le dossier `configs/`.

Exemple d’exécution :

```bash
python scripts/run_all_configs.py
```

---

### `outputs/`

Ce dossier contient les fichiers générés automatiquement.

```text
outputs/heatmaps/
outputs/passmaps/
```

Les heatmaps sont générées dans :

```text
outputs/heatmaps/
```

Les pass maps sont générées dans :

```text
outputs/passmaps/
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

## Utilisation

### Générer les visualisations pour Robin Le Normand

Depuis la racine du projet :

```bash
python scripts/generate_player_pass_analysis.py --config configs/robin_le_normand.json
```

Le script effectue automatiquement les étapes suivantes :

1. chargement du fichier de configuration ;
2. chargement du contexte de compétition et de match ;
3. chargement des événements StatsBomb ;
4. filtrage des passes du joueur ;
5. préparation des coordonnées ;
6. calcul des métriques ;
7. génération de la pass density heatmap ;
8. génération de la pass map ;
9. export des images dans le dossier `outputs/`.

---

## Exemple de sortie terminal

```text
Loading analysis context...
Preparing player passes...
Analysis summary
----------------
Player: Robin Aime Robert Le Normand
Team: ...
Position: ...
Competition: ...
Season: ...
Match: ...
Date: ...
Total passes: ...
Completed passes: ...
Completion rate: ...
Generating pass density heatmap...
Heatmap saved to: outputs/heatmaps/robin_aime_robert_le_normand_pass_density_heatmap.png
Generating pass map...
Pass map saved to: outputs/passmaps/robin_aime_robert_le_normand_pass_map.png
Done.
```

Les valeurs exactes sont récupérées automatiquement depuis StatsBomb Open Data.

---

## Méthodologie

Le pipeline suit les étapes suivantes.

### 1. Chargement des données

Les données sont chargées avec `statsbombpy` à partir des identifiants suivants :

```text
competition_id
season_id
match_id
```

### 2. Filtrage des passes

Les événements sont filtrés pour ne conserver que les passes :

```python
events[events["type"] == "Pass"]
```

### 3. Sélection du joueur

Les passes sont ensuite filtrées sur le nom exact du joueur :

```python
passes[passes["player"] == player_name]
```

### 4. Préparation des coordonnées

Les coordonnées StatsBomb sont transformées en colonnes exploitables :

```text
location           -> x, y
pass_end_location  -> end_x, end_y
```

### 5. Création des features

Le projet ajoute plusieurs variables utiles :

```text
is_completed
x_progression
y_progression
is_forward_pass
is_long_pass
```

### 6. Calcul des métriques

Les métriques principales sont calculées à partir du DataFrame préparé.

### 7. Génération des visualisations

Deux visualisations sont générées :

- une heatmap de densité des points de départ des passes ;
- une pass map avec flèches.

---

## Limites actuelles

Cette version du projet présente plusieurs limites :

- l’analyse porte sur un seul joueur ;
- l’analyse porte sur un seul match ;
- les visualisations ne prennent pas encore en compte le contexte tactique complet ;
- les passes progressives sont approximées à partir de la progression en `x` ;
- les passes longues sont définies avec un seuil simple de `pass_length >= 30` ;
- les métriques ne sont pas encore exportées dans un fichier CSV.

---

## Prochaines évolutions prévues

Les prochaines évolutions logiques du projet sont :

1. exporter automatiquement les métriques dans un fichier CSV ;
2. automatiser l’analyse de plusieurs joueurs ;
3. comparer plusieurs défenseurs centraux ;
4. ajouter un notebook de comparaison ;
5. enrichir les métriques avec les passes progressives ;
6. améliorer la documentation analytique dans le README ;
7. préparer une version portfolio publiable.

---

## Statut du projet

```text
Statut : version automatisée fonctionnelle
Visualisations : heatmap + pass map
Source : StatsBomb Open Data
Automatisation : configuration JSON + script Python
Cas validé : Robin Aime Robert Le Normand
```

---

## Commandes utiles

### Lancer l’analyse principale

```bash
python scripts/generate_player_pass_analysis.py --config configs/robin_le_normand.json
```

### Lancer toutes les configurations

```bash
python scripts/run_all_configs.py
```

### Vérifier l’état Git

```bash
git status
```

### Ajouter tous les changements

```bash
git add -A
```

### Créer un commit

```bash
git commit -m "Update README with automated pass analysis workflow"
```

### Envoyer sur GitHub

```bash
git push
```