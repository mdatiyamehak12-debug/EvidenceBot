"""
EvidenceBot - Page 2: Literature Explorer
=========================================
Presents detailed research paper cards retrieved from PubMed,
including titles, authors, journals, DOIs, abstract previews, and official links.
Zero informal emojis; deeptech telemetry design.
"""

import streamlit as st
from utils.ui_components import (
    apply_theme,
    render_sidebar,
    render_paper_card,
    render_disclaimer,
)
from backend.pubmed import search_pubmed, fetch_paper_details

st.set_page_config(
    page_title="EvidenceBot – Literature Explorer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply unified styling and sidebar
apply_theme()
render_sidebar(current_page="Literature Explorer")

# Page Header
st.markdown(
    """
    <div style="margin-bottom: 22px;">
        <div style="margin-bottom:6px;">
            <span class="mono-tag" style="color:#38bdf8; background:rgba(14,165,233,0.1); border:1px solid rgba(14,165,233,0.25);">
                PUBMED DATABASE EXPLORER
            </span>
        </div>
        <h2 style="color: #ffffff; margin-bottom: 4px; font-weight:800; letter-spacing:-0.03em;">Literature Explorer</h2>
        <p style="color: #94a3b8; margin: 0; font-size:0.98rem;">Explore peer-reviewed scientific publications, clinical trial records, and journal metadata directly from the National Library of Medicine.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Search Bar for ad-hoc queries
st.markdown(
    """
    <div style="margin-bottom:8px;">
        <span class="mono-tag" style="color:#94a3b8; background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.1);">TARGETED PUBMED QUERY</span>
    </div>
    """,
    unsafe_allow_html=True
)
col_s1, col_s2 = st.columns([4, 1])

with col_s1:
    search_term = st.text_input(
        "Enter keywords, diseases, therapies, or gene targets:",
        placeholder="e.g., crispr cas9 sickle cell disease trial",
        label_visibility="collapsed"
    )

with col_s2:
    search_btn = st.button("Search PubMed →", type="primary", use_container_width=True)

display_papers = []
cited_pmids_set = set()

if search_btn and search_term.strip():
    with st.spinner("Executing NCBI Entrez ESearch..."):
        pmids = search_pubmed(search_term.strip(), max_results=8)
        if pmids:
            display_papers = fetch_paper_details(pmids)
            st.session_state["papers_explorer_cache"] = display_papers
            st.session_state["papers_explorer_query"] = search_term.strip()
        else:
            display_papers = []
            st.session_state["papers_explorer_cache"] = []
            st.session_state["papers_explorer_query"] = search_term.strip()
            st.warning(f"No peer-reviewed publications matching \"{search_term.strip()}\" were found on PubMed.")

elif "papers_explorer_cache" in st.session_state:
    display_papers = st.session_state["papers_explorer_cache"]
    q_name = st.session_state.get("papers_explorer_query", "")
    st.info(f"Showing PubMed publications for custom search: \"{q_name}\"")

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
    st.caption("No papers loaded yet. Enter a topic in the search box above or run a query on the Evidence Synthesis console.")

render_disclaimer()
