"""
EvidenceBot - Page 1: Evidence Synthesis Engine
================================================
Autonomous literature synthesis pipeline: queries PubMed, indexes with FAISS dense vectors,
evaluates sufficiency against cosine thresholds, synthesizes answers, and verifies citations.
Zero informal emojis, sleek deeptech telemetry layout.
"""

import streamlit as st
from utils import config
from utils.ui_components import (
    apply_theme,
    render_sidebar,
    render_confidence_badge,
    render_disclaimer,
)
from backend.rag_pipeline import run_rag_pipeline

# Configure page
st.set_page_config(
    page_title="EvidenceBot – Evidence Synthesis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply unified styling and sidebar
apply_theme()
render_sidebar(current_page="Evidence Synthesis")

# Page Header
st.markdown(
    """
    <div style="margin-bottom: 22px;">
        <div style="margin-bottom:6px;">
            <span class="mono-tag" style="color:#38bdf8; background:rgba(14,165,233,0.1); border:1px solid rgba(14,165,233,0.25);">
                SYNTHESIS ENGINE &bull; RAG PIPELINE
            </span>
        </div>
        <h2 style="color: #ffffff; margin-bottom: 4px; font-weight:800; letter-spacing:-0.03em;">Evidence Synthesis Console</h2>
        <p style="color: #94a3b8; margin: 0; font-size:0.98rem;">Submit a biomedical, pharmacological, or clinical inquiry to synthesize peer-reviewed literature with deterministic citation tracing.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Retrieve any query passed from the home dashboard
prefill_query = st.session_state.pop("query_to_run", None)
if prefill_query:
    st.session_state["active_query"] = prefill_query

current_query_val = st.session_state.get("active_query", "")

# Search Settings Collapsible
with st.expander("Advanced Retrieval & Abstention Parameters", expanded=False):
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        max_papers = st.slider(
            "Max PubMed Papers to Ingest",
            min_value=3,
            max_value=15,
            value=config.DEFAULT_MAX_PAPERS,
            help="Number of candidate scientific papers to fetch from PubMed."
        )
    with col_s2:
        threshold = st.slider(
            "Abstention Similarity Threshold",
            min_value=0.20,
            max_value=0.60,
            value=config.MIN_SIMILARITY_THRESHOLD,
            step=0.02,
            help="If the top evidence chunk scores below this cosine similarity threshold, EvidenceBot abstains."
        )

# Question Input Area
user_question = st.text_area(
    "Biomedical Research Inquiry:",
    value=current_query_val,
    height=95,
    placeholder="e.g. Does zinc supplementation reduce the duration or severity of the common cold?"
)

col_search, col_reset = st.columns([1, 4])
with col_search:
    search_clicked = st.button("Execute Synthesis →", type="primary", use_container_width=True)
with col_reset:
    if st.button("Clear Input"):
        st.session_state["active_query"] = ""
        st.session_state.pop("latest_result", None)
        st.rerun()

auto_trigger = prefill_query is not None and len(prefill_query.strip()) > 0

# =====================================================================
# Execution & Loading Telemetry
# =====================================================================
if search_clicked or auto_trigger:
    clean_q = user_question.strip()
    if not clean_q:
        st.warning("Please enter a biomedical question first.")
    else:
        st.session_state["active_query"] = clean_q
        
        status_box = st.status("Executing Biomedical RAG Pipeline...", expanded=True)
        
        try:
            status_box.write("**Phase 1/4:** Formulating search and querying NCBI Entrez (`esearch`)...")
            status_box.write("**Phase 2/4:** Parsing candidate peer-reviewed abstracts (`efetch`)...")
            status_box.write("**Phase 3/4:** Encoding dense vectors via SentenceTransformers & indexing in FAISS...")
            status_box.write("**Phase 4/4:** Evaluating confidence threshold & synthesizing grounded claims...")
            
            result = run_rag_pipeline(clean_q, max_papers=max_papers, threshold=threshold)
            st.session_state["latest_result"] = result
            st.session_state["latest_question"] = clean_q
            
            status_box.update(label="Evidence Pipeline Complete", state="complete", expanded=False)
        except Exception as err:
            status_box.update(label="Pipeline Execution Error", state="error")
            st.error(f"Encountered pipeline error: {err}")

# =====================================================================
# Results Display Section
# =====================================================================
if "latest_result" in st.session_state:
    result = st.session_state["latest_result"]
    question_display = st.session_state.get("latest_question", "")

    st.markdown("---")
    st.markdown(f"**Target Inquiry:** *\"{question_display}\"*")

    # A. Abstention Condition
    if result.get("is_abstention"):
        top_score = result.get("max_score", 0.0)
        badge_html = render_confidence_badge("Insufficient", top_score)
        st.markdown(badge_html, unsafe_allow_html=True)

        ab_rep = result.get("abstention_report") or {}
        search_query = ab_rep.get("search_query") or question_display
        papers_count = ab_rep.get("papers_retrieved_count", len(result.get("papers", [])))
        insufficient_reason = ab_rep.get("reason") or result.get("reason", "Retrieved evidence does not meet confidence standards.")
        additional_research = ab_rep.get("additional_research_required") or "Targeted randomized clinical trials or systematic reviews directly addressing this specific hypothesis."

        st.markdown(
            f"""
            <div class="abstention-box">
                <div style="font-size: 1.05rem; font-weight: 700; color: #fb7185; margin-bottom: 10px;">
                    EMPIRICAL ABSTENTION ACTIVATED: Insufficient reliable evidence in retrieved literature.
                </div>
                <p style="color: #cbd5e1; font-size: 0.90rem; margin-bottom: 12px; line-height:1.6;">
                    EvidenceBot strictly enforces an empirical abstention protocol. In scientific and biomedical inquiry, 
                    refusing to synthesize speculative claims prevents dangerous hallucinations and medical misinformation.
                </p>
                <div style="background-color: #090e17; border: 1px solid rgba(244, 63, 94, 0.25); border-radius: 6px; padding: 12px 16px;">
                    <ul style="margin: 0; padding-left: 18px; line-height: 1.8; color: #e2e8f0; font-size: 0.88rem; font-family:'JetBrains Mono', monospace;">
                        <li><strong>Query Ingestion:</strong> {search_query}</li>
                        <li><strong>Candidate Records:</strong> {papers_count} publication(s) from NCBI PubMed</li>
                        <li><strong>Abstention Trigger:</strong> {insufficient_reason}</li>
                        <li><strong>Future Direction:</strong> {additional_research}</li>
                    </ul>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        col_ab1, col_ab2 = st.columns(2)
        with col_ab1:
            st.page_link("pages/2_Research_Papers.py", label="Inspect Candidate Papers on Literature Explorer →")
        with col_ab2:
            st.page_link("pages/3_Evidence_Analysis.py", label="Inspect Abstention Diagnostics on Grounding Audit →")

    # B. Successful Evidence Synthesis
    else:
        conf = result.get("confidence", "Moderate")
        top_score = result.get("max_score", 0.0)
        provider = result.get("provider", "Synthesizer")
        
        # Evidence Status Badges
        st.markdown(
            f"""
            <div style="margin-bottom:12px;">
                {render_confidence_badge(conf, top_score)}
                <span class="mono-tag" style="color:#38bdf8; background:rgba(14,165,233,0.1); border:1px solid rgba(14,165,233,0.25);">MODEL: {provider}</span>
                <span class="mono-tag" style="color:#94a3b8; background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.1);">CHUNKS: {len(result.get('chunks', []))}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Formatted Answer Display
        st.markdown(
            f"""
            <div class="answer-box">
                {st.session_state['latest_result'].get('answer', '')}
            </div>
            """,
            unsafe_allow_html=True
        )

        # Citation Section
        st.markdown(
            """
            <div style="margin-top:24px; margin-bottom:8px;">
                <span class="mono-tag" style="color:#94a3b8; background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.1);">CITATION ATTRIBUTION AUDIT</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        citation_rep = result.get("citation_report") or {}
        verified_items = citation_rep.get("verified_citations", [])
        hallucinated_pmids = citation_rep.get("hallucinated_pmids", [])
        missing_citations = citation_rep.get("missing_citations", [])
        unsupported_claims = citation_rep.get("unsupported_claims", [])

        if hallucinated_pmids:
            st.error(
                f"UNVERIFIED CITATIONS DETECTED: The draft referenced unverified PMID(s): "
                f"`{', '.join(hallucinated_pmids)}`. These did not exist in the retrieved literature."
            )

        if missing_citations or unsupported_claims:
            col_w1, col_w2 = st.columns(2)
            with col_w1:
                if missing_citations:
                    st.warning(f"{len(missing_citations)} assertion(s) lacked a direct PMID citation.")
            with col_w2:
                if unsupported_claims:
                    st.warning(f"{len(unsupported_claims)} assertion(s) cited weakly relevant sources (relevance < {config.MIN_SIMILARITY_THRESHOLD:.2f}).")

        if verified_items:
            st.markdown(f"Verified **{len(verified_items)}** peer-reviewed citation(s) linked to authenticated NCBI records:")
            
            for item in verified_items:
                authors_str = ", ".join(item.get("authors", [])[:3])
                if len(item.get("authors", [])) > 3:
                    authors_str += " et al."
                
                doi_str = f" | DOI: {item.get('doi')}" if item.get("doi") else ""
                rel_score = item.get("relevance_score", 0.0)
                rel_badge = f'<span class="badge-pill badge-high">RELEVANCE: {rel_score:.2f}</span>' if rel_score >= 0.40 else f'<span class="badge-pill badge-moderate">RELEVANCE: {rel_score:.2f}</span>'

                st.markdown(
                    f"""
                    <div class="bio-card" style="padding:14px 18px; margin-bottom:10px;">
                        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:8px;">
                            <div>
                                <a href="{item.get('url')}" target="_blank" style="font-weight:700; color:#38bdf8; text-decoration:none; font-size:0.98rem; letter-spacing:-0.015em;">
                                    {item.get('title')} &rarr;
                                </a>
                                <div style="font-size:0.82rem; color:#94a3b8; margin-top:2px;">
                                    {authors_str} &bull; <em>{item.get('journal', 'Journal')}</em> ({item.get('year', 'N/A')}){doi_str}
                                </div>
                            </div>
                            <div>
                                {rel_badge}
                                <span class="mono-tag" style="background:#111827; color:#38bdf8; border:1px solid rgba(14,165,233,0.3);">PMID {item.get('pmid')}</span>
                            </div>
                        </div>
                        <div style="background-color:rgba(255,255,255,0.03); border-left:2px solid #0ea5e9; padding:8px 12px; margin-top:10px; border-radius:4px; font-size:0.86rem; color:#cbd5e1;">
                            <strong>Asserted Claim:</strong> "{item.get('claim_context')}"
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            col_l1, col_l2 = st.columns(2)
            with col_l1:
                st.page_link("pages/2_Research_Papers.py", label="View Complete Abstract Records on Literature Explorer →")
            with col_l2:
                st.page_link("pages/3_Evidence_Analysis.py", label="View Claim-by-Claim Verification on Grounding Audit →")
        else:
            verified_pmids = result.get("verified_pmids", [])
            if verified_pmids:
                st.write(
                    f"EvidenceBot verified **{len(verified_pmids)}** peer-reviewed publication(s) cited in this answer: "
                    + ", ".join([f"[`PMID: {p}`](https://pubmed.ncbi.nlm.nih.gov/{p}/)" for p in verified_pmids])
                )
            else:
                st.caption("No individual citations were extracted for this query.")

# Scientific Disclaimer
render_disclaimer()
