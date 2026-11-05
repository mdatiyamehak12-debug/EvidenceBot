"""
EvidenceBot - Premium Scientific AI Research Platform UI Design System
========================================================================
Premium Dark Theme Palette:
- Main background: #0B1120
- Secondary background: #111827
- Cards: #172033
- Primary text: #F8FAFC
- Secondary text: #94A3B8
- Accent teal: #2DD4BF
- Borders: #263449

Uses textwrap.dedent on all HTML to prevent CommonMark from rendering raw HTML/CSS as code blocks.
"""

import streamlit as st
import textwrap
from typing import List, Optional, Any, Dict
from utils.helpers import format_author_list, format_pubmed_url
from utils.history_manager import load_search_history, clear_search_history


def render_html(html_str: str):
    """
    Renders HTML cleanly using Streamlit markdown.
    Applies textwrap.dedent and strips leading/trailing whitespace
    so that CommonMark NEVER treats indented HTML lines as code blocks.
    """
    st.markdown(textwrap.dedent(html_str).strip(), unsafe_allow_html=True)


# =====================================================================
# Premium Dark Theme CSS
# =====================================================================

DARK_THEME_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global Typography & Palette */
    html, body, [class*="css"], [class*="st-"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        color: #F8FAFC;
    }

    /* Main Dark Background */
    .stApp {
        background-color: #0B1120 !important;
    }

    /* Container Spacing & Alignment */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 960px !important;
        margin: 0 auto !important;
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #F8FAFC !important;
        font-weight: 700 !important;
        letter-spacing: -0.028em !important;
    }

    /* Hide Streamlit Default Pages Navigation in Sidebar */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }

    /* Streamlit Header Cleanup */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Top Navigation Bar */
    .top-nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 6px 0 20px 0;
        margin-bottom: 6px;
        border-bottom: 1px solid #263449;
    }

    /* Hero Section */
    .hero-container {
        text-align: center;
        padding: 44px 16px 26px 16px;
        margin: 0 auto;
        max-width: 780px;
    }
    .hero-eyebrow {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.80rem;
        font-weight: 700;
        color: #2DD4BF;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-bottom: 12px;
    }
    .hero-title {
        font-size: 2.85rem !important;
        font-weight: 800 !important;
        line-height: 1.18 !important;
        color: #F8FAFC !important;
        letter-spacing: -0.04em !important;
        margin-bottom: 14px !important;
    }
    .hero-title span.accent {
        color: #2DD4BF;
    }
    .hero-subtitle {
        font-size: 1.12rem;
        font-weight: 400;
        color: #94A3B8;
        line-height: 1.6;
        margin: 0 auto 28px auto;
        max-width: 620px;
    }

    /* Native Textarea Styled as Elevated Dark Search Input */
    .stTextArea textarea {
        background-color: #172033 !important;
        border: 1px solid #263449 !important;
        border-radius: 16px !important;
        color: #F8FAFC !important;
        font-size: 1.05rem !important;
        padding: 16px 20px !important;
        line-height: 1.55 !important;
        box-shadow: 0 4px 24px -2px rgba(0, 0, 0, 0.45) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .stTextArea textarea:focus {
        border-color: #2DD4BF !important;
        box-shadow: 0 0 0 3px rgba(45, 212, 191, 0.20), 0 8px 32px -4px rgba(0, 0, 0, 0.6) !important;
    }
    .stTextArea textarea::placeholder {
        color: #64748B !important;
    }

    /* Primary & Secondary Buttons */
    div.stButton > button[kind="primary"] {
        background-color: #2DD4BF !important;
        color: #0B1120 !important;
        border: 1px solid #2DD4BF !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        border-radius: 12px !important;
        padding: 0.58rem 1.4rem !important;
        box-shadow: 0 2px 10px rgba(45, 212, 191, 0.25) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #14B8A6 !important;
        border-color: #14B8A6 !important;
        color: #0B1120 !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 18px rgba(45, 212, 191, 0.45) !important;
    }

    div.stButton > button[kind="secondary"] {
        background-color: #172033 !important;
        color: #94A3B8 !important;
        border: 1px solid #263449 !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        border-radius: 10px !important;
        padding: 0.48rem 1.1rem !important;
        transition: all 0.15s ease !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        background-color: #1E293B !important;
        border-color: #2DD4BF !important;
        color: #2DD4BF !important;
    }

    /* Popover in Dark Mode */
    [data-testid="stPopover"] > button {
        background-color: #172033 !important;
        border: 1px solid #263449 !important;
        color: #94A3B8 !important;
        border-radius: 10px !important;
    }
    [data-testid="stPopover"] > button:hover {
        border-color: #2DD4BF !important;
        color: #2DD4BF !important;
    }
    [data-testid="stPopoverBody"] {
        background-color: #172033 !important;
        border: 1px solid #263449 !important;
        color: #F8FAFC !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
    }

    /* Sleek Dark Left Sidebar */
    [data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 1px solid #263449 !important;
        padding-top: 1rem !important;
    }
    [data-testid="stSidebar"] .block-container {
        padding-top: 1rem !important;
        padding-left: 1.1rem !important;
        padding-right: 1.1rem !important;
    }
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #F8FAFC !important;
    }
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] div {
        color: #94A3B8;
    }
    [data-testid="stSidebar"] .stButton > button {
        background-color: #172033 !important;
        border: 1px solid #263449 !important;
        color: #F8FAFC !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        text-align: left !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        transition: all 0.15s ease !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        display: block !important;
        width: 100% !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: #1E293B !important;
        border-color: #2DD4BF !important;
        color: #2DD4BF !important;
    }

    .empty-history-text {
        color: #64748B;
        font-size: 0.82rem;
        padding: 12px;
        text-align: center;
        background: #172033;
        border-radius: 8px;
        border: 1px dashed #263449;
        margin: 8px 0;
    }

    /* Search Results Cards */
    .query-header-card {
        background: #172033;
        border: 1px solid #263449;
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
    }
    .query-header-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.74rem;
        font-weight: 700;
        color: #2DD4BF;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 4px;
    }
    .query-header-text {
        font-size: 1.25rem;
        font-weight: 700;
        color: #F8FAFC;
        line-height: 1.4;
    }

    /* AI Research Synthesis Card */
    .synthesis-card {
        background: #172033;
        border: 1px solid #263449;
        border-left: 4px solid #2DD4BF;
        border-radius: 14px;
        padding: 28px 32px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
        line-height: 1.8;
        font-size: 1.02rem;
        color: #F8FAFC;
    }
    .synthesis-card h3 {
        font-size: 1.15rem !important;
        color: #F8FAFC !important;
        margin-top: 22px !important;
        margin-bottom: 10px !important;
        font-weight: 700 !important;
        border-bottom: 1px solid #263449;
        padding-bottom: 6px;
    }
    .synthesis-card h3:first-child {
        margin-top: 0 !important;
    }
    .synthesis-card p {
        color: #E2E8F0;
        margin-bottom: 12px;
    }

    /* Retrieved Research Paper Card */
    .paper-card {
        background: #172033;
        border: 1px solid #263449;
        border-radius: 14px;
        padding: 22px 26px;
        margin-bottom: 16px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.25);
        transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
    }
    .paper-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45);
        border-color: #2DD4BF;
    }
    .paper-title {
        font-weight: 700;
        font-size: 1.08rem;
        color: #F8FAFC;
        line-height: 1.45;
        margin-bottom: 8px;
    }
    .paper-title a {
        color: #F8FAFC !important;
        text-decoration: none;
    }
    .paper-title a:hover {
        color: #2DD4BF !important;
        text-decoration: underline;
    }
    .paper-meta {
        font-size: 0.86rem;
        color: #94A3B8;
        margin-bottom: 12px;
        line-height: 1.6;
    }
    .paper-meta strong {
        color: #F8FAFC;
    }
    .paper-excerpt-box {
        background: #111827;
        border: 1px solid #263449;
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 0.88rem;
        color: #CBD5E1;
        line-height: 1.65;
        margin-top: 10px;
    }

    /* Badges & Status Pills */
    .pill-badge {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.74rem;
        font-weight: 600;
        letter-spacing: 0.03em;
        font-family: 'JetBrains Mono', monospace;
    }
    .pill-teal {
        background-color: rgba(45, 212, 191, 0.12);
        color: #2DD4BF;
        border: 1px solid rgba(45, 212, 191, 0.35);
    }
    .pill-high {
        background-color: rgba(16, 185, 129, 0.12);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.35);
    }
    .pill-moderate {
        background-color: rgba(245, 158, 11, 0.12);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.35);
    }
    .pill-insufficient {
        background-color: rgba(239, 68, 68, 0.12);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.35);
    }

    /* Abstention Notice */
    .abstention-alert {
        background: #172033;
        border: 1px solid rgba(239, 68, 68, 0.4);
        border-left: 4px solid #EF4444;
        border-radius: 14px;
        padding: 24px 28px;
        margin-bottom: 22px;
        box-shadow: 0 4px 20px rgba(239, 68, 68, 0.10);
    }
    .abstention-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #F87171;
        margin-bottom: 8px;
    }
    .abstention-desc {
        color: #94A3B8;
        font-size: 0.92rem;
        line-height: 1.65;
        margin: 0;
    }

    /* Loading status widget styling */
    [data-testid="stStatusWidget"] {
        background-color: #172033 !important;
        border: 1px solid #263449 !important;
        color: #F8FAFC !important;
        border-radius: 12px !important;
    }
    [data-testid="stStatusWidget"] * {
        color: #F8FAFC !important;
    }

    /* Minimalist Footer */
    .minimal-footer {
        text-align: center;
        padding-top: 40px;
        padding-bottom: 24px;
        font-size: 0.78rem;
        color: #64748B;
        line-height: 1.6;
        border-top: 1px solid #263449;
        margin-top: 48px;
    }
</style>
"""


def apply_theme():
    """Applies the premium dark theme with teal accents."""
    render_html(DARK_THEME_CSS)


def render_brand_logo_svg() -> str:
    """Returns a clean, modern minimalist SVG logo for Bio EvidenceBot."""
    return (
        '<svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">'
        '<rect width="32" height="32" rx="8" fill="#2DD4BF"/>'
        '<circle cx="16" cy="16" r="9" stroke="#0B1120" stroke-width="1.8" stroke-dasharray="2 2"/>'
        '<path d="M10 16C10 12.686 12.686 10 16 10C19.314 10 22 12.686 22 16C22 19.314 19.314 22 16 22" stroke="#0B1120" stroke-width="1.8" stroke-linecap="round"/>'
        '<circle cx="16" cy="16" r="2.8" fill="#0B1120"/>'
        '</svg>'
    )


def render_top_nav():
    """
    Renders clean top navigation:
    - Left: EvidenceBot branding and subtitle
    - Right: Clean minimal About modal trigger
    """
    col_left, col_right = st.columns([4, 1.2])
    with col_left:
        render_html(
            f"""
            <div style="display:flex; align-items:center; gap:12px; padding: 6px 0;">
                {render_brand_logo_svg()}
                <div>
                    <div style="font-size:1.20rem; font-weight:800; color:#F8FAFC; letter-spacing:-0.03em; line-height:1.15;">
                        EVIDENCEBOT
                    </div>
                    <div style="font-size:0.72rem; color:#2DD4BF; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; font-family:'JetBrains Mono', monospace;">
                        AI Research Assistant
                    </div>
                </div>
            </div>
            """
        )
    with col_right:
        with st.popover("About", use_container_width=True):
            st.markdown(
                """
                ### About EvidenceBot
                **EvidenceBot** is an AI-powered scientific research assistant designed for exploring biomedical literature and clinical evidence.
                
                - **Data Source:** Live programmatic connection to the National Library of Medicine (NCBI PubMed) & Europe PMC.
                - **Dense Vector Search:** In-memory FAISS vector indexing with 768-dim SentenceTransformers embeddings.
                - **Anti-Hallucination:** Answers are strictly grounded in retrieved peer-reviewed abstracts with verified PubMed PMIDs.
                - **Empirical Abstention:** Actively withholds conclusions when evidence is absent, conflicting, or insufficient.
                
                *For academic research and scientific inquiry. Not personal medical advice.*
                """
            )


def render_sidebar(current_page: str = "Home"):
    """
    Renders minimal, uncluttered dark left sidebar for Recent Searches.
    - 'New Research' button at top
    - List of recent searches (latest first)
    - Clicking any item reopens that search
    - Small clear history button
    """
    with st.sidebar:
        render_html(
            f"""
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:14px; padding-bottom:12px; border-bottom:1px solid #263449;">
                {render_brand_logo_svg()}
                <div>
                    <div style="font-size:1.05rem; font-weight:700; color:#F8FAFC; line-height:1.2;">EVIDENCEBOT</div>
                    <div style="font-size:0.70rem; color:#2DD4BF; font-family:'JetBrains Mono', monospace;">Research History</div>
                </div>
            </div>
            """
        )

        # "New Research" button
        if st.button("➕ New Research", key="sidebar_new_btn", use_container_width=True):
            st.session_state["active_query"] = ""
            st.session_state.pop("latest_result", None)
            st.session_state.pop("latest_question", None)
            st.rerun()

        st.markdown("<div style='margin-bottom:14px;'></div>", unsafe_allow_html=True)
        st.caption("RECENT SEARCHES")

        recent_searches = load_search_history()

        if recent_searches:
            for idx, item in enumerate(recent_searches[:10]):
                q_text = item.get("query", "")
                display_label = q_text[:30] + "..." if len(q_text) > 30 else q_text

                if st.button(f"🔍 {display_label}", key=f"hist_btn_{idx}", use_container_width=True):
                    st.session_state["active_query"] = q_text
                    st.session_state["query_to_run"] = q_text
                    st.rerun()

            st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)
            col_c1, col_c2 = st.columns([1.2, 1])
            with col_c1:
                if st.button("Clear History", key="btn_clear_hist", type="secondary", use_container_width=True):
                    clear_search_history()
                    st.rerun()
            with col_c2:
                render_html(
                    f"""
                    <div style="font-size:0.72rem; color:#64748B; text-align:right; padding-top:6px; font-family:'JetBrains Mono', monospace;">
                        {len(recent_searches)} queries
                    </div>
                    """
                )
        else:
            render_html(
                """
                <div class="empty-history-text">
                    No recent searches yet.<br>
                    Your research questions will appear here.
                </div>
                """
            )


def render_confidence_badge(confidence: str, similarity_score: Optional[float] = None) -> str:
    """Returns styled minimal badge for confidence level."""
    score_str = f" &bull; {similarity_score:.2f}" if similarity_score is not None else ""
    c_lower = confidence.lower()
    if "high" in c_lower:
        return f'<span class="pill-badge pill-high">● High Reliability{score_str}</span>'
    elif "moderate" in c_lower:
        return f'<span class="pill-badge pill-moderate">● Moderate Evidence{score_str}</span>'
    else:
        return f'<span class="pill-badge pill-insufficient">● Preliminary / Sparse{score_str}</span>'


def render_evidence_availability(is_available: bool, count: int = 0, year_range: str = "All Years"):
    """Renders clean evidence overview banner."""
    if is_available and count > 0:
        render_html(
            f"""
            <div style="background:#172033; border:1px solid #263449; border-left:4px solid #2DD4BF; border-radius:12px; padding:14px 20px; margin-bottom:18px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
                <div style="font-weight:700; color:#F8FAFC; font-size:0.95rem;">
                    Scientific Evidence Available &bull; <span style="color:#2DD4BF;">{count} Peer-Reviewed Publication(s)</span>
                </div>
                <div style="font-size:0.78rem; font-family:'JetBrains Mono', monospace; color:#94A3B8;">
                    CORPUS: NCBI PUBMED
                </div>
            </div>
            """
        )


def render_paper_card(paper: Any, is_cited: bool = False):
    """
    Renders an individual research paper in a clean dark card.
    Contains:
    - Research paper title (clickable link to PubMed)
    - Authors
    - Publication year
    - Journal name
    - Abstract or relevant evidence
    - PubMed ID
    - Direct original research link
    """
    authors_formatted = format_author_list(paper.authors, max_authors=4)
    pubmed_url = format_pubmed_url(paper.pmid)
    year_str = str(paper.year) if paper.year else "N/A"
    journal_str = paper.journal if paper.journal else "Biomedical Literature"
    
    cited_badge = '<span class="pill-badge pill-teal" style="font-size:0.70rem; margin-left:6px;">VERIFIED CITATION</span>' if is_cited else ''

    abstract_clean = paper.abstract.strip() if paper.abstract else "No structured abstract summary provided in NCBI PubMed database records."
    if len(abstract_clean) > 450:
        abstract_clean = abstract_clean[:450] + "..."

    doi_elem = f" &bull; DOI: {paper.doi}" if getattr(paper, "doi", None) else ""

    render_html(
        f"""
        <div class="paper-card">
            <div class="paper-title">
                <a href="{pubmed_url}" target="_blank">{paper.title}</a>
            </div>
            <div class="paper-meta">
                <strong>{authors_formatted}</strong> &bull; <em>{journal_str}</em> ({year_str}){doi_elem}
                <div style="margin-top:6px; display:flex; align-items:center; gap:6px; flex-wrap:wrap;">
                    <span class="pill-badge pill-teal">PMID: {paper.pmid}</span>
                    {cited_badge}
                    <a href="{pubmed_url}" target="_blank" style="font-size:0.80rem; color:#2DD4BF; text-decoration:none; font-weight:600; margin-left:8px;">
                        Open on PubMed ↗
                    </a>
                </div>
            </div>
            <div class="paper-excerpt-box">
                {abstract_clean}
            </div>
        </div>
        """
    )


def render_claim_status_badge(status: str) -> str:
    """Renders claim status pill."""
    status_clean = status.upper().replace("_", " ")
    if "SUPPORTED" in status_clean and "PARTIALLY" not in status_clean:
        return f'<span class="pill-badge pill-high">✓ {status_clean}</span>'
    elif "PARTIALLY" in status_clean:
        return f'<span class="pill-badge pill-moderate">~ {status_clean}</span>'
    else:
        return f'<span class="pill-badge pill-insufficient">✗ {status_clean}</span>'


def render_disclaimer():
    """Renders minimal institutional disclaimer at the footer."""
    render_html(
        """
        <div class="minimal-footer">
            EvidenceBot synthesizes peer-reviewed literature indexed on NCBI PubMed Central and Europe PMC for research and educational exploration.<br>
            Strict deterministic citation verification enforced. Not clinical advice.
        </div>
        """
    )
