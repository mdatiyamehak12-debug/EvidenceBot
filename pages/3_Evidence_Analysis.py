"""
Bio EvidenceBot - Grounding & Verification Audit (Page 3)
=========================================================
Deep scientific verification dashboard:
1. Audits empirical support against PubMed peer-reviewed literature.
2. Performs comprehensive citation validation (PMID existence, metadata fidelity, claim relevance).
3. Identifies missing citations and unsupported claims.
4. Breaks down abstention diagnostics and trigger conditions.
"""

import streamlit as st
from utils import config
from utils.ui_components import (
    apply_theme,
    render_sidebar,
    render_confidence_badge,
    render_claim_status_badge,
    render_disclaimer,
    render_html,
)
from backend.evidence_checker import verify_answer_claims
from backend.citation_checker import validate_citations_comprehensive

st.set_page_config(
    page_title="EvidenceBot – Grounding & Audit",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply unified dark styling and sidebar
apply_theme()
render_sidebar(current_page="Grounding & Audit")

# Page Header Card
render_html(
    """
    <div class="query-header-card" style="margin-bottom:20px;">
        <div class="query-header-label">VERIFICATION & AUDIT CONSOLE</div>
        <div class="query-header-text" style="font-size:1.6rem;">Grounding & Verification Audit</div>
        <p style="color:#94A3B8; margin:6px 0 0 0; font-size:0.95rem;">
            Atomic claim-level fact-checking, citation provenance verification, and scientific abstention diagnostics.
        </p>
    </div>
    """
)

if "latest_result" in st.session_state:
    res = st.session_state["latest_result"]
    question = st.session_state.get("latest_question", "")
    answer_text = res.get("answer", "")
    chunks = res.get("chunks", [])
    papers = res.get("papers", [])
    is_abstained = res.get("is_abstention", False)
    top_score = res.get("max_score", 0.0)

    st.markdown(f"**Target Inquiry:** *\"{question}\"*")
    st.markdown("---")

    st.markdown("#### Grounding Telemetry")

    claims_data = res.get("verified_claims", [])
    if not claims_data and answer_text and chunks and not is_abstained:
        with st.spinner("Executing claim-level NLI verification..."):
            claim_objs = verify_answer_claims(answer_text, chunks)
            claims_data = [c.to_dict() for c in claim_objs]
            st.session_state["latest_result"]["verified_claims"] = claims_data

    citation_rep = res.get("citation_report")
    if not citation_rep and answer_text and papers and chunks and not is_abstained:
        audit_obj = validate_citations_comprehensive(
            answer_text,
            papers=papers,
            chunks=chunks,
            relevance_threshold=config.MIN_SIMILARITY_THRESHOLD
        )
        citation_rep = audit_obj.to_dict()
        st.session_state["latest_result"]["citation_report"] = citation_rep

    citation_rep = citation_rep or {}
    verified_citations = citation_rep.get("verified_citations", [])
    hallucinated_pmids = citation_rep.get("hallucinated_pmids", [])
    missing_citations = citation_rep.get("missing_citations", [])
    unsupported_claims = citation_rep.get("unsupported_claims", [])

    total_claims = len(claims_data)
    supported_count = sum(1 for c in claims_data if c.get("status") == "SUPPORTED")
    partial_count = sum(1 for c in claims_data if c.get("status") == "PARTIALLY_SUPPORTED")
    contradicted_count = sum(1 for c in claims_data if c.get("status") == "CONTRADICTED")
    insufficient_count = sum(1 for c in claims_data if c.get("status") in ("INSUFFICIENT_EVIDENCE", "UNCERTAIN_HUMAN_REVIEW"))

    col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
    with col_m1:
        st.metric("Assertions Audited", total_claims)
    with col_m2:
        st.metric("Directly Supported", supported_count)
    with col_m3:
        st.metric("Verified Citations", len(verified_citations))
    with col_m4:
        st.metric("Conflicting Claims", contradicted_count)
    with col_m5:
        st.metric("Unverified PMIDs", len(hallucinated_pmids))

    st.markdown("#### Semantic Relevance vs. Abstention Baseline")
    progress_val = min(1.0, max(0.0, top_score))
    st.progress(progress_val, text=f"Top Cosine Alignment: {top_score:.2f} (Abstention Threshold: {config.MIN_SIMILARITY_THRESHOLD:.2f})")

    if is_abstained:
        st.error(
            f"SCIENTIFIC ABSTENTION ACTIVATED: Top cosine similarity ({top_score:.2f}) did not meet minimum threshold ({config.MIN_SIMILARITY_THRESHOLD:.2f}). "
            "EvidenceBot actively refused to synthesize ungrounded claims."
        )
    else:
        st.success(
            f"EMPIRICAL BASELINE SATISFIED: Top retrieved passage cosine alignment ({top_score:.2f} >= {config.MIN_SIMILARITY_THRESHOLD:.2f})."
        )

    st.markdown("---")

    tab_claims, tab_citations, tab_abstention = st.tabs([
        "Claim Grounding Feed",
        "Citation Integrity Audit",
        "Abstention Diagnostics"
    ])

    with tab_claims:
        st.markdown("#### Claim-by-Claim Verification Feed")
        if claims_data:
            filter_status = st.selectbox(
                "Filter Claims by Verification Status:",
                options=["All Claims", "SUPPORTED", "PARTIALLY_SUPPORTED", "CONTRADICTED", "INSUFFICIENT_EVIDENCE", "UNCERTAIN_HUMAN_REVIEW"],
                index=0
            )

            filtered_claims = [
                c for c in claims_data
                if filter_status == "All Claims" or c.get("status") == filter_status
            ]

            for item in filtered_claims:
                status_badge = render_claim_status_badge(item.get("status", "UNCERTAIN_HUMAN_REVIEW"))
                study_badge = f'<span class="pill-badge" style="background:#111827; color:#94A3B8; border:1px solid #263449;">{item.get("study_type", "Biomedical Literature")}</span>'
                abstract_badge = '<span class="pill-badge pill-teal">Abstract-Level Evidence</span>'
                score_badge = f'<span class="pill-badge pill-moderate">SIM: {item.get("confidence_score", 0.0):.2f}</span>'

                render_html(
                    f"""
                    <div class="paper-card" style="margin-bottom:12px; border-left:3px solid #2DD4BF;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                            <span style="font-weight:700; color:#2DD4BF; font-family:'JetBrains Mono', monospace; font-size:0.85rem;">ASSERTION #{item.get('claim_id')}</span>
                            <div>
                                {status_badge}
                                {score_badge}
                            </div>
                        </div>
                        <div style="font-size:0.96rem; font-weight:600; color:#F8FAFC; margin-bottom:10px;">
                            "{item.get('claim_text')}"
                        </div>
                        <div style="margin-bottom:10px;">
                            {study_badge}
                            {abstract_badge}
                        </div>
                        <div style="background-color:#111827; border-left:2px solid #2DD4BF; padding:10px 14px; border-radius:4px; font-size:0.86rem; color:#CBD5E1; margin-bottom:10px;">
                            <strong>Verification Logic:</strong> {item.get('reason')}
                        </div>
                    </div>
                    """
                )

                if item.get("has_causal_overstatement"):
                    st.warning(
                        "Correlation vs. Causation Notice: This assertion asserts direct causality, "
                        "but the supporting study is observational or preclinical."
                    )

                if item.get("matched_excerpt"):
                    with st.expander(f"Supporting Evidence Excerpt (PMID: {item.get('matched_pmid', 'N/A')})", expanded=False):
                        st.markdown(f"**Source Study:** *{item.get('matched_paper_title', 'PubMed Publication')}*")
                        st.markdown(f"> *\"{item.get('matched_excerpt')}\"*")
                        if item.get("matched_url"):
                            st.markdown(f"[View Verified Record on PubMed &bull; PMID {item.get('matched_pmid')}]({item['matched_url']})")

                st.markdown("")

        else:
            if is_abstained:
                st.info("Claim decomposition is not applicable because EvidenceBot abstained before generating speculative claims.")
            else:
                st.info("No claim-level decomposition records available for this query.")

    with tab_citations:
        st.markdown("#### Comprehensive Citation Integrity Audit")
        col_cit1, col_cit2 = st.columns(2)
        with col_cit1:
            render_html(
                f"""
                <div class="paper-card" style="border-left: 3px solid #10B981;">
                    <div style="font-size:0.75rem; color:#2DD4BF; font-family:'JetBrains Mono', monospace; text-transform:uppercase;">Verified Citations</div>
                    <div style="font-size:1.8rem; font-weight:800; color:#34D399;">{len(verified_citations)}</div>
                    <small style="color:#94A3B8;">Authentic PMIDs matched directly to NCBI database records.</small>
                </div>
                """
            )
        with col_cit2:
            h_color = "#EF4444" if hallucinated_pmids else "#10B981"
            h_text_color = "#F87171" if hallucinated_pmids else "#34D399"
            render_html(
                f"""
                <div class="paper-card" style="border-left: 3px solid {h_color};">
                    <div style="font-size:0.75rem; color:#2DD4BF; font-family:'JetBrains Mono', monospace; text-transform:uppercase;">Unverified Inventions</div>
                    <div style="font-size:1.8rem; font-weight:800; color:{h_text_color};">{len(hallucinated_pmids)}</div>
                    <small style="color:#94A3B8;">Invented PMIDs that did not exist in retrieved literature.</small>
                </div>
                """
            )

        st.markdown("---")

        if verified_citations:
            for v_cit in verified_citations:
                authors_str = ", ".join(v_cit.get("authors", [])[:3])
                if len(v_cit.get("authors", [])) > 3:
                    authors_str += " et al."

                doi_str = f" | DOI: {v_cit.get('doi')}" if v_cit.get("doi") else ""
                r_score = v_cit.get("relevance_score", 0.0)
                r_badge = f'<span class="pill-badge pill-high">RELEVANCE: {r_score:.2f}</span>' if r_score >= 0.40 else f'<span class="pill-badge pill-moderate">RELEVANCE: {r_score:.2f}</span>'

                render_html(
                    f"""
                    <div class="paper-card" style="padding:14px 18px; margin-bottom:10px;">
                        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:8px;">
                            <div>
                                <a href="{v_cit.get('url')}" target="_blank" style="font-weight:700; color:#F8FAFC; text-decoration:none; font-size:0.98rem; letter-spacing:-0.015em;">
                                    {v_cit.get('title')} &rarr;
                                </a>
                                <div style="font-size:0.82rem; color:#94A3B8; margin-top:2px;">
                                    {authors_str} &bull; <em>{v_cit.get('journal', 'Journal')}</em> ({v_cit.get('year', 'N/A')}){doi_str}
                                </div>
                            </div>
                            <div>
                                {r_badge}
                                <span class="pill-badge pill-teal">PMID {v_cit.get('pmid')}</span>
                            </div>
                        </div>
                        <div style="background-color:#111827; border-left:2px solid #2DD4BF; padding:8px 12px; margin-top:10px; border-radius:4px; font-size:0.86rem; color:#CBD5E1;">
                            <strong>Asserted Context:</strong> "{v_cit.get('claim_context')}"
                        </div>
                    </div>
                    """
                )
        else:
            st.info("No verified citations recorded.")

        if missing_citations:
            st.warning(f"Identified {len(missing_citations)} assertion(s) in the draft that made factual statements without citing a source PMID.")
        else:
            st.success("Citation Completeness: All substantive assertions include source PMIDs.")

    with tab_abstention:
        st.markdown("#### Empirical Abstention Subsystem")
        ab_rep = res.get("abstention_report") or {}

        if is_abstained:
            render_html(
                f"""
                <div class="abstention-alert">
                    <h4 style="color:#F87171; margin-top:0;">Empirical Abstention Enforced</h4>
                    <p style="font-weight:600; font-size:1.02rem; color:#F87171;">
                        No sufficient scientific evidence found for this query.
                    </p>
                    <hr style="border:0; border-top:1px solid rgba(239,68,68,0.3); margin:12px 0;">
                    <ul style="line-height:1.8; color:#CBD5E1; font-size:0.88rem; font-family:'JetBrains Mono', monospace;">
                        <li><strong>Query Ingestion:</strong> {ab_rep.get('search_query', question)}</li>
                        <li><strong>Candidate Records:</strong> {ab_rep.get('papers_retrieved_count', len(papers))} publication(s)</li>
                        <li><strong>Trigger Diagnosis:</strong> {ab_rep.get('reason', res.get('reason', 'N/A'))}</li>
                        <li><strong>Next Steps:</strong> {ab_rep.get('additional_research_required', 'Targeted clinical trials.')}</li>
                    </ul>
                </div>
                """
            )
        else:
            st.success("Abstention Guard Inactive: Retrieved literature satisfied all confidence criteria and established adequate empirical grounding.")

else:
    st.info("No active query in session. Execute a synthesis on the Research Dashboard to view grounding telemetry and diagnostics.")

render_disclaimer()
