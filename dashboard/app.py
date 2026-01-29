
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings

warnings.filterwarnings('ignore')

# CONFIGURATION DE LA PAGE


st.set_page_config(
    page_title="RetailRocket Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS personnalise moderne
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Styles */
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0;
        padding-top: 1rem;
    }
    .sub-header {
        color: #64748b;
        font-size: 1.1rem;
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    /* Metric Cards */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        border-color: #667eea;
    }
    div[data-testid="stMetric"] label {
        color: #64748b;
        font-weight: 500;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #1e293b;
        font-weight: 700;
        font-size: 1.8rem;
    }
    
    /* Section Headers */
    .stMarkdown h2 {
        color: #1e293b;
        font-weight: 600;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
        display: inline-block;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ff0000 0%, #ff0000 100%);
    }
    section[data-testid="stSidebar"] .stMarkdown {
        color: #e2e8f0;
    }
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stSlider label {
        color: #cbd5e1 !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(102, 126, 234, 0.4);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px -2px rgba(102, 126, 234, 0.5);
    }
    
    /* Download Buttons */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.4);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f1f5f9;
        border-radius: 12px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        font-weight: 500;
        color: #64748b;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }
    
    /* DataFrames */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Info/Warning/Success boxes */
    .stAlert {
        border-radius: 12px;
        border: none;
    }
    
    /* Plotly Charts Container */
    .js-plotly-plot {
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
        margin: 2rem 0;
    }
    
    /* Custom card class */
    .custom-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }
    
    /* Gradient text */
    .gradient-text {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
</style>
""", unsafe_allow_html=True)


# CHARGEMENT DES DONNEES (avec cache)

@st.cache_data(ttl=3600)
def load_data():
    """Charge les donnees preparees."""
    try:
        visitors = pd.read_csv('../data/clean/visitor_features.csv')
        products = pd.read_csv('../data/clean/product_features.csv')
        
        try:
            events = pd.read_csv('../data/clean/events_clean.csv')
            events['timestamp'] = pd.to_datetime(events['timestamp'])
            events['date'] = events['timestamp'].dt.date
        except:
            events = None
            
        try:
            kpis = pd.read_csv('../data/clean/kpi_business_summary.csv')
        except:
            kpis = None
            
        return visitors, products, events, kpis
    
    except Exception as e:
        st.error(f"Erreur de chargement: {e}")
        return None, None, None, None


def calculate_kpis(visitors):
    """Calcule les KPIs principaux."""
    
    total_visitors = len(visitors)
    visitors_with_cart = (visitors['n_addtocart'] > 0).sum()
    visitors_with_purchase = (visitors['n_transaction'] > 0).sum()
    
    conversion_rate = visitors_with_purchase / total_visitors * 100
    view_to_cart = visitors_with_cart / total_visitors * 100
    cart_to_purchase = visitors_with_purchase / visitors_with_cart * 100 if visitors_with_cart > 0 else 0
    abandonment_rate = (1 - visitors_with_purchase / visitors_with_cart) * 100 if visitors_with_cart > 0 else 0
    avg_views = visitors['n_view'].mean()
    
    return {
        'total_visitors': total_visitors,
        'visitors_with_cart': visitors_with_cart,
        'visitors_with_purchase': visitors_with_purchase,
        'conversion_rate': conversion_rate,
        'view_to_cart': view_to_cart,
        'cart_to_purchase': cart_to_purchase,
        'abandonment_rate': abandonment_rate,
        'avg_views': avg_views
    }


# COMPOSANTS GRAPHIQUES

def create_funnel_chart(kpis):
    """Cree un graphique entonnoir de conversion."""
    
    stages = ['Visiteurs', 'Ajout Panier', 'Achat']
    values = [
        kpis['total_visitors'],
        kpis['visitors_with_cart'],
        kpis['visitors_with_purchase']
    ]
    
    fig = go.Figure(go.Funnel(
        y=stages,
        x=values,
        textposition="inside",
        textinfo="value+percent initial",
        marker=dict(
            color=['#3b82f6', '#8b5cf6', '#10b981'],
            line=dict(width=2, color='white')
        ),
        connector=dict(line=dict(color="royalblue", dash="dot", width=2))
    ))
    
    fig.update_layout(
        title=dict(text="Entonnoir de Conversion", font=dict(size=18)),
        height=400,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig


def create_conversion_gauge(value, title="Taux de Conversion"):
    """Cree une jauge pour le taux de conversion."""
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={'suffix': "%", 'font': {'size': 40}},
        gauge={
            'axis': {'range': [0, 5], 'ticksuffix': '%'},
            'bar': {'color': "#3b82f6"},
            'steps': [
                {'range': [0, 1], 'color': "#fee2e2"},
                {'range': [1, 2], 'color': "#fef3c7"},
                {'range': [2, 5], 'color': "#d1fae5"}
            ],
            'threshold': {
                'line': {'color': "#10b981", 'width': 4},
                'thickness': 0.75,
                'value': 2
            }
        },
        title={'text': title, 'font': {'size': 16}}
    ))
    
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=60, b=20))
    
    return fig


def create_behavior_distribution(visitors):
    """Cree la distribution des comportements visiteurs."""
    
    def segment_visitor(row):
        if row['n_transaction'] > 0:
            return 'Acheteur'
        elif row['n_addtocart'] > 0:
            return 'Panier abandonne'
        elif row['n_view'] > 5:
            return 'Explorateur'
        else:
            return 'Rebond'
    
    visitors = visitors.copy()
    visitors['segment'] = visitors.apply(segment_visitor, axis=1)
    segment_counts = visitors['segment'].value_counts()
    
    colors = {
        'Acheteur': '#10b981',
        'Panier abandonne': '#f59e0b',
        'Explorateur': '#3b82f6',
        'Rebond': '#ef4444'
    }
    
    fig = px.pie(
        values=segment_counts.values,
        names=segment_counts.index,
        color=segment_counts.index,
        color_discrete_map=colors,
        hole=0.4
    )
    
    fig.update_layout(
        title=dict(text="Segmentation Visiteurs", font=dict(size=18)),
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2)
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    return fig


def create_product_pareto(products, top_n=20):
    """Cree un diagramme de Pareto des produits."""
    
    top_products = products.nlargest(top_n, 'n_view').copy()
    top_products = top_products.sort_values('n_view', ascending=False)
    
    top_products['cumsum'] = top_products['n_view'].cumsum()
    top_products['cum_percent'] = top_products['cumsum'] / products['n_view'].sum() * 100
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Bar(
            x=top_products['itemid'].astype(str),
            y=top_products['n_view'],
            name="Vues",
            marker_color='#3b82f6'
        ),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(
            x=top_products['itemid'].astype(str),
            y=top_products['cum_percent'],
            name="% Cumule",
            mode='lines+markers',
            line=dict(color='#ef4444', width=2),
            marker=dict(size=6)
        ),
        secondary_y=True
    )
    
    fig.add_hline(y=80, line_dash="dash", line_color="green", 
                  annotation_text="80%", secondary_y=True)
    
    fig.update_layout(
        title=dict(text=f"Top {top_n} Produits (Pareto)", font=dict(size=18)),
        height=400,
        xaxis_title="Produit ID",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    
    fig.update_yaxes(title_text="Nombre de vues", secondary_y=False)
    fig.update_yaxes(title_text="% Cumule", secondary_y=True)
    
    return fig


# SIDEBAR - FILTRES

def render_sidebar(visitors, products):
    """Rendu de la sidebar avec filtres."""
    
    st.sidebar.markdown("## Filtres")
    
    segments = ['Tous', 'Acheteurs', 'Panier abandonne', 'Explorateurs', 'Rebond']
    selected_segment = st.sidebar.selectbox("Segment visiteur", segments)
    
    min_views = int(visitors['n_view'].min())
    max_views = int(min(visitors['n_view'].max(), 100))
    view_range = st.sidebar.slider(
        "Nombre de vues",
        min_value=min_views,
        max_value=max_views,
        value=(min_views, max_views)
    )
    
    top_n = st.sidebar.slider("Top N produits", 10, 50, 20)
    
    if st.sidebar.button("Reinitialiser les filtres"):
        st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### A propos")
    st.sidebar.markdown("""
    Dashboard d'analyse des donnees 
    RetailRocket E-commerce.
    
    **Periode**: Mai - Sep 2015  
    **Source**: Kaggle
    """)
    
    return {
        'segment': selected_segment,
        'view_range': view_range,
        'top_n': top_n
    }


def apply_filters(visitors, filters):
    """Applique les filtres aux donnees."""
    
    df = visitors.copy()
    
    def segment_visitor(row):
        if row['n_transaction'] > 0:
            return 'Acheteurs'
        elif row['n_addtocart'] > 0:
            return 'Panier abandonne'
        elif row['n_view'] > 5:
            return 'Explorateurs'
        else:
            return 'Rebond'
    
    df['segment_filter'] = df.apply(segment_visitor, axis=1)
    
    if filters['segment'] != 'Tous':
        df = df[df['segment_filter'] == filters['segment']]
    
    df = df[(df['n_view'] >= filters['view_range'][0]) & 
            (df['n_view'] <= filters['view_range'][1])]
    
    return df


# PAGE PRINCIPALE

def main():
    """Point d'entree principal du dashboard."""
    
    st.markdown('<p class="main-header"> RetailRocket Analytics</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header"> Dashboard E-commerce - Analyse des performances en temps réel</p>', unsafe_allow_html=True)
    
    with st.spinner("Chargement des donnees..."):
        visitors, products, events, kpis_df = load_data()
    
    if visitors is None:
        st.error("Impossible de charger les donnees. Verifiez que les fichiers existent dans data/clean/")
        st.stop()
    
    filters = render_sidebar(visitors, products)
    filtered_visitors = apply_filters(visitors, filters)
    kpis = calculate_kpis(filtered_visitors)
    
    if len(filtered_visitors) < len(visitors):
        st.info(f" Filtres actifs: {len(filtered_visitors):,} visiteurs sur {len(visitors):,}")
    
    # SECTION 1: KPIs PRINCIPAUX
    st.markdown("##  KPIs Principaux")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label=" Visiteurs", value=f"{kpis['total_visitors']:,}")
    
    with col2:
        st.metric(label=" Taux de Conversion", value=f"{kpis['conversion_rate']:.2f}%")
    
    with col3:
        st.metric(label=" View → Cart", value=f"{kpis['view_to_cart']:.2f}%")
    
    with col4:
        st.metric(label=" Taux Abandon", value=f"{kpis['abandonment_rate']:.1f}%")
    
    # SECTION 2: ENTONNOIR ET CONVERSION
    st.markdown("---")
    st.markdown("##  Analyse de Conversion")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        funnel_fig = create_funnel_chart(kpis)
        st.plotly_chart(funnel_fig, key="funnel")
    
    with col2:
        gauge_fig = create_conversion_gauge(kpis['conversion_rate'])
        st.plotly_chart(gauge_fig, key="gauge")
        
        st.markdown("###  Insights")
        if kpis['view_to_cart'] < 3:
            st.warning(" Taux View→Cart faible (<3%). Optimiser les fiches produits.")
        if kpis['abandonment_rate'] > 60:
            st.warning(" Taux Abandon panier élevé. Revoir le checkout.")
        if kpis['conversion_rate'] >= 1:
            st.success(" Conversion dans la moyenne e-commerce.")
    
    # SECTION 3: SEGMENTATION ET PRODUITS
    st.markdown("---")
    st.markdown("##  Segmentation & Produits")
    
    col1, col2 = st.columns(2)
    
    with col1:
        behavior_fig = create_behavior_distribution(filtered_visitors)
        st.plotly_chart(behavior_fig, key="behavior")
    
    with col2:
        pareto_fig = create_product_pareto(products, filters['top_n'])
        st.plotly_chart(pareto_fig, key="pareto")
    
    # SECTION 4: TABLEAU DETAILLE
    st.markdown("---")
    st.markdown("##  Données Détaillées")
    
    tab1, tab2 = st.tabs([" Top Visiteurs", " Top Produits"])
    
    with tab1:
        top_visitors = filtered_visitors.nlargest(20, 'n_view')[
            ['visitorid', 'n_view', 'n_addtocart', 'n_transaction', 'unique_items']
        ]
        top_visitors.columns = ['ID Visiteur', 'Vues', 'Ajouts Panier', 'Achats', 'Produits Uniques']
        st.dataframe(top_visitors, hide_index=True)
    
    with tab2:
        top_prods = products.nlargest(20, 'n_view')[
            ['itemid', 'n_view', 'n_addtocart', 'n_transaction', 'view_to_cart']
        ]
        top_prods.columns = ['ID Produit', 'Vues', 'Paniers', 'Achats', 'Taux Conv.']
        top_prods['Taux Conv.'] = top_prods['Taux Conv.'].apply(lambda x: f"{x:.2%}" if pd.notna(x) else "N/A")
        st.dataframe(top_prods, hide_index=True)
    
    # SECTION 5: TELECHARGEMENT
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        csv = filtered_visitors.to_csv(index=False)
        st.download_button(
            label=" Télécharger Visiteurs (CSV)",
            data=csv,
            file_name="visitors_filtered.csv",
            mime="text/csv"
        )
    
    with col2:
        csv_products = products.to_csv(index=False)
        st.download_button(
            label=" Télécharger Produits (CSV)",
            data=csv_products,
            file_name="products.csv",
            mime="text/csv"
        )
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; padding: 2rem 0;'>
            <p style='color: #64748b; font-size: 0.9rem; margin-bottom: 0.5rem;'>
                Fait avec ❤️ par Ryma Sitayeb
            </p>
            <p style='color: #94a3b8; font-size: 0.8rem;'>
                RetailRocket Analytics Dashboard • 2026 • v2.0
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
