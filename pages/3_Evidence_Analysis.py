"""
EvidenceBot - Page 3: Evidence & Grounding Analysis
==================================================
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
)
from backend.evidence_checker import verify_answer_claims
from backend.citation_checker import validate_citations_comprehensive

st.set_page_config(
    page_title="EvidenceBot – Grounding & Audit",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply unified styling and sidebar
apply_theme()
render_sidebar(current_page="Grounding & Audit")

# Page Header
st.markdown(
    """
    <div style="margin-bottom: 22px;">
        <h2 style="color: #0f172a; margin-bottom: 4px; font-weight:800; letter-spacing:-0.02em;">🔬 Evidence Grounding & Verification Audit</h2>
        <p style="color: #64748b; margin: 0; font-size:1.02rem;">Atomic claim-level fact-checking, citation provenance verification, and scientific abstention diagnostics.</p>
    </div>
    """,
    unsafe_allow_html=True
)

if "latest_result" in st.session_state:
    res = st.session_state["latest_result"]
    question = st.session_state.get("latest_question", "")
    answer_text = res.get("answer", "")
    chunks = res.get("chunks", [])
    papers = res.get("papers", [])
    is_abstained = res.get("is_abstention", False)
    top_score = res.get("max_score", 0.0)

    st.markdown(f"**Analyzed Biomedical Query:** *\"{question}\"*")
    st.markdown("---")

    # =====================================================================
    # 1. Verification Metric Cards & Alignment Gauge
    # =====================================================================
    st.markdown("### 📊 Verification Status Overview")

    # Retrieve or run claim verification
    claims_data = res.get("verified_claims", [])
    if not claims_data and answer_text and chunks and not is_abstained:
        with st.spinner("Analyzing claim-level empirical grounding..."):
            claim_objs = verify_answer_claims(answer_text, chunks)
            claims_data = [c.to_dict() for c in claim_objs]
            st.session_state["latest_result"]["verified_claims"] = claims_data

    # Retrieve or run citation audit
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
        st.metric("Claims Audited", total_claims)
    with col_m2:
        st.metric("Directly Supported", supported_count)
    with col_m3:
        st.metric("Verified Citations", len(verified_citations))
    with col_m4:
        st.metric("Contradicted Findings", contradicted_count)
    with col_m5:
        st.metric("Hallucinated PMIDs", len(hallucinated_pmids))

    # Similarity Score vs Threshold Gauge
    st.markdown("#### 🎯 Semantic Similarity vs. Abstention Threshold")
    progress_val = min(1.0, max(0.0, top_score))
    st.progress(progress_val, text=f"Top Cosine Similarity: {top_score:.2f} (Required Threshold: {config.MIN_SIMILARITY_THRESHOLD:.2f})")

    if is_abstained:
        st.error(
            f"🔴 **Scientific Abstention Enforced:** Top score ({top_score:.2f}) did not satisfy the required threshold ({config.MIN_SIMILARITY_THRESHOLD:.2f}). "
            "EvidenceBot actively refused to synthesize ungrounded conclusions."
        )
    else:
        st.success(
            f"🟢 **Empirical Baseline Verified:** Retrieved passages demonstrated strong semantic alignment ({top_score:.2f} >= {config.MIN_SIMILARITY_THRESHOLD:.2f})."
        )

    st.markdown("---")

    # =====================================================================
    # 2. Detailed Verification Tabs
    # =====================================================================
    tab_claims, tab_citations, tab_abstention = st.tabs([
        "📋 Claim Grounding Feed",
        "📚 Citation Integrity Audit",
        "🛡️ Abstention Diagnostics"
    ])

    # -----------------------------------------------------------------
    # TAB 1: Claim Grounding Feed
    # -----------------------------------------------------------------
    with tab_claims:
        st.markdown("#### Claim-by-Claim Verification Feed")
        st.caption("Every factual assertion in the synthesized answer is individually verified against retrieved PubMed excerpts:")

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
                study_badge = f'<span class="badge-pill badge-prelim">{item.get("study_type", "Biomedical Literature")}</span>'
                abstract_badge = '<span class="badge-pill badge-cyan">Abstract-Level Evidence</span>'
                score_badge = f'<span class="badge-pill badge-moderate">Similarity: {item.get("confidence_score", 0.0):.2f}</span>'

                st.markdown(
                    f"""
                    <div class="bio-card" style="margin-bottom:12px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                            <span style="font-weight:700; color:#0f2b48;">Claim #{item.get('claim_id')}</span>
                            <div>
                                {status_badge}
                                {score_badge}
                            </div>
                        </div>
                        <div style="font-size:1.02rem; font-weight:500; color:#1e293b; margin-bottom:10px;">
                            "{item.get('claim_text')}"
                        </div>
                        <div style="margin-bottom:10px;">
                            {study_badge}
                            {abstract_badge}
                        </div>
                        <div style="background-color:#f8fafc; border-left:3px solid #00b4d8; padding:10px 14px; border-radius:4px; font-size:0.88rem; margin-bottom:10px;">
                            <strong>Verification Reason:</strong> {item.get('reason')}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if item.get("has_causal_overstatement"):
                    st.warning(
                        "⚠️ **Correlation vs. Causation Caution**: This claim asserts direct causality, "
                        "but the supporting study is observational or preclinical. Observational associations do not establish clinical causation."
                    )

                if item.get("matched_excerpt"):
                    with st.expander(f"🔍 Supporting Excerpt & Source Study (PMID: {item.get('matched_pmid', 'N/A')})", expanded=False):
                        st.markdown(f"**Source Study:** *{item.get('matched_paper_title', 'PubMed Publication')}*")
                        st.markdown(f"> *\"{item.get('matched_excerpt')}\"*")
                        if item.get("matched_url"):
                            st.markdown(f"[🔗 View Verified Record on PubMed [PMID: {item.get('matched_pmid')}]]({item['matched_url']})")

                st.markdown("")

        else:
            if is_abstained:
                st.info("ℹ️ Claim decomposition is not applicable because EvidenceBot abstained before generating speculative claims.")
            else:
                st.info("No claim-level decomposition records available for this query.")

    # -----------------------------------------------------------------
    # TAB 2: Citation Integrity Audit
    # -----------------------------------------------------------------
    with tab_citations:
        st.markdown("#### 📚 Comprehensive Citation Integrity Audit")
        st.caption("EvidenceBot audits all citations to ensure PMIDs exist in retrieved literature, metadata is authentic, and claims are supported.")

        col_cit1, col_cit2 = st.columns(2)
        with col_cit1:
            st.markdown(
                f"""
                <div class="bio-card" style="border-left: 4px solid #10b981;">
                    <h5 style="color:#047857; margin-top:0;">✅ Verified PubMed Citations</h5>
                    <p style="font-size:1.8rem; font-weight:700; color:#065f46; margin:0;">{len(verified_citations)}</p>
                    <small style="color:#64748b;">Authentic PMIDs matched directly to NCBI database records.</small>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col_cit2:
            h_color = "#ef4444" if hallucinated_pmids else "#10b981"
            h_text_color = "#991b1b" if hallucinated_pmids else "#065f46"
            st.markdown(
                f"""
                <div class="bio-card" style="border-left: 4px solid {h_color};">
                    <h5 style="color:{h_text_color}; margin-top:0;">🛡️ Hallucinated References</h5>
                    <p style="font-size:1.8rem; font-weight:700; color:{h_text_color}; margin:0;">{len(hallucinated_pmids)}</p>
                    <small style="color:#64748b;">Invented PMIDs that did not exist in retrieved literature.</small>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("---")

        # 1. Verified Citations List
        st.markdown("##### 1. Verified Citations with Clickable PubMed Links")
        if verified_citations:
            for v_cit in verified_citations:
                authors_str = ", ".join(v_cit.get("authors", [])[:3])
                if len(v_cit.get("authors", [])) > 3:
                    authors_str += " et al."
                
                doi_str = f" | DOI: {v_cit.get('doi')}" if v_cit.get("doi") else ""
                r_score = v_cit.get("relevance_score", 0.0)
                r_badge = f'<span class="badge-pill badge-high">Relevance: {r_score:.2f}</span>' if r_score >= 0.40 else f'<span class="badge-pill badge-moderate">Relevance: {r_score:.2f}</span>'

                st.markdown(
                    f"""
                    <div class="bio-card" style="padding:12px 16px; margin-bottom:10px;">
                        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                            <div>
                                <a href="{v_cit.get('url')}" target="_blank" style="font-weight:700; color:#0077b6; text-decoration:none; font-size:1.02rem;">
                                    🔗 {v_cit.get('title')}
                                </a>
                                <div style="font-size:0.85rem; color:#64748b; margin-top:2px;">
                                    {authors_str} • <em>{v_cit.get('journal', 'Journal')}</em> ({v_cit.get('year', 'N/A')}){doi_str}
                                </div>
                            </div>
                            <div>
                                {r_badge}
                                <span class="badge-pill badge-cyan">PMID: {v_cit.get('pmid')}</span>
                            </div>
                        </div>
                        <div style="background-color:#f8fafc; border-left:3px solid #00b4d8; padding:8px 12px; margin-top:8px; border-radius:4px; font-size:0.86rem; color:#334155;">
                            <strong>Claim Context:</strong> "{v_cit.get('claim_context')}"
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("No verified citations recorded.")

        # 2. Missing Citations
        st.markdown("##### 2. Missing Citations (Factual Claims Lacking a PMID)")
        if missing_citations:
            st.warning(f"Identified {len(missing_citations)} assertion(s) in the draft that made factual statements without citing a source PMID:")
            for mc in missing_citations:
                st.markdown(f"- ⚠️ *\"{mc}\"*")
        else:
            st.success("✅ No missing citations detected. All substantive assertions include source PMIDs.")

        # 3. Unsupported Claims
        st.markdown("##### 3. Unsupported Claims (Cited Paper Weakly Relevant to Assertion)")
        if unsupported_claims:
            st.warning(f"Identified {len(unsupported_claims)} claim(s) where the cited source had weak semantic relevance (< {config.MIN_SIMILARITY_THRESHOLD:.2f}):")
            for uc in unsupported_claims:
                st.markdown(
                    f"""
                    <div class="bio-card" style="border-left:4px solid #f59e0b; margin-bottom:8px;">
                        <strong>Claim:</strong> "{uc.get('claim')}"<br>
                        <strong>Cited PMID:</strong> <code>{uc.get('cited_pmid')}</code> | <strong>Similarity:</strong> {uc.get('relevance_score'):.2f}<br>
                        <small style="color:#64748b;"><strong>Audit Note:</strong> {uc.get('reason')}</small>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.success("✅ All citations demonstrate strong semantic relevance to the claims citing them.")

        # 4. Unused Retrieved Papers
        unused_pmids = citation_rep.get("unused_retrieved_pmids", [])
        if unused_pmids:
            with st.expander(f"📦 Unused Retrieved Papers ({len(unused_pmids)} publications retrieved but not cited)", expanded=False):
                st.caption("These candidate papers were retrieved from PubMed during the initial search but were not directly cited in the final synthesis:")
                for upmid in unused_pmids:
                    match_p = next((p for p in papers if p.pmid == upmid), None)
                    p_title = match_p.title if match_p else "PubMed Publication"
                    st.markdown(f"- [`PMID: {upmid}`](https://pubmed.ncbi.nlm.nih.gov/{upmid}/) — *{p_title}*")

    # -----------------------------------------------------------------
    # TAB 3: Abstention Diagnostics
    # -----------------------------------------------------------------
    with tab_abstention:
        st.markdown("#### 🛡️ Scientific Abstention Diagnostics")
        st.caption("EvidenceBot actively refuses to generate answers when literature is insufficient, conflicting, or irrelevant.")

        ab_rep = res.get("abstention_report") or {}

        # 5 Trigger Conditions Overview
        st.markdown("##### The 5 Scientific Abstention Triggers:")
        
        c_tr1, c_tr2, c_tr3, c_tr4, c_tr5 = st.columns(5)
        with c_tr1:
            st.markdown(
                """
                <div class="bio-card" style="text-align:center; padding:10px;">
                    <div style="font-size:1.4rem;">1️⃣</div>
                    <strong style="font-size:0.85rem;">Zero Papers</strong>
                    <div style="font-size:0.75rem; color:#64748b;">No results found in PubMed</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with c_tr2:
            st.markdown(
                """
                <div class="bio-card" style="text-align:center; padding:10px;">
                    <div style="font-size:1.4rem;">2️⃣</div>
                    <strong style="font-size:0.85rem;">Empty Abstracts</strong>
                    <div style="font-size:0.75rem; color:#64748b;">Title-only records without text</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with c_tr3:
            st.markdown(
                """
                <div class="bio-card" style="text-align:center; padding:10px;">
                    <div style="font-size:1.4rem;">3️⃣</div>
                    <strong style="font-size:0.85rem;">Low Relevance</strong>
                    <div style="font-size:0.75rem; color:#64748b;">Similarity below threshold (< 0.32)</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with c_tr4:
            st.markdown(
                """
                <div class="bio-card" style="text-align:center; padding:10px;">
                    <div style="font-size:1.4rem;">4️⃣</div>
                    <strong style="font-size:0.85rem;">Conflicting Evidence</strong>
                    <div style="font-size:0.75rem; color:#64748b;">Direct contradictions in literature</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with c_tr5:
            st.markdown(
                """
                <div class="bio-card" style="text-align:center; padding:10px;">
                    <div style="font-size:1.4rem;">5️⃣</div>
                    <strong style="font-size:0.85rem;">Unsupported Claims</strong>
                    <div style="font-size:0.75rem; color:#64748b;">No verified supporting passages</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("---")

        if is_abstained:
            st.markdown(
                f"""
                <div class="abstention-box">
                    <h4 style="color:#be123c; margin-top:0;">🛑 Scientific Abstention Status: Enforced</h4>
                    <p style="font-weight:600; font-size:1.05rem; color:#9f1239;">
                        "{config.ABSTENTION_MESSAGE}"
                    </p>
                    <hr style="border:0; border-top:1px solid #fecdd3; margin:12px 0;">
                    <ul style="line-height:1.8; color:#1e293b;">
                        <li><strong>What was searched:</strong> <code>{ab_rep.get('search_query', question)}</code></li>
                        <li><strong>How many papers were retrieved:</strong> <strong>{ab_rep.get('papers_retrieved_count', len(papers))}</strong> publication(s)</li>
                        <li><strong>Why the evidence was insufficient:</strong> {ab_rep.get('reason', res.get('reason', 'N/A'))}</li>
                        <li><strong>What additional research may be required:</strong> {ab_rep.get('additional_research_required', 'Targeted clinical trials.')}</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.success("✅ **Abstention Not Triggered:** Retrieved literature exceeded confidence thresholds and provided adequate, grounded evidence to answer the inquiry.")

    st.markdown("---")

    # =====================================================================
    # 3. Scientific Methodology & Limitations Notice
    # =====================================================================
    st.markdown("### ⚠️ Methodological Limitations & Safety Guardrails")
    col_c1, col_c2 = st.columns(2)

    with col_c1:
        st.markdown(
            """
            <div class="bio-card" style="border-left: 4px solid #f59e0b;">
                <h5 style="color:#b45309; margin-top:0;">⚖️ Correlation vs. Causation</h5>
                <p style="font-size:0.87rem; color:#475569; margin:0;">
                    Epidemiological cohort studies routinely observe that deficient serum biomarker levels 
                    correlate with elevated disease risk. However, correlation alone does not prove that therapeutic 
                    supplementation reverses disease endpoints. EvidenceBot actively downgrades causal claims when only 
                    correlational data exists.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_c2:
        st.markdown(
            """
            <div class="bio-card" style="border-left: 4px solid #00b4d8;">
                <h5 style="color:#0369a1; margin-top:0;">📖 Abstract-Only Limitation</h5>
                <p style="font-size:0.87rem; color:#475569; margin:0;">
                    All retrieved excerpts represent peer-reviewed <strong>abstract summaries</strong> indexed on NCBI PubMed. 
                    Full study protocols, adverse-event tables, sub-group stratification, and complete statistical distributions 
                    require review of full-text publications.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

else:
    st.info("💡 No question has been analyzed yet. Run a search on **Ask EvidenceBot** to view similarity metrics, citation verification, and abstention diagnostics.")

# Disclaimer
render_disclaimer()
