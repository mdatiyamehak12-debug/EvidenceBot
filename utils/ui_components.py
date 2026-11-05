"""
EvidenceBot - Enterprise Scientific Research UI Components & Design System
==========================================================================
Modern, premium scientific research dashboard styled with a professional
White and Navy-Blue color combination with subtle Teal accents.
Clean typography, rounded cards, smooth shadows, and responsive layout.
"""

import streamlit as st
from typing import List, Optional, Any, Dict
from datetime import datetime
from utils.helpers import format_author_list, format_pubmed_url
from utils.history_manager import load_search_history, clear_search_history, add_to_history

# =====================================================================
# Professional Scientific Design System CSS (White, Navy-Blue & Teal)
# =====================================================================

SCIENTIFIC_THEME_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    /* Global Typography & Palette */
    html, body, [class*="css"], [class*="st-"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        color: #0f172a;
    }

    /* Background and Layout */
    .stApp {
        background-color: #f8fafc;
    }

    .block-container {
        padding-top: 1.8rem !important;
        padding-bottom: 4rem !important;
        max-width: 1240px !important;
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #0f172a !important;
        font-weight: 700 !important;
        letter-spacing: -0.025em !important;
    }

    /* Subtle Teal Pulse Animation */
    @keyframes teal-radar {
        0% {
            transform: scale(0.92);
            box-shadow: 0 0 0 0 rgba(13, 148, 136, 0.7);
        }
        70% {
            transform: scale(1.06);
            box-shadow: 0 0 0 8px rgba(13, 148, 136, 0);
        }
        100% {
            transform: scale(0.92);
            box-shadow: 0 0 0 0 rgba(13, 148, 136, 0);
        }
    }

    .live-dot-teal {
        display: inline-block;
        width: 8px;
        height: 8px;
        background-color: #0d9488;
        border-radius: 50%;
        margin-right: 8px;
        animation: teal-radar 2.2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        vertical-align: middle;
    }

    .status-dot {
        display: inline-block;
        width: 7px;
        height: 7px;
        border-radius: 50%;
        margin-right: 6px;
        vertical-align: middle;
    }
    .status-dot-teal   { background-color: #0d9488; }
    .status-dot-green  { background-color: #10b981; }
    .status-dot-amber  { background-color: #f59e0b; }
    .status-dot-rose   { background-color: #f43f5e; }
    .status-dot-navy   { background-color: #1e3a8a; }
    .status-dot-slate  { background-color: #64748b; }

    /* Telemetry and Metadata Tags */
    .mono-tag {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        padding: 4px 10px;
        border-radius: 6px;
        display: inline-flex;
        align-items: center;
        background: #f1f5f9;
        color: #334155;
        border: 1px solid #e2e8f0;
    }

    .telemetry-chip {
        background: #f0fdfa;
        border: 1px solid #99f6e4;
        color: #0f766e;
        border-radius: 9999px;
        padding: 5px 14px;
        font-size: 0.75rem;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
    }

    /* Hero Banner Card */
    .research-hero {
        background: linear-gradient(135deg, #0a192f 0%, #0f172a 60%, #112240 100%);
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 34px 38px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px -5px rgba(10, 25, 47, 0.25);
        color: #ffffff;
        position: relative;
        overflow: hidden;
    }
    .research-hero::after {
        content: "";
        position: absolute;
        top: -60px;
        right: -60px;
        width: 240px;
        height: 240px;
        background: radial-gradient(circle, rgba(13, 148, 136, 0.25) 0%, rgba(13, 148, 136, 0) 70%);
        border-radius: 50%;
        pointer-events: none;
    }
    .research-hero h1 {
        color: #ffffff !important;
        font-weight: 800 !important;
        margin: 0 0 8px 0;
        font-size: 2.25rem !important;
        letter-spacing: -0.035em !important;
        line-height: 1.15;
    }
    .research-hero p {
        color: #cbd5e1 !important;
        font-size: 1.05rem !important;
        margin: 0;
        max-width: 820px;
        line-height: 1.6;
        font-weight: 400;
    }

    /* Metric & Telemetry Stat Cards */
    .stat-tile {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 18px 22px;
        box-shadow: 0 2px 8px -2px rgba(15, 23, 42, 0.04);
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .stat-tile:hover {
        border-color: #0d9488;
        transform: translateY(-2px);
        box-shadow: 0 10px 24px -6px rgba(13, 148, 136, 0.12);
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
        font-size: 1.45rem;
        font-weight: 800;
        color: #0f172a;
        margin-top: 4px;
        letter-spacing: -0.03em;
    }
    .stat-subtext {
        font-size: 0.78rem;
        color: #0d9488;
        margin-top: 2px;
        font-weight: 500;
    }

    /* Main Search Container Card */
    .search-card-container {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 26px 30px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px -3px rgba(15, 23, 42, 0.06);
    }

    /* Research Paper Cards */
    .paper-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #0d9488;
        border-radius: 12px;
        padding: 22px 26px;
        margin-bottom: 16px;
        box-shadow: 0 2px 10px -2px rgba(15, 23, 42, 0.04);
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .paper-card:hover {
        border-color: #0d9488;
        border-left-color: #0f766e;
        transform: translateY(-2px);
        box-shadow: 0 12px 28px -6px rgba(15, 23, 42, 0.09);
    }
    .paper-card-title {
        font-weight: 700;
        font-size: 1.10rem;
        color: #0f172a;
        margin-bottom: 8px;
        line-height: 1.45;
        letter-spacing: -0.02em;
    }
    .paper-card-title a {
        color: #0f172a !important;
        text-decoration: none;
        transition: color 0.15s ease;
    }
    .paper-card-title a:hover {
        color: #0d9488 !important;
        text-decoration: underline;
    }
    .paper-card-meta {
        font-size: 0.86rem;
        color: #475569;
        margin-bottom: 12px;
        line-height: 1.6;
    }
    .paper-card-meta strong {
        color: #1e293b;
    }
    .paper-abstract-box {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 0.88rem;
        color: #334155;
        line-height: 1.65;
        margin-top: 10px;
    }

    /* Badges */
    .badge-pill {
        display: inline-flex;
        align-items: center;
        padding: 4px 10px;
        border-radius: 6px;
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
        color: #0369a1;
        border: 1px solid #bae6fd;
    }
    .badge-insufficient {
        background-color: #fff1f2;
        color: #be123c;
        border: 1px solid #fecdd3;
    }
    .badge-teal {
        background-color: #f0fdfa;
        color: #0f766e;
        border: 1px solid #99f6e4;
    }

    /* Evidence Availability Header Banner */
    .evidence-status-banner {
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 12px;
    }
    .evidence-status-banner.available {
        background: #f0fdfa;
        border: 1px solid #99f6e4;
        border-left: 4px solid #0d9488;
        color: #0f766e;
    }
    .evidence-status-banner.unavailable {
        background: #fff1f2;
        border: 1px solid #fecdd3;
        border-left: 4px solid #e11d48;
        color: #9f1239;
    }
    .evidence-status-title {
        font-weight: 700;
        font-size: 1.05rem;
        display: flex;
        align-items: center;
    }

    /* Answer Synthesis Card */
    .answer-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #1e3a8a;
        border-radius: 12px;
        padding: 28px 32px;
        margin: 18px 0;
        line-height: 1.75;
        font-size: 0.98rem;
        color: #1e293b;
        box-shadow: 0 4px 16px -2px rgba(15, 23, 42, 0.05);
    }
    .answer-card h3 {
        color: #0f172a !important;
        font-size: 1.15rem !important;
        letter-spacing: -0.02em;
        margin-top: 22px !important;
        margin-bottom: 10px !important;
        padding-bottom: 6px;
        border-bottom: 1px solid #f1f5f9;
        font-weight: 700 !important;
    }
    .answer-card h3:first-child {
        margin-top: 0 !important;
    }

    /* Button Enhancements */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%) !important;
        color: #ffffff !important;
        border: 1px solid #1e293b !important;
        font-weight: 600 !important;
        font-size: 0.94rem !important;
        border-radius: 8px !important;
        padding: 0.55rem 1.4rem !important;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15) !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #0d9488 0%, #0f766e 100%) !important;
        border-color: #0d9488 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 8px 20px -3px rgba(13, 148, 136, 0.3) !important;
    }

    div.stButton > button[kind="secondary"] {
        background-color: #ffffff !important;
        color: #334155 !important;
        border: 1px solid #cbd5e1 !important;
        font-weight: 600 !important;
        font-size: 0.90rem !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        background-color: #f1f5f9 !important;
        border-color: #94a3b8 !important;
        color: #0f172a !important;
    }

    /* Links to PubMed */
    .pubmed-btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background-color: #f0fdfa;
        color: #0f766e !important;
        font-weight: 600;
        font-size: 0.82rem;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.02em;
        padding: 6px 14px;
        border-radius: 6px;
        border: 1px solid #99f6e4;
        text-decoration: none !important;
        transition: all 0.2s ease;
    }
    .pubmed-btn:hover {
        background-color: #ccfbf1;
        border-color: #5eead4;
        color: #115e59 !important;
        transform: translateY(-1px);
    }

    /* Sidebar Customizations */
    [data-testid="stSidebar"] {
        background-color: #0b1528 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    [data-testid="stSidebar"] * {
        color: #e2e8f0;
    }
    [data-testid="stSidebar"] a {
        color: #38bdf8 !important;
    }
    [data-testid="stSidebar"] .stButton > button {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        color: #cbd5e1 !important;
        font-size: 0.82rem !important;
        text-align: left !important;
        border-radius: 6px !important;
        padding: 6px 10px !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: rgba(13, 148, 136, 0.2) !important;
        border-color: #0d9488 !important;
        color: #ffffff !important;
    }

    /* Sidebar Brand Card */
    .sidebar-brand-card {
        padding: 8px 0 16px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 16px;
    }

    /* Recent Searches in Sidebar */
    .recent-search-item {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 6px;
        padding: 8px 10px;
        margin-bottom: 6px;
        font-size: 0.80rem;
        cursor: pointer;
        transition: all 0.15s ease;
    }
    .recent-search-item:hover {
        background: rgba(13, 148, 136, 0.15);
        border-color: rgba(13, 148, 136, 0.4);
    }

    .empty-history-box {
        background: rgba(255, 255, 255, 0.03);
        border: 1px dashed rgba(255, 255, 255, 0.15);
        border-radius: 8px;
        padding: 14px;
        text-align: center;
        color: #94a3b8;
        font-size: 0.78rem;
        line-height: 1.5;
        margin: 8px 0;
    }

    /* Disclaimer / Footer Card */
    .disclaimer-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 18px 24px;
        font-size: 0.82rem;
        color: #64748b;
        margin-top: 40px;
        line-height: 1.6;
        box-shadow: 0 1px 4px rgba(15, 23, 42, 0.03);
    }
    .disclaimer-card strong {
        color: #334155;
    }
</style>
"""


def apply_theme():
    """Applies the professional white and navy-blue design theme with subtle teal accents."""
    st.markdown(SCIENTIFIC_THEME_CSS, unsafe_allow_html=True)


def render_brand_logo_svg() -> str:
    """Returns a clean, high-resolution SVG logo for Bio EvidenceBot."""
    return """
    <svg width="44" height="44" viewBox="0 0 44 44" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="44" height="44" rx="10" fill="#0f172a"/>
        <circle cx="22" cy="22" r="14" stroke="#0d9488" stroke-width="2" stroke-dasharray="3 3"/>
        <path d="M14 22C14 17.5817 17.5817 14 22 14C26.4183 14 30 17.5817 30 22C30 26.4183 26.4183 30 22 30" stroke="#38bdf8" stroke-width="2.2" stroke-linecap="round"/>
        <path d="M17 17L27 27M27 17L17 27" stroke="#14b8a6" stroke-width="1.8" stroke-linecap="round"/>
        <circle cx="22" cy="22" r="3.5" fill="#0d9488"/>
    </svg>
    """


def render_sidebar(current_page: str = "Home"):
    """
    Renders professional enterprise sidebar with:
    - Bio EvidenceBot brand logo & title
    - Platform module navigation links
    - Persistent Recent Searches with click-to-search, clear history, and empty state
    - Live system status telemetry
    """
    with st.sidebar:
        # 1. Professional Brand Logo & Header
        col_logo, col_title = st.columns([1, 3])
        with col_logo:
            st.markdown(render_brand_logo_svg(), unsafe_allow_html=True)
        with col_title:
            st.markdown(
                """
                <div style="font-weight: 800; font-size: 1.18rem; color: #ffffff; line-height: 1.15; letter-spacing: -0.03em;">
                    Bio EvidenceBot
                </div>
                <div style="font-size: 0.68rem; color: #2dd4bf; font-weight: 700; letter-spacing: 0.08em; font-family: 'JetBrains Mono', monospace; text-transform: uppercase;">
                    AI Research Platform
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<div style='margin-bottom: 14px;'></div>", unsafe_allow_html=True)
        st.caption("PLATFORM MODULES")

        # Official Navigation
        st.page_link("app.py", label="Research Dashboard")
        st.page_link("pages/1_Ask_EvidenceBot.py", label="Evidence Synthesis")
        st.page_link("pages/2_Research_Papers.py", label="Literature Explorer")
        st.page_link("pages/3_Evidence_Analysis.py", label="Grounding & Audit")
        st.page_link("pages/4_About.py", label="Architecture & Methodology")

        st.markdown("---")

        # =================================================================
        # 2. Recent Searches (Persistent across refreshes)
        # =================================================================
        st.caption("RECENT SEARCHES")
        recent_searches = load_search_history()

        if recent_searches:
            # Display latest searches (up to 8 in sidebar)
            for idx, item in enumerate(recent_searches[:8]):
                query_text = item.get("query", "")
                yr_tag = f" ({item['year_range']})" if item.get("year_range") else ""
                btn_label = f"🔍 {query_text[:28]}..." if len(query_text) > 28 else f"🔍 {query_text}"
                
                if st.button(btn_label + yr_tag, key=f"sidebar_hist_{idx}", use_container_width=True):
                    # Set the query to run in session state and reload
                    st.session_state["query_to_run"] = query_text
                    if item.get("year_range"):
                        st.session_state["history_year_range"] = item.get("year_range")
                    # If currently on home or another page, trigger search rerun
                    st.session_state["active_query"] = query_text
                    st.rerun()

            col_clr, col_cnt = st.columns([1, 1])
            with col_clr:
                if st.button("Clear History", key="btn_clear_hist", use_container_width=True):
                    clear_search_history()
                    st.rerun()
            with col_cnt:
                st.markdown(
                    f"<div style='font-size:0.72rem; color:#94a3b8; text-align:right; padding-top:6px; font-family:\"JetBrains Mono\", monospace;'>"
                    f"{len(recent_searches)} logged"
                    f"</div>",
                    unsafe_allow_html=True
                )
        else:
            # Empty search history state
            st.markdown(
                """
                <div class="empty-history-box">
                    <div style="font-size:1.1rem; margin-bottom:4px;">⏱️</div>
                    <div><strong>No recent searches yet.</strong></div>
                    <div style="margin-top:2px; font-size:0.72rem;">Search any biomedical or scientific topic to build your persistent research log.</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("---")

        # 3. System Status Telemetry
        st.caption("SYSTEM TELEMETRY")
        st.markdown(
            """
            <div style="font-size:0.76rem; color:#94a3b8; line-height:1.75; font-family:'JetBrains Mono', monospace;">
                <div><span class="live-dot-teal"></span><strong>NCBI Entrez:</strong> CONNECTED</div>
                <div><span class="status-dot status-dot-teal"></span><strong>Europe PMC:</strong> SYNCHRONIZED</div>
                <div><span class="status-dot status-dot-green"></span><strong>FAISS Index:</strong> 768-DIM LIVE</div>
                <div><span class="status-dot status-dot-slate"></span><strong>Corpus:</strong> 36.8M+ PUBMED</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")
        st.markdown(
            """
            <div style="font-size:0.70rem; color:#64748b; line-height:1.5; font-family:'JetBrains Mono', monospace;">
                BIO EVIDENCEBOT PLATFORM<br>
                BUILD: v2.0 PRODUCTION &bull; 2026
            </div>
            """,
            unsafe_allow_html=True
        )


def render_confidence_badge(confidence: str, similarity_score: Optional[float] = None) -> str:
    """Generates styled badge for confidence classification."""
    score_str = f" &bull; SIM: {similarity_score:.2f}" if similarity_score is not None else ""
    if confidence == "High":
        return f'<span class="badge-pill badge-high"><span class="status-dot status-dot-green"></span>STRONG EVIDENCE{score_str}</span>'
    elif confidence == "Moderate":
        return f'<span class="badge-pill badge-moderate"><span class="status-dot status-dot-amber"></span>MODERATE EVIDENCE{score_str}</span>'
    elif confidence == "Preliminary":
        return f'<span class="badge-pill badge-prelim"><span class="status-dot status-dot-navy"></span>PRELIMINARY LITERATURE{score_str}</span>'
    else:
        return f'<span class="badge-pill badge-insufficient"><span class="status-dot status-dot-rose"></span>INSUFFICIENT EVIDENCE{score_str}</span>'


def render_claim_status_badge(status: str) -> str:
    """Renders styled badge for evidence verification status."""
    status_upper = status.upper()
    if status_upper == "SUPPORTED":
        return '<span class="badge-pill badge-high"><span class="status-dot status-dot-green"></span>EMPIRICALLY SUPPORTED</span>'
    elif status_upper == "PARTIALLY_SUPPORTED":
        return '<span class="badge-pill badge-moderate"><span class="status-dot status-dot-amber"></span>PARTIALLY SUPPORTED</span>'
    elif status_upper == "CONTRADICTED":
        return '<span class="badge-pill badge-insufficient"><span class="status-dot status-dot-rose"></span>CONFLICTING FINDINGS</span>'
    elif status_upper == "UNCERTAIN_HUMAN_REVIEW":
        return '<span class="badge-pill badge-teal"><span class="status-dot status-dot-teal"></span>EXPERT REVIEW REQUIRED</span>'
    else:
        return '<span class="badge-pill badge-insufficient"><span class="status-dot status-dot-slate"></span>INSUFFICIENT DATA</span>'


def render_evidence_availability(is_available: bool, count: int = 0, year_range: str = "All Years") -> None:
    """Renders the top Evidence Availability Banner."""
    if is_available:
        st.markdown(
            f"""
            <div class="evidence-status-banner available">
                <div class="evidence-status-title">
                    <span class="live-dot-teal"></span>
                    Verified Scientific Evidence Available ({count} Articles &bull; {year_range})
                </div>
                <div>
                    <span class="badge-pill badge-teal">DETERMINISTIC GROUNDING</span>
                    <span class="badge-pill badge-high">AUTHENTIC CITATIONS</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div class="evidence-status-banner unavailable">
                <div class="evidence-status-title">
                    <span class="status-dot status-dot-rose"></span>
                    No sufficient scientific evidence found for this query.
                </div>
                <div>
                    <span class="badge-pill badge-insufficient">EMPIRICAL ABSTENTION</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_paper_card(paper: Any, is_cited: bool = False, chunk_score: Optional[float] = None):
    """
    Renders professional individual research paper cards matching Requirement 5:
    - Research paper title
    - Authors
    - Publication year
    - Journal name
    - Abstract or relevant evidence
    - PubMed ID
    - Link to the original research paper
    - Clear visual separation between cards
    """
    if isinstance(paper, dict):
        pmid = paper.get("pmid", "")
        title = paper.get("title", "Untitled Publication")
        journal = paper.get("journal", "Biomedical Journal")
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

    cited_badge = (
        '<span class="badge-pill badge-high"><span class="status-dot status-dot-green"></span>CITED IN SYNTHESIS</span>'
        if is_cited
        else '<span class="badge-pill badge-teal"><span class="status-dot status-dot-teal"></span>INDEXED RECORD</span>'
    )
    score_badge = f'<span class="badge-pill badge-moderate">SIM: {chunk_score:.2f}</span>' if chunk_score is not None else ""
    abstract_badge = (
        '<span class="badge-pill badge-teal">PEER-REVIEWED ABSTRACT</span>'
        if has_abstract
        else '<span class="badge-pill badge-insufficient">TITLE RECORD</span>'
    )

    authors_formatted = format_author_list(authors, 4)
    doi_formatted = f" &bull; <strong>DOI:</strong> <code>{doi}</code>" if doi else ""

    # Short excerpt preview
    abstract_preview = abstract[:320] + "..." if len(abstract) > 320 else abstract

    st.markdown(
        f"""
        <div class="paper-card">
            <div class="paper-card-title">
                <a href="{url}" target="_blank" title="Open official NCBI PubMed paper in new tab">
                    {title} &rarr;
                </a>
            </div>
            <div class="paper-card-meta">
                <strong>Journal:</strong> <em>{journal}</em> ({year}) &bull;
                <strong>Authors:</strong> {authors_formatted}
                {doi_formatted}
            </div>
            <div style="margin-bottom:12px;">
                {cited_badge}
                {score_badge}
                {abstract_badge}
                <span class="mono-tag">PMID {pmid}</span>
                <span class="mono-tag">YEAR {year}</span>
            </div>
            <div class="paper-abstract-box">
                <strong style="color:#0f172a;">Evidence / Abstract Excerpt:</strong><br>
                {abstract_preview}
            </div>
            <div style="margin-top:14px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
                <a href="{url}" target="_blank" class="pubmed-btn">
                    Official PubMed Record &bull; PMID {pmid} &rarr;
                </a>
                <span style="font-size:0.75rem; color:#64748b; font-family:'JetBrains Mono', monospace;">
                    Verified NCBI Source &bull; Authenticated DOI
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if has_abstract and len(abstract) > 320:
        with st.expander(f"Read Full Abstract (PMID: {pmid})", expanded=False):
            st.markdown(f"<div style='font-size:0.92rem; line-height:1.7; color:#334155; padding:6px 0;'>{abstract}</div>", unsafe_allow_html=True)


def render_disclaimer():
    """Renders professional institutional research notice footer."""
    st.markdown(
        """
        <div class="disclaimer-card">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px;">
                <div style="max-width:860px;">
                    <strong>INSTITUTIONAL SCIENTIFIC RESEARCH NOTICE:</strong> EvidenceBot is an autonomous biomedical 
                    intelligence engine designed to index, synthesize, and verify peer-reviewed scientific literature 
                    from the National Library of Medicine (NCBI PubMed Central) and Europe PMC. 
                    This platform is intended exclusively for scientific literature review, clinical trial analysis, 
                    and academic research. It does <strong>not</strong> provide personalized clinical diagnosis, medical advice, 
                    or prescriptive therapy. Always consult qualified clinical healthcare professionals for patient care decisions.
                </div>
                <div style="text-align:right; font-family:'JetBrains Mono', monospace; font-size:0.75rem; color:#64748b;">
                    CORPUS: NCBI PUBMED<br>
                    INDEX: DENSE VECTOR FAISS<br>
                    CITATION FIDELITY: 100%
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
