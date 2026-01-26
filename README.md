# RetailRocket Analytics — Projet E-commerce

Projet d'analyse e‑commerce contenant : nettoyage et pipeline de données, notebooks d'EDA et un dashboard Streamlit pour visualiser les KPI.

## Contenu du dépôt

- `dashboard/` : application Streamlit (lancer avec `streamlit run dashboard/app.py`).
- `data/` : fichiers bruts (CSV) d'origine.
- `notebooks/` : notebooks Jupyter pour EDA et AB testing.
- `scripts/` : scripts utilitaires (ex. `data_pipeline.py`).
- `outputs/` : données et figures générées (CSV et images).

## Prérequis

- Git
- Python 3.8+ (3.9/3.10 recommandés)
- Outils : `pip`, `virtualenv` ou `venv`

## Récupérer le projet

1. Depuis Git remplacez https://github.com/sitayeb2025/ecommerce-DATA.git par l'URL du dépôt:

```bash
git clone <https://github.com/sitayeb2025/ecommerce-DATA.git>
cd data-ecommerce
# (optionnel) pour récupérer la branche 'dev' :
git checkout dev
```

2. Si le dépôt est hébergé sur GitHub/GitLab vous pouvez aussi télécharger le ZIP via l'interface web.
python scripts/data_pipeline.py
## Installer les dépendances




```bash
pip install streamlit pandas numpy plotly
```


- Lancer le pipeline de préparation des données :

```bash
python scripts/data_pipeline.py
```

- Lancer le dashboard Streamlit :

```bash
streamlit run dashboard/app.py
```

- Ouvrir les notebooks :

```bash
jupyter lab  # ou jupyter notebook
```

## Mettre à jour / pousser des modifications

- Vérifier l'état : `git status`
- Ajouter des fichiers : `git add <path>`
- Commit : `git commit -m "Message de commit"`
- Pousser : `git push origin dev` (ou `git push --set-upstream origin main` si nécessaire)

## Structure rapide

- `dashboard/app.py` : application Streamlit principale.
- `scripts/data_pipeline.py` : ETL / nettoyage des fichiers d'entrée.
- `outputs/data/` : sorties CSV (ex. `events_clean.csv`, `kpi_business_summary.csv`).

# data-ecommerce
# ecommerce-DATA
# ecommerce-DATA
# ecommerce-DATA
