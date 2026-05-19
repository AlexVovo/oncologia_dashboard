import streamlit as st
import pandas as pd
import sys
from pathlib import Path

try:
    import plotly.express as px
except Exception as _e:  # pragma: no cover - runtime dependency
    px = None
    plotly_import_error = _e

sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils.theme import apply_dark_theme, render_card, render_intro

st.set_page_config(
    page_title="Dashboard - Oncologia Pediátrica",
    page_icon="🧒",
    layout="wide"
)

apply_dark_theme()

st.title("Dashboard - Oncologia Pediátrica")

render_intro(
    "Painel de acompanhamento de casos pediátricos oncológicos, com foco em diagnósticos, evolução anual "
    "e distribuição hospitalar para o MVP."
)

uploaded_file = st.file_uploader(
    "Envie um arquivo CSV com dados de oncologia pediátrica",
    type=["csv"]
)

default_data_path = Path(__file__).resolve().parents[1] / "data" / "oncoped.csv"

if uploaded_file is None:
    if default_data_path.exists():
        st.success("Carregando dados reais de Oncologia Pediátrica.")
        df = pd.read_csv(default_data_path)
    else:
        st.warning("Base local não encontrada. Usando dados de exemplo.")
        df = pd.DataFrame({
            "Estado": ["SP", "RJ", "MG", "BA"],
            "Ano": [2024, 2024, 2024, 2024],
            "Hospital": [
                "Hospital das Clínicas",
                "INCA",
                "Hospital da Baleia",
                "Hospital Martagão Gesteira",
            ],
            "Tipo": [
                "Leucemia",
                "Linfoma",
                "Neuroblastoma",
                "Sarcoma Ósseo",
            ],
            "Sexo": ["M", "F", "M", "F"],
            "Faixa_Etaria": ["0-4", "10-14", "0-4", "15-19"],
            "Casos": [33, 20, 16, 13],
        })
else:
    df = pd.read_csv(uploaded_file)

if "Tipo" not in df.columns or "Casos" not in df.columns:
    st.error("O arquivo precisa conter ao menos as colunas 'Tipo' e 'Casos'.")
    st.stop()

st.sidebar.header("🔎 Filtros")

ano = st.sidebar.multiselect(
    "Ano",
    options=df["Ano"].dropna().unique(),
    default=df["Ano"].dropna().unique(),
)

estado = st.sidebar.multiselect(
    "Estado",
    options=df["Estado"].dropna().unique(),
    default=df["Estado"].dropna().unique(),
)

hospital = st.sidebar.multiselect(
    "Hospital",
    options=df["Hospital"].dropna().unique(),
    default=df["Hospital"].dropna().unique(),
)

if "Faixa_Etaria" in df.columns:
    faixa = st.sidebar.multiselect(
        "Faixa Etária",
        options=df["Faixa_Etaria"].dropna().unique(),
        default=df["Faixa_Etaria"].dropna().unique(),
    )
else:
    faixa = df["Tipo"].dropna().unique()

filters = [
    df["Ano"].isin(ano),
    df["Estado"].isin(estado),
    df["Hospital"].isin(hospital),
]
if "Faixa_Etaria" in df.columns:
    filters.append(df["Faixa_Etaria"].isin(faixa))

df_filtrado = df.loc[pd.concat(filters, axis=1).all(axis=1)]

st.subheader("📌 Indicadores")

col1, col2, col3, col4 = st.columns(4)

total_casos = int(df_filtrado["Casos"].sum()) if not df_filtrado.empty else 0

if not df_filtrado.empty:
    principal_tipo = df_filtrado.groupby("Tipo", as_index=False)["Casos"].sum().sort_values("Casos", ascending=False).iloc[0]
    hospitais_distintos = df_filtrado["Hospital"].nunique()
    estados_distintos = df_filtrado["Estado"].nunique()
else:
    principal_tipo = pd.Series({"Tipo": "—", "Casos": 0})
    hospitais_distintos = 0
    estados_distintos = 0

with col1:
    render_card("Casos", f"{total_casos}", "Total de casos no recorte atual.", "cyan")
with col2:
    render_card(
        "Maior diagnóstico",
        principal_tipo["Tipo"],
        f"{int(principal_tipo['Casos'])} casos no conjunto filtrado.",
        "blue",
    )
with col3:
    render_card("Hospitais", f"{hospitais_distintos}", "Serviços diferentes no recorte.", "rose")
with col4:
    render_card("Estados", f"{estados_distintos}", "UFs presentes no filtro.", "amber")

st.divider()

st.subheader("📊 Distribuição por Tipo de Diagnóstico")
if px is None:
    st.error(
        "A biblioteca `plotly` não está disponível neste ambiente. Instale `plotly` ou atualize `requirements.txt` e redeploy. Os gráficos interativos não serão mostrados."
    )
else:
    fig = px.pie(
        df_filtrado.groupby("Tipo", as_index=False)["Casos"].sum(),
        names="Tipo",
        values="Casos",
        hole=0.46,
        color_discrete_sequence=["#2dd4bf", "#60a5fa", "#fb7185", "#fbbf24", "#a78bfa", "#22c55e"],
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e5edf7",
        legend_title_text="Tipo",
    )
    st.plotly_chart(fig, width="stretch")

st.subheader("📈 Evolução anual")
if px is None:
    st.info("Gráficos de evolução não estão disponíveis sem `plotly`.")
else:
    fig2 = px.bar(
        df_filtrado.groupby(["Ano", "Tipo"], as_index=False)["Casos"].sum(),
        x="Ano",
        y="Casos",
        color="Tipo",
        barmode="group",
        color_discrete_sequence=["#2dd4bf", "#60a5fa", "#fb7185", "#fbbf24", "#a78bfa", "#22c55e"],
    )
    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e5edf7",
        legend_title_text="Tipo",
        xaxis_title="Ano",
        yaxis_title="Casos",
    )
    st.plotly_chart(fig2, width="stretch")

st.subheader("📋 Tabela de casos")
st.dataframe(df_filtrado.reset_index(drop=True), width="stretch")
