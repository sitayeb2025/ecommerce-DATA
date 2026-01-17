# Dashboard E-commerce RetailRocket

Application Streamlit professionnelle pour l'analyse des donnees e-commerce.

## Structure

```
dashboard/
├── app.py                      # Application principale
├── pages/
│   ├── 1_Analyse_Temporelle.py # Tendances et patterns temporels
│   ├── 2_Analyse_Produits.py   # Performance produits
│   └── 3_AB_Testing.py         # Simulateur A/B test
└── README.md
```

## Installation

```bash
pip install streamlit pandas numpy plotly scipy
```

## Lancement

Depuis la racine du projet:

```bash
cd dashboard
streamlit run app.py
```

Ou directement:

```bash
streamlit run dashboard/app.py
```

## Fonctionnalites

### Page Principale

- KPIs temps reel (visiteurs, conversion, abandon)
- Entonnoir de conversion interactif
- Segmentation visiteurs (pie chart)
- Pareto des produits
- Export CSV

### Analyse Temporelle

- Tendances journalieres
- Heatmap heures x jours
- Evolution du taux de conversion

### Analyse Produits

- Scatter plot performance
- Top convertisseurs
- Recherche produit

### A/B Testing

- Simulateur interactif
- Calcul significativite
- Recommandations automatiques

## Prerequis

Les fichiers suivants doivent exister dans `outputs/data/`:

- `visitor_features.csv`
- `product_features.csv`
- `events_clean.csv` (optionnel pour analyse temporelle)
- `ab_test_results.csv` (optionnel)

Executez d'abord le pipeline de donnees:

```bash
python scripts/data_pipeline.py
```

## Configuration

Le dashboard utilise le cache Streamlit pour optimiser les performances.
Les donnees sont rechargees toutes les heures (TTL = 3600s).
# ecommerce-DATA
