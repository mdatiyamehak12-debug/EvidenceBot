"""
EvidenceBot - Enterprise Bio-Intelligence UI Components & Design System
========================================================================
Design architecture inspired by cutting-edge industrial AI and deeptech aesthetics (Mind Robotics style),
specifically translated and tailored for computational biology, dense literature retrieval, and empirical clinical verification.
Zero informal emojis; features CentraNo2/Plus Jakarta Sans geometric typography, subtle live motion telemetry, and obsidian/petroleum glassmorphism.
"""

import streamlit as st
from typing import List, Optional, Any, Dict
from utils.helpers import format_author_list, format_pubmed_url

# =====================================================================
# Design System: Deeptech Bio-Intelligence Aesthetic (Mind Robotics inspired)
# =====================================================================

CORE_THEME_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    /* Global Typography - Geometric Grotesque (CentraNo2 / Plus Jakarta Sans) */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        letter-spacing: -0.02em;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3.5rem;
        max-width: 1220px;
    }

    /* Live Telemetry Pulse Animation */
    @keyframes live-radar {
        0% {
            transform: scale(0.92);
            box-shadow: 0 0 0 0 rgba(14, 165, 233, 0.7);
        }
        70% {
            transform: scale(1.06);
            box-shadow: 0 0 0 8px rgba(14, 165, 233, 0);
        }
        100% {
            transform: scale(0.92);
            box-shadow: 0 0 0 0 rgba(14, 165, 233, 0);
        }
    }

    @keyframes green-radar {
        0% {
            transform: scale(0.92);
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
        }
        70% {
            transform: scale(1.06);
            box-shadow: 0 0 0 8px rgba(16, 185, 129, 0);
        }
        100% {
            transform: scale(0.92);
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
        }
    }

    .live-dot-cyan {
        display: inline-block;
        width: 7px;
        height: 7px;
        background-color: #0ea5e9;
        border-radius: 50%;
        margin-right: 8px;
        animation: live-radar 2.2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        vertical-align: middle;
    }

    .live-dot-green {
        display: inline-block;
        width: 7px;
        height: 7px;
        background-color: #10b981;
        border-radius: 50%;
        margin-right: 8px;
        animation: green-radar 2.2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        vertical-align: middle;
    }

    /* Status Indicator Dots */
    .status-dot {
        display: inline-block;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        margin-right: 6px;
        vertical-align: middle;
    }
    .status-dot-green { background-color: #10b981; }
    .status-dot-amber { background-color: #f59e0b; }
    .status-dot-rose  { background-color: #f43f5e; }
    .status-dot-cyan  { background-color: #06b6d4; }
    .status-dot-slate { background-color: #64748b; }

    /* Technical Telemetry Monospace Tags */
    .mono-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        padding: 3px 8px;
        border-radius: 4px;
        display: inline-flex;
        align-items: center;
        text-transform: uppercase;
    }

    /* Primary Action Buttons */
    button[kind="primary"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        letter-spacing: -0.01em !important;
        border-radius: 6px !important;
        padding: 0.55rem 1.25rem !important;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    button[kind="primary"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 20px -3px rgba(14, 165, 233, 0.35) !important;
    }
</style>
"""

# Obsidian & Deep Petroleum Theme (Default Mind Robotics Dark Tech Style)
DARK_THEME_CSS = CORE_THEME_CSS + """
<style>
    body, [class*="css"] {
        color: #e2e8f0;
        background-color: #06090e;
    }

    /* Mind Robotics Style Hero Header */
    .hero-container {
        background: radial-gradient(circle at 85% 20%, rgba(14, 165, 233, 0.15) 0%, transparent 60%),
                    linear-gradient(180deg, #090e17 0%, #06090e 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 36px 40px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    .hero-container h1 {
        color: #ffffff !important;
        font-weight: 800;
        margin: 0;
        font-size: 2.35rem;
        letter-spacing: -0.04em;
        line-height: 1.1;
    }
    .hero-container p {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-top: 10px;
        margin-bottom: 0;
        font-weight: 400;
        max-width: 820px;
        line-height: 1.6;
    }
    .telemetry-chip {
        background: rgba(14, 165, 233, 0.08);
        border: 1px solid rgba(14, 165, 233, 0.22);
        color: #38bdf8;
        border-radius: 9999px;
        padding: 5px 14px;
        font-size: 0.74rem;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
    }

    /* Telemetry Metric Cards */
    .stat-tile {
        background: #090e17;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        padding: 18px 22px;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .stat-tile:hover {
        border-color: rgba(14, 165, 233, 0.4);
        transform: translateY(-2px);
        box-shadow: 0 10px 24px -6px rgba(14, 165, 233, 0.12);
    }
    .stat-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.70rem;
        text-transform: uppercase;
        color: #64748b;
        letter-spacing: 0.08em;
        font-weight: 600;
    }
    .stat-value {
        font-size: 1.4rem;
        font-weight: 800;
        color: #ffffff;
        margin-top: 4px;
        letter-spacing: -0.03em;
    }
    .stat-subtext {
        font-size: 0.78rem;
        color: #0284c7;
        margin-top: 2px;
    }

    /* Publication & Grounding Cards */
    .bio-card {
        background-color: #090e17;
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 8px;
        padding: 22px 24px;
        margin-bottom: 14px;
        color: #e2e8f0;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .bio-card:hover {
        border-color: rgba(14, 165, 233, 0.4);
        transform: translateY(-2px);
        box-shadow: 0 12px 28px -6px rgba(0, 0, 0, 0.4);
    }

    /* Architecture Module Cards */
    .feature-card {
        background-color: #090e17;
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 8px;
        padding: 22px;
        height: 100%;
        border-top: 2px solid #0ea5e9;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .feature-card:hover {
        border-color: #0ea5e9;
        transform: translateY(-2px);
        box-shadow: 0 12px 24px -4px rgba(14, 165, 233, 0.1);
    }
    .feature-title {
        color: #ffffff;
        font-size: 0.98rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin-bottom: 6px;
    }
    .feature-desc {
        color: #94a3b8;
        font-size: 0.88rem;
        line-height: 1.55;
    }

    /* Badges */
    .badge-pill {
        display: inline-flex;
        align-items: center;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 0.72rem;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 6px;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        font-family: 'JetBrains Mono', monospace;
    }
    .badge-high {
        background-color: rgba(16, 185, 129, 0.1);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .badge-moderate {
        background-color: rgba(245, 158, 11, 0.1);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    .badge-prelim {
        background-color: rgba(14, 165, 233, 0.1);
        color: #38bdf8;
        border: 1px solid rgba(14, 165, 233, 0.3);
    }
    .badge-insufficient {
        background-color: rgba(244, 63, 94, 0.1);
        color: #fb7185;
        border: 1px solid rgba(244, 63, 94, 0.3);
    }
    .badge-cyan {
        background-color: rgba(6, 182, 212, 0.1);
        color: #22d3ee;
        border: 1px solid rgba(6, 182, 212, 0.3);
    }

    .mono-tag {
        background: #111827;
        color: #94a3b8;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Answer Container */
    .answer-box {
        background-color: #090e17;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-left: 3px solid #0ea5e9;
        border-radius: 8px;
        padding: 26px 30px;
        margin: 18px 0;
        line-height: 1.7;
        font-size: 0.95rem;
        color: #e2e8f0;
    }
    .answer-box h3 {
        color: #ffffff !important;
        font-size: 1.05rem !important;
        letter-spacing: -0.02em;
        margin-top: 18px !important;
        margin-bottom: 8px !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        padding-bottom: 6px;
    }
    .answer-box h3:first-child {
        margin-top: 0 !important;
    }

    /* Abstention Box */
    .abstention-box {
        background-color: #17090c;
        border: 1px solid rgba(244, 63, 94, 0.3);
        border-left: 3px solid #f43f5e;
        border-radius: 8px;
        padding: 22px 26px;
        color: #fecdd3;
        font-size: 0.94rem;
        line-height: 1.65;
    }

    /* PubMed Outbound Link */
    .pubmed-link-btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background-color: #06090e;
        color: #38bdf8 !important;
        font-weight: 600;
        font-size: 0.82rem;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.02em;
        padding: 6px 12px;
        border-radius: 4px;
        border: 1px solid rgba(14, 165, 233, 0.3);
        text-decoration: none !important;
        transition: all 0.2s ease;
    }
    .pubmed-link-btn:hover {
        background-color: rgba(14, 165, 233, 0.12);
        border-color: #0ea5e9;
        color: #7dd3fc !important;
    }

    .disclaimer-card {
        background-color: #090e17;
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 6px;
        padding: 14px 18px;
        font-size: 0.80rem;
        color: #64748b;
        margin-top: 32px;
        line-height: 1.55;
    }
</style>
"""

# Clean Studio Light Theme
LIGHT_THEME_CSS = CORE_THEME_CSS + """
<style>
    body, [class*="css"] {
        color: #0f172a;
        background-color: #ffffff;
    }

    .hero-container {
        background: linear-gradient(135deg, #090e17 0%, #0e1e38 55%, #0369a1 100%);
        border-radius: 12px;
        padding: 36px 40px;
        color: #ffffff;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px -10px rgba(9, 14, 23, 0.2);
    }
    .hero-container h1 {
        color: #ffffff !important;
        font-weight: 800;
        margin: 0;
        font-size: 2.35rem;
        letter-spacing: -0.04em;
        line-height: 1.1;
    }
    .hero-container p {
        color: #cbd5e1;
        font-size: 1.05rem;
        margin-top: 10px;
        margin-bottom: 0;
        font-weight: 400;
        max-width: 820px;
        line-height: 1.6;
    }
    .telemetry-chip {
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.25);
        color: #f0f9ff;
        border-radius: 9999px;
        padding: 5px 14px;
        font-size: 0.74rem;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
    }

    .stat-tile {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 18px 22px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .stat-tile:hover {
        border-color: #0284c7;
        transform: translateY(-2px);
        box-shadow: 0 10px 20px -6px rgba(2, 132, 199, 0.1);
    }
    .stat-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.70rem;
        text-transform: uppercase;
        color: #64748b;
        letter-spacing: 0.08em;
        font-weight: 600;
    }
    .stat-value {
        font-size: 1.4rem;
        font-weight: 800;
        color: #0f172a;
        margin-top: 4px;
        letter-spacing: -0.03em;
    }
    .stat-subtext {
        font-size: 0.78rem;
        color: #0284c7;
        margin-top: 2px;
    }

    .bio-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 22px 24px;
        margin-bottom: 14px;
        box-shadow: 0 1px 3px 0 rgba(15, 23, 42, 0.03);
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .bio-card:hover {
        border-color: #0284c7;
        transform: translateY(-2px);
        box-shadow: 0 10px 24px -6px rgba(2, 132, 199, 0.08);
    }

    .feature-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 22px;
        height: 100%;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        border-top: 2px solid #0284c7;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .feature-card:hover {
        border-color: #0284c7;
        transform: translateY(-2px);
        box-shadow: 0 10px 20px -4px rgba(15, 23, 42, 0.06);
    }
    .feature-title {
        font-size: 0.98rem;
        font-weight: 700;
        color: #0f172a;
        letter-spacing: -0.02em;
        margin-bottom: 6px;
    }
    .feature-desc {
        font-size: 0.88rem;
        color: #64748b;
        line-height: 1.55;
    }

    .badge-pill {
        display: inline-flex;
        align-items: center;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 0.72rem;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 6px;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        font-family: 'JetBrains Mono', monospace;
    }
    .badge-high {
        background-color: #ecfdf5;
        color: #047857;
        border: 1px solid #a7f3d0;
    }
    .badge-moderate {
        background-color: #fffbeb;
        color: #b45309;
        border: 1px solid #fde68a;
    }
    .badge-prelim {
        background-color: #f0f9ff;
        color: #0284c7;
        border: 1px solid #bae6fd;
    }
    .badge-insufficient {
        background-color: #fef2f2;
        color: #b91c1c;
        border: 1px solid #fecaca;
    }
    .badge-cyan {
        background-color: #f0fdfa;
        color: #0f766e;
        border: 1px solid #ccfbf1;
    }

    .mono-tag {
        background: #f8fafc;
        color: #475569;
        border: 1px solid #e2e8f0;
    }

    .answer-box {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 3px solid #0284c7;
        border-radius: 8px;
        padding: 26px 30px;
        margin: 18px 0;
        line-height: 1.7;
        font-size: 0.95rem;
        color: #1e293b;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
    }
    .answer-box h3 {
        color: #0f172a !important;
        font-size: 1.05rem !important;
        letter-spacing: -0.02em;
        margin-top: 18px !important;
        margin-bottom: 8px !important;
        border-bottom: 1px solid #f1f5f9;
        padding-bottom: 6px;
    }
    .answer-box h3:first-child {
        margin-top: 0 !important;
    }

    .abstention-box {
        background-color: #fff1f2;
        border: 1px solid #fecdd3;
        border-left: 3px solid #e11d48;
        border-radius: 8px;
        padding: 22px 26px;
        color: #881337;
        font-size: 0.94rem;
        line-height: 1.65;
    }

    .pubmed-link-btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background-color: #f8fafc;
        color: #0284c7 !important;
        font-weight: 600;
        font-size: 0.82rem;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.02em;
        padding: 6px 12px;
        border-radius: 4px;
        border: 1px solid #cbd5e1;
        text-decoration: none !important;
        transition: all 0.2s ease;
    }
    .pubmed-link-btn:hover {
        background-color: #e0f2fe;
        border-color: #7dd3fc;
        color: #0369a1 !important;
    }

    .disclaimer-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 14px 18px;
        font-size: 0.80rem;
        color: #64748b;
        margin-top: 32px;
        line-height: 1.55;
    }
</style>
"""


def apply_theme():
    """Applies theme. Defaults to Dark mode (Mind Robotics style) or user choice."""
    theme = st.session_state.get("theme_choice", "Dark")
    if theme == "Light":
        st.markdown(LIGHT_THEME_CSS, unsafe_allow_html=True)
    else:
        st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)


def render_sidebar(current_page: str = "Home"):
    """
    Renders professional enterprise sidebar with minimalist typography and zero casual emojis.
    """
    with st.sidebar:
        # Header Brand
        col_img, col_txt = st.columns([1, 3])
        with col_img:
            st.image("assets/logo.png", width=42)
        with col_txt:
            st.markdown(
                '<div style="font-weight:800; font-size:1.15rem; color:#f8fafc; line-height:1.15; letter-spacing:-0.035em;">EvidenceBot</div>'
                '<div style="font-size:0.68rem; color:#38bdf8; font-weight:700; letter-spacing:0.08em; font-family:\'JetBrains Mono\', monospace;">BIO-INTELLIGENCE ENGINE</div>',
                unsafe_allow_html=True
            )

        st.markdown("<div style='margin-bottom: 14px;'></div>", unsafe_allow_html=True)
        st.caption("PLATFORM MODULES")

        # Official Navigation (Clean Minimalist Labels)
        st.page_link("app.py", label="Discovery & Search")
        st.page_link("pages/1_Ask_EvidenceBot.py", label="Evidence Synthesis")
        st.page_link("pages/2_Research_Papers.py", label="Literature Explorer")
        st.page_link("pages/3_Evidence_Analysis.py", label="Grounding & Audit")
        st.page_link("pages/4_About.py", label="Architecture & Methodology")

        st.markdown("---")

        # System Telemetry Status (Mind Robotics Live Telemetry Style)
        st.caption("SYSTEM STATUS")
        st.markdown(
            """
            <div style="font-size:0.76rem; color:#94a3b8; margin-bottom:12px; line-height:1.7;">
                <div><span class="live-dot-green"></span><strong>NCBI Entrez Gateway:</strong> ONLINE</div>
                <div><span class="live-dot-cyan"></span><strong>FAISS Dense Index:</strong> SYNCHRONIZED</div>
                <div><span class="status-dot status-dot-slate"></span><strong>Inference Engine:</strong> GEMINI 2.5 FLASH</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption("INTERFACE THEME")
        theme_options = ["Dark", "Light"]
        current_theme = st.session_state.get("theme_choice", "Dark")
        selected_theme = st.radio(
            "Interface Mode",
            options=theme_options,
            index=theme_options.index(current_theme),
            horizontal=True,
            label_visibility="collapsed"
        )
        if selected_theme != current_theme:
            st.session_state["theme_choice"] = selected_theme
            st.rerun()

        st.markdown("---")
        st.markdown(
            """
            <div style="font-size:0.72rem; color:#64748b; line-height:1.5; font-family:'JetBrains Mono', monospace;">
                CORPUS: NCBI PUBMED<br>
                BUILD: v1.0.0 PRODUCTION
            </div>
            """,
            unsafe_allow_html=True
        )


def render_confidence_badge(confidence: str, similarity_score: Optional[float] = None) -> str:
    """Generates styled badge for confidence classification with zero emojis."""
    score_str = f" • SIM: {similarity_score:.2f}" if similarity_score is not None else ""
    if confidence == "High":
        return f'<span class="badge-pill badge-high"><span class="status-dot status-dot-green"></span>STRONG EVIDENCE{score_str}</span>'
    elif confidence == "Moderate":
        return f'<span class="badge-pill badge-moderate"><span class="status-dot status-dot-amber"></span>MODERATE EVIDENCE{score_str}</span>'
    elif confidence == "Preliminary":
        return f'<span class="badge-pill badge-prelim"><span class="status-dot status-dot-cyan"></span>PRELIMINARY LITERATURE{score_str}</span>'
    else:
        return f'<span class="badge-pill badge-insufficient"><span class="status-dot status-dot-rose"></span>INSUFFICIENT EVIDENCE{score_str}</span>'


def render_claim_status_badge(status: str) -> str:
    """Renders styled badge for evidence verification status with zero emojis."""
    status_upper = status.upper()
    if status_upper == "SUPPORTED":
        return '<span class="badge-pill badge-high"><span class="status-dot status-dot-green"></span>EMPIRICALLY SUPPORTED</span>'
    elif status_upper == "PARTIALLY_SUPPORTED":
        return '<span class="badge-pill badge-moderate"><span class="status-dot status-dot-amber"></span>PARTIALLY SUPPORTED</span>'
    elif status_upper == "CONTRADICTED":
        return '<span class="badge-pill badge-insufficient"><span class="status-dot status-dot-rose"></span>CONFLICTING FINDINGS</span>'
    elif status_upper == "UNCERTAIN_HUMAN_REVIEW":
        return '<span class="badge-pill badge-cyan"><span class="status-dot status-dot-cyan"></span>EXPERT REVIEW REQUIRED</span>'
    else:
        return '<span class="badge-pill badge-insufficient"><span class="status-dot status-dot-slate"></span>INSUFFICIENT DATA</span>'


def render_paper_card(paper: Any, is_cited: bool = False, chunk_score: Optional[float] = None):
    """
    Renders clean research publication card with verified links and metadata.
    """
    if isinstance(paper, dict):
        pmid = paper.get("pmid", "")
        title = paper.get("title", "Untitled Publication")
        journal = paper.get("journal", "Unknown Journal")
        year = paper.get("year", "N/A")
        authors = paper.get("authors", [])
        doi = paper.get("doi")
        url = paper.get("url") or format_pubmed_url(pmid)
        abstract = paper.get("abstract", "")
        has_abstract = bool(abstract and "no abstract" not in abstract.lower())
    else:
        pmid = paper.pmid
        title = paper.title
        journal = paper.journal
        year = paper.year
        authors = paper.authors
        doi = paper.doi
        url = paper.url
        abstract = paper.abstract
        has_abstract = getattr(paper, "has_abstract", bool(abstract and "no abstract" not in abstract.lower()))

    cited_badge = '<span class="badge-pill badge-high"><span class="status-dot status-dot-green"></span>CITED IN SYNTHESIS</span>' if is_cited else '<span class="badge-pill badge-prelim"><span class="status-dot status-dot-cyan"></span>INDEXED RECORD</span>'
    score_badge = f'<span class="badge-pill badge-moderate">SIM: {chunk_score:.2f}</span>' if chunk_score is not None else ""
    abstract_status = (
        '<span class="badge-pill badge-cyan">FULL ABSTRACT</span>'
        if has_abstract
        else '<span class="badge-pill badge-insufficient">TITLE RECORD</span>'
    )

    authors_formatted = format_author_list(authors, 3)
    doi_formatted = f" &bull; <strong>DOI:</strong> {doi}" if doi else ""

    st.markdown(
        f"""
        <div class="bio-card">
            <div style="font-weight:700; font-size:1.02rem; color:#f8fafc; margin-bottom:6px; line-height:1.4; letter-spacing:-0.02em;">
                {title}
            </div>
            <div style="font-size:0.84rem; color:#94a3b8; margin-bottom:12px;">
                <strong>Journal:</strong> {journal} ({year}) &bull; 
                <strong>Authors:</strong> {authors_formatted}
                {doi_formatted}
            </div>
            <div style="margin-bottom:12px;">
                {cited_badge}
                {score_badge}
                {abstract_status}
                <span class="mono-tag">PMID {pmid}</span>
            </div>
            <a href="{url}" target="_blank" class="pubmed-link-btn">
                PUBMED RECORD &bull; PMID {pmid} &rarr;
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

    if has_abstract:
        with st.expander(f"Abstract Preview (PMID: {pmid})", expanded=False):
            st.markdown(f"<div style='font-size:0.90rem; line-height:1.65; color:#cbd5e1;'>{abstract}</div>", unsafe_allow_html=True)


def render_disclaimer():
    """Renders professional non-clinical institutional disclaimer with zero emojis."""
    st.markdown(
        """
        <div class="disclaimer-card">
            <strong>INSTITUTIONAL RESEARCH NOTICE:</strong> EvidenceBot is an empirical biomedical intelligence platform 
            engineered to index, synthesize, and verify peer-reviewed scientific literature indexed on the National Library of Medicine (NCBI PubMed). 
            It is designed strictly for scientific discovery, literature review, and educational use and does <strong>not</strong> constitute medical advice, 
            clinical diagnosis, or treatment recommendations. Always consult a licensed clinical specialist for patient care decisions.
        </div>
        """,
        unsafe_allow_html=True
    )
