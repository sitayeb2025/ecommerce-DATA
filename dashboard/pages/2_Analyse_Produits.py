"""
Page d'analyse des produits pour le dashboard E-commerce.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Analyse Produits", page_icon="📦", layout="wide")

# CSS Moderne
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp { font-family: 'Inter', sans-serif; }
    
    .page-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .page-subtitle {
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #ffffff 0%, #ecfdf5 100%);
        border: 1px solid #a7f3d0;
        border-radius: 16px;
        padding: 1.2rem;
        box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.1);
        transition: all 0.3s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px -3px rgba(16, 185, 129, 0.2);
        border-color: #10b981;
    }
    div[data-testid="stMetric"] label {
        color: #059669;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.8rem;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #065f46;
        font-weight: 700;
    }
    
    .stMarkdown h2, .stMarkdown h3 {
        color: #1e293b;
        font-weight: 600;
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #065f46 0%, #064e3b 100%);
    }
    section[data-testid="stSidebar"] .stMarkdown {
        color: #d1fae5;
    }
    section[data-testid="stSidebar"] .stMarkdown h2 {
        color: #ecfdf5 !important;
        border-bottom: 2px solid #10b981;
    }
    
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #a7f3d0, transparent);
        margin: 2rem 0;
    }
    
    .stTextInput input {
        border-radius: 12px;
        border: 2px solid #a7f3d0;
        padding: 0.75rem 1rem;
    }
    .stTextInput input:focus {
        border-color: #10b981;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2);
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_products():
    """Charge les donnees produits."""
    return pd.read_csv('../data/clean/product_features.csv')


def create_performance_scatter(products):
    """Scatter plot vues vs conversion."""
    
    df = products[products['n_view'] > 10].copy()
    df['view_to_cart_pct'] = df['view_to_cart'].fillna(0) * 100
    
    fig = px.scatter(
        df,
        x='n_view',
        y='view_to_cart_pct',
        size='n_transaction',
        color='n_addtocart',
        hover_data=['itemid'],
        color_continuous_scale='Viridis',
        labels={
            'n_view': 'Nombre de vues',
            'view_to_cart_pct': 'Taux View->Cart (%)',
            'n_addtocart': 'Ajouts panier',
            'n_transaction': 'Achats'
        }
    )
    
    fig.update_layout(
        title=dict(
            text="🎯 Performance Produits: Vues vs Conversion",
            font=dict(size=18, color='#1e293b')
        ),
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


def create_category_analysis(products):
    """Analyse par categorie de performance."""
    
    def categorize(row):
        if row['n_transaction'] > 0:
            return 'Vendus'
        elif row['n_addtocart'] > 0:
            return 'Panier seulement'
        elif row['n_view'] > 50:
            return 'Bien vus'
        else:
            return 'Peu vus'
    
    products = products.copy()
    products['category'] = products.apply(categorize, axis=1)
    cat_counts = products['category'].value_counts()
    
    colors = {
        'Vendus': '#10b981',
        'Panier seulement': '#f59e0b',
        'Bien vus': '#3b82f6',
        'Peu vus': '#94a3b8'
    }
    
    fig = px.bar(
        x=cat_counts.index,
        y=cat_counts.values,
        color=cat_counts.index,
        color_discrete_map=colors,
        labels={'x': 'Categorie', 'y': 'Nombre de produits'}
    )
    
    fig.update_layout(
        title=dict(
            text="📊 Distribution des Produits par Performance",
            font=dict(size=18, color='#1e293b')
        ),
        showlegend=False,
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


def create_top_converters(products, n=15):
    """Top produits par taux de conversion."""
    
    df = products[products['n_view'] >= 20].copy()
    df['view_to_cart_pct'] = df['view_to_cart'].fillna(0) * 100
    
    top = df.nlargest(n, 'view_to_cart_pct')
    
    fig = px.bar(
        top,
        x='view_to_cart_pct',
        y='itemid',
        orientation='h',
        color='n_view',
        color_continuous_scale='Blues',
        labels={
            'view_to_cart_pct': 'Taux View->Cart (%)',
            'itemid': 'Produit ID',
            'n_view': 'Vues'
        }
    )
    
    fig.update_layout(
        title=dict(
            text=f"🏆 Top {n} Produits par Conversion (min 20 vues)",
            font=dict(size=18, color='#1e293b')
        ),
        yaxis={'categoryorder': 'total ascending'},
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


# =============================================================================
# PAGE PRINCIPALE
# =============================================================================

def main():
    st.markdown('<p class="page-header">📦 Analyse Produits</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">🔍 Performance et opportunités produits</p>', unsafe_allow_html=True)
    
    products = load_products()
    
    # KPIs produits
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📦 Total Produits", f"{len(products):,}")
    with col2:
        sold_pct = (products['n_transaction'] > 0).mean() * 100
        st.metric("✅ Produits vendus", f"{sold_pct:.1f}%")
    with col3:
        avg_views = products['n_view'].mean()
        st.metric("👁️ Vues moyennes", f"{avg_views:.1f}")
    with col4:
        avg_conv = products[products['view_to_cart'] > 0]['view_to_cart'].mean() * 100
        st.metric("🎯 Conv. moyenne", f"{avg_conv:.2f}%")
    
    # Filtres
    st.sidebar.markdown("## 🔧 Filtres Produits")
    min_views = st.sidebar.slider("👁️ Vues minimum", 0, 100, 0)
    show_only_sold = st.sidebar.checkbox("✅ Produits vendus uniquement")
    
    # Filtrage
    filtered = products[products['n_view'] >= min_views]
    if show_only_sold:
        filtered = filtered[filtered['n_transaction'] > 0]
    
    st.info(f"📊 {len(filtered):,} produits affichés")
    
    # Graphiques
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_category_analysis(filtered), key="cat", use_container_width=True)
    
    with col2:
        st.plotly_chart(create_top_converters(filtered), key="top", use_container_width=True)
    
    st.plotly_chart(create_performance_scatter(filtered), key="scatter", use_container_width=True)
    
    # Tableau
    st.markdown("---")
    st.markdown("### 🔍 Recherche Produit")
    
    search_id = st.text_input("🔎 Rechercher un produit (ID)", placeholder="Entrez l'ID du produit...")
    
    if search_id:
        result = products[products['itemid'].astype(str).str.contains(search_id)]
        if len(result) > 0:
            st.dataframe(result, hide_index=True, use_container_width=True)
        else:
            st.warning("⚠️ Aucun produit trouvé")


if __name__ == "__main__":
    main()
