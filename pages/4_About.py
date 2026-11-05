"""
EvidenceBot - Page 4: Architecture & Methodology
================================================
Technical documentation on EvidenceBot's design philosophy,
retrieval-augmented generation (RAG) architecture, underlying technologies, and governance protocols.
Zero informal emojis; deeptech telemetry design.
"""

import streamlit as st
from utils.ui_components import apply_theme, render_sidebar, render_disclaimer

st.set_page_config(
    page_title="EvidenceBot – Architecture & Methodology",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply unified styling and sidebar
apply_theme()
render_sidebar(current_page="Platform Architecture")

# Page Header
st.markdown(
    """
    <div style="margin-bottom: 22px;">
        <div style="margin-bottom:6px;">
            <span class="mono-tag" style="color:#0f766e; background:#f0fdfa; border:1px solid #99f6e4;">
                SYSTEM ARCHITECTURE & GOVERNANCE
            </span>
        </div>
        <h2 style="color: #0f172a; margin-bottom: 4px; font-weight:800; letter-spacing:-0.03em;">Architecture & Methodology</h2>
        <p style="color: #475569; margin: 0; font-size:0.98rem;">Enterprise Retrieval-Augmented Generation (RAG) framework, PubMed data provenance, and deterministic verification protocols.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 1. Platform Philosophy
st.markdown(
    """
    <div style="margin-bottom:10px;">
        <span class="mono-tag" style="color:#94a3b8; background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.1);">DESIGN PRINCIPLES</span>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    In the biomedical sciences, ungrounded artificial intelligence outputs are hazardous. 
    Standard large language models (LLMs) routinely invent non-existent PubMed citations, synthesize conflicting clinical claims without nuance, 
    and output speculative conclusions when scientific consensus does not exist.

    EvidenceBot enforces three architectural invariants:
    - **Empirical Literature Grounding:** All synthesized statements originate strictly from authentic peer-reviewed abstracts indexed on the National Library of Medicine (NCBI PubMed).
    - **Deterministic Provenance:** All factual claims are deterministically attributed to specific PubMed Identifiers (`PMID`).
    - **Empirical Abstention:** The engine autonomously halts generation and withholds conclusions when retrieved literature fails confidence thresholds.
    """
)

st.markdown("---")

# 2. Pipeline Architecture
st.markdown(
    """
    <div style="margin-bottom:10px;">
        <span class="mono-tag" style="color:#94a3b8; background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.1);">EXECUTION PIPELINE</span>
    </div>
    """,
    unsafe_allow_html=True
)
st.caption("EvidenceBot executes an end-to-end 6-stage scientific discovery and verification pipeline:")

col_s1, col_s2, col_s3 = st.columns(3)

with col_s1:
    st.markdown(
        """
        <div class="feature-card">
            <div class="stat-label">Stage 01</div>
            <div class="feature-title">NCBI Entrez Querying</div>
            <div class="feature-desc">Formulates search syntax and queries NCBI PubMed E-Utilities (<code>esearch</code>) to identify relevant peer-reviewed publication IDs.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_s2:
    st.markdown(
        """
        <div class="feature-card">
            <div class="stat-label">Stage 02</div>
            <div class="feature-title">Abstract Extraction</div>
            <div class="feature-desc">Downloads PubMed XML via <code>efetch</code>, parsing titles, journals, authors, and structured abstracts with medical abbreviation preservation.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_s3:
    st.markdown(
        """
        <div class="feature-card">
            <div class="stat-label">Stage 03</div>
            <div class="feature-title">Dense FAISS Vector Index</div>
            <div class="feature-desc">Encodes passages into dense 384/768-dimensional vectors using <code>all-MiniLM-L6-v2</code>. FAISS executes sub-millisecond Cosine Similarity ranking.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("")
col_s4, col_s5, col_s6 = st.columns(3)

with col_s4:
    st.markdown(
        """
        <div class="feature-card">
            <div class="stat-label">Stage 04</div>
            <div class="feature-title">Abstention Evaluation</div>
            <div class="feature-desc">Audits candidate chunk similarity against a strict cosine threshold (0.32). If literature is absent or off-target, generation halts immediately.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_s5:
    st.markdown(
        """
        <div class="feature-card">
            <div class="stat-label">Stage 05</div>
            <div class="feature-title">Constrained Synthesis</div>
            <div class="feature-desc">Inference engine receives strict prompt constraints restricting output strictly to facts present in retrieved excerpts.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_s6:
    st.markdown(
        """
        <div class="feature-card">
            <div class="stat-label">Stage 06</div>
            <div class="feature-title">Provenance Audit</div>
            <div class="feature-desc">Parses generated text to ensure every cited PMID exists in the retrieved set and matches its parent publication metadata.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# 3. Technology Stack
st.markdown(
    """
    <div style="margin-bottom:10px;">
        <span class="mono-tag" style="color:#94a3b8; background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.1);">CORE TECHNOLOGY STACK</span>
    </div>
    """,
    unsafe_allow_html=True
)

tech_col1, tech_col2 = st.columns(2)

with tech_col1:
    st.markdown(
        """
        <div class="stat-tile">
            <div class="stat-label">Ingestion & Runtime</div>
            <ul style="margin: 8px 0 0 16px; padding: 0; color: #cbd5e1; font-size: 0.88rem; line-height: 1.8;">
                <li><strong>Python 3.14:</strong> High-performance core backend runtime.</li>
                <li><strong>Streamlit:</strong> Multi-page reactive biomedical dashboard.</li>
                <li><strong>NCBI PubMed E-Utilities:</strong> Direct programmatic REST gateway (<code>esearch</code>, <code>efetch</code>).</li>
                <li><strong>ElementTree & BeautifulSoup4:</strong> Robust XML schema parsing.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

with tech_col2:
    st.markdown(
        """
        <div class="stat-tile">
            <div class="stat-label">Vector Retrieval & Inference</div>
            <ul style="margin: 8px 0 0 16px; padding: 0; color: #cbd5e1; font-size: 0.88rem; line-height: 1.8;">
                <li><strong>SentenceTransformers:</strong> Dense semantic embedding models (<code>all-MiniLM-L6-v2</code>).</li>
                <li><strong>FAISS (Meta AI):</strong> GPU/CPU optimized dense vector index (<code>IndexFlatIP</code>).</li>
                <li><strong>Google Gemini 2.5:</strong> Grounded scientific synthesis with deterministic fallback.</li>
                <li><strong>Pytest & Unittest:</strong> Complete automated test suite (28/28 passing).</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# 4. Limitations
st.markdown("### Methodological Scope & Limitations")
st.markdown(
    """
    1. **Abstract-Level Evidence:** EvidenceBot indexes peer-reviewed **abstract summaries** from PubMed. While abstracts capture primary endpoints, full clinical protocols, adverse-event tables, and sub-group distributions require full-text manuscripts.
    2. **Publication Bias:** Biomedical databases catalog published studies, which historically favor statistically significant findings.
    3. **Clinical Governance:** EvidenceBot synthesizes academic literature for exploration, research, and education. It does not replace clinical judgment or individual physician consultation.
    """
)

# Standard Disclaimer
render_disclaimer()
