import streamlit as st
import pandas as pd
import plotly.express as px
import os
from ai_engine import AIEngine
from processor import DataProcessor
from config import setup_logging, validate_config

# ── Configuración de Página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="PCSBUR | Market Intelligence Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilo personalizado (Dark Theme)
st.markdown("""
<style>
    .metric-card {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #333;
    }
    .stMetric {
        background-color: #0e1117;
        padding: 15px;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Configuración global
setup_logging()
validate_config()

# Instanciar motores
engine = AIEngine()
processor = DataProcessor()

# ── Datos de Sesión ───────────────────────────────────────────────────────────
if "market_data" not in st.session_state:
    st.session_state.market_data = pd.DataFrame()

# ── Sidebar ──────────────────────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/color/96/artificial-intelligence.png", width=80)
st.sidebar.title("Configuración")
st.sidebar.markdown("---")

services_to_search = st.sidebar.multiselect(
    "Servicios a investigar",
    [
        "mantenimiento preventivo laptop",
        "formateo windows 10/11",
        "instalación ssd",
        "reparación de pantalla laptop",
        "instalación programas/antivirus"
    ],
    default=["mantenimiento preventivo laptop", "formateo windows 10/11"]
)

if st.sidebar.button("🚀 Actualizar Mercado", use_container_width=True):
    with st.spinner("Consultando inteligencia de mercado en Calderón..."):
        all_records = []
        for svc in services_to_search:
            res = engine.get_market_data(svc)
            records = processor.parse_response(res)
            all_records.extend(records)
        
        if all_records:
            st.session_state.market_data = pd.DataFrame(all_records)
            st.success("Mercado actualizado correctamente")
        else:
            st.error("No se obtuvieron datos de la IA")

st.sidebar.markdown("---")
st.sidebar.info("Este dashboard utiliza Blackbox AI (blackbox-pro) para analizar precios reales en Calderón, Quito.")

# ── Header ──────────────────────────────────────────────────────────────────
st.title("🧠 PCSBUR Market Intelligence")
st.subheader("Análisis de competencia y precios en Calderón, Quito")

if not st.session_state.market_data.empty:
    df = st.session_state.market_data
    
    # ── Métricas ──────────────────────────────────────────────────────────────
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_price = df["precio_prom_usd"].mean()
        st.metric("Precio Promedio Mercado", f"${avg_price:.2f} USD")
        
    with col2:
        count_prov = df["proveedor"].nunique()
        st.metric("Proveedores Encontrados", count_prov)
        
    with col3:
        cheapest = df.loc[df["precio_min_usd"] > 0, "precio_min_usd"].min()
        st.metric("Precio Mínimo Detectado", f"${cheapest:.2f} USD")

    st.markdown("---")

    # ── Gráficos ──────────────────────────────────────────────────────────────
    c1, c2 = st.columns([2, 1])

    with c1:
        st.write("### Comparativa de Precios por Servicio")
        # Graficar Min, Max y Promedio
        df_melt = df.melt(
            id_vars=["servicio"], 
            value_vars=["precio_min_usd", "precio_max_usd", "precio_prom_usd"],
            var_name="Tipo de Precio", 
            value_name="USD"
        )
        fig = px.bar(
            df_melt, 
            x="servicio", 
            y="USD", 
            color="Tipo de Precio",
            barmode="group",
            template="plotly_dark",
            color_discrete_sequence=["#1f77b4", "#ff7f0e", "#2ca02c"]
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.write("### Distribución de Ofertas")
        fig_pie = px.pie(
            df, 
            names="servicio", 
            values="precio_prom_usd",
            template="plotly_dark",
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # ── Tabla de Detalles ─────────────────────────────────────────────────────
    st.write("### Detalle de Locales y Ofertas")
    st.dataframe(
        df[["servicio", "proveedor", "precio_prom_usd", "descripcion", "fuente", "fecha_consulta"]],
        use_container_width=True,
        hide_index=True
    )

    # Botones de descarga
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Reporte CSV",
        data=csv,
        file_name='reporte_mercado_pcsbur.csv',
        mime='text/csv',
    )

else:
    st.warning("👈 Haz clic en 'Actualizar Mercado' en la barra lateral para comenzar la investigación.")
    
    # Placeholder visual
    st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&q=80&w=2070", caption="Análisis de datos de mercado")
