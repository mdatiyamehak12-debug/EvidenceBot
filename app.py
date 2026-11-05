"""
Bio EvidenceBot - AI-Powered Biomedical Research Assistant
==========================================================
Discover, analyse and synthesise scientific evidence from peer-reviewed literature.
Powered by NCBI PubMed Central, Europe PMC, SentenceTransformers, and FAISS.
Premium dark-themed scientific AI research interface.
"""

import streamlit as st
from utils import config
from utils.ui_components import (
    apply_theme,
    render_top_nav,
    render_sidebar,
    render_confidence_badge,
    render_evidence_availability,
    render_paper_card,
    render_disclaimer,
    render_html,
)
from utils.history_manager import add_to_history
from backend.rag_pipeline import run_rag_pipeline

# =====================================================================
# Page Configuration
# =====================================================================
st.set_page_config(
    page_title="EvidenceBot – AI Research Assistant",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply unified dark scientific design theme & sidebar
apply_theme()
render_sidebar()

# Handle query triggered from recent search sidebar click
auto_query = st.session_state.pop("query_to_run", None)
if auto_query:
    st.session_state["active_query"] = auto_query

# =====================================================================
# State Routing: Homepage vs. Search Results Page
# =====================================================================
has_results = "latest_result" in st.session_state and st.session_state.get("latest_question")

if not has_results:
    # =================================================================
    # HOMEPAGE INTERFACE (Minimalist Dark Experience)
    # =================================================================
    
    # 1. Top Navigation
    render_top_nav()

    # 2. Centre Hero Typography
    render_html(
        """
        <div class="hero-container">
            <div class="hero-eyebrow">EVIDENCEBOT</div>
            <h1 class="hero-title">
                Research Smarter.<br>
                <span class="accent">Discover Scientific Evidence.</span>
            </h1>
            <p class="hero-subtitle">
                Your AI-powered companion for exploring biomedical research and scientific literature.
            </p>
        </div>
        """
    )

    # 3. Prominent Search Box
    col_l, col_center, col_r = st.columns([0.05, 0.90, 0.05])
    with col_center:
        current_input_val = st.session_state.get("active_query", "")
        
        search_query = st.text_area(
            "Search Query",
            value=current_input_val,
            height=70,
            placeholder="Ask any biomedical or scientific research question...",
            label_visibility="collapsed",
            key="home_search_input"
        )
        
        col_btn_spacer, col_btn_action = st.columns([3.8, 1.2])
        with col_btn_action:
            search_button = st.button("Search Evidence →", type="primary", use_container_width=True)

        # Clean, subtle sample research inquiries
        render_html(
            """
            <div style="text-align:center; margin-top:16px; margin-bottom:10px;">
                <span style="font-size:0.80rem; color:#64748B; font-weight:500;">Try asking:</span>
            </div>
            """
        )

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("Zinc & cold duration", key="ex1", use_container_width=True):
                st.session_state["active_query"] = "Does zinc supplementation reduce the duration or severity of common cold symptoms?"
                st.session_state["query_to_run"] = st.session_state["active_query"]
                st.rerun()
        with c2:
            if st.button("Metformin in T2D", key="ex2", use_container_width=True):
                st.session_state["active_query"] = "What is the primary cellular mechanism of action of metformin in type 2 diabetes?"
                st.session_state["query_to_run"] = st.session_state["active_query"]
                st.rerun()
        with c3:
            if st.button("Omega-3 & heart health", key="ex3", use_container_width=True):
                st.session_state["active_query"] = "Does dietary omega-3 fatty acid supplementation prevent major adverse cardiovascular events in healthy individuals?"
                st.session_state["query_to_run"] = st.session_state["active_query"]
                st.rerun()
        with c4:
            if st.button("Spirulina & MS (Abstention)", key="ex4", use_container_width=True):
                st.session_state["active_query"] = "Can spirulina microalgae supplementation cure multiple sclerosis in human patients?"
                st.session_state["query_to_run"] = st.session_state["active_query"]
                st.rerun()

    # Trigger Search Execution
    should_search = search_button or (auto_query is not None and len(auto_query.strip()) > 0)
    
    if should_search:
        target_q = search_query.strip() if search_query else (auto_query.strip() if auto_query else "")
        if not target_q:
            st.warning("Please enter a research question or clinical inquiry first.")
        else:
            st.session_state["active_query"] = target_q
            add_to_history(target_q)

            status_box = st.status("Searching PubMed and synthesising scientific evidence...", expanded=True)
            try:
                status_box.write("&bull; Querying National Library of Medicine (NCBI PubMed & Europe PMC)...")
                status_box.write("&bull; Indexing candidate abstracts in dense FAISS vector index...")
                status_box.write("&bull; Evaluating evidence sufficiency and synthesising grounded consensus...")

                # Sensible backend defaults: 10 papers, default similarity threshold
                result = run_rag_pipeline(
                    target_q,
                    max_papers=10,
                    threshold=float(config.MIN_SIMILARITY_THRESHOLD)
                )

                st.session_state["latest_result"] = result
                st.session_state["latest_question"] = target_q
                status_box.update(label="Evidence Synthesis Complete", state="complete", expanded=False)
                st.rerun()
            except Exception as e:
                status_box.update(label="Retrieval Error", state="error")
                st.error(f"Error during research synthesis: {e}")

else:
    # =================================================================
    # SEARCH RESULTS PAGE (Separate, Clean Dark View)
    # =================================================================
    
    # Top Navigation with "← Ask another question" Action
    col_nav1, col_nav2 = st.columns([1.5, 4.5])
    with col_nav1:
        if st.button("← Ask another question", key="btn_back_home", type="secondary"):
            st.session_state["active_query"] = ""
            st.session_state.pop("latest_result", None)
            st.session_state.pop("latest_question", None)
            st.rerun()
    with col_nav2:
        render_top_nav()

    result = st.session_state["latest_result"]
    question_display = st.session_state.get("latest_question", "")
    is_abstention = result.get("is_abstention", False)
    retrieved_papers = result.get("papers", [])
    verified_pmids = set(result.get("verified_pmids", []))
    confidence_val = result.get("confidence", "Moderate")
    top_score = result.get("max_score", 0.0)

    # 1. Research Question Display
    render_html(
        f"""
        <div class="query-header-card">
            <div class="query-header-label">Research Inquiry</div>
            <div class="query-header-text">"{question_display}"</div>
        </div>
        """
    )

    # 2. Supporting Evidence & Overview
    render_evidence_availability(
        is_available=(not is_abstention and len(retrieved_papers) > 0),
        count=len(retrieved_papers)
    )

    # 3. AI-Generated Scientific Answer OR Abstention Notice
    if is_abstention:
        render_html(
            f"""
            <div class="abstention-alert">
                <div class="abstention-title">
                    No sufficient scientific evidence found for this query.
                </div>
                <p class="abstention-desc">
                    EvidenceBot strictly enforces an empirical abstention protocol. In scientific and biomedical research, 
                    refusing to synthesize unsupported claims prevents dangerous hallucinations and clinical misinformation.
                </p>
                <div style="background:#111827; border:1px solid rgba(239, 68, 68, 0.3); border-radius:8px; padding:12px 16px; margin-top:12px; font-size:0.86rem; color:#F8FAFC; font-family:'JetBrains Mono', monospace;">
                    <div><strong>Inquiry:</strong> {question_display}</div>
                    <div><strong>Abstention Reason:</strong> {result.get('reason', 'Retrieved literature does not meet confidence standards.')}</div>
                </div>
            </div>
            """
        )

        if retrieved_papers:
            st.markdown(f"#### Retrieved Candidate Papers ({len(retrieved_papers)} Records Evaluated)")
            st.caption("These publications were retrieved from PubMed but fell below relevance thresholds for factual synthesis:")
            for p in retrieved_papers:
                render_paper_card(p, is_cited=False)

    else:
        # Reliability Badge & Model Source
        render_html(
            f"""
            <div style="margin-bottom:12px; display:flex; align-items:center; flex-wrap:wrap; gap:8px;">
                {render_confidence_badge(confidence_val, top_score)}
                <span class="pill-badge pill-teal">ENGINE: {result.get('provider', 'Synthesizer')}</span>
                <span class="pill-badge" style="background:rgba(255,255,255,0.05); color:#94A3B8; border:1px solid #263449;">
                    {len(retrieved_papers)} STUDIES EVALUATED
                </span>
            </div>
            """
        )

        # AI Research Synthesis
        st.markdown("#### AI Research Synthesis")
        answer_text = result.get("answer", "")
        render_html(
            f"""
            <div class="synthesis-card">
                {answer_text}
            </div>
            """
        )

        # 4. References & Authenticated Citations
        citation_rep = result.get("citation_report") or {}
        verified_items = citation_rep.get("verified_citations", [])
        if verified_items:
            st.markdown(f"#### References ({len(verified_items)} Authenticated Citations)")
            for idx, item in enumerate(verified_items, 1):
                authors_str = ", ".join(item.get("authors", [])[:3])
                if len(item.get("authors", [])) > 3:
                    authors_str += " et al."
                render_html(
                    f"""
                    <div style="background:#172033; border:1px solid #263449; border-left:3px solid #2DD4BF; border-radius:10px; padding:14px 18px; margin-bottom:10px; box-shadow:0 2px 8px rgba(0,0,0,0.2);">
                        <div style="font-weight:700; font-size:0.98rem; color:#F8FAFC;">
                            [{idx}] <a href="{item.get('url')}" target="_blank" style="color:#F8FAFC; text-decoration:none;">{item.get('title')}</a>
                        </div>
                        <div style="font-size:0.84rem; color:#94A3B8; margin-top:4px;">
                            {authors_str} &bull; <em>{item.get('journal', 'Journal')}</em> ({item.get('year', 'N/A')}) &bull; PMID: <code>{item.get('pmid')}</code>
                        </div>
                        <div style="font-size:0.86rem; color:#CBD5E1; margin-top:8px; background:#111827; border:1px solid #263449; padding:8px 12px; border-radius:6px;">
                            <strong>Cited Context:</strong> "{item.get('claim_context')}"
                        </div>
                    </div>
                    """
                )

        # 5. Retrieved Research Papers
        st.markdown("---")
        st.markdown(f"#### Retrieved Research Papers ({len(retrieved_papers)} Publications)")
        st.caption("Peer-reviewed scientific publications retrieved directly from the National Library of Medicine:")

        for paper in retrieved_papers:
            is_cited = paper.pmid in verified_pmids
            render_paper_card(paper, is_cited=is_cited)

# Institutional Disclaimer Footer
render_disclaimer()
