"""
Bio EvidenceBot - Evidence Synthesis Console (Page 1)
======================================================
Autonomous literature synthesis pipeline: queries PubMed & Europe PMC,
indexes with FAISS dense vectors, evaluates sufficiency against cosine thresholds,
synthesizes answers, and verifies citations.
"""

import streamlit as st
from utils import config
from utils.ui_components import (
    apply_theme,
    render_sidebar,
    render_confidence_badge,
    render_evidence_availability,
    render_disclaimer,
    render_paper_card,
    render_html,
)
from utils.history_manager import add_to_history
from backend.rag_pipeline import run_rag_pipeline

# Configure page
st.set_page_config(
    page_title="EvidenceBot – Evidence Synthesis Console",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply unified dark scientific design theme & sidebar
apply_theme()
render_sidebar(current_page="Evidence Synthesis")

# Page Header Card
render_html(
    """
    <div class="query-header-card" style="margin-bottom:20px;">
        <div class="query-header-label">SYNTHESIS ENGINE &bull; RAG PIPELINE</div>
        <div class="query-header-text" style="font-size:1.6rem;">Evidence Synthesis Console</div>
        <p style="color:#94A3B8; margin:6px 0 0 0; font-size:0.95rem;">
            Submit a biomedical inquiry to synthesize peer-reviewed literature with deterministic citation tracing.
        </p>
    </div>
    """
)

# Retrieve any query passed from the home dashboard or sidebar
prefill_query = st.session_state.pop("query_to_run", None)
if prefill_query:
    st.session_state["active_query"] = prefill_query

current_query_val = st.session_state.get("active_query", "")

# Research Question Input Area
user_question = st.text_area(
    "Biomedical Research Inquiry:",
    value=current_query_val,
    height=80,
    placeholder="e.g. Does zinc supplementation reduce the duration or severity of the common cold?",
    label_visibility="collapsed"
)

col_search, col_reset, col_spc = st.columns([1.8, 1, 3.2])
with col_search:
    search_clicked = st.button("Search Evidence →", type="primary", use_container_width=True)
with col_reset:
    clear_clicked = st.button("Clear Input", type="secondary", use_container_width=True)

if clear_clicked:
    st.session_state["active_query"] = ""
    st.session_state.pop("latest_result", None)
    st.session_state.pop("latest_question", None)
    st.rerun()

# Execution & Loading Telemetry
auto_trigger = prefill_query is not None and len(prefill_query.strip()) > 0
should_run = search_clicked or auto_trigger

if should_run:
    clean_q = user_question.strip()
    if not clean_q:
        st.warning("Please enter a research inquiry or scientific question first.")
    else:
        st.session_state["active_query"] = clean_q
        add_to_history(clean_q)

        status_box = st.status("Retrieving Peer-Reviewed Research from PubMed...", expanded=True)

        try:
            status_box.write("&bull; Querying NCBI Entrez E-Utilities and Europe PMC database mirror...")
            status_box.write("&bull; Parsing candidate abstracts and generating 768-dim FAISS dense vector index...")
            status_box.write("&bull; Evaluating evidence sufficiency and formulating verified answer...")

            result = run_rag_pipeline(
                clean_q,
                max_papers=10,
                threshold=float(config.MIN_SIMILARITY_THRESHOLD)
            )
            st.session_state["latest_result"] = result
            st.session_state["latest_question"] = clean_q

            status_box.update(label="Evidence Synthesis Complete", state="complete", expanded=False)
        except Exception as err:
            status_box.update(label="Pipeline Execution Error", state="error")
            st.error(f"Encountered pipeline error: {err}")

# Results Dashboard
if "latest_result" in st.session_state:
    result = st.session_state["latest_result"]
    question_display = st.session_state.get("latest_question", "")
    is_abstention = result.get("is_abstention", False)
    retrieved_papers = result.get("papers", [])
    verified_pmids = set(result.get("verified_pmids", []))
    confidence_val = result.get("confidence", "Moderate")
    top_score = result.get("max_score", 0.0)

    st.markdown("---")
    st.markdown(f"### Research Findings for: *\"{question_display}\"*")

    render_evidence_availability(
        is_available=(not is_abstention and len(retrieved_papers) > 0),
        count=len(retrieved_papers)
    )

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
                <div style="background:#111827; border:1px solid rgba(239,68,68,0.3); border-radius:8px; padding:12px 16px; margin-top:12px; font-size:0.86rem; color:#F8FAFC; font-family:'JetBrains Mono', monospace;">
                    <div><strong>Inquiry:</strong> {question_display}</div>
                    <div><strong>Abstention Reason:</strong> {result.get('reason', 'Retrieved literature does not meet confidence standards.')}</div>
                </div>
            </div>
            """
        )

        if retrieved_papers:
            st.markdown(f"#### Retrieved Candidate Papers ({len(retrieved_papers)} Records Evaluated)")
            for p in retrieved_papers:
                render_paper_card(p, is_cited=False)

    else:
        render_html(
            f"""
            <div style="margin-bottom:12px; display:flex; align-items:center; flex-wrap:wrap; gap:8px;">
                {render_confidence_badge(confidence_val, top_score)}
                <span class="pill-badge pill-teal">ENGINE: {result.get('provider', 'Synthesizer')}</span>
                <span class="pill-badge" style="background:rgba(255,255,255,0.05); color:#94A3B8; border:1px solid #263449;">{len(retrieved_papers)} STUDIES EVALUATED</span>
            </div>
            """
        )

        st.markdown("#### AI Research Synthesis")
        answer_text = result.get("answer", "")
        render_html(
            f"""
            <div class="synthesis-card">
                {answer_text}
            </div>
            """
        )

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

        st.markdown("---")
        st.markdown(f"#### Retrieved Research Papers ({len(retrieved_papers)} Publications)")
        for paper in retrieved_papers:
            is_cited = paper.pmid in verified_pmids
            render_paper_card(paper, is_cited=is_cited)

render_disclaimer()
