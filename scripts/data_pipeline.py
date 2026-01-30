"""
Data Engineering Pipeline - RetailRocket E-commerce
Nettoyage et preparation des donnees
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
import os

warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)

# Configuration
RAW_DATA_PATH = 'data/'
CLEAN_DATA_PATH = 'data/clean/'
os.makedirs(CLEAN_DATA_PATH, exist_ok=True)

print('[OK] Configuration terminee')
print(f'   Donnees brutes : {RAW_DATA_PATH}')
print(f'   Donnees nettoyees : {CLEAN_DATA_PATH}')


# 1. CHARGEMENT

print('\nCHARGEMENT DES DONNEES BRUTES')
print('=' * 50)

events_raw = pd.read_csv(f'{RAW_DATA_PATH}events.csv')
print(f'[OK] events.csv : {len(events_raw):,} lignes')


# 2. NETTOYAGE

print('\nNETTOYAGE')
print('=' * 50)

VALID_EVENTS = ['view', 'addtocart', 'transaction']

# Suppression doublons
before = len(events_raw)
events_clean = events_raw.drop_duplicates()
print(f'[OK] Doublons supprimes : {before - len(events_clean):,}')

# Validation evenements
events_clean = events_clean[events_clean['event'].isin(VALID_EVENTS)]
print(f'[OK] Evenements valides uniquement')

# Suppression NaN critiques
events_clean = events_clean.dropna(subset=['timestamp', 'visitorid', 'itemid'])
print(f'[OK] Lignes sans NaN critiques')

print(f'\nResultat : {len(events_clean):,} lignes (supprime {before - len(events_clean):,})')


# 3. CONVERSION DES TYPES

print('\nCONVERSION DES TYPES')
print('=' * 50)

memory_before = events_clean.memory_usage(deep=True).sum() / 1024**2

# Timestamp -> datetime
events_clean['datetime'] = pd.to_datetime(events_clean['timestamp'], unit='ms')
print(f'[OK] datetime : {events_clean["datetime"].min()} -> {events_clean["datetime"].max()}')

# Optimisation IDs
events_clean['visitorid'] = events_clean['visitorid'].astype('uint32')
events_clean['itemid'] = events_clean['itemid'].astype('uint32')
print('[OK] visitorid, itemid -> uint32')

# Event comme categorie
events_clean['event'] = events_clean['event'].astype('category')
print('[OK] event -> category')

memory_after = events_clean.memory_usage(deep=True).sum() / 1024**2
print(f'\nMemoire : {memory_before:.1f} MB -> {memory_after:.1f} MB (gain {(1-memory_after/memory_before)*100:.0f}%)')

# 4. FEATURE ENGINEERING

print('\nFEATURE ENGINEERING')
print('=' * 50)

# Features temporelles
events_clean['date'] = events_clean['datetime'].dt.date
events_clean['year'] = events_clean['datetime'].dt.year.astype('uint16')
events_clean['month'] = events_clean['datetime'].dt.month.astype('uint8')
events_clean['day'] = events_clean['datetime'].dt.day.astype('uint8')
events_clean['hour'] = events_clean['datetime'].dt.hour.astype('uint8')
events_clean['day_of_week'] = events_clean['datetime'].dt.dayofweek.astype('uint8')
events_clean['is_weekend'] = (events_clean['day_of_week'] >= 5).astype('uint8')

print('[OK] Features temporelles : date, year, month, day, hour, day_of_week, is_weekend')

# Flag conversion
buyers = events_clean[events_clean['event'] == 'transaction']['visitorid'].unique()
events_clean['visitor_converted'] = events_clean['visitorid'].isin(buyers).astype('uint8')
print(f'[OK] visitor_converted : {len(buyers):,} acheteurs identifies')


# 5. FEATURES VISITEURS

print('\nFEATURES VISITEURS')
print('=' * 50)

visitor_features = events_clean.groupby('visitorid').agg(
    total_events=('event', 'count'),
    unique_items=('itemid', 'nunique'),
    first_event=('datetime', 'min'),
    last_event=('datetime', 'max')
).reset_index()

# Comptage par type
event_counts = events_clean.pivot_table(
    index='visitorid', 
    columns='event', 
    aggfunc='size', 
    fill_value=0
).reset_index()
event_counts.columns = ['visitorid', 'n_addtocart', 'n_transaction', 'n_view']

visitor_features = visitor_features.merge(event_counts, on='visitorid')

# Ratios
visitor_features['cart_rate'] = (visitor_features['n_addtocart'] / visitor_features['n_view']).fillna(0)
visitor_features['conversion_rate'] = (visitor_features['n_transaction'] / visitor_features['n_view']).fillna(0)

# Segmentation
def segment_visitor(row):
    if row['n_transaction'] > 0:
        return 'buyer'
    elif row['n_addtocart'] > 0:
        return 'cart_abandoner'
    else:
        return 'browser'

visitor_features['segment'] = visitor_features.apply(segment_visitor, axis=1)

print(f'[OK] {len(visitor_features):,} visiteurs profiles')
print(f'   Segments : {visitor_features["segment"].value_counts().to_dict()}')


# 6. FEATURES PRODUITS.

print('\nFEATURES PRODUITS')
print('=' * 50)

product_features = events_clean.groupby('itemid').agg(
    total_events=('event', 'count'),
    unique_visitors=('visitorid', 'nunique'),
    first_seen=('datetime', 'min'),
    last_seen=('datetime', 'max')
).reset_index()

# Comptage par type
prod_events = events_clean.pivot_table(
    index='itemid', 
    columns='event', 
    aggfunc='size', 
    fill_value=0
).reset_index()
prod_events.columns = ['itemid', 'n_addtocart', 'n_transaction', 'n_view']

product_features = product_features.merge(prod_events, on='itemid')

# Taux conversion
product_features['view_to_cart'] = (product_features['n_addtocart'] / product_features['n_view']).fillna(0)
product_features['cart_to_purchase'] = (product_features['n_transaction'] / product_features['n_addtocart']).replace([np.inf], 0).fillna(0)

print(f'[OK] {len(product_features):,} produits profiles')

# 7. EXPORT

print('\nEXPORT')
print('=' * 50)

# Events
events_export = events_clean.copy()
events_export['datetime'] = events_export['datetime'].astype(str)
events_export['date'] = events_export['date'].astype(str)
events_export.to_csv(f'{CLEAN_DATA_PATH}events_clean.csv', index=False)
print(f'[OK] {CLEAN_DATA_PATH}events_clean.csv')

# Visitors
visitor_export = visitor_features.copy()
visitor_export['first_event'] = visitor_export['first_event'].astype(str)
visitor_export['last_event'] = visitor_export['last_event'].astype(str)
visitor_export.to_csv(f'{CLEAN_DATA_PATH}visitor_features.csv', index=False)
print(f'[OK] {CLEAN_DATA_PATH}visitor_features.csv')

# Products
product_export = product_features.copy()
product_export['first_seen'] = product_export['first_seen'].astype(str)
product_export['last_seen'] = product_export['last_seen'].astype(str)
product_export.to_csv(f'{CLEAN_DATA_PATH}product_features.csv', index=False)
print(f'[OK] {CLEAN_DATA_PATH}product_features.csv')

# RESUME

print('\n' + '=' * 60)
print('PIPELINE DATA ENGINEERING TERMINE')
print('=' * 60)
print(f'\n> Events nettoyes    : {len(events_clean):,} lignes')
print(f'> Visitor features   : {len(visitor_features):,} visiteurs')
print(f'> Product features   : {len(product_features):,} produits')
print(f'\nFichiers exportes dans : {CLEAN_DATA_PATH}')
print('=' * 60)
