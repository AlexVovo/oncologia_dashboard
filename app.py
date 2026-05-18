import streamlit as st
from utils.theme import apply_dark_theme, render_card

st.set_page_config(
    page_title="Painel Oncológico Integrado",
    page_icon="🎗️",
    layout="wide"
)

apply_dark_theme()

st.title("Painel Oncológico Integrado")

st.sidebar.header("Fontes de dados")
st.sidebar.markdown(
    """
    - [DATASUS](https://datasus.saude.gov.br) — bases de vigilância e atenção hospitalar.
    - [INCA](https://www.gov.br/inca/pt-br) — diretrizes, publicações e programas de controle do câncer.
    - [Controle do Câncer](https://www.inca.gov.br/controle-do-cancer) — informações sobre o Registro Hospitalar de Câncer (RHC).

    Acesse os painéis pelo menu lateral de páginas do Streamlit.
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-panel hero-home">
        <p><strong>Panorama integrado de oncologia clínica e epidemiológica.</strong></p>
        <p>Dashboard de apoio à gestão com indicadores e recursos para as áreas de colo do útero, pediatria e protocolos clínicos.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([2, 1])

with left:
    st.markdown(
        """
        <div class="section-panel">
            <h2>O que você encontrará aqui</h2>
            <ul>
                <li>Resumo dos principais painéis do MVP.</li>
                <li>Direcionamento para prioridades assistenciais.</li>
                <li>Detalhes para acompanhamento de oncologia pediátrica e colo do útero.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-panel">
            <h2>Por que este dashboard?</h2>
            <p>Para levar dados reais à operação com uma leitura rápida de resultados, ações e próximas etapas.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    st.markdown(
        """
        <div class="summary-panel">
            <div class="stats-card">
                <div class="stat-title">Painéis</div>
                <div class="stat-value">3</div>
                <div class="stat-note">Colo do útero, pediatria e protocolos clínicos.</div>
            </div>
            <div class="stats-card">
                <div class="stat-title">Foco</div>
                <div class="stat-value">Assit + epi</div>
                <div class="stat-note">Conexão entre cuidado e vigilância.</div>
            </div>
            <div class="stats-card">
                <div class="stat-title">Status</div>
                <div class="stat-value">MVP</div>
                <div class="stat-note">Evolução contínua com dados reais.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

st.markdown(
    """
    <div class="section-panel">
        <h2>Recursos úteis</h2>
        <ul>
            <li><a href="https://datasus.saude.gov.br" target="_blank">DATASUS</a> — sistema do SUS para informações em saúde.</li>
            <li><a href="https://www.gov.br/inca/pt-br" target="_blank">INCA</a> — políticas, protocolos e publicações em oncologia.</li>
            <li><a href="https://www.inca.gov.br/controle-do-cancer" target="_blank">Controle do Câncer</a> — RHC, vigilância e registros hospitalares.</li>
            <li><a href="https://www.inca.gov.br/publicacoes" target="_blank">Publicações INCA</a> — manuais, boletins e guias técnicos.</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)
with col1:
    render_card(
        "Colo do útero",
        "Acesso direto",
        "Painel assistencial e epidemiológico com dados reais.",
        "rose",
        href="?page=Colo%20Utero",
    )
with col2:
    render_card(
        "Oncologia pediátrica",
        "Monitoramento swift",
        "Análise por diagnóstico, evolução e hospitalizações.",
        "cyan",
        href="?page=Oncoped",
    )
with col3:
    render_card(
        "Protocolos",
        "Consolidação clínica",
        "Fluxos e critérios para apoiar decisões assistenciais.",
        "amber",
        href="?page=Protocolos",
    )

st.divider()

st.markdown(
    """
    <div class="section-panel">
        <h2>Próximos passos</h2>
        <ol>
            <li>Explore o painel de Colo do Útero para análises de atenção e acesso.</li>
            <li>Consulte o painel Pediátrico para casos, diagnósticos e evolução anual.</li>
            <li>Use o módulo Protocolos para consolidar fluxos clínicos e referências.</li>
        </ol>
    </div>
    """,
    unsafe_allow_html=True,
)
