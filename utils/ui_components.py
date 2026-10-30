"""
EvidenceBot - Enterprise UI Components & Design System
======================================================
Production-grade visual architecture, typography, responsive card layouts,
and navigation for a high-performance biomedical research intelligence platform.
"""

import streamlit as st
from typing import List, Optional, Any, Dict
from utils.helpers import format_author_list, format_pubmed_url

# =====================================================================
# Production CSS: Modern Life Sciences & Biomedical Intelligence
# =====================================================================
LIGHT_THEME_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: #0f172a;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3.5rem;
        max-width: 1240px;
    }

    /* Enterprise Hero Banner */
    .top-banner {
        background: linear-gradient(135deg, #091e3a 0%, #0f3460 55%, #0284c7 100%);
        border-radius: 14px;
        padding: 30px 36px;
        color: #ffffff;
        margin-bottom: 28px;
        box-shadow: 0 10px 25px -5px rgba(9, 30, 58, 0.15), 0 8px 10px -6px rgba(9, 30, 58, 0.1);
        position: relative;
        overflow: hidden;
    }
    .top-banner h1 {
        color: #ffffff !important;
        font-weight: 800;
        margin: 0;
        font-size: 2.3rem;
        letter-spacing: -0.025em;
    }
    .top-banner p {
        color: #e0f2fe;
        font-size: 1.08rem;
        margin-top: 8px;
        margin-bottom: 0;
        font-weight: 400;
        max-width: 850px;
    }

    /* Premium Clean Cards */
    .bio-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 22px 26px;
        margin-bottom: 18px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px -1px rgba(0, 0, 0, 0.05);
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .bio-card:hover {
        box-shadow: 0 10px 20px -3px rgba(15, 23, 42, 0.08), 0 4px 6px -4px rgba(15, 23, 42, 0.04);
        border-color: #cbd5e1;
    }

    /* Feature Cards */
    .feature-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 24px;
        height: 100%;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        border-top: 4px solid #0284c7;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(15, 23, 42, 0.07);
    }
    .feature-icon {
        font-size: 1.7rem;
        margin-bottom: 12px;
        display: inline-block;
    }
    .feature-title {
        font-size: 1.12rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 8px;
        letter-spacing: -0.01em;
    }
    .feature-desc {
        font-size: 0.92rem;
        color: #64748b;
        line-height: 1.55;
    }

    /* Pill Badges */
    .badge-pill {
        display: inline-flex;
        align-items: center;
        padding: 5px 12px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 8px;
        margin-bottom: 6px;
        letter-spacing: 0.01em;
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
        background-color: #f0fdf4;
        color: #0f766e;
        border: 1px solid #ccfbf1;
    }

    /* Answer Container */
    .answer-box {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 5px solid #0284c7;
        border-radius: 12px;
        padding: 26px 30px;
        margin: 20px 0;
        line-height: 1.75;
        font-size: 0.98rem;
        color: #1e293b;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
    }
    .answer-box h3 {
        color: #0f172a !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        margin-top: 18px !important;
        margin-bottom: 8px !important;
        border-bottom: 1px solid #f1f5f9;
        padding-bottom: 6px;
    }
    .answer-box h3:first-child {
        margin-top: 0 !important;
    }

    /* Professional Abstention Notice Container */
    .abstention-box {
        background-color: #fff1f2;
        border: 1px solid #fecdd3;
        border-left: 5px solid #e11d48;
        border-radius: 12px;
        padding: 24px 28px;
        margin: 20px 0;
        color: #881337;
    }

    /* Verified PubMed Button */
    .pubmed-link-btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background-color: #f8fafc;
        color: #0284c7 !important;
        font-weight: 600;
        font-size: 0.88rem;
        padding: 7px 14px;
        border-radius: 8px;
        border: 1px solid #cbd5e1;
        text-decoration: none !important;
        transition: all 0.15s ease;
    }
    .pubmed-link-btn:hover {
        background-color: #e0f2fe;
        border-color: #7dd3fc;
        color: #0369a1 !important;
    }

    /* Disclaimers */
    .disclaimer-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px 20px;
        font-size: 0.84rem;
        color: #64748b;
        margin-top: 36px;
        line-height: 1.6;
    }
</style>
"""

DARK_THEME_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: #f1f5f9;
        background-color: #0b1329;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3.5rem;
        max-width: 1240px;
    }

    .top-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 60%, #0369a1 100%);
        border-radius: 14px;
        padding: 30px 36px;
        color: #ffffff;
        margin-bottom: 28px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
        border: 1px solid #334155;
    }
    .top-banner h1 {
        color: #ffffff !important;
        font-weight: 800;
        margin: 0;
        font-size: 2.3rem;
    }
    .top-banner p {
        color: #bae6fd;
        font-size: 1.08rem;
        margin-top: 8px;
        margin-bottom: 0;
    }

    .bio-card {
        background-color: #111e38;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 22px 26px;
        margin-bottom: 18px;
        color: #f1f5f9;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    .bio-card:hover {
        border-color: #38bdf8;
    }

    .feature-card {
        background-color: #111e38;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 24px;
        height: 100%;
        border-top: 4px solid #38bdf8;
    }
    .feature-title {
        color: #f8fafc;
        font-size: 1.12rem;
        font-weight: 700;
    }
    .feature-desc {
        color: #94a3b8;
    }

    .badge-pill {
        display: inline-flex;
        align-items: center;
        padding: 5px 12px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 8px;
        margin-bottom: 6px;
    }
    .badge-high {
        background-color: #064e3b;
        color: #6ee7b7;
        border: 1px solid #059669;
    }
    .badge-moderate {
        background-color: #451a03;
        color: #fcd34d;
        border: 1px solid #b45309;
    }
    .badge-prelim {
        background-color: #082f49;
        color: #7dd3fc;
        border: 1px solid #0284c7;
    }
    .badge-insufficient {
        background-color: #450a0a;
        color: #fca5a5;
        border: 1px solid #991b1b;
    }
    .badge-cyan {
        background-color: #042f2e;
        color: #5eead4;
        border: 1px solid #0f766e;
    }

    .answer-box {
        background-color: #111e38;
        border: 1px solid #1e293b;
        border-left: 5px solid #38bdf8;
        border-radius: 12px;
        padding: 26px 30px;
        margin: 20px 0;
        line-height: 1.75;
        color: #f1f5f9;
    }
    .answer-box h3 {
        color: #f8fafc !important;
        font-size: 1.15rem !important;
        border-bottom: 1px solid #1e293b;
    }

    .abstention-box {
        background-color: #2a0b12;
        border: 1px solid #881337;
        border-left: 5px solid #f43f5e;
        border-radius: 12px;
        padding: 24px 28px;
        color: #fecdd3;
    }

    .pubmed-link-btn {
        background-color: #0f172a;
        color: #38bdf8 !important;
        border: 1px solid #1e293b;
        padding: 7px 14px;
        border-radius: 8px;
        text-decoration: none !important;
    }
    .pubmed-link-btn:hover {
        background-color: #1e293b;
        color: #7dd3fc !important;
    }

    .disclaimer-card {
        background-color: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 10px;
        padding: 16px 20px;
        font-size: 0.84rem;
        color: #94a3b8;
    }
</style>
"""


def apply_theme():
    """Applies theme according to user session preference."""
    theme = st.session_state.get("theme_choice", "Light")
    if theme == "Dark":
        st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)
    else:
        st.markdown(LIGHT_THEME_CSS, unsafe_allow_html=True)


def render_sidebar(current_page: str = "Home"):
    """
    Renders professional enterprise sidebar with clear product navigation.
    """
    with st.sidebar:
        # Header Brand
        col_img, col_txt = st.columns([1, 3])
        with col_img:
            st.image("assets/logo.png", width=52)
        with col_txt:
            st.markdown(
                '<div style="font-weight:800; font-size:1.2rem; color:#0f172a; line-height:1.15; letter-spacing:-0.02em;">EvidenceBot</div>'
                '<div style="font-size:0.72rem; color:#0284c7; font-weight:700; letter-spacing:0.04em;">LITERATURE INTELLIGENCE</div>',
                unsafe_allow_html=True
            )

        st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)
        st.caption("PLATFORM")

        # Official Navigation
        st.page_link("app.py", label="Discovery & Search", icon="🔍")
        st.page_link("pages/1_Ask_EvidenceBot.py", label="Evidence Synthesis", icon="💬")
        st.page_link("pages/2_Research_Papers.py", label="Literature Explorer", icon="📚")
        st.page_link("pages/3_Evidence_Analysis.py", label="Grounding & Audit", icon="🔬")
        st.page_link("pages/4_About.py", label="Platform Architecture", icon="🛡️")

        st.markdown("---")

        # Appearance
        st.caption("PREFERENCES")
        theme_options = ["Light", "Dark"]
        current_theme = st.session_state.get("theme_choice", "Light")
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
            <div style="font-size:0.76rem; color:#64748b; line-height:1.5;">
                <strong>Data Ingestion:</strong> National Center for Biotechnology Information (NCBI PubMed E-Utilities)<br>
                <strong>System Version:</strong> v1.0.0 Production
            </div>
            """,
            unsafe_allow_html=True
        )


def render_confidence_badge(confidence: str, similarity_score: Optional[float] = None) -> str:
    """Generates styled badge for confidence classification."""
    score_str = f" • Sim: {similarity_score:.2f}" if similarity_score is not None else ""
    if confidence == "High":
        return f'<span class="badge-pill badge-high">🟢 Strong Scientific Evidence{score_str}</span>'
    elif confidence == "Moderate":
        return f'<span class="badge-pill badge-moderate">🟡 Moderate Evidence{score_str}</span>'
    elif confidence == "Preliminary":
        return f'<span class="badge-pill badge-prelim">🔵 Preliminary Literature{score_str}</span>'
    else:
        return f'<span class="badge-pill badge-insufficient">🔴 Insufficient Evidence{score_str}</span>'


def render_claim_status_badge(status: str) -> str:
    """Renders styled badge for evidence verification status."""
    status_upper = status.upper()
    if status_upper == "SUPPORTED":
        return '<span class="badge-pill badge-high">🟢 EMPIRICALLY SUPPORTED</span>'
    elif status_upper == "PARTIALLY_SUPPORTED":
        return '<span class="badge-pill badge-moderate">🟡 PARTIALLY SUPPORTED</span>'
    elif status_upper == "CONTRADICTED":
        return '<span class="badge-pill badge-insufficient">🔴 CONFLICTING / CONTRADICTED</span>'
    elif status_upper == "UNCERTAIN_HUMAN_REVIEW":
        return '<span class="badge-pill badge-cyan">🟣 CLINICAL EXPERT REVIEW REQUIRED</span>'
    else:
        return '<span class="badge-pill badge-insufficient">⚪ INSUFFICIENT DATA</span>'


def render_paper_card(paper: Any, is_cited: bool = False, chunk_score: Optional[float] = None):
    """
    Renders research publication card with verified links and metadata.
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

    cited_badge = '<span class="badge-pill badge-high">Cited in Synthesis</span>' if is_cited else '<span class="badge-pill badge-prelim">Indexed Literature</span>'
    score_badge = f'<span class="badge-pill badge-moderate">Relevance: {chunk_score:.2f}</span>' if chunk_score is not None else ""
    abstract_status = (
        '<span class="badge-pill badge-cyan">Full Abstract</span>'
        if has_abstract
        else '<span class="badge-pill badge-insufficient">Title-Only Record</span>'
    )

    authors_formatted = format_author_list(authors, 3)
    doi_formatted = f" &bull; <strong>DOI:</strong> {doi}" if doi else ""

    st.markdown(
        f"""
        <div class="bio-card">
            <div style="font-weight:700; font-size:1.06rem; color:#0f172a; margin-bottom:6px; line-height:1.4;">
                {title}
            </div>
            <div style="font-size:0.86rem; color:#64748b; margin-bottom:12px;">
                <strong>Journal:</strong> {journal} ({year}) &bull; 
                <strong>Authors:</strong> {authors_formatted}
                {doi_formatted}
            </div>
            <div style="margin-bottom:14px;">
                {cited_badge}
                {score_badge}
                {abstract_status}
                <span class="badge-pill badge-prelim">PMID: {pmid}</span>
            </div>
            <a href="{url}" target="_blank" class="pubmed-link-btn">
                🔗 View Verified Record on PubMed [PMID: {pmid}]
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

    if has_abstract:
        with st.expander(f"📄 Abstract Preview (PMID: {pmid})", expanded=False):
            st.markdown(f"<div style='font-size:0.92rem; line-height:1.65; color:#334155;'>{abstract}</div>", unsafe_allow_html=True)


def render_disclaimer():
    """Renders professional non-clinical institutional disclaimer."""
    st.markdown(
        """
        <div class="disclaimer-card">
            ⚖️ <strong>Institutional Research Advisory:</strong> EvidenceBot is an AI-powered scientific intelligence platform 
            engineered to query, analyze, and synthesize peer-reviewed biomedical literature indexed on the National Library of Medicine (NCBI PubMed). 
            It is designed strictly for research, discovery, and educational purposes and does <strong>not</strong> constitute medical advice, clinical diagnosis, 
            or individual treatment recommendations. Always consult a licensed medical practitioner for clinical healthcare decisions.
        </div>
        """,
        unsafe_allow_html=True
    )
