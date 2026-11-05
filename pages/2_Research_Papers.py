"""
EvidenceBot - Page 2: Literature Explorer
=========================================
Presents detailed research paper cards retrieved from PubMed & Europe PMC,
including titles, authors, journals, DOIs, abstracts, and official links.
Supports custom publication year range filtering.
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

# Page Header
st.markdown(
    """
    <div style="margin-bottom: 22px;">
        <div style="margin-bottom:6px;">
            <span class="mono-tag" style="color:#0f766e; background:#f0fdfa; border:1px solid #99f6e4;">
                PUBMED & EUROPE PMC DATABASE EXPLORER
            </span>
        </div>
        <h2 style="color: #0f172a; margin-bottom: 4px; font-weight:800; letter-spacing:-0.03em;">Literature Explorer</h2>
        <p style="color: #475569; margin: 0; font-size:0.98rem;">Explore peer-reviewed scientific publications, clinical trial records, and journal metadata directly from the National Library of Medicine.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Retrieve any query passed from sidebar or home
prefill = st.session_state.pop("query_to_run", None)
if prefill:
    st.session_state["papers_explorer_query"] = prefill

current_query_val = st.session_state.get("papers_explorer_query", "")

# Publication Year Filter for Explorer
col_y1, col_y2 = st.columns([1, 2])
with col_y1:
    preset_choice = st.selectbox(
        "Publication Year Preset:",
        options=[
            "All Years (1900–2026)",
            "2020–2026 (Recent 6 Years)",
            "2010–2020 (Last Decade)",
            "2000–2010 (Millennium Era)",
            "1900–2000 (Historical)",
            "Custom Range"
        ],
        index=0
    )

with col_y2:
    calc_range = (1900, CURRENT_YEAR)
    if preset_choice == "2020–2026 (Recent 6 Years)":
        calc_range = (2020, CURRENT_YEAR)
    elif preset_choice == "2010–2020 (Last Decade)":
        calc_range = (2010, 2020)
    elif preset_choice == "2000–2010 (Millennium Era)":
        calc_range = (2000, 2010)
    elif preset_choice == "1900–2000 (Historical)":
        calc_range = (1900, 2000)

    min_year_val, max_year_val = st.slider(
        "Filter by Publication Year:",
        min_value=1900,
        max_value=CURRENT_YEAR,
        value=calc_range,
        step=1
    )

year_label = f"{min_year_val}–{max_year_val}" if (min_year_val > 1900 or max_year_val < CURRENT_YEAR) else "All Years"

# Search Bar for ad-hoc queries
col_s1, col_s2 = st.columns([4, 1])
with col_s1:
    search_term = st.text_input(
        "Enter keywords, diseases, therapies, or gene targets:",
        value=current_query_val,
        placeholder="e.g., crispr cas9 sickle cell disease trial",
        label_visibility="collapsed"
    )

with col_s2:
    search_btn = st.button("Search PubMed →", type="primary", use_container_width=True)

display_papers = []
cited_pmids_set = set()

auto_search = bool(prefill and prefill.strip())

if (search_btn or auto_search) and search_term.strip():
    clean_term = search_term.strip()
    st.session_state["papers_explorer_query"] = clean_term
    add_to_history(clean_term, year_range=year_label)

    with st.spinner(f"Retrieving PubMed papers for '{clean_term}' ({year_label})..."):
        retriever = PubMedRetriever()
        q_min = min_year_val if min_year_val > 1900 else None
        q_max = max_year_val if max_year_val < CURRENT_YEAR else None
        search_res = retriever.retrieve(clean_term, max_results=10, min_year=q_min, max_year=q_max)

        display_papers = search_res.papers
        st.session_state["papers_explorer_cache"] = display_papers
        st.session_state["papers_explorer_query"] = clean_term
        st.session_state["papers_explorer_year"] = year_label

        if not display_papers:
            st.warning(f"No peer-reviewed publications matching \"{clean_term}\" ({year_label}) were found on PubMed.")

elif "papers_explorer_cache" in st.session_state:
    display_papers = st.session_state["papers_explorer_cache"]
    q_name = st.session_state.get("papers_explorer_query", "")
    yr_cached = st.session_state.get("papers_explorer_year", "All Years")
    st.info(f"Showing PubMed publications for custom search: \"{q_name}\" ({yr_cached})")

elif "latest_result" in st.session_state and st.session_state["latest_result"].get("papers"):
    display_papers = st.session_state["latest_result"]["papers"]
    cited_pmids_set = set(st.session_state["latest_result"].get("verified_pmids", []))
    last_q = st.session_state.get("latest_question", "")
    st.info(f"Showing {len(display_papers)} publications retrieved for recent inquiry: \"{last_q}\"")

if display_papers:
    st.markdown(f"### Retrieved Publications ({len(display_papers)} Records)")
    for paper in display_papers:
        is_cited = paper.pmid in cited_pmids_set
        render_paper_card(paper, is_cited=is_cited)
else:
    st.caption("No papers loaded yet. Enter a topic in the search box above or run a query on the Research Dashboard.")

render_disclaimer()
