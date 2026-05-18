import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils.theme import apply_dark_theme, render_card, render_intro

st.set_page_config(
    page_title="Protocolos Clínicos",
    page_icon="🧾",
    layout="wide"
)

apply_dark_theme()

st.title("Protocolos Clínicos")

render_intro(
    "Central de protocolos, fluxos e critérios de cuidado para oncologia, com foco em coesão assistencial e monitoramento."
)

default_data_path = Path(__file__).resolve().parents[1] / "data" / "protocolos.csv"

if default_data_path.exists():
    df = pd.read_csv(default_data_path)
    st.success("Carregando protocolos clínicos reais.")
else:
    st.warning("Arquivo de protocolos não encontrado. Usando dados de exemplo.")
    df = pd.DataFrame({
        "Linha_de_Cuidado": [
            "Colo do útero",
            "Colo do útero",
            "Oncologia Pediátrica",
        ],
        "Etapa": [
            "Rastreamento",
            "Diagnóstico",
            "Avaliação inicial",
        ],
        "Objetivo": [
            "Detecção precoce",
            "Confirmação histológica",
            "Triagem multidisciplinar",
        ],
        "Descricao": [
            "Citologia oncótica a cada 3 anos para mulheres de 25 a 64 anos.",
            "Biópsia ou colposcopia em lesões suspeitas de alto grau.",
            "Encaminhamento interdisciplinar para suspeita de câncer pediátrico.",
        ],
        "Referencia": [
            "Ministério da Saúde",
            "INCA",
            "SBOT",
        ],
    })

protocolos_disponiveis = df["Linha_de_Cuidado"].dropna().unique().tolist()
linha_selecionada = st.sidebar.selectbox(
    "Linha de cuidado",
    options=protocolos_disponiveis,
    index=0 if protocolos_disponiveis else -1,
)

st.sidebar.markdown("---")

if "Ano" in df.columns:
    anos = df["Ano"].dropna().unique().tolist()
    if anos:
        ano_selecionado = st.sidebar.selectbox("Ano", options=anos, index=0)
    else:
        ano_selecionado = None
else:
    ano_selecionado = None

if linha_selecionada:
    df_filtrado = df[df["Linha_de_Cuidado"] == linha_selecionada]
else:
    df_filtrado = df.copy()

if ano_selecionado is not None and "Ano" in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado["Ano"] == ano_selecionado]

total_protocolos = len(df_filtrado)
linhas_unicas = df["Linha_de_Cuidado"].nunique()
referencias_unicas = df["Referencia"].nunique()

col1, col2, col3 = st.columns(3)
with col1:
    render_card("Protocolos", f"{total_protocolos}", "Itens carregados no recorte atual.", "cyan")
with col2:
    render_card("Linhas", f"{linhas_unicas}", "Linhas de cuidado cadastradas.", "blue")
with col3:
    render_card("Fontes", f"{referencias_unicas}", "Referências técnicas utilizadas.", "amber")

st.divider()

st.subheader("📋 Protocolos por etapa")

for _, row in df_filtrado.iterrows():
    with st.expander(f"{row['Etapa']} — {row['Objetivo']}"):
        st.markdown(f"**Linha de cuidado:** {row['Linha_de_Cuidado']}")
        st.markdown(f"**Descrição:** {row['Descricao']}")
        st.markdown(f"**Referência:** {row['Referencia']}")
        if "Ano" in row and not pd.isna(row.get("Ano")):
            st.markdown(f"**Ano:** {int(row['Ano'])}")

st.divider()

st.subheader("📌 Observações de implementação")
st.markdown(
    """
    - Integre os protocolos aos fluxos assistenciais para obedecer triagem e tratamentos.
    - Mantenha critérios de elegibilidade atualizados conforme diretrizes nacionais.
    - Use este módulo como base para consolidar documentos e checklists.
    """,
)
