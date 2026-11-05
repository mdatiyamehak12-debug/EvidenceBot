"""
Bio EvidenceBot - Literature Explorer (Page 2)
==============================================
Presents detailed research paper cards retrieved from PubMed & Europe PMC,
including titles, authors, journals, DOIs, abstracts, and official links.
"""

import streamlit as st
from utils.ui_components import (
    apply_theme,
    render_sidebar,
    render_paper_card,
    render_disclaimer,
    render_html,
)
from utils.history_manager import add_to_history
from backend.pubmed import PubMedRetriever

st.set_page_config(
    page_title="EvidenceBot – Literature Explorer",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply unified dark styling and sidebar
apply_theme()
render_sidebar(current_page="Literature Explorer")

# Page Header Card
render_html(
    """
    <div class="query-header-card" style="margin-bottom:20px;">
        <div class="query-header-label">PUBMED & EUROPE PMC &bull; DATABASE EXPLORER</div>
        <div class="query-header-text" style="font-size:1.6rem;">Literature Explorer</div>
        <p style="color:#94A3B8; margin:6px 0 0 0; font-size:0.95rem;">
            Explore peer-reviewed scientific publications, clinical trial records, and journal metadata directly from the National Library of Medicine.
        </p>
    </div>
    """
)

# Retrieve any query passed from sidebar or home
prefill = st.session_state.pop("query_to_run", None)
if prefill:
    st.session_state["papers_explorer_query"] = prefill

current_query_val = st.session_state.get("papers_explorer_query", "")

col_s1, col_s2 = st.columns([4, 1.2])
with col_s1:
    search_term = st.text_input(
        "Enter keywords, diseases, therapies, or gene targets:",
        value=current_query_val,
        placeholder="e.g., crispr cas9 sickle cell disease trial, zinc cold severity",
        label_visibility="collapsed"
    )
with col_s2:
    search_btn = st.button("Search PubMed →", type="primary", use_container_width=True)

display_papers = []
cited_pmids_set = set()

auto_search = bool(prefill and prefill.strip())
should_search = (search_btn or auto_search) and search_term.strip()

if should_search:
    clean_term = search_term.strip()
    st.session_state["papers_explorer_query"] = clean_term
    add_to_history(clean_term)

    with st.spinner(f"Retrieving PubMed papers for '{clean_term}'..."):
        retriever = PubMedRetriever()
        search_res = retriever.retrieve(clean_term, max_results=10)

        display_papers = search_res.papers
        st.session_state["papers_explorer_cache"] = display_papers
        st.session_state["papers_explorer_query"] = clean_term

        if not display_papers:
            st.warning(f"No peer-reviewed publications matching \"{clean_term}\" were found on PubMed.")

elif "papers_explorer_cache" in st.session_state:
    display_papers = st.session_state["papers_explorer_cache"]
    q_name = st.session_state.get("papers_explorer_query", "")
    st.info(f"Showing cached PubMed publications for inquiry: \"{q_name}\"")

elif "latest_result" in st.session_state and st.session_state["latest_result"].get("papers"):
    display_papers = st.session_state["latest_result"]["papers"]
    cited_pmids_set = set(st.session_state["latest_result"].get("verified_pmids", []))
    last_q = st.session_state.get("latest_question", "")
    st.info(f"Showing {len(display_papers)} publications retrieved from recent inquiry: \"{last_q}\"")

if display_papers:
    st.markdown(f"### Retrieved Publications ({len(display_papers)} Records)")
    for paper in display_papers:
        is_cited = paper.pmid in cited_pmids_set
        render_paper_card(paper, is_cited=is_cited)
else:
    render_html(
        """
        <div class="query-header-card" style="text-align:center; padding:36px;">
            <div style="font-size:1.15rem; font-weight:700; color:#F8FAFC; margin-bottom:8px;">No Papers Loaded Yet</div>
            <div style="font-size:0.90rem; color:#94A3B8; max-width:550px; margin:0 auto;">
                Enter a scientific keyword, clinical trial topic, or disease name in the search box above to retrieve records directly from the National Library of Medicine.
            </div>
        </div>
        """
    )

render_disclaimer()
