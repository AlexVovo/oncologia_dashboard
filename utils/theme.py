import html

import streamlit as st


def apply_dark_theme() -> None:
    st.markdown(
        """
        <style>
            :root {
                --bg: #0b1020;
                --surface: #121a2e;
                --surface-2: #172238;
                --border: rgba(148, 163, 184, 0.20);
                --text: #e5edf7;
                --muted: #93a4b8;
                --cyan: #2dd4bf;
                --blue: #60a5fa;
                --rose: #fb7185;
                --amber: #fbbf24;
            }

            .stApp {
                background:
                    radial-gradient(circle at 15% 0%, rgba(45, 212, 191, 0.10), transparent 28rem),
                    linear-gradient(145deg, #070b16 0%, var(--bg) 44%, #101827 100%);
                color: var(--text);
            }

            [data-testid="stSidebar"] {
                background: rgba(12, 18, 32, 0.96);
                border-right: 1px solid var(--border);
            }

            [data-testid="stSidebar"] * {
                color: var(--text);
            }

            h1, h2, h3 {
                color: var(--text);
                letter-spacing: 0;
            }

            p, li, label, span {
                color: var(--text);
            }

            .block-container {
                padding-top: 2.1rem;
                padding-bottom: 3rem;
                max-width: 1220px;
            }

            div[data-testid="stMetric"],
            div[data-testid="stDataFrame"],
            div[data-testid="stPlotlyChart"] {
                background: rgba(18, 26, 46, 0.78);
                border: 1px solid var(--border);
                border-radius: 8px;
                padding: 1rem;
                box-shadow: 0 18px 48px rgba(0, 0, 0, 0.24);
            }

            div[data-testid="stMetric"] label,
            div[data-testid="stMetric"] [data-testid="stMetricValue"] {
                color: var(--text);
            }

            div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
                color: var(--cyan);
            }

            .modern-card {
                min-height: 138px;
                background: linear-gradient(155deg, rgba(23, 34, 56, 0.94), rgba(14, 21, 36, 0.96));
                border: 1px solid var(--border);
                border-radius: 8px;
                padding: 1rem;
                box-shadow: 0 18px 48px rgba(0, 0, 0, 0.26);
            }

            .modern-card__kicker {
                color: var(--muted);
                font-size: 0.78rem;
                font-weight: 700;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                margin-bottom: 0.35rem;
            }

            .modern-card__value {
                color: var(--text);
                font-size: clamp(1.35rem, 2vw, 2rem);
                font-weight: 800;
                line-height: 1.1;
                margin-bottom: 0.6rem;
            }

            .modern-card__body {
                color: var(--muted);
                font-size: 0.92rem;
                line-height: 1.45;
            }

            .accent-cyan { border-top: 3px solid var(--cyan); }
            .accent-blue { border-top: 3px solid var(--blue); }
            .accent-rose { border-top: 3px solid var(--rose); }
            .accent-amber { border-top: 3px solid var(--amber); }

            .hero-panel {
                background: rgba(14, 23, 44, 0.88);
                border: 1px solid rgba(148, 163, 184, 0.14);
                border-radius: 16px;
                padding: 1.4rem 1.5rem;
                margin: 0.75rem 0 1.25rem;
                box-shadow: 0 28px 70px rgba(0, 0, 0, 0.20);
                backdrop-filter: blur(10px);
                overflow: hidden;
            }

            .hero-panel.hero-home {
                position: relative;
                background: linear-gradient(135deg, rgba(11, 24, 46, 0.98), rgba(20, 35, 59, 0.92));
                border: 1px solid rgba(96, 165, 250, 0.22);
                box-shadow: 0 36px 100px rgba(45, 212, 191, 0.12);
            }

            .hero-panel.hero-home::before {
                content: "";
                position: absolute;
                top: -1.2rem;
                right: -1.1rem;
                width: 16rem;
                height: 16rem;
                background: radial-gradient(circle, rgba(96, 165, 250, 0.18), transparent 58%);
                pointer-events: none;
            }

            .hero-panel.hero-home::after {
                content: "";
                position: absolute;
                bottom: -1.6rem;
                left: -1.6rem;
                width: 13rem;
                height: 13rem;
                background: radial-gradient(circle, rgba(251, 113, 133, 0.12), transparent 55%);
                pointer-events: none;
            }

            .hero-pill-grid {
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 0.75rem;
                margin-top: 1rem;
            }

            .hero-pill {
                background: rgba(14, 23, 44, 0.9);
                border: 1px solid rgba(148, 163, 184, 0.12);
                border-radius: 999px;
                color: var(--text);
                font-size: 0.85rem;
                font-weight: 700;
                padding: 0.65rem 0.95rem;
                text-align: center;
            }

            .summary-panel {
                display: grid;
                gap: 1rem;
            }

            .stats-card {
                background: linear-gradient(135deg, rgba(18, 26, 46, 0.96), rgba(14, 21, 36, 0.98));
                border: 1px solid rgba(148, 163, 184, 0.16);
                border-radius: 18px;
                padding: 1rem 1.1rem;
                box-shadow: 0 16px 40px rgba(0, 0, 0, 0.18);
            }

            .stat-title {
                color: var(--muted);
                font-size: 0.75rem;
                font-weight: 700;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                margin-bottom: 0.55rem;
            }

            .stat-value {
                color: var(--text);
                font-size: clamp(1.8rem, 2.5vw, 2.8rem);
                font-weight: 800;
                margin-bottom: 0.55rem;
            }

            .stat-note {
                color: var(--muted);
                font-size: 0.92rem;
                line-height: 1.5;
            }

            .section-panel {
                background: rgba(14, 23, 44, 0.88);
                border: 1px solid rgba(148, 163, 184, 0.14);
                border-radius: 18px;
                padding: 1.25rem;
                margin-bottom: 1rem;
                box-shadow: 0 18px 46px rgba(0, 0, 0, 0.18);
            }

            .section-panel h2 {
                margin-top: 0;
                margin-bottom: 0.75rem;
            }

            .section-panel p,
            .section-panel li {
                color: var(--muted);
            }

            .section-panel ul,
            .section-panel ol {
                margin-left: 1.2rem;
            }

            .hero-panel p,
            .hero-panel li {
                color: var(--text);
            }

            .hero-panel ul,
            .hero-panel ol {
                margin: 0.75rem 0 0 1rem;
                padding-left: 1rem;
                color: var(--muted);
            }

            .hero-panel li {
                margin-bottom: 0.45rem;
            }

            .hero-panel strong {
                color: #ffffff;
                font-size: 1rem;
            }

            .modern-card {
                min-height: 160px;
                background: linear-gradient(160deg, rgba(18, 26, 46, 0.92), rgba(11, 18, 32, 0.95));
                border: 1px solid rgba(148, 163, 184, 0.16);
                border-radius: 18px;
                padding: 1.25rem;
                box-shadow: 0 22px 42px rgba(0, 0, 0, 0.18);
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }

            .modern-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 26px 56px rgba(0, 0, 0, 0.22);
            }

            .card-link {
                display: block;
                text-decoration: none;
            }

            .card-link:hover .modern-card {
                transform: translateY(-2px) scale(1.01);
            }

            .modern-card__value {
                color: var(--text);
                font-size: clamp(1.5rem, 2vw, 2.25rem);
                font-weight: 800;
                line-height: 1.05;
                margin-bottom: 0.55rem;
            }

            .stAlert {
                background: rgba(23, 34, 56, 0.92);
                border: 1px solid var(--border);
                border-radius: 8px;
                color: var(--text);
            }

            iframe {
                border-radius: 8px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_card(title: str, value: str, body: str, accent: str = "cyan", href: str | None = None) -> None:
    safe_title = html.escape(title)
    safe_value = html.escape(value)
    safe_body = html.escape(body)
    safe_accent = accent if accent in {"cyan", "blue", "rose", "amber"} else "cyan"

    link_open = f'<a class="card-link" href="{html.escape(href, quote=True)}">' if href else ""
    link_close = "</a>" if href else ""

    st.markdown(
        f"""
        {link_open}
        <div class="modern-card accent-{safe_accent}">
            <div class="modern-card__kicker">{safe_title}</div>
            <div class="modern-card__value">{safe_value}</div>
            <div class="modern-card__body">{safe_body}</div>
        </div>
        {link_close}
        """,
        unsafe_allow_html=True,
    )


def render_intro(text: str) -> None:
    st.markdown(f'<div class="hero-panel"><p>{html.escape(text)}</p></div>', unsafe_allow_html=True)
