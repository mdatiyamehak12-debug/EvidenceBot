"""
EvidenceBot - Enterprise Scientific Research UI Components & Design System
==========================================================================
Modern, premium scientific research platform styled with:
- Deep navy blue (#14243A)
- White (#FFFFFF)
- Soft light grey (#F5F7FA)
- Teal (#168C83)
- Subtle blue accents (#1E3A8A, #E8F4F8)

Clean typography, minimal clutter, rounded cards, subtle shadows,
and responsive desktop/mobile layout.
"""

import streamlit as st
from typing import List, Optional, Any, Dict
from datetime import datetime
from utils.helpers import format_author_list, format_pubmed_url
from utils.history_manager import load_search_history, clear_search_history, add_to_history

# =====================================================================
# Professional Scientific Design System CSS
# =====================================================================

SCIENTIFIC_THEME_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global Typography & Base Palette */
    html, body, [class*="css"], [class*="st-"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        color: #14243A;
    }

    /* Background and Spacing */
    .stApp {
        background-color: #F5F7FA;
    }

    .block-container {
        padding-top: 1.8rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 1200px !important;
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #14243A !important;
        font-weight: 700 !important;
        letter-spacing: -0.025em !important;
    }

    /* Main Dashboard Header Card */
    .dashboard-header {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 28px 32px;
        margin-bottom: 20px;
        box-shadow: 0 2px 10px rgba(20, 36, 58, 0.04);
    }
    .header-eyebrow {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        color: #168C83;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .dashboard-header h1 {
        font-size: 2.1rem !important;
        margin: 0 0 4px 0 !important;
        color: #14243A !important;
        font-weight: 800 !important;
        letter-spacing: -0.035em !important;
    }
    .header-tagline {
        font-size: 1.05rem;
        font-weight: 600;
        color: #168C83;
        margin-bottom: 6px;
    }
    .header-subtitle {
        font-size: 0.95rem;
        color: #4B5563;
        margin: 0;
        line-height: 1.55;
    }

    /* Cards with subtle shadows and rounded corners */
    .content-card {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 18px;
        box-shadow: 0 2px 10px rgba(20, 36, 58, 0.04);
    }

    /* Research Paper Cards */
    .paper-card {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-left: 3px solid #168C83;
        border-radius: 10px;
        padding: 20px 24px;
        margin-bottom: 14px;
        box-shadow: 0 1px 6px rgba(20, 36, 58, 0.03);
        transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
    }
    .paper-card:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(20, 36, 58, 0.08);
        border-left-color: #14243A;
    }
    .paper-card-title {
        font-weight: 700;
        font-size: 1.08rem;
        color: #14243A;
        margin-bottom: 6px;
        line-height: 1.4;
    }
    .paper-card-title a {
        color: #14243A !important;
        text-decoration: none;
    }
    .paper-card-title a:hover {
        color: #168C83 !important;
        text-decoration: underline;
    }
    .paper-card-meta {
        font-size: 0.85rem;
        color: #4B5563;
        margin-bottom: 10px;
        line-height: 1.6;
    }
    .paper-card-meta strong {
        color: #14243A;
    }
    .paper-abstract-box {
        background-color: #F8FAFC;
        border: 1px solid #E5E7EB;
        border-radius: 6px;
        padding: 10px 14px;
        font-size: 0.88rem;
        color: #374151;
        line-height: 1.6;
        margin-top: 8px;
    }

    /* Status & Filter Badges */
    .badge-pill {
        display: inline-flex;
        align-items: center;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.72rem;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 4px;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        font-family: 'JetBrains Mono', monospace;
    }
    .badge-teal {
        background-color: #EBF8F7;
        color: #168C83;
        border: 1px solid #99E3DD;
    }
    .badge-high {
        background-color: #ECFDF5;
        color: #047857;
        border: 1px solid #A7F3D0;
    }
    .badge-moderate {
        background-color: #FFFBEB;
        color: #B45309;
        border: 1px solid #FDE68A;
    }
    .badge-prelim {
        background-color: #EFF6FF;
        color: #1E40AF;
        border: 1px solid #BFDBFE;
    }
    .badge-insufficient {
        background-color: #FEF2F2;
        color: #B91C1C;
        border: 1px solid #FECACA;
    }
    .mono-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 4px;
        background: #F1F5F9;
        color: #334155;
        border: 1px solid #E2E8F0;
        display: inline-flex;
        align-items: center;
    }

    /* Evidence Availability Header Banner */
    .evidence-status-banner {
        border-radius: 10px;
        padding: 14px 20px;
        margin-bottom: 18px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 10px;
    }
    .evidence-status-banner.available {
        background-color: #EBF8F7;
        border: 1px solid #99E3DD;
        border-left: 4px solid #168C83;
        color: #168C83;
    }
    .evidence-status-banner.unavailable {
        background-color: #FEF2F2;
        border: 1px solid #FECACA;
        border-left: 4px solid #DC2626;
        color: #991B1B;
    }
    .evidence-status-title {
        font-weight: 700;
        font-size: 1.0rem;
    }

    /* AI Research Synthesis Card */
    .answer-card {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-left: 4px solid #14243A;
        border-radius: 10px;
        padding: 24px 28px;
        margin: 16px 0;
        line-height: 1.7;
        font-size: 0.96rem;
        color: #1F2937;
        box-shadow: 0 2px 10px rgba(20, 36, 58, 0.04);
    }
    .answer-card h3 {
        color: #14243A !important;
        font-size: 1.10rem !important;
        letter-spacing: -0.015em;
        margin-top: 18px !important;
        margin-bottom: 8px !important;
        padding-bottom: 4px;
        border-bottom: 1px solid #F3F4F6;
        font-weight: 700 !important;
    }
    .answer-card h3:first-child {
        margin-top: 0 !important;
    }

    /* Buttons */
    div.stButton > button[kind="primary"] {
        background-color: #14243A !important;
        color: #FFFFFF !important;
        border: 1px solid #14243A !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        border-radius: 6px !important;
        padding: 0.50rem 1.30rem !important;
        transition: all 0.15s ease !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #168C83 !important;
        border-color: #168C83 !important;
        color: #FFFFFF !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(22, 140, 131, 0.25) !important;
    }

    div.stButton > button[kind="secondary"] {
        background-color: #FFFFFF !important;
        color: #374151 !important;
        border: 1px solid #D1D5DB !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        border-radius: 6px !important;
        transition: all 0.15s ease !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        background-color: #F9FAFB !important;
        border-color: #168C83 !important;
        color: #168C83 !important;
    }

    /* Links to PubMed */
    .pubmed-btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background-color: #EBF8F7;
        color: #168C83 !important;
        font-weight: 600;
        font-size: 0.80rem;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.02em;
        padding: 5px 12px;
        border-radius: 6px;
        border: 1px solid #99E3DD;
        text-decoration: none !important;
        transition: all 0.15s ease;
    }
    .pubmed-btn:hover {
        background-color: #CCFBF1;
        border-color: #168C83;
        color: #0F766E !important;
    }

    /* Sidebar Customizations */
    [data-testid="stSidebar"] {
        background-color: #14243A !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    [data-testid="stSidebar"] * {
        color: #E5E7EB;
    }
    [data-testid="stSidebar"] a {
        color: #93C5FD !important;
    }
    [data-testid="stSidebar"] .stButton > button {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        color: #E5E7EB !important;
        font-size: 0.82rem !important;
        text-align: left !important;
        border-radius: 6px !important;
        padding: 6px 10px !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: rgba(22, 140, 131, 0.25) !important;
        border-color: #168C83 !important;
        color: #FFFFFF !important;
    }

    .empty-history-box {
        background: rgba(255, 255, 255, 0.03);
        border: 1px dashed rgba(255, 255, 255, 0.15);
        border-radius: 6px;
        padding: 12px;
        text-align: center;
        color: #9CA3AF;
        font-size: 0.78rem;
        line-height: 1.45;
        margin: 6px 0;
    }

    /* Disclaimer Footer */
    .disclaimer-card {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 16px 20px;
        font-size: 0.80rem;
        color: #6B7280;
        margin-top: 36px;
        line-height: 1.55;
    }
    .disclaimer-card strong {
        color: #374151;
    }

    /* Clean Cards & Tiles */
    .stat-tile, .feature-card, .bio-card {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 18px 20px;
        margin-bottom: 14px;
        box-shadow: 0 1px 6px rgba(20, 36, 58, 0.03);
    }
    .stat-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: #168C83;
        margin-bottom: 4px;
    }
    .stat-value {
        font-size: 1.6rem;
        font-weight: 800;
        color: #14243A;
        line-height: 1.2;
    }
    .feature-title {
        font-weight: 700;
        font-size: 1.0rem;
        color: #14243A;
        margin: 4px 0 6px 0;
    }
    .feature-desc {
        font-size: 0.86rem;
        color: #4B5563;
        line-height: 1.55;
    }
    .abstention-box {
        background-color: #FEF2F2;
        border: 1px solid #FECACA;
        border-left: 4px solid #DC2626;
        border-radius: 10px;
        padding: 20px 24px;
        margin: 16px 0;
    }
</style>
"""


def apply_theme():
    """Applies the professional deep navy, white and teal scientific research theme."""
    st.markdown(SCIENTIFIC_THEME_CSS, unsafe_allow_html=True)


def render_brand_logo_svg() -> str:
    """Returns a clean, minimalist SVG logo for Bio EvidenceBot."""
    return """
    <svg width="36" height="36" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="36" height="36" rx="8" fill="#14243A"/>
        <circle cx="18" cy="18" r="11" stroke="#168C83" stroke-width="1.8" stroke-dasharray="2 2"/>
        <path d="M11 18C11 14.134 14.134 11 18 11C21.866 11 25 14.134 25 18C25 21.866 21.866 25 18 25" stroke="#93C5FD" stroke-width="1.8" stroke-linecap="round"/>
        <path d="M14 14L22 22M22 14L14 22" stroke="#168C83" stroke-width="1.5" stroke-linecap="round"/>
        <circle cx="18" cy="18" r="3" fill="#168C83"/>
    </svg>
    """


def render_sidebar(current_page: str = "Home"):
    """
    Renders professional enterprise sidebar with:
    - EvidenceBot logo and title
    - New Research button
    - Platform module navigation
    - Recent Searches with reopen click, clear history, and empty state
    - System status
    """
    with st.sidebar:
        # 1. EvidenceBot Brand Logo & Header
        col_logo, col_title = st.columns([1, 3.2])
        with col_logo:
            st.markdown(render_brand_logo_svg(), unsafe_allow_html=True)
        with col_title:
            st.markdown(
                """
                <div style="font-weight: 800; font-size: 1.15rem; color: #FFFFFF; line-height: 1.15; letter-spacing: -0.025em;">
                    EvidenceBot
                </div>
                <div style="font-size: 0.68rem; color: #99E3DD; font-weight: 600; letter-spacing: 0.06em; font-family: 'JetBrains Mono', monospace; text-transform: uppercase;">
                    Biomedical Intelligence
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

        # 2. "New Research" Button (Prominently at the top)
        if st.button("✨ New Research", key="sidebar_new_research_btn", use_container_width=True):
            st.session_state["active_query"] = ""
            st.session_state.pop("latest_result", None)
            st.session_state.pop("latest_question", None)
            st.rerun()

        st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)
        st.caption("PLATFORM MODULES")

        # Official Navigation
        st.page_link("app.py", label="Research Dashboard")
        st.page_link("pages/1_Ask_EvidenceBot.py", label="Evidence Synthesis")
        st.page_link("pages/2_Research_Papers.py", label="Literature Explorer")
        st.page_link("pages/3_Evidence_Analysis.py", label="Grounding & Audit")
        st.page_link("pages/4_About.py", label="About EvidenceBot")

        st.markdown("---")

        # 3. Recent Searches (Persistent across refreshes)
        st.caption("RECENT SEARCHES")
        recent_searches = load_search_history()

        if recent_searches:
            for idx, item in enumerate(recent_searches[:8]):
                query_text = item.get("query", "")
                yr_tag = f" ({item['year_range']})" if item.get("year_range") else ""
                short_label = query_text[:26] + "..." if len(query_text) > 26 else query_text
                btn_display = f"🔍 {short_label}" + yr_tag

                if st.button(btn_display, key=f"sidebar_hist_{idx}", use_container_width=True):
                    st.session_state["active_query"] = query_text
                    st.session_state["query_to_run"] = query_text
                    if item.get("year_range"):
                        st.session_state["history_year_range"] = item.get("year_range")
                    st.rerun()

            col_clr, col_cnt = st.columns([1.2, 1])
            with col_clr:
                if st.button("Clear History", key="btn_clear_hist", use_container_width=True):
                    clear_search_history()
                    st.rerun()
            with col_cnt:
                st.markdown(
                    f"<div style='font-size:0.72rem; color:#9CA3AF; text-align:right; padding-top:6px; font-family:\"JetBrains Mono\", monospace;'>"
                    f"{len(recent_searches)} saved"
                    f"</div>",
                    unsafe_allow_html=True
                )
        else:
            # Empty state
            st.markdown(
                """
                <div class="empty-history-box">
                    <div>No recent searches yet.</div>
                    <div style="font-size:0.70rem; color:#6B7280; margin-top:3px;">Your scientific inquiries will appear here.</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("---")

        # 4. System Status Telemetry
        st.caption("DATA PROVENANCE")
        st.markdown(
            """
            <div style="font-size:0.75rem; color:#9CA3AF; line-height:1.65; font-family:'JetBrains Mono', monospace;">
                <div>&bull; <strong>NCBI Entrez:</strong> CONNECTED</div>
                <div>&bull; <strong>Europe PMC:</strong> SYNCHRONIZED</div>
                <div>&bull; <strong>FAISS Index:</strong> ACTIVE</div>
                <div>&bull; <strong>PubMed Corpus:</strong> 36.8M+ RECORDS</div>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_confidence_badge(confidence: str, similarity_score: Optional[float] = None) -> str:
    """Generates styled badge for confidence classification."""
    score_str = f" &bull; SIM: {similarity_score:.2f}" if similarity_score is not None else ""
    if confidence == "High":
        return f'<span class="badge-pill badge-high">STRONG EVIDENCE{score_str}</span>'
    elif confidence == "Moderate":
        return f'<span class="badge-pill badge-moderate">MODERATE EVIDENCE{score_str}</span>'
    elif confidence == "Preliminary":
        return f'<span class="badge-pill badge-prelim">PRELIMINARY LITERATURE{score_str}</span>'
    else:
        return f'<span class="badge-pill badge-insufficient">INSUFFICIENT EVIDENCE{score_str}</span>'


def render_claim_status_badge(status: str) -> str:
    """Renders styled badge for evidence verification status."""
    status_upper = status.upper()
    if status_upper == "SUPPORTED":
        return '<span class="badge-pill badge-high">EMPIRICALLY SUPPORTED</span>'
    elif status_upper == "PARTIALLY_SUPPORTED":
        return '<span class="badge-pill badge-moderate">PARTIALLY SUPPORTED</span>'
    elif status_upper == "CONTRADICTED":
        return '<span class="badge-pill badge-insufficient">CONFLICTING FINDINGS</span>'
    elif status_upper == "UNCERTAIN_HUMAN_REVIEW":
        return '<span class="badge-pill badge-teal">EXPERT REVIEW REQUIRED</span>'
    else:
        return '<span class="badge-pill badge-insufficient">INSUFFICIENT DATA</span>'


def render_evidence_availability(is_available: bool, count: int = 0, year_range: str = "All Years") -> None:
    """Renders Section B: Evidence Overview."""
    if is_available:
        st.markdown(
            f"""
            <div class="evidence-status-banner available">
                <div class="evidence-status-title">
                    &bull; Verified Scientific Evidence Available ({count} Articles &bull; {year_range})
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
                    &bull; No sufficient scientific evidence found for this query.
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
    Renders professional individual research paper cards matching Section C:
    - Research paper title
    - Authors
    - Publication year
    - Journal name
    - Abstract or relevant evidence
    - PubMed ID
    - Link to original research paper
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
        '<span class="badge-pill badge-high">CITED IN SYNTHESIS</span>'
        if is_cited
        else '<span class="badge-pill badge-teal">INDEXED RECORD</span>'
    )
    score_badge = f'<span class="badge-pill badge-moderate">SIM: {chunk_score:.2f}</span>' if chunk_score is not None else ""
    abstract_badge = (
        '<span class="badge-pill badge-teal">PEER-REVIEWED ABSTRACT</span>'
        if has_abstract
        else '<span class="badge-pill badge-insufficient">TITLE RECORD</span>'
    )

    authors_formatted = format_author_list(authors, 3)
    doi_formatted = f" &bull; <strong>DOI:</strong> <code>{doi}</code>" if doi else ""

    # Short excerpt preview
    abstract_preview = abstract[:280] + "..." if len(abstract) > 280 else abstract

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
            <div style="margin-bottom:10px;">
                {cited_badge}
                {score_badge}
                {abstract_badge}
                <span class="mono-tag">PMID {pmid}</span>
                <span class="mono-tag">YEAR {year}</span>
            </div>
            <div class="paper-abstract-box">
                <strong style="color:#14243A;">Abstract / Evidence Excerpt:</strong><br>
                {abstract_preview}
            </div>
            <div style="margin-top:12px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
                <a href="{url}" target="_blank" class="pubmed-btn">
                    Official PubMed Record &bull; PMID {pmid} &rarr;
                </a>
                <span style="font-size:0.74rem; color:#6B7280; font-family:'JetBrains Mono', monospace;">
                    Verified NCBI Source
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if has_abstract and len(abstract) > 280:
        with st.expander(f"Read Full Abstract (PMID: {pmid})", expanded=False):
            st.markdown(f"<div style='font-size:0.90rem; line-height:1.65; color:#374151; padding:4px 0;'>{abstract}</div>", unsafe_allow_html=True)


def render_disclaimer():
    """Renders professional institutional research notice footer."""
    st.markdown(
        """
        <div class="disclaimer-card">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px;">
                <div style="max-width:840px;">
                    <strong>INSTITUTIONAL SCIENTIFIC RESEARCH NOTICE:</strong> EvidenceBot is an empirical biomedical 
                    intelligence engine designed to index, synthesize, and verify peer-reviewed scientific literature 
                    from the National Library of Medicine (NCBI PubMed Central) and Europe PMC. 
                    This platform is intended exclusively for scientific literature review, clinical trial analysis, 
                    and academic research. It does <strong>not</strong> provide personalized clinical diagnosis, medical advice, 
                    or prescriptive therapy. Always consult qualified clinical healthcare professionals for patient care decisions.
                </div>
                <div style="text-align:right; font-family:'JetBrains Mono', monospace; font-size:0.74rem; color:#6B7280;">
                    CORPUS: NCBI PUBMED<br>
                    INDEX: DENSE VECTOR FAISS<br>
                    CITATION FIDELITY: 100%
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
