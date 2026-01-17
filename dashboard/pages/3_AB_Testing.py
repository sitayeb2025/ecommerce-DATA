"""
Page des resultats A/B Testing pour le dashboard.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import norm

st.set_page_config(page_title="A/B Testing", page_icon="🧪", layout="wide")

# CSS Moderne
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp { font-family: 'Inter', sans-serif; }
    
    .page-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);
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
        background: linear-gradient(135deg, #ffffff 0%, #f5f3ff 100%);
        border: 1px solid #c4b5fd;
        border-radius: 16px;
        padding: 1.2rem;
        box-shadow: 0 4px 6px -1px rgba(139, 92, 246, 0.1);
        transition: all 0.3s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px -3px rgba(139, 92, 246, 0.2);
        border-color: #8b5cf6;
    }
    div[data-testid="stMetric"] label {
        color: #7c3aed;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.8rem;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #5b21b6;
        font-weight: 700;
    }
    
    .stMarkdown h2, .stMarkdown h3 {
        color: #1e293b;
        font-weight: 600;
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #5b21b6 0%, #4c1d95 100%);
    }
    section[data-testid="stSidebar"] .stMarkdown {
        color: #ede9fe;
    }
    section[data-testid="stSidebar"] .stMarkdown h2 {
        color: #f5f3ff !important;
        border-bottom: 2px solid #8b5cf6;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(139, 92, 246, 0.4);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px -3px rgba(139, 92, 246, 0.5);
    }
    
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #c4b5fd, transparent);
        margin: 2rem 0;
    }
    
    .stAlert {
        border-radius: 12px;
        border: none;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_ab_results():
    """Charge les resultats du test A/B."""
    try:
        return pd.read_csv('../outputs/data/ab_test_results.csv')
    except:
        return None


def simulate_ab_test(n_per_group, baseline_rate, effect):
    """Simule un test A/B."""
    np.random.seed(42)
    
    variant_rate = baseline_rate * (1 + effect)
    
    control = np.random.binomial(1, baseline_rate, n_per_group)
    variant = np.random.binomial(1, variant_rate, n_per_group)
    
    return {
        'control_rate': control.mean(),
        'variant_rate': variant.mean(),
        'control_n': n_per_group,
        'variant_n': n_per_group
    }


def calculate_significance(control_rate, variant_rate, n_control, n_variant):
    """Calcule la significativite statistique."""
    
    p_pool = (control_rate * n_control + variant_rate * n_variant) / (n_control + n_variant)
    se = np.sqrt(p_pool * (1 - p_pool) * (1/n_control + 1/n_variant))
    
    if se == 0:
        return 0, 1
    
    z_stat = (variant_rate - control_rate) / se
    p_value = 2 * (1 - norm.cdf(abs(z_stat)))
    
    return z_stat, p_value


def create_ab_comparison(control_rate, variant_rate):
    """Graphique de comparaison A/B."""
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=['🅰️ Control', '🅱️ Variant'],
        y=[control_rate * 100, variant_rate * 100],
        marker_color=['#3b82f6', '#10b981'],
        text=[f'{control_rate*100:.2f}%', f'{variant_rate*100:.2f}%'],
        textposition='outside',
        textfont=dict(size=16, color='#1e293b')
    ))
    
    lift = (variant_rate - control_rate) / control_rate * 100
    
    fig.add_annotation(
        x=1, y=variant_rate * 100,
        text=f'<b>+{lift:.1f}%</b>',
        showarrow=True,
        arrowhead=2,
        arrowcolor='#10b981',
        font=dict(size=18, color='#10b981')
    )
    
    fig.update_layout(
        title=dict(
            text="📊 Comparaison des Taux de Conversion",
            font=dict(size=20, color='#1e293b')
        ),
        yaxis_title="Taux (%)",
        height=450,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(gridcolor='#e2e8f0')
    )
    
    return fig


# =============================================================================
# PAGE PRINCIPALE
# =============================================================================

def main():
    st.markdown('<p class="page-header">🧪 Simulateur A/B Testing</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">⚡ Simulez et analysez des tests A/B en temps réel</p>', unsafe_allow_html=True)
    
    # Sidebar - Parametres
    st.sidebar.markdown("## ⚙️ Paramètres du Test")
    
    baseline = st.sidebar.slider(
        "📈 Taux baseline (%)",
        min_value=0.5,
        max_value=10.0,
        value=2.69,
        step=0.1
    ) / 100
    
    effect = st.sidebar.slider(
        "🎯 Effet simulé (%)",
        min_value=-30,
        max_value=50,
        value=15
    ) / 100
    
    sample_size = st.sidebar.slider(
        "👥 Taille échantillon (par groupe)",
        min_value=1000,
        max_value=100000,
        value=50000,
        step=1000
    )
    
    alpha = st.sidebar.selectbox(
        "📊 Niveau de significativité",
        [0.01, 0.05, 0.10],
        index=1
    )
    
    # Simulation
    if st.sidebar.button("🚀 Lancer la simulation", type="primary"):
        with st.spinner("⏳ Simulation en cours..."):
            results = simulate_ab_test(sample_size, baseline, effect)
            z_stat, p_value = calculate_significance(
                results['control_rate'],
                results['variant_rate'],
                results['control_n'],
                results['variant_n']
            )
            
            st.session_state['ab_results'] = results
            st.session_state['ab_stats'] = {'z': z_stat, 'p': p_value}
    
    # Affichage resultats
    if 'ab_results' in st.session_state:
        results = st.session_state['ab_results']
        stats = st.session_state['ab_stats']
        
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🅰️ Taux Control", f"{results['control_rate']*100:.2f}%")
        with col2:
            st.metric("🅱️ Taux Variant", f"{results['variant_rate']*100:.2f}%")
        with col3:
            lift = (results['variant_rate'] - results['control_rate']) / results['control_rate'] * 100
            st.metric("📈 Lift", f"{lift:+.1f}%")
        with col4:
            significant = stats['p'] < alpha
            st.metric("🎲 p-value", f"{stats['p']:.4f}")
        
        # Resultat
        st.markdown("---")
        
        if significant:
            if lift > 0:
                st.success(f"✅ **RESULTAT SIGNIFICATIF** - Le variant est meilleur (p={stats['p']:.4f} < {alpha})")
                st.balloons()
            else:
                st.error(f"⚠️ **RESULTAT SIGNIFICATIF** - Le variant est moins bon (p={stats['p']:.4f} < {alpha})")
        else:
            st.warning(f"⏳ **NON SIGNIFICATIF** - Pas assez de preuves (p={stats['p']:.4f} > {alpha})")
        
        # Graphique
        st.plotly_chart(
            create_ab_comparison(results['control_rate'], results['variant_rate']),
            use_container_width=True
        )
        
        # Interpretation
        st.markdown("### 📊 Interprétation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); 
                        padding: 1.5rem; border-radius: 16px; border: 1px solid #bae6fd;">
                <h4 style="color: #0369a1; margin-top: 0;">📈 Statistiques</h4>
            """, unsafe_allow_html=True)
            st.markdown(f"""
- **Z-score**: `{stats['z']:.2f}`
- **p-value**: `{stats['p']:.6f}`
- **Seuil alpha**: `{alpha}`
- **Échantillon total**: `{sample_size * 2:,}`
            """)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); 
                        padding: 1.5rem; border-radius: 16px; border: 1px solid #a7f3d0;">
                <h4 style="color: #059669; margin-top: 0;">💡 Recommandation</h4>
            """, unsafe_allow_html=True)
            if significant and lift > 0:
                st.markdown("""
🚀 **Déployer le variant** sur 100% du trafic.

**Actions:**
1. Déploiement progressif (10% → 50% → 100%)
2. Monitoring des métriques secondaires
3. Documentation des résultats
                """)
            elif not significant:
                st.markdown(f"""
⏳ **Continuer le test** ou augmenter l'échantillon.

**Taille recommandée:** ~{int(sample_size * 1.5):,} par groupe
                """)
            st.markdown("</div>", unsafe_allow_html=True)
    
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%); 
                    padding: 2rem; border-radius: 16px; border: 1px solid #c4b5fd; text-align: center;">
            <h3 style="color: #7c3aed; margin: 0;">🧪 Prêt à tester ?</h3>
            <p style="color: #6b7280; margin-top: 0.5rem;">
                Configurez les paramètres dans la barre latérale et lancez une simulation
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Resultats precedents
    st.markdown("---")
    st.markdown("### 📁 Résultats Précédents")
    
    ab_history = load_ab_results()
    if ab_history is not None:
        st.dataframe(ab_history, use_container_width=True, hide_index=True)
    else:
        st.info("💾 Aucun résultat A/B sauvegardé. Exécutez le notebook ab_testing.ipynb.")


if __name__ == "__main__":
    main()
