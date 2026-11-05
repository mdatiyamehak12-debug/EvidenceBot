"""
Bio EvidenceBot - AI-Powered Biomedical Research Assistant
==========================================================
Discover, analyse and synthesise scientific evidence from peer-reviewed literature.
Powered by NCBI PubMed Central, Europe PMC, SentenceTransformers, and FAISS.
"""

import streamlit as st
from datetime import datetime
from utils import config
from utils.ui_components import (
    apply_theme,
    render_sidebar,
    render_disclaimer,
    render_confidence_badge,
    render_paper_card,
    render_evidence_availability,
)
from utils.history_manager import add_to_history, load_search_history
from backend.rag_pipeline import run_rag_pipeline

# =====================================================================
# Page Configuration
# =====================================================================
st.set_page_config(
    page_title="EvidenceBot – AI-Powered Biomedical Research Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply unified scientific design theme & sidebar
apply_theme()
render_sidebar(current_page="Home")

CURRENT_YEAR = 2026

# Check for query passed via sidebar recent search click
auto_execute_query = st.session_state.pop("query_to_run", None)
if auto_execute_query:
    st.session_state["active_query"] = auto_execute_query

current_query_val = st.session_state.get("active_query", "")

# =====================================================================
# 1. Main Dashboard Header
# =====================================================================
st.markdown(
    """
    <div class="dashboard-header">
        <div class="header-eyebrow">NATIONAL LIBRARY OF MEDICINE &bull; NCBI PUBMED &bull; PEER-REVIEWED LITERATURE</div>
        <h1>EvidenceBot</h1>
        <div class="header-tagline">AI-Powered Biomedical Research Assistant</div>
        <p class="header-subtitle">Discover, analyse and synthesise scientific evidence from peer-reviewed literature.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================================================
# 2. Research Inquiry Input Area
# =====================================================================
st.markdown(
    """
    <div style="font-size:0.90rem; font-weight:700; color:#14243A; margin-bottom:6px;">
        Research Question or Clinical Inquiry
    </div>
    """,
    unsafe_allow_html=True
)

sample_placeholder = "e.g., Does zinc supplementation reduce the duration or severity of the common cold?"
search_query = st.text_area(
    "Research Question or Clinical Inquiry:",
    value=current_query_val,
    height=85,
    placeholder=sample_placeholder,
    label_visibility="collapsed",
    help="Type any biomedical, pharmacological, or clinical research inquiry to search PubMed."
)

# Actions: Search Button & Clear Button
col_btn1, col_btn2, col_spacer = st.columns([1.8, 1, 3.2])
with col_btn1:
    search_clicked = st.button("🔍 Search & Synthesise Evidence", type="primary", use_container_width=True)
with col_btn2:
    clear_clicked = st.button("Clear Input", type="secondary", use_container_width=True)

if clear_clicked:
    st.session_state["active_query"] = ""
    st.session_state.pop("latest_result", None)
    st.session_state.pop("latest_question", None)
    st.rerun()

# Example Research Queries (Clean Minimalist Chips)
st.markdown(
    """
    <div style="margin-top:12px; margin-bottom:6px; font-size:0.82rem; font-weight:600; color:#6B7280;">
        Example Research Inquiries:
    </div>
    """,
    unsafe_allow_html=True
)

c_ex1, c_ex2, c_ex3, c_ex4 = st.columns(4)

with c_ex1:
    if st.button("Zinc supplementation & cold duration", key="ex_q1", use_container_width=True):
        st.session_state["active_query"] = "Does zinc supplementation reduce the duration or severity of common cold symptoms?"
        st.session_state["query_to_run"] = st.session_state["active_query"]
        st.rerun()

with c_ex2:
    if st.button("Metformin cellular pathway in T2D", key="ex_q2", use_container_width=True):
        st.session_state["active_query"] = "What is the primary cellular mechanism of action of metformin in type 2 diabetes?"
        st.session_state["query_to_run"] = st.session_state["active_query"]
        st.rerun()

with c_ex3:
    if st.button("Omega-3 & cardiovascular events", key="ex_q3", use_container_width=True):
        st.session_state["active_query"] = "Does dietary omega-3 fatty acid supplementation prevent major adverse cardiovascular events in healthy individuals?"
        st.session_state["query_to_run"] = st.session_state["active_query"]
        st.rerun()

with c_ex4:
    if st.button("Spirulina curing MS (Abstention)", key="ex_q4", use_container_width=True):
        st.session_state["active_query"] = "Can spirulina microalgae supplementation cure multiple sclerosis in human patients?"
        st.session_state["query_to_run"] = st.session_state["active_query"]
        st.rerun()

# =====================================================================
# 3. Collapsible Advanced Research Filters
# =====================================================================
# Keep advanced filters collapsed by default to maintain clean, uncluttered interface
with st.expander("⚙️ Advanced Research Filters", expanded=False):
    st.caption("Customise publication year range, paper retrieval volume, article type, and relevance thresholds:")
    
    col_f1, col_f2, col_f3 = st.columns([2.2, 1.4, 1.4])

    with col_f1:
        st.markdown("**Publication Year Range**")
        col_y_start, col_y_end = st.columns(2)
        with col_y_start:
            starting_year = st.number_input(
                "Starting Publication Year",
                min_value=1800,
                max_value=2030,
                value=int(st.session_state.get("start_year_val", 1900)),
                step=1,
                help="Type any valid starting 4-digit year (e.g., 1985, 2000, 2015)."
            )
        with col_y_end:
            ending_year = st.number_input(
                "Ending Publication Year",
                min_value=1800,
                max_value=2030,
                value=int(st.session_state.get("end_year_val", CURRENT_YEAR)),
                step=1,
                help="Type any valid ending 4-digit year (e.g., 1995, 2010, 2026)."
            )
        
        # Convenient "All Years" reset button
        if st.button("Set to All Years (1900–2026)", key="btn_all_years", type="secondary"):
            st.session_state["start_year_val"] = 1900
            st.session_state["end_year_val"] = CURRENT_YEAR
            st.rerun()

    with col_f2:
        st.markdown("**Article Limit**")
        max_papers = st.number_input(
            "Maximum Research Papers to Retrieve",
            min_value=1,
            max_value=100,
            value=int(st.session_state.get("max_papers_val", 10)),
            step=5,
            help="Configurable limit controlling the number of PubMed records to ingest (e.g., 5, 10, 15, 20, 50, 100)."
        )
        
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
            help="Filter candidate PubMed publications by study design."
        )

    with col_f3:
        st.markdown("**Relevance Guard**")
        threshold_val = st.slider(
            "Abstention Cosine Threshold",
            min_value=0.20,
            max_value=0.60,
            value=float(config.MIN_SIMILARITY_THRESHOLD),
            step=0.02,
            help="Cosine threshold for empirical abstention. If the top paper chunk scores below this value, EvidenceBot halts synthesis to prevent hallucination."
        )

# Validate Year Range Input
year_validation_error = False
if starting_year > ending_year:
    st.error(f"⚠️ Validation Error: Starting Publication Year ({starting_year}) cannot be greater than Ending Publication Year ({ending_year}). Please correct the range.")
    year_validation_error = True

# Compute display label for year filter
is_all_years = (starting_year <= 1900 and ending_year >= CURRENT_YEAR)
active_year_label = "All Years (1900–2026)" if is_all_years else f"{starting_year}–{ending_year}"

# =====================================================================
# 4. Pipeline Execution & Loading Animation
# =====================================================================
should_execute = search_clicked or (auto_execute_query is not None and len(auto_execute_query.strip()) > 0)

if should_execute:
    clean_q = search_query.strip()
    if not clean_q:
        st.warning("Please enter a research inquiry or scientific question first.")
    elif year_validation_error:
        st.warning("Please fix the publication year range error before searching.")
    else:
        st.session_state["active_query"] = clean_q
        st.session_state["start_year_val"] = starting_year
        st.session_state["end_year_val"] = ending_year
        st.session_state["max_papers_val"] = max_papers

        # Save to persistent search history (latest first, deduplicated)
        add_to_history(clean_q, year_range=active_year_label)

        # Loading animation
        status_box = st.status("Retrieving Peer-Reviewed Research from PubMed...", expanded=True)
        try:
            status_box.write(f"&bull; Applying publication year filter (`{active_year_label}`) and article limit (`{max_papers} papers`)...")
            status_box.write("&bull; Querying NCBI Entrez E-Utilities and Europe PMC database mirror...")
            status_box.write("&bull; Parsing candidate abstracts and generating 768-dim FAISS dense vector index...")
            status_box.write("&bull; Evaluating evidence sufficiency and formulating verified answer with authentic citations...")

            q_min = starting_year if not is_all_years else None
            q_max = ending_year if not is_all_years else None
            q_type = article_type_choice if article_type_choice != "All Article Types" else None

            result = run_rag_pipeline(
                clean_q,
                max_papers=int(max_papers),
                threshold=float(threshold_val),
                min_year=q_min,
                max_year=q_max,
                article_type=q_type
            )

            st.session_state["latest_result"] = result
            st.session_state["latest_question"] = clean_q
            st.session_state["latest_year_range"] = active_year_label

            status_box.update(label="Evidence Retrieval & Synthesis Complete", state="complete", expanded=False)
        except Exception as err:
            status_box.update(label="Retrieval Error", state="error")
            st.error(f"Error executing research pipeline: {err}")

# =====================================================================
# 5. Professional Research Results Dashboard (Organised into Sections)
# =====================================================================
if "latest_result" in st.session_state:
    result = st.session_state["latest_result"]
    question_display = st.session_state.get("latest_question", "")
    active_year_range = st.session_state.get("latest_year_range", active_year_label)
    is_abstention = result.get("is_abstention", False)
    retrieved_papers = result.get("papers", [])
    verified_pmids = set(result.get("verified_pmids", []))
    confidence_val = result.get("confidence", "Moderate")
    top_score = result.get("max_score", 0.0)

    st.markdown("---")
    st.markdown(f"### Research Findings for: *\"{question_display}\"*")

    # -----------------------------------------------------------------
    # SECTION B: Evidence Overview
    # -----------------------------------------------------------------
    st.markdown("#### Evidence Overview")
    render_evidence_availability(
        is_available=(not is_abstention and len(retrieved_papers) > 0),
        count=len(retrieved_papers),
        year_range=active_year_range
    )

    if is_abstention:
        # Clear, unambiguous insufficient evidence notification
        st.markdown(
            f"""
            <div style="background-color: #FEF2F2; border: 1px solid #FECACA; border-left: 4px solid #DC2626; border-radius: 10px; padding: 20px 24px; margin: 16px 0;">
                <div style="font-size: 1.08rem; font-weight: 700; color: #991B1B; margin-bottom: 6px;">
                    No sufficient scientific evidence found for this query.
                </div>
                <p style="color: #4B5563; font-size: 0.90rem; line-height: 1.6; margin: 0 0 10px 0;">
                    EvidenceBot strictly enforces an empirical abstention protocol. In scientific and biomedical research, 
                    refusing to synthesize unsupported claims prevents dangerous hallucinations and clinical misinformation.
                </p>
                <div style="background-color: #FFFFFF; border: 1px solid #FECACA; border-radius: 6px; padding: 10px 14px; font-size: 0.84rem; font-family:'JetBrains Mono', monospace; color:#1F2937;">
                    <div><strong>Inquiry:</strong> {question_display}</div>
                    <div><strong>Publication Filter:</strong> {active_year_range}</div>
                    <div><strong>Abstention Trigger:</strong> {result.get('reason', 'Retrieved literature does not meet confidence standards.')}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if retrieved_papers:
            st.markdown(f"#### Retrieved Candidate Papers ({len(retrieved_papers)} Records Evaluated)")
            st.caption("These candidate publications were retrieved but fell below cosine confidence thresholds:")
            for p in retrieved_papers:
                render_paper_card(p, is_cited=False)

    else:
        # -----------------------------------------------------------------
        # SECTION A: AI Research Synthesis
        # -----------------------------------------------------------------
        st.markdown(
            f"""
            <div style="margin-bottom:10px; display:flex; align-items:center; flex-wrap:wrap; gap:6px;">
                {render_confidence_badge(confidence_val, top_score)}
                <span class="mono-tag" style="background:#EBF8F7; color:#168C83; border:1px solid #99E3DD;">
                    ENGINE: {result.get('provider', 'Synthesizer')}
                </span>
                <span class="mono-tag">CHUNKS: {len(result.get('chunks', []))}</span>
                <span class="mono-tag">YEARS: {active_year_range}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("#### AI Research Synthesis")
        answer_text = result.get("answer", "")
        st.markdown(
            f"""
            <div class="answer-card">
                {answer_text}
            </div>
            """,
            unsafe_allow_html=True
        )

        # -----------------------------------------------------------------
        # SECTION D: References & Citations
        # -----------------------------------------------------------------
        citation_rep = result.get("citation_report") or {}
        verified_items = citation_rep.get("verified_citations", [])
        if verified_items:
            st.markdown(f"#### References ({len(verified_items)} Authenticated Citations)")
            for idx, item in enumerate(verified_items, 1):
                authors_str = ", ".join(item.get("authors", [])[:3])
                if len(item.get("authors", [])) > 3:
                    authors_str += " et al."
                st.markdown(
                    f"""
                    <div style="background:#FFFFFF; border:1px solid #E5E7EB; border-left:3px solid #168C83; border-radius:6px; padding:10px 14px; margin-bottom:8px;">
                        <div style="font-weight:700; font-size:0.95rem; color:#14243A;">
                            [{idx}] <a href="{item.get('url')}" target="_blank" style="color:#14243A; text-decoration:none;">{item.get('title')}</a>
                        </div>
                        <div style="font-size:0.82rem; color:#4B5563; margin-top:2px;">
                            {authors_str} &bull; <em>{item.get('journal', 'Journal')}</em> ({item.get('year', 'N/A')}) &bull; PMID: <code>{item.get('pmid')}</code>
                        </div>
                        <div style="font-size:0.84rem; color:#374151; margin-top:4px; background:#F8FAFC; padding:4px 8px; border-radius:4px;">
                            <strong>Cited Context:</strong> "{item.get('claim_context')}"
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # -----------------------------------------------------------------
        # SECTION C: Retrieved Research Papers
        # -----------------------------------------------------------------
        st.markdown("---")
        st.markdown(f"#### Retrieved Research Papers ({len(retrieved_papers)} Publications)")
        st.caption(f"Peer-reviewed scientific publications retrieved from PubMed matching **{active_year_range}**:")

        for paper in retrieved_papers:
            is_cited = paper.pmid in verified_pmids
            render_paper_card(paper, is_cited=is_cited)

else:
    # Clean Initial State: Show core platform capabilities without visual noise
    st.markdown("---")
    st.markdown(
        """
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:14px; margin-top:10px;">
            <div class="content-card" style="border-top:3px solid #168C83;">
                <div style="font-family:'JetBrains Mono', monospace; font-size:0.70rem; color:#168C83; font-weight:700; text-transform:uppercase;">Subsystem 01</div>
                <div style="font-weight:700; font-size:1.02rem; color:#14243A; margin:4px 0 6px 0;">Live PubMed Retrieval</div>
                <div style="font-size:0.86rem; color:#4B5563; line-height:1.55;">
                    Autonomous programmatic queries via NCBI Entrez E-Utilities and Europe PMC. Supports custom publication year ranges and article type constraints.
                </div>
            </div>
            <div class="content-card" style="border-top:3px solid #168C83;">
                <div style="font-family:'JetBrains Mono', monospace; font-size:0.70rem; color:#168C83; font-weight:700; text-transform:uppercase;">Subsystem 02</div>
                <div style="font-weight:700; font-size:1.02rem; color:#14243A; margin:4px 0 6px 0;">Dense Vector Indexing</div>
                <div style="font-size:0.86rem; color:#4B5563; line-height:1.55;">
                    In-memory FAISS dense index with 768-dim SentenceTransformers embeddings. Extracts semantically relevant scientific claim passages in milliseconds.
                </div>
            </div>
            <div class="content-card" style="border-top:3px solid #168C83;">
                <div style="font-family:'JetBrains Mono', monospace; font-size:0.70rem; color:#168C83; font-weight:700; text-transform:uppercase;">Subsystem 03</div>
                <div style="font-weight:700; font-size:1.02rem; color:#14243A; margin:4px 0 6px 0;">Deterministic Grounding</div>
                <div style="font-size:0.86rem; color:#4B5563; line-height:1.55;">
                    Synthesizes objective scientific consensus based strictly on retrieved abstract excerpts with zero invented citations or external clinical claims.
                </div>
            </div>
            <div class="content-card" style="border-top:3px solid #168C83;">
                <div style="font-family:'JetBrains Mono', monospace; font-size:0.70rem; color:#168C83; font-weight:700; text-transform:uppercase;">Subsystem 04</div>
                <div style="font-weight:700; font-size:1.02rem; color:#14243A; margin:4px 0 6px 0;">Empirical Abstention</div>
                <div style="font-size:0.86rem; color:#4B5563; line-height:1.55;">
                    Safely withholds answers when literature is sparse, contradictory, or below cosine thresholds, preventing dangerous medical hallucinations.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Refined Institutional Disclaimer Footer
render_disclaimer()
