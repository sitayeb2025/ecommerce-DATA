"""
Page d'analyse temporelle pour le dashboard E-commerce.
Visualisations des tendances et patterns temporels.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Analyse Temporelle", page_icon="📅", layout="wide")

# CSS Moderne
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp { font-family: 'Inter', sans-serif; }
    
    .page-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
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
        background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%);
        border: 1px solid #bfdbfe;
        border-radius: 16px;
        padding: 1.2rem;
        box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.1);
        transition: all 0.3s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px -3px rgba(59, 130, 246, 0.2);
        border-color: #3b82f6;
    }
    div[data-testid="stMetric"] label {
        color: #3b82f6;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.8rem;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #1e40af;
        font-weight: 700;
    }
    
    .stMarkdown h2 {
        color: #1e293b;
        font-weight: 600;
        border-bottom: 3px solid #3b82f6;
        display: inline-block;
        padding-bottom: 0.5rem;
    }
    
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #bfdbfe, transparent);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_events():
    """Charge les evenements avec timestamps."""
    try:
        events = pd.read_csv('../outputs/data/events_clean.csv')
        # Timestamp en millisecondes Unix -> conversion avec unit='ms'
        events['timestamp'] = pd.to_datetime(events['timestamp'], unit='ms')
        events['date'] = events['timestamp'].dt.date
        events['hour'] = events['timestamp'].dt.hour
        events['day_of_week'] = events['timestamp'].dt.dayofweek
        events['week'] = events['timestamp'].dt.isocalendar().week
        return events
    except Exception as e:
        st.error(f"Erreur: {e}")
        return None


def create_daily_trend(events):
    """Tendance journaliere des evenements."""
    daily = events.groupby(['date', 'event']).size().unstack(fill_value=0)
    
    fig = go.Figure()
    
    colors = {'view': '#3b82f6', 'addtocart': '#f59e0b', 'transaction': '#10b981'}
    
    for event_type in ['view', 'addtocart', 'transaction']:
        if event_type in daily.columns:
            fig.add_trace(go.Scatter(
                x=daily.index,
                y=daily[event_type],
                name=event_type.title(),
                mode='lines',
                line=dict(color=colors.get(event_type, '#666'))
            ))
    
    fig.update_layout(
        title=dict(
            text=" Tendance Journalière des Événements",
            font=dict(size=18, color='#1e293b')
        ),
        xaxis_title="Date",
        yaxis_title="Nombre d'événements",
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='#e2e8f0'),
        yaxis=dict(gridcolor='#e2e8f0')
    )
    
    return fig


def create_hourly_heatmap(events):
    """Heatmap heures x jours de la semaine."""
    
    pivot = events.groupby(['day_of_week', 'hour']).size().unstack(fill_value=0)
    
    days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=[days[i] for i in pivot.index],
        colorscale='Blues',
        hovertemplate='Jour: %{y}<br>Heure: %{x}h<br>Événements: %{z}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text=" Activité par Jour et Heure",
            font=dict(size=18, color='#1e293b')
        ),
        xaxis_title="Heure",
        yaxis_title="Jour de la semaine",
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


def create_conversion_trend(events):
    """Evolution du taux de conversion dans le temps."""
    
    daily_stats = events.groupby('date').agg({
        'visitorid': 'nunique',
        'event': lambda x: (x == 'transaction').sum()
    }).reset_index()
    
    daily_stats.columns = ['date', 'visitors', 'transactions']
    daily_stats['conversion_rate'] = daily_stats['transactions'] / daily_stats['visitors'] * 100
    
    # Moyenne mobile 7 jours
    daily_stats['conv_ma7'] = daily_stats['conversion_rate'].rolling(7).mean()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=daily_stats['date'],
        y=daily_stats['conversion_rate'],
        name='Taux journalier',
        mode='lines',
        line=dict(color='#94a3b8', width=1),
        opacity=0.5
    ))
    
    fig.add_trace(go.Scatter(
        x=daily_stats['date'],
        y=daily_stats['conv_ma7'],
        name='Moyenne 7j',
        mode='lines',
        line=dict(color='#3b82f6', width=3)
    ))
    
    fig.update_layout(
        title=dict(
            text=" Évolution du Taux de Conversion",
            font=dict(size=18, color='#1e293b')
        ),
        xaxis_title="Date",
        yaxis_title="Taux de conversion (%)",
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='#e2e8f0'),
        yaxis=dict(gridcolor='#e2e8f0')
    )
    
    return fig


# =============================================================================
# PAGE PRINCIPALE
# =============================================================================

def main():
    st.markdown('<p class="page-header"> Analyse Temporelle</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle"> Découvrez les patterns et tendances dans le temps</p>', unsafe_allow_html=True)
    
    events = load_events()
    
    if events is None:
        st.warning(" Fichier events_clean.csv non disponible. Exécutez d'abord le pipeline de données.")
        st.info(" Utilisez le script data_pipeline.py pour générer les données.")
        st.stop()
    
    # Metriques periode
    col1, col2, col3, col4 = st.columns(4)
    
    date_min = events['date'].min()
    date_max = events['date'].max()
    nb_days = (date_max - date_min).days + 1
    
    with col1:
        st.metric(" Période", f"{nb_days} jours")
    with col2:
        st.metric(" Premier jour", str(date_min))
    with col3:
        st.metric("  Dernier jour", str(date_max))
    with col4:
        st.metric(" Événements/jour", f"{len(events) / nb_days:,.0f}")
    
    # Graphiques
    st.markdown("---")
    
    st.plotly_chart(create_daily_trend(events), use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_hourly_heatmap(events), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_conversion_trend(events), use_container_width=True)


if __name__ == "__main__":
    main()
