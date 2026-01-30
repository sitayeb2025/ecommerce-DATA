## Objectif du projet ##

Ce projet vise à analyser et améliorer un site e-commerce en se basant sur les données utilisateurs.
Les objectifs principaux sont :

   -Comprendre le comportement des visiteurs : identifier comment les utilisateurs naviguent et interagissent avec le site.
   -Repérer les points de friction : trouver les étapes où les visiteurs abandonnent ou hésitent.
   -Optimiser la conversion : tester des changements (A/B tests) pour augmenter les ventes et réduire l’abandon panier.
   -Fournir des insights clairs : créer un dashboard interactif pour visualiser les résultats et soutenir la prise de décision.



##  Source des données
- Provenance : [Kaggle](https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset )  
- Les données sont simulées pour les A/B tests dans le projet.




##  Lancer le projet – étape par étape

Récupérer le projet

1️ **Cloner le dépôt GitHub**
```bash
 git clone https://github.com/sitayeb2025/ecommerce-DATA.git

 cd ecommerce-DATA

2️ **Créer un environnement virtuel(recommandé)**

 python -m venv .venv

**Activer l’environnement **

 Windows : .venv\Scripts\activate

 Mac/Linux : source .venv/bin/activate

3️ Installer les dépendances

 pip install -r requirements.txt

4️ Préparer les données

Télécharger le fichier zip depuis " https://www.kaggle.com/datasets/retailrocket/  ecommerce-dataset"
 
 créer le dossier 'data' dans la racine de projet

 prendre les fichiers extraites et les mettres dans 'data'

 preparation des donnèes pour le dashboard
 python scripts/data_pipeline.py

5️ Lancer le dashboard Streamlit

 cd dashboard
 streamlit run app.py

 '''Une fois la commande exécutée, le dashboard s’ouvre automatiquement dans votre navigateur.'''



Architecture du projet

DATA-ECOMMERCE-1/
│
├── .venv/                  # Environnement virtuel Python
│
├── dashboard/              # Application Streamlit
│   ├── app.py               # Point d’entrée principal du dashboard
│   └── pages/               # Pages secondaires (Analyse, A/B Testing, etc.)
│
├── data/                    # Données du projet
│   ├── clean/               # Données nettoyées et préparées
│   └──  /                   # Données brutes (Kaggle)
│             
│
├── notebooks/               # Notebooks d’analyse exploratoire (EDA)
│
├── scripts/                 # Scripts Python
│   └── data_pipeline.py     # Nettoyage, transformation et feature engineering
│
├── .gitignore               # Fichiers ignorés par Git
│
├── La decumentation PDF     # La decumentation de projetcd
│
├── README.md                # Documentation du projet
│
└── Requirements.txt     #Dépendances Python du projet.
