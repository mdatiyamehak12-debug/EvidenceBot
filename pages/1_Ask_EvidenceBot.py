"""
EvidenceBot - Page 1: Ask EvidenceBot
=====================================
The primary question answering interface: queries PubMed, indexes with FAISS,
evaluates sufficiency, synthesizes grounded answers, and audits citations.
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
    page_icon="💬",
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
        <h2 style="color: #0f172a; margin-bottom: 4px; font-weight:800; letter-spacing:-0.02em;">💬 Evidence Synthesis Engine</h2>
        <p style="color: #64748b; margin: 0; font-size:1.02rem;">Submit a biomedical, pharmacological, or clinical inquiry to synthesize peer-reviewed literature with deterministic citation tracing.</p>
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
with st.expander("⚙️ Advanced Retrieval & Abstention Parameters", expanded=False):
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

# Large Question Input Area
user_question = st.text_area(
    "**Biomedical Question:**",
    value=current_query_val,
    height=95,
    placeholder="e.g. Does zinc supplementation reduce the duration or severity of the common cold?"
)

col_search, col_reset = st.columns([1, 4])
with col_search:
    search_clicked = st.button("🚀 Synthesize Evidence", type="primary", use_container_width=True)
with col_reset:
    if st.button("Clear Question"):
        st.session_state["active_query"] = ""
        st.session_state.pop("latest_result", None)
        st.rerun()

# Automatically trigger search if navigated from home page with prefill
auto_trigger = prefill_query is not None and len(prefill_query.strip()) > 0

# =====================================================================
# Execution & Loading Indicator
# =====================================================================
if search_clicked or auto_trigger:
    clean_q = user_question.strip()
    if not clean_q:
        st.warning("⚠️ Please enter a biomedical question first.")
    else:
        st.session_state["active_query"] = clean_q
        
        # Step-by-step progress status box
        status_box = st.status("🔬 Synthesizing PubMed Evidence...", expanded=True)
        
        try:
            status_box.write("🔍 **Step 1/4:** Searching PubMed database via NCBI E-Utilities (`esearch`)...")
            status_box.write("📄 **Step 2/4:** Downloading and parsing peer-reviewed abstracts (`efetch`)...")
            status_box.write("⚡ **Step 3/4:** Encoding passages with SentenceTransformers & indexing into FAISS...")
            status_box.write("🛡️ **Step 4/4:** Checking evidence sufficiency threshold & synthesizing answer...")
            
            result = run_rag_pipeline(clean_q, max_papers=max_papers, threshold=threshold)
            st.session_state["latest_result"] = result
            st.session_state["latest_question"] = clean_q
            
            status_box.update(label="✅ Evidence Pipeline Complete!", state="complete", expanded=False)
        except Exception as err:
            status_box.update(label="❌ Pipeline Error", state="error")
            st.error(f"Encountered an error: {err}")

# =====================================================================
# Results Display Section
# =====================================================================
if "latest_result" in st.session_state:
    result = st.session_state["latest_result"]
    question_display = st.session_state.get("latest_question", "")

    st.markdown("---")
    st.markdown(f"**Research Question:** *\"{question_display}\"*")

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
                <div style="font-size: 1.15rem; font-weight: 700; color: #be123c; margin-bottom: 12px; display: flex; align-items: flex-start; gap: 8px;">
                    <span>🛑</span>
                    <span>I could not find sufficient reliable evidence in the retrieved literature to provide a confident answer.</span>
                </div>
                <p style="color: #4b5563; font-size: 0.93rem; margin-bottom: 14px;">
                    EvidenceBot strictly enforces an empirical abstention protocol. In scientific and biomedical inquiry, 
                    refusing to synthesize speculative claims prevents dangerous hallucinations and medical misinformation.
                </p>
                <div style="background-color: #ffffff; border: 1px solid #fecdd3; border-radius: 8px; padding: 14px 18px; margin-top: 10px;">
                    <ul style="margin: 0; padding-left: 18px; line-height: 1.8; color: #1e293b; font-size: 0.92rem;">
                        <li><strong>What was searched:</strong> <code>{search_query}</code></li>
                        <li><strong>How many papers were retrieved:</strong> <strong>{papers_count}</strong> peer-reviewed publication(s) from NCBI PubMed</li>
                        <li><strong>Why the evidence was insufficient:</strong> {insufficient_reason}</li>
                        <li><strong>What additional research may be required:</strong> {additional_research}</li>
                    </ul>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        col_ab1, col_ab2 = st.columns(2)
        with col_ab1:
            st.page_link(
                "pages/2_Research_Papers.py",
                label="📚 Inspect candidate papers retrieved from PubMed",
                icon="📄"
            )
        with col_ab2:
            st.page_link(
                "pages/3_Evidence_Analysis.py",
                label="🔬 View deep abstention diagnostics on Evidence Analysis",
                icon="📊"
            )

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
                <span class="badge-pill badge-cyan">Engine: {provider}</span>
                <span class="badge-pill badge-prelim">Evidence Chunks: {len(result.get('chunks', []))}</span>
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
        st.markdown("### 📚 Citation Validation & Verification")
        
        citation_rep = result.get("citation_report") or {}
        verified_items = citation_rep.get("verified_citations", [])
        hallucinated_pmids = citation_rep.get("hallucinated_pmids", [])
        missing_citations = citation_rep.get("missing_citations", [])
        unsupported_claims = citation_rep.get("unsupported_claims", [])

        # Hallucination alert if present
        if hallucinated_pmids:
            st.error(
                f"🚨 **Hallucinated Citations Detected:** The draft referenced unverified PMID(s): "
                f"`{', '.join(hallucinated_pmids)}`. These did not exist in the retrieved literature."
            )

        # Missing or unsupported warnings
        if missing_citations or unsupported_claims:
            col_w1, col_w2 = st.columns(2)
            with col_w1:
                if missing_citations:
                    st.warning(f"⚠️ **{len(missing_citations)}** factual claim(s) lacked a direct PMID citation.")
            with col_w2:
                if unsupported_claims:
                    st.warning(f"⚠️ **{len(unsupported_claims)}** claim(s) cited weakly relevant sources (relevance < {config.MIN_SIMILARITY_THRESHOLD:.2f}).")

        if verified_items:
            st.markdown(f"EvidenceBot verified **{len(verified_items)}** peer-reviewed citation(s) linked to authentic NCBI records:")
            
            for item in verified_items:
                authors_str = ", ".join(item.get("authors", [])[:3])
                if len(item.get("authors", [])) > 3:
                    authors_str += " et al."
                
                doi_str = f" | DOI: {item.get('doi')}" if item.get("doi") else ""
                rel_score = item.get("relevance_score", 0.0)
                rel_badge = f'<span class="badge-pill badge-high">Relevance: {rel_score:.2f}</span>' if rel_score >= 0.40 else f'<span class="badge-pill badge-moderate">Relevance: {rel_score:.2f}</span>'

                st.markdown(
                    f"""
                    <div class="bio-card" style="padding:12px 16px; margin-bottom:10px;">
                        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                            <div>
                                <a href="{item.get('url')}" target="_blank" style="font-weight:700; color:#0077b6; text-decoration:none; font-size:1.02rem;">
                                    🔗 {item.get('title')}
                                </a>
                                <div style="font-size:0.85rem; color:#64748b; margin-top:2px;">
                                    {authors_str} • <em>{item.get('journal', 'Journal')}</em> ({item.get('year', 'N/A')}){doi_str}
                                </div>
                            </div>
                            <div>
                                {rel_badge}
                                <span class="badge-pill badge-cyan">PMID: {item.get('pmid')}</span>
                            </div>
                        </div>
                        <div style="background-color:#f8fafc; border-left:3px solid #00b4d8; padding:8px 12px; margin-top:8px; border-radius:4px; font-size:0.86rem; color:#334155;">
                            <strong>Claim Context:</strong> "{item.get('claim_context')}"
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # Deep audit navigation
            col_l1, col_l2 = st.columns(2)
            with col_l1:
                st.page_link(
                    "pages/2_Research_Papers.py",
                    label="👉 Read full abstracts on Research Papers",
                    icon="📚"
                )
            with col_l2:
                st.page_link(
                    "pages/3_Evidence_Analysis.py",
                    label="👉 View claim audit & study designs on Evidence Analysis",
                    icon="🔬"
                )
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
