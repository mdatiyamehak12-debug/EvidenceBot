"""
EvidenceBot - Modern Scientific AI Research Platform UI Design System
====================================================================
Inspired by ChatGPT, Perplexity, and premium modern SaaS interfaces.
Clean, spacious, minimal, elegant, and professional.

Color Palette:
- Background: Warm off-white (#F8FAFC)
- Primary text: Deep navy (#172B4D)
- Accent: Elegant teal (#168C83)
- Secondary text: Soft grey (#64748B)
- Cards: Pure white (#FFFFFF)
- Borders: Subtle grey (#E2E8F0)
"""

import streamlit as st
from typing import List, Optional, Any, Dict
from utils.helpers import format_author_list, format_pubmed_url
from utils.history_manager import load_search_history, clear_search_history

# =====================================================================
# Modern Minimalist Scientific Design System CSS
# =====================================================================

SCIENTIFIC_THEME_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global Typography & Palette */
    html, body, [class*="css"], [class*="st-"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        color: #172B4D;
    }

    /* Clean Warm Off-White Background */
    .stApp {
        background-color: #F8FAFC !important;
    }

    /* Container Spacing & Alignment (Perplexity / ChatGPT style) */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 980px !important;
        margin: 0 auto !important;
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #172B4D !important;
        font-weight: 700 !important;
        letter-spacing: -0.028em !important;
    }

    /* Hide Streamlit Default Pages Nav in Sidebar (clean custom sidebar) */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }

    /* Streamlit Header & Status Cleanup */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* =====================================================================
       Minimal Top Navigation Bar
       ===================================================================== */
    .top-nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 8px 0 24px 0;
        margin-bottom: 8px;
        border-bottom: 1px solid #EDF2F7;
    }
    .top-nav-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        text-decoration: none;
    }
    .brand-title {
        font-size: 1.25rem;
        font-weight: 800;
        color: #172B4D;
        letter-spacing: -0.03em;
        line-height: 1.1;
    }
    .brand-subtitle {
        font-size: 0.72rem;
        font-weight: 600;
        color: #168C83;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        font-family: 'JetBrains Mono', monospace;
    }

    /* =====================================================================
       Hero Section (ChatGPT / Perplexity Inspiration)
       ===================================================================== */
    .hero-container {
        text-align: center;
        padding: 50px 16px 28px 16px;
        margin: 0 auto;
        max-width: 780px;
    }
    .hero-title {
        font-size: 2.85rem !important;
        font-weight: 800 !important;
        line-height: 1.18 !important;
        color: #172B4D !important;
        letter-spacing: -0.04em !important;
        margin-bottom: 16px !important;
    }
    .hero-title span.accent {
        color: #168C83;
    }
    .hero-subtitle {
        font-size: 1.12rem;
        font-weight: 400;
        color: #64748B;
        line-height: 1.6;
        margin: 0 auto 34px auto;
        max-width: 620px;
    }

    /* =====================================================================
       Prominent Search Box (Perplexity-Style Elevated Container)
       ===================================================================== */
    .search-card-wrapper {
        background: #FFFFFF;
        border-radius: 18px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 24px -2px rgba(23, 43, 77, 0.07), 0 2px 6px -1px rgba(23, 43, 77, 0.04);
        padding: 10px 14px 10px 18px;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 18px;
    }
    .search-card-wrapper:focus-within {
        border-color: #168C83;
        box-shadow: 0 0 0 3px rgba(22, 140, 131, 0.14), 0 8px 30px -4px rgba(23, 43, 77, 0.10);
    }

    /* Streamlit text input & text area inside custom search */
    .stTextArea textarea, .stTextInput input {
        border: none !important;
        box-shadow: none !important;
        background: transparent !important;
        font-size: 1.05rem !important;
        color: #172B4D !important;
        line-height: 1.5 !important;
        padding: 6px 0 !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border: none !important;
        box-shadow: none !important;
    }
    .stTextArea textarea::placeholder, .stTextInput input::placeholder {
        color: #94A3B8 !important;
        font-weight: 400 !important;
    }

    /* Example Query Chips (Subtle, Clean) */
    .example-chips-container {
        display: flex;
        align-items: center;
        justify-content: center;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 14px;
        margin-bottom: 24px;
    }
    .example-chip-label {
        font-size: 0.80rem;
        color: #64748B;
        font-weight: 500;
        margin-right: 4px;
    }

    /* Primary & Secondary Action Buttons */
    div.stButton > button[kind="primary"] {
        background-color: #168C83 !important;
        color: #FFFFFF !important;
        border: 1px solid #168C83 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        border-radius: 12px !important;
        padding: 0.55rem 1.4rem !important;
        box-shadow: 0 2px 8px rgba(22, 140, 131, 0.20) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #137870 !important;
        border-color: #137870 !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 14px rgba(22, 140, 131, 0.30) !important;
    }

    div.stButton > button[kind="secondary"] {
        background-color: #FFFFFF !important;
        color: #64748B !important;
        border: 1px solid #E2E8F0 !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        border-radius: 10px !important;
        padding: 0.45rem 1.0rem !important;
        transition: all 0.15s ease !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        background-color: #F8FAFC !important;
        border-color: #CBD5E1 !important;
        color: #172B4D !important;
    }

    /* =====================================================================
       Minimal, Sleek Left Sidebar (ChatGPT-style Recent Inquiries)
       ===================================================================== */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
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
        color: #172B4D !important;
    }
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] div {
        color: #475569;
    }
    [data-testid="stSidebar"] .stButton > button {
        background-color: #FFFFFF !important;
        border: 1px solid #EDF2F7 !important;
        color: #172B4D !important;
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
        background-color: #F1F5F9 !important;
        border-color: #CBD5E1 !important;
        color: #168C83 !important;
    }

    /* Sidebar "New Research" Button */
    .sidebar-new-btn button {
        background-color: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
        color: #172B4D !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        border-radius: 10px !important;
        padding: 9px 14px !important;
    }
    .sidebar-new-btn button:hover {
        background-color: #EBF8F7 !important;
        border-color: #99E3DD !important;
        color: #168C83 !important;
    }

    .empty-history-text {
        color: #94A3B8;
        font-size: 0.82rem;
        padding: 12px;
        text-align: center;
        background: #F8FAFC;
        border-radius: 8px;
        border: 1px dashed #E2E8F0;
        margin: 8px 0;
    }

    /* =====================================================================
       Search Results Interface Cards
       ===================================================================== */
    /* Target Inquiry Banner */
    .query-header-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 18px 22px;
        margin-bottom: 22px;
        box-shadow: 0 2px 10px rgba(23, 43, 77, 0.04);
    }
    .query-header-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 700;
        color: #168C83;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 4px;
    }
    .query-header-text {
        font-size: 1.30rem;
        font-weight: 700;
        color: #172B4D;
        line-height: 1.35;
        letter-spacing: -0.02em;
    }

    /* AI Research Synthesis Card */
    .synthesis-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px -2px rgba(23, 43, 77, 0.05);
        line-height: 1.75;
        font-size: 1.02rem;
        color: #172B4D;
    }
    .synthesis-card h3 {
        font-size: 1.15rem !important;
        color: #172B4D !important;
        margin-top: 22px !important;
        margin-bottom: 10px !important;
        font-weight: 700 !important;
    }
    .synthesis-card h3:first-child {
        margin-top: 0 !important;
    }

    /* Retrieved Research Paper Card */
    .paper-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 22px 26px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(23, 43, 77, 0.03);
        transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
    }
    .paper-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px -4px rgba(23, 43, 77, 0.08);
        border-color: #CBD5E1;
    }
    .paper-title {
        font-weight: 700;
        font-size: 1.08rem;
        color: #172B4D;
        line-height: 1.45;
        margin-bottom: 8px;
    }
    .paper-title a {
        color: #172B4D !important;
        text-decoration: none;
    }
    .paper-title a:hover {
        color: #168C83 !important;
        text-decoration: underline;
    }
    .paper-meta {
        font-size: 0.86rem;
        color: #64748B;
        margin-bottom: 12px;
        line-height: 1.6;
    }
    .paper-meta strong {
        color: #172B4D;
    }
    .paper-excerpt-box {
        background: #F8FAFC;
        border: 1px solid #EDF2F7;
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 0.88rem;
        color: #334155;
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
        background-color: #EBF8F7;
        color: #168C83;
        border: 1px solid #99E3DD;
    }
    .pill-high {
        background-color: #ECFDF5;
        color: #047857;
        border: 1px solid #A7F3D0;
    }
    .pill-moderate {
        background-color: #FFFBEB;
        color: #B45309;
        border: 1px solid #FDE68A;
    }
    .pill-insufficient {
        background-color: #FEF2F2;
        color: #B91C1C;
        border: 1px solid #FECACA;
    }

    /* Abstention Notice */
    .abstention-alert {
        background: #FFFFFF;
        border: 1px solid #FECACA;
        border-left: 4px solid #DC2626;
        border-radius: 14px;
        padding: 22px 26px;
        margin-bottom: 20px;
        box-shadow: 0 2px 12px rgba(220, 38, 38, 0.05);
    }
    .abstention-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #991B1B;
        margin-bottom: 8px;
    }
    .abstention-desc {
        color: #475569;
        font-size: 0.92rem;
        line-height: 1.65;
        margin: 0;
    }

    /* Minimalist Footer */
    .minimal-footer {
        text-align: center;
        padding-top: 40px;
        padding-bottom: 20px;
        font-size: 0.78rem;
        color: #94A3B8;
        line-height: 1.6;
        border-top: 1px solid #EDF2F7;
        margin-top: 48px;
    }
</style>
"""


def apply_theme():
    """Applies the warm off-white, deep navy, and elegant teal modern design theme."""
    st.markdown(SCIENTIFIC_THEME_CSS, unsafe_allow_html=True)


def render_brand_logo_svg() -> str:
    """Returns a clean, modern minimalist SVG logo for Bio EvidenceBot."""
    return """
    <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="32" height="32" rx="8" fill="#168C83"/>
        <circle cx="16" cy="16" r="9" stroke="#FFFFFF" stroke-width="1.8" stroke-dasharray="2 2"/>
        <path d="M10 16C10 12.686 12.686 10 16 10C19.314 10 22 12.686 22 16C22 19.314 19.314 22 16 22" stroke="#FFFFFF" stroke-width="1.8" stroke-linecap="round"/>
        <circle cx="16" cy="16" r="2.8" fill="#FFFFFF"/>
    </svg>
    """


def render_top_nav():
    """
    Renders clean top navigation:
    - Left: EvidenceBot branding and subtitle
    - Right: Clean minimal About modal trigger
    """
    col_left, col_right = st.columns([4, 1.2])
    with col_left:
        st.markdown(
            f"""
            <div style="display:flex; align-items:center; gap:12px; padding: 6px 0;">
                {render_brand_logo_svg()}
                <div>
                    <div style="font-size:1.20rem; font-weight:800; color:#172B4D; letter-spacing:-0.03em; line-height:1.15;">
                        EvidenceBot
                    </div>
                    <div style="font-size:0.72rem; color:#64748B; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; font-family:'JetBrains Mono', monospace;">
                        AI Research Assistant
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
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


def render_sidebar():
    """
    Renders minimal, uncluttered left sidebar for Recent Searches.
    - 'New Research' button at top
    - List of recent searches (latest first)
    - Clicking any item reopens that search
    - Small clear history button
    """
    with st.sidebar:
        st.markdown(
            f"""
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:14px; padding-bottom:12px; border-bottom:1px solid #EDF2F7;">
                {render_brand_logo_svg()}
                <div>
                    <div style="font-size:1.05rem; font-weight:700; color:#172B4D; line-height:1.2;">EvidenceBot</div>
                    <div style="font-size:0.70rem; color:#64748B; font-family:'JetBrains Mono', monospace;">Research History</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
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
                st.markdown(
                    f"<div style='font-size:0.72rem; color:#94A3B8; text-align:right; padding-top:6px; font-family:\"JetBrains Mono\", monospace;'>"
                    f"{len(recent_searches)} queries"
                    f"</div>",
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                """
                <div class="empty-history-text">
                    No recent searches yet.<br>
                    Your research questions will appear here.
                </div>
                """,
                unsafe_allow_html=True
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
        st.markdown(
            f"""
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-left:4px solid #168C83; border-radius:12px; padding:14px 20px; margin-bottom:18px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
                <div style="font-weight:700; color:#172B4D; font-size:0.95rem;">
                    Scientific Evidence Available &bull; <span style="color:#168C83;">{count} Peer-Reviewed Publication(s)</span>
                </div>
                <div style="font-size:0.78rem; font-family:'JetBrains Mono', monospace; color:#64748B;">
                    CORPUS: NCBI PUBMED
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_paper_card(paper: Any, is_cited: bool = False):
    """
    Renders an individual research paper in a clean white card.
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

    st.markdown(
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
                    <a href="{pubmed_url}" target="_blank" style="font-size:0.80rem; color:#168C83; text-decoration:none; font-weight:600; margin-left:8px;">
                        Open on PubMed ↗
                    </a>
                </div>
            </div>
            <div class="paper-excerpt-box">
                {abstract_clean}
            </div>
        </div>
        """,
        unsafe_allow_html=True
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
    st.markdown(
        """
        <div class="minimal-footer">
            EvidenceBot synthesizes peer-reviewed literature indexed on NCBI PubMed Central and Europe PMC for research and educational exploration.<br>
            Strict deterministic citation verification enforced. Not clinical advice.
        </div>
        """,
        unsafe_allow_html=True
    )
