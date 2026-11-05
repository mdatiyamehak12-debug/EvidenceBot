"""
Bio EvidenceBot - Architecture & Methodology (Page 4)
======================================================
Technical documentation on EvidenceBot's design philosophy,
retrieval-augmented generation (RAG) architecture, underlying technologies, and governance protocols.
"""

import streamlit as st
from utils.ui_components import apply_theme, render_sidebar, render_disclaimer, render_html

st.set_page_config(
    page_title="EvidenceBot – Architecture & Methodology",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply unified dark styling and sidebar
apply_theme()
render_sidebar(current_page="Platform Architecture")

# Page Header Card
render_html(
    """
    <div class="query-header-card" style="margin-bottom:20px;">
        <div class="query-header-label">SYSTEM ARCHITECTURE & GOVERNANCE</div>
        <div class="query-header-text" style="font-size:1.6rem;">Architecture & Methodology</div>
        <p style="color:#94A3B8; margin:6px 0 0 0; font-size:0.95rem;">
            Enterprise Retrieval-Augmented Generation (RAG) framework, PubMed data provenance, and deterministic verification protocols.
        </p>
    </div>
    """
)

# 1. Platform Philosophy
st.markdown("#### Design Principles & Architectural Invariants")
st.markdown(
    """
    In biomedical and pharmacological sciences, ungrounded artificial intelligence outputs present severe clinical risks. 
    Standard large language models (LLMs) routinely invent non-existent PubMed citations, synthesize conflicting clinical claims without nuance, 
    and output speculative conclusions when scientific consensus does not exist.

    EvidenceBot enforces three core architectural invariants:
    - **Empirical Literature Grounding:** All synthesized statements originate strictly from authentic peer-reviewed abstracts indexed on the National Library of Medicine (NCBI PubMed and Europe PMC).
    - **Deterministic Provenance:** All factual claims are deterministically attributed to specific PubMed Identifiers (`PMID`).
    - **Empirical Abstention:** The engine autonomously halts generation and withholds conclusions when retrieved literature fails cosine confidence thresholds.
    """
)

st.markdown("---")

# 2. Pipeline Architecture
st.markdown("#### Execution Pipeline")
st.caption("EvidenceBot executes an end-to-end 6-stage scientific discovery and verification pipeline:")

col_s1, col_s2, col_s3 = st.columns(3)

with col_s1:
    render_html(
        """
        <div class="paper-card">
            <div style="font-size:0.75rem; color:#2DD4BF; font-family:'JetBrains Mono', monospace; text-transform:uppercase;">Stage 01</div>
            <div style="font-weight:700; font-size:1.0rem; color:#F8FAFC; margin:4px 0 6px 0;">NCBI Entrez Querying</div>
            <div style="font-size:0.86rem; color:#94A3B8; line-height:1.55;">Queries NCBI PubMed E-Utilities (<code>esearch</code>) and Europe PMC to identify relevant peer-reviewed publication IDs.</div>
        </div>
        """
    )

with col_s2:
    render_html(
        """
        <div class="paper-card">
            <div style="font-size:0.75rem; color:#2DD4BF; font-family:'JetBrains Mono', monospace; text-transform:uppercase;">Stage 02</div>
            <div style="font-weight:700; font-size:1.0rem; color:#F8FAFC; margin:4px 0 6px 0;">Abstract Extraction</div>
            <div style="font-size:0.86rem; color:#94A3B8; line-height:1.55;">Downloads PubMed XML via <code>efetch</code>, parsing titles, journals, authors, and structured abstracts.</div>
        </div>
        """
    )

with col_s3:
    render_html(
        """
        <div class="paper-card">
            <div style="font-size:0.75rem; color:#2DD4BF; font-family:'JetBrains Mono', monospace; text-transform:uppercase;">Stage 03</div>
            <div style="font-weight:700; font-size:1.0rem; color:#F8FAFC; margin:4px 0 6px 0;">Dense Vector Index</div>
            <div style="font-size:0.86rem; color:#94A3B8; line-height:1.55;">Encodes passages into dense vectors using <code>all-MiniLM-L6-v2</code>. FAISS executes sub-millisecond ranking.</div>
        </div>
        """
    )

st.markdown("")
col_s4, col_s5, col_s6 = st.columns(3)

with col_s4:
    render_html(
        """
        <div class="paper-card">
            <div style="font-size:0.75rem; color:#2DD4BF; font-family:'JetBrains Mono', monospace; text-transform:uppercase;">Stage 04</div>
            <div style="font-weight:700; font-size:1.0rem; color:#F8FAFC; margin:4px 0 6px 0;">Abstention Check</div>
            <div style="font-size:0.86rem; color:#94A3B8; line-height:1.55;">Audits candidate chunk similarity against strict cosine threshold (0.32). If literature is absent, synthesis halts.</div>
        </div>
        """
    )

with col_s5:
    render_html(
        """
        <div class="paper-card">
            <div style="font-size:0.75rem; color:#2DD4BF; font-family:'JetBrains Mono', monospace; text-transform:uppercase;">Stage 05</div>
            <div style="font-weight:700; font-size:1.0rem; color:#F8FAFC; margin:4px 0 6px 0;">Constrained Synthesis</div>
            <div style="font-size:0.86rem; color:#94A3B8; line-height:1.55;">Inference engine receives strict constraints restricting output strictly to facts present in retrieved excerpts.</div>
        </div>
        """
    )

with col_s6:
    render_html(
        """
        <div class="paper-card">
            <div style="font-size:0.75rem; color:#2DD4BF; font-family:'JetBrains Mono', monospace; text-transform:uppercase;">Stage 06</div>
            <div style="font-weight:700; font-size:1.0rem; color:#F8FAFC; margin:4px 0 6px 0;">Provenance Audit</div>
            <div style="font-size:0.86rem; color:#94A3B8; line-height:1.55;">Parses generated text to ensure every cited PMID exists in the retrieved set and matches publication metadata.</div>
        </div>
        """
    )

st.markdown("---")

# 3. Technology Stack
st.markdown("#### Core Technology Stack")

tech_col1, tech_col2 = st.columns(2)

with tech_col1:
    render_html(
        """
        <div class="paper-card">
            <div style="font-size:0.75rem; color:#2DD4BF; font-family:'JetBrains Mono', monospace; text-transform:uppercase;">Ingestion & Runtime</div>
            <ul style="margin: 8px 0 0 16px; padding: 0; color: #94A3B8; font-size: 0.88rem; line-height: 1.8;">
                <li><strong>Python:</strong> Core backend runtime environment.</li>
                <li><strong>Streamlit:</strong> Reactive biomedical AI dashboard.</li>
                <li><strong>NCBI PubMed E-Utilities:</strong> Direct programmatic REST gateway (<code>esearch</code>, <code>efetch</code>).</li>
                <li><strong>Europe PMC Mirror:</strong> Zero-downtime redundant fallback for NCBI API outages.</li>
            </ul>
        </div>
        """
    )

with tech_col2:
    render_html(
        """
        <div class="paper-card">
            <div style="font-size:0.75rem; color:#2DD4BF; font-family:'JetBrains Mono', monospace; text-transform:uppercase;">Vector Retrieval & Inference</div>
            <ul style="margin: 8px 0 0 16px; padding: 0; color: #94A3B8; font-size: 0.88rem; line-height: 1.8;">
                <li><strong>SentenceTransformers:</strong> Dense semantic embedding models (<code>all-MiniLM-L6-v2</code>).</li>
                <li><strong>FAISS (Meta AI):</strong> High-performance dense vector index (<code>IndexFlatIP</code>).</li>
                <li><strong>Grounded LLMs:</strong> Google Gemini / OpenAI with deterministic fallback.</li>
                <li><strong>Automated Test Suite:</strong> 37 automated regression & unit tests.</li>
            </ul>
        </div>
        """
    )

# Standard Disclaimer
render_disclaimer()
