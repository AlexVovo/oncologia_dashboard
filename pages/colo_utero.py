import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils.theme import apply_dark_theme, render_card, render_intro

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------

st.set_page_config(layout="wide")
apply_dark_theme()

st.title("Dashboard - Câncer do Colo do Útero")

render_intro("Análise epidemiológica e assistencial com filtros, indicadores, evolução temporal e mapa interativo.")

# ---------------------------------------------------
# UPLOAD CSV
# ---------------------------------------------------

uploaded_file = st.file_uploader(
    "Envie um arquivo CSV",
    type=["csv"]
)

# ---------------------------------------------------
# DADOS REAIS
# ---------------------------------------------------

default_data_path = Path(__file__).resolve().parents[1] / "data" / "colo_utero.csv"

if uploaded_file is None:
    if default_data_path.exists():
        st.success("Carregando dados reais de Câncer do Colo do Útero.")
        df = pd.read_csv(default_data_path)
    else:
        st.warning("Base local não encontrada. Usando dados de exemplo.")
        df = pd.DataFrame({
            "Estado": ["RS", "SP", "RJ", "MG", "BA", "RS", "SP"],
            "Ano": [2022, 2022, 2023, 2023, 2024, 2024, 2024],
            "Hospital": [
                "Hospital A",
                "Hospital B",
                "Hospital C",
                "Hospital D",
                "Hospital E",
                "Hospital A",
                "Hospital B"
            ],
            "Faixa_Etaria": [
                "20-29",
                "30-39",
                "40-49",
                "50-59",
                "60+",
                "30-39",
                "40-49"
            ],
            "Tempo_Tratamento": [45, 62, 38, 71, 55, 49, 66],
            "Pacientes": [120, 300, 180, 210, 140, 130, 280],
        })
else:
    df = pd.read_csv(uploaded_file)

# ---------------------------------------------------
# COORDENADAS POR ESTADO (fallback quando não há Latitude/Longitude)
# ---------------------------------------------------

state_centroids = {
    "AC": (-9.0238, -70.8120),
    "AL": (-9.5713, -36.7820),
    "AP": (1.4154, -51.7251),
    "AM": (-3.4168, -65.8561),
    "BA": (-12.9714, -38.5014),
    "CE": (-3.7172, -38.5434),
    "DF": (-15.7939, -47.8828),
    "ES": (-20.3155, -40.3128),
    "GO": (-16.6869, -49.2648),
    "MA": (-2.5307, -44.3068),
    "MT": (-12.6819, -55.7250),
    "MS": (-20.4497, -54.6468),
    "MG": (-19.9167, -43.9345),
    "PA": (-1.4558, -48.5024),
    "PB": (-7.1195, -34.8450),
    "PR": (-25.4284, -49.2733),
    "PE": (-8.0476, -34.8770),
    "PI": (-5.0919, -42.8034),
    "RJ": (-22.9136, -43.2096),
    "RN": (-5.7945, -35.2110),
    "RS": (-30.0346, -51.2177),
    "RO": (-8.7608, -63.9000),
    "RR": (2.8196, -60.6730),
    "SC": (-27.5945, -48.5477),
    "SP": (-23.5338, -46.6253),
    "SE": (-10.9472, -37.0731),
    "TO": (-10.1847, -48.3336),
}

if "Estado" in df.columns:
    df["Estado"] = df["Estado"].astype(str).str.strip().str.upper()

if "Latitude" not in df.columns:
    df["Latitude"] = None
if "Longitude" not in df.columns:
    df["Longitude"] = None

missing_coords = df["Latitude"].isna() | df["Longitude"].isna()
if missing_coords.any() and "Estado" in df.columns:
    coords = df.loc[missing_coords, "Estado"].map(state_centroids)
    df.loc[missing_coords, "Latitude"] = coords.map(lambda v: v[0] if isinstance(v, tuple) else None)
    df.loc[missing_coords, "Longitude"] = coords.map(lambda v: v[1] if isinstance(v, tuple) else None)

remaining_missing = df[df["Latitude"].isna() | df["Longitude"].isna()]["Estado"].unique()
if len(remaining_missing) > 0:
    st.warning(
        "Ainda existem estados sem coordenadas definidas: "
        f"{', '.join(map(str, remaining_missing))}. "
        "Adicione Latitude/Longitude ao CSV para esses registros."
    )

# ---------------------------------------------------
# SIDEBAR FILTROS
# ---------------------------------------------------

st.sidebar.header("🔎 Filtros")

# Estado
estado = st.sidebar.multiselect(
    "Estado",
    options=df["Estado"].unique(),
    default=df["Estado"].unique()
)

# Ano
ano = st.sidebar.multiselect(
    "Ano",
    options=df["Ano"].unique(),
    default=df["Ano"].unique()
)

# Hospital
hospital = st.sidebar.multiselect(
    "Hospital",
    options=df["Hospital"].unique(),
    default=df["Hospital"].unique()
)

# Faixa etária
faixa = st.sidebar.multiselect(
    "Faixa Etária",
    options=df["Faixa_Etaria"].unique(),
    default=df["Faixa_Etaria"].unique()
)

# ---------------------------------------------------
# FILTRAGEM
# ---------------------------------------------------

df_filtrado = df[
    (df["Estado"].isin(estado)) &
    (df["Ano"].isin(ano)) &
    (df["Hospital"].isin(hospital)) &
    (df["Faixa_Etaria"].isin(faixa))
]

# ---------------------------------------------------
# KPIs
# ---------------------------------------------------

st.subheader("📌 Indicadores")

col1, col2, col3, col4 = st.columns(4)

tempo_medio = df_filtrado["Tempo_Tratamento"].mean() if not df_filtrado.empty else 0

total_pacientes = df_filtrado["Pacientes"].sum()

total_hospitais = df_filtrado["Hospital"].nunique()

total_estados = df_filtrado["Estado"].nunique()

with col1:
    render_card("Tempo médio", f"{tempo_medio:.1f} dias", "Intervalo médio até tratamento.", "rose")

with col2:
    render_card("Pacientes", f"{total_pacientes:,}".replace(",", "."), "Total no recorte filtrado.", "cyan")

with col3:
    render_card("Hospitais", f"{total_hospitais}", "Serviços distintos no filtro.", "blue")

with col4:
    render_card("Estados", f"{total_estados}", "UFs presentes na seleção.", "amber")

st.divider()

# ---------------------------------------------------
# MAPA INTERATIVO
# ---------------------------------------------------

st.subheader("🗺️ Distribuição territorial")

if {"Latitude", "Longitude"}.issubset(df_filtrado.columns) and not df_filtrado.empty:
    mapa_df = (
        df_filtrado
        .groupby(["Estado", "Latitude", "Longitude"], as_index=False)
        .agg(Pacientes=("Pacientes", "sum"), Tempo_Medio=("Tempo_Tratamento", "mean"))
    )

    mapa_df["Tempo_Medio"] = mapa_df["Tempo_Medio"].round(1)
    mapa_df["Raio"] = mapa_df["Pacientes"].clip(lower=80) * 120

    view_state = pdk.ViewState(
        latitude=float(mapa_df["Latitude"].mean()),
        longitude=float(mapa_df["Longitude"].mean()),
        zoom=4,
        pitch=35,
    )

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=mapa_df,
        get_position="[Longitude, Latitude]",
        get_radius="Raio",
        get_fill_color="[45, 212, 191, 145]",
        get_line_color="[229, 237, 247, 210]",
        line_width_min_pixels=1,
        pickable=True,
        auto_highlight=True,
    )

    st.pydeck_chart(
        pdk.Deck(
            map_style=pdk.map_styles.CARTO_DARK,
            initial_view_state=view_state,
            layers=[layer],
            tooltip={
                "html": "<b>{Estado}</b><br/>Pacientes: {Pacientes}<br/>Tempo médio: {Tempo_Medio} dias",
                "style": {"backgroundColor": "#121a2e", "color": "#e5edf7"},
            },
        ),
        width="stretch",
    )
else:
    st.info(
        "O mapa interativo exige colunas `Latitude` e `Longitude`. "
        "Adicione essas coordenadas ao CSV ou geocode os locais para ativar a visualização territorial."
    )

st.divider()

# ---------------------------------------------------
# GRÁFICO 1
# ---------------------------------------------------

st.subheader("⏳ Tempo Médio até Tratamento")

fig1 = px.bar(
    df_filtrado,
    x="Estado",
    y="Tempo_Tratamento",
    color="Estado",
    text="Tempo_Tratamento",
    color_discrete_sequence=["#2dd4bf", "#60a5fa", "#fb7185", "#fbbf24", "#a78bfa"],
)

fig1.update_layout(
    yaxis_title="Dias",
    xaxis_title="Estado",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#e5edf7",
    legend_title_text="Estado",
)

st.plotly_chart(fig1, width="stretch")

# ---------------------------------------------------
# GRÁFICO 2
# ---------------------------------------------------

st.subheader("📈 Evolução por Ano")

fig2 = px.line(
    df_filtrado,
    x="Ano",
    y="Pacientes",
    color="Estado",
    markers=True,
    color_discrete_sequence=["#2dd4bf", "#60a5fa", "#fb7185", "#fbbf24", "#a78bfa"],
)

fig2.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#e5edf7",
    legend_title_text="Estado",
)

st.plotly_chart(fig2, width="stretch")

# ---------------------------------------------------
# TABELA
# ---------------------------------------------------

st.subheader("📋 Dados Filtrados")

st.dataframe(
    df_filtrado,
    width="stretch"
)
