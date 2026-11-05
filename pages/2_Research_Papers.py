"""
Bio EvidenceBot - Literature Explorer (Page 2)
==============================================
Presents detailed research paper cards retrieved from PubMed & Europe PMC,
including titles, authors, journals, DOIs, abstracts, and official links.
Supports custom publication year range filtering and article volume limits.
"""

import streamlit as st
from utils.ui_components import (
    apply_theme,
    render_sidebar,
    render_paper_card,
    render_disclaimer,
)
from utils.history_manager import add_to_history
from backend.pubmed import PubMedRetriever

st.set_page_config(
    page_title="EvidenceBot – Literature Explorer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply unified styling and sidebar
apply_theme()
render_sidebar(current_page="Literature Explorer")

CURRENT_YEAR = 2026

# Page Header Card
st.markdown(
    """
    <div class="dashboard-header">
        <div class="header-eyebrow">PUBMED & EUROPE PMC &bull; DATABASE EXPLORER &bull; METADATA INGESTION</div>
        <h1 style="font-size: 1.85rem !important;">Literature Explorer</h1>
        <div class="header-tagline">Peer-Reviewed Research Repository</div>
        <p class="header-subtitle">Explore peer-reviewed scientific publications, clinical trial records, and journal metadata directly from the National Library of Medicine.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Retrieve any query passed from sidebar or home
prefill = st.session_state.pop("query_to_run", None)
if prefill:
    st.session_state["papers_explorer_query"] = prefill

current_query_val = st.session_state.get("papers_explorer_query", "")

# =====================================================================
# 1. Search Query Input Box
# =====================================================================
st.markdown(
    """
    <div style="font-size:0.90rem; font-weight:700; color:#14243A; margin-bottom:6px;">
        Literature Search Keywords or Clinical Topics
    </div>
    """,
    unsafe_allow_html=True
)

col_s1, col_s2 = st.columns([4, 1.2])
with col_s1:
    search_term = st.text_input(
        "Enter keywords, diseases, therapies, or gene targets:",
        value=current_query_val,
        placeholder="e.g., crispr cas9 sickle cell disease trial, zinc cold severity",
        label_visibility="collapsed"
    )
with col_s2:
    search_btn = st.button("🔍 Search PubMed", type="primary", use_container_width=True)

# =====================================================================
# 2. Collapsible Advanced Research Filters
# =====================================================================
with st.expander("⚙️ Advanced Research Filters", expanded=False):
    st.caption("Customise publication year range, paper retrieval volume, and article study design:")

    col_f1, col_f2 = st.columns([2.2, 1.8])

    with col_f1:
        st.markdown("**Publication Year Range**")
        col_y_start, col_y_end = st.columns(2)
        with col_y_start:
            starting_year = st.number_input(
                "Starting Publication Year",
                min_value=1800,
                max_value=2030,
                value=int(st.session_state.get("exp_start_year_val", 1900)),
                step=1,
                key="exp_start_year",
                help="Type any valid starting 4-digit year (e.g., 1985, 2000, 2015)."
            )
        with col_y_end:
            ending_year = st.number_input(
                "Ending Publication Year",
                min_value=1800,
                max_value=2030,
                value=int(st.session_state.get("exp_end_year_val", CURRENT_YEAR)),
                step=1,
                key="exp_end_year",
                help="Type any valid ending 4-digit year (e.g., 1995, 2010, 2026)."
            )

        if st.button("Set to All Years (1900–2026)", key="exp_btn_all_years", type="secondary"):
            st.session_state["exp_start_year_val"] = 1900
            st.session_state["exp_end_year_val"] = CURRENT_YEAR
            st.rerun()

    with col_f2:
        st.markdown("**Article Limit & Type**")
        col_lim, col_typ = st.columns(2)
        with col_lim:
            max_papers = st.number_input(
                "Maximum Papers to Retrieve",
                min_value=1,
                max_value=100,
                value=int(st.session_state.get("exp_max_papers_val", 10)),
                step=5,
                key="exp_max_papers",
                help="Controls the number of PubMed records to fetch (e.g., 5, 10, 20, 50, 100)."
            )
        with col_typ:
            article_type_choice = st.selectbox(
                "Article Type Filter",
                options=[
                    "All Article Types",
                    "Clinical Trial",
                    "Randomized Controlled Trial",
                    "Meta-Analysis / Systematic Review",
                    "Review Article"
                ],
                index=0,
                key="exp_article_type",
                help="Filter candidate PubMed publications by study design."
            )

# Year validation
year_validation_error = False
if starting_year > ending_year:
    st.error(f"⚠️ Validation Error: Starting Publication Year ({starting_year}) cannot be greater than Ending Publication Year ({ending_year}). Please correct the range.")
    year_validation_error = True

is_all_years = (starting_year <= 1900 and ending_year >= CURRENT_YEAR)
active_year_label = "All Years (1900–2026)" if is_all_years else f"{starting_year}–{ending_year}"

# =====================================================================
# 3. Execution & Retrieval
# =====================================================================
display_papers = []
cited_pmids_set = set()

auto_search = bool(prefill and prefill.strip())
should_search = (search_btn or auto_search) and not year_validation_error

if should_search and search_term.strip():
    clean_term = search_term.strip()
    st.session_state["papers_explorer_query"] = clean_term
    st.session_state["exp_start_year_val"] = starting_year
    st.session_state["exp_end_year_val"] = ending_year
    st.session_state["exp_max_papers_val"] = max_papers

    add_to_history(clean_term, year_range=active_year_label)

    with st.spinner(f"Retrieving up to {max_papers} PubMed papers for '{clean_term}' ({active_year_label})..."):
        retriever = PubMedRetriever()
        q_min = starting_year if not is_all_years else None
        q_max = ending_year if not is_all_years else None
        q_type = article_type_choice if article_type_choice != "All Article Types" else None

        search_res = retriever.retrieve(
            clean_term,
            max_results=int(max_papers),
            min_year=q_min,
            max_year=q_max,
            article_type=q_type
        )

        display_papers = search_res.papers
        st.session_state["papers_explorer_cache"] = display_papers
        st.session_state["papers_explorer_query"] = clean_term
        st.session_state["papers_explorer_year"] = active_year_label

        if not display_papers:
            st.warning(f"No peer-reviewed publications matching \"{clean_term}\" ({active_year_label}) were found on PubMed.")

elif "papers_explorer_cache" in st.session_state:
    display_papers = st.session_state["papers_explorer_cache"]
    q_name = st.session_state.get("papers_explorer_query", "")
    yr_cached = st.session_state.get("papers_explorer_year", active_year_label)
    st.info(f"Showing cached PubMed publications for inquiry: \"{q_name}\" ({yr_cached})")

elif "latest_result" in st.session_state and st.session_state["latest_result"].get("papers"):
    display_papers = st.session_state["latest_result"]["papers"]
    cited_pmids_set = set(st.session_state["latest_result"].get("verified_pmids", []))
    last_q = st.session_state.get("latest_question", "")
    st.info(f"Showing {len(display_papers)} publications retrieved from recent inquiry: \"{last_q}\"")

# =====================================================================
# 4. Display Paper Cards
# =====================================================================
if display_papers:
    st.markdown(f"### Retrieved Publications ({len(display_papers)} Records)")
    st.caption(f"Peer-reviewed records matching search criteria ({active_year_label}):")
    for paper in display_papers:
        is_cited = paper.pmid in cited_pmids_set
        render_paper_card(paper, is_cited=is_cited)
else:
    st.markdown("---")
    st.markdown(
        """
        <div class="content-card" style="text-align:center; padding:32px;">
            <div style="font-size:1.1rem; font-weight:700; color:#14243A; margin-bottom:6px;">No Papers Loaded Yet</div>
            <div style="font-size:0.90rem; color:#6B7280; max-width:550px; margin:0 auto;">
                Enter a scientific keyword, clinical trial topic, or disease name in the search box above to retrieve records directly from the National Library of Medicine.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

render_disclaimer()
