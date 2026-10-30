"""
EvidenceBot - Page 4: About & Platform Architecture
===================================================
Provides comprehensive documentation on EvidenceBot's design philosophy,
system architecture, underlying technologies, limitations, and biomedical disclaimers.
"""

import streamlit as st
from utils.ui_components import apply_theme, render_sidebar, render_disclaimer

st.set_page_config(
    page_title="EvidenceBot – Platform Architecture",
    page_icon="🛡️",
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
        <h2 style="color: #0f172a; margin-bottom: 4px; font-weight:800; letter-spacing:-0.02em;">🛡️ Platform Architecture & Governance</h2>
        <p style="color: #64748b; margin: 0; font-size:1.02rem;">Enterprise Retrieval-Augmented Generation (RAG) framework, PubMed data provenance, and ethical abstention protocols.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================================================
# 1. Project Overview & Mission
# =====================================================================
st.markdown("### 🎯 Project Overview & Mission")
st.markdown(
    """
    In the life sciences and healthcare, hallucinated artificial intelligence outputs are not merely inconvenient—they are hazardous. 
    Standard large language models (LLMs) often generate fabricated medical references, invent non-existent PubMed IDs (PMIDs), 
    and answer questions even when real scientific consensus does not exist.

    **EvidenceBot was engineered to solve this through three core principles:**
    1. **Empirical Literature Grounding:** Synthesizes answers strictly from real scientific abstracts retrieved from the U.S. National Library of Medicine (NCBI PubMed).
    2. **Guaranteed Citation Provenance:** Links every cited finding to an authentic PubMed ID (`[PMID: 12345678]`).
    3. **Ethical Scientific Abstention:** Actively withholds generation and admits when available peer-reviewed evidence is insufficient.
    """
)

st.markdown("---")

# =====================================================================
# 2. How EvidenceBot Works (The RAG Pipeline)
# =====================================================================
st.markdown("### 🔄 How EvidenceBot Works")
st.caption("EvidenceBot follows an end-to-end 6-stage Retrieval-Augmented Generation (RAG) architecture:")

col_s1, col_s2, col_s3 = st.columns(3)

with col_s1:
    st.markdown(
        """
        <div class="bio-card" style="height:100%;">
            <div style="font-weight:700; color:#0f2b48; font-size:1.05rem;">1. Live PubMed Query</div>
            <p style="font-size:0.88rem; color:#64748b; margin-top:8px;">
                When a user asks a question, EvidenceBot connects to the official NCBI E-Utilities API (<code>esearch</code>) 
                to identify the most relevant peer-reviewed publication IDs.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_s2:
    st.markdown(
        """
        <div class="bio-card" style="height:100%;">
            <div style="font-weight:700; color:#0f2b48; font-size:1.05rem;">2. Abstract Ingestion & Chunking</div>
            <p style="font-size:0.88rem; color:#64748b; margin-top:8px;">
                PubMed XML records are downloaded via <code>efetch</code>, parsed, and split into overlapping sentence passages 
                while preserving medical abbreviations (e.g. <em>et al.</em>, <em>p &lt; 0.05</em>).
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_s3:
    st.markdown(
        """
        <div class="bio-card" style="height:100%;">
            <div style="font-weight:700; color:#0f2b48; font-size:1.05rem;">3. FAISS Vector Ranking</div>
            <p style="font-size:0.88rem; color:#64748b; margin-top:8px;">
                Passages are converted into dense mathematical vectors using <code>all-MiniLM-L6-v2</code>. 
                FAISS performs sub-millisecond Cosine Similarity matching against the question.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("")
col_s4, col_s5, col_s6 = st.columns(3)

with col_s4:
    st.markdown(
        """
        <div class="bio-card" style="height:100%;">
            <div style="font-weight:700; color:#0f2b48; font-size:1.05rem;">4. Abstention Threshold Check</div>
            <p style="font-size:0.88rem; color:#64748b; margin-top:8px;">
                Before any generation occurs, similarity scores are audited against a strict threshold (0.32). 
                If literature is irrelevant or absent, EvidenceBot openly abstains.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_s5:
    st.markdown(
        """
        <div class="bio-card" style="height:100%;">
            <div style="font-weight:700; color:#0f2b48; font-size:1.05rem;">5. Grounded Synthesis</div>
            <p style="font-size:0.88rem; color:#64748b; margin-top:8px;">
                The LLM (Gemini, OpenAI, or the built-in Extractive Synthesizer) receives a strict system instruction 
                to formulate answers using <em>only</em> the retrieved passages.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_s6:
    st.markdown(
        """
        <div class="bio-card" style="height:100%;">
            <div style="font-weight:700; color:#0f2b48; font-size:1.05rem;">6. Citation Verification Audit</div>
            <p style="font-size:0.88rem; color:#64748b; margin-top:8px;">
                The generated answer is regex-parsed to verify that every cited PMID corresponds to an actual 
                retrieved paper, ensuring zero hallucinated citations.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# =====================================================================
# 3. Technologies Used
# =====================================================================
st.markdown("### 💻 Technology Stack")

tech_col1, tech_col2 = st.columns(2)

with tech_col1:
    st.markdown(
        """
        - **Python 3.14**: High-performance backend runtime.
        - **Streamlit**: Responsive, multi-page scientific dashboard framework.
        - **NCBI PubMed E-Utilities**: Direct REST API integration with PubMed (`esearch` and `efetch`).
        - **BeautifulSoup4 & ElementTree**: Robust XML parsing for scientific publications.
        """
    )

with tech_col2:
    st.markdown(
        """
        - **Sentence Transformers (`all-MiniLM-L6-v2`)**: Dense semantic text representations.
        - **FAISS (Facebook AI Similarity Search)**: Sub-millisecond Cosine Similarity index (`IndexFlatIP`).
        - **Google Gemini & OpenAI SDKs**: Grounded multi-paper synthesis with zero-API fallback.
        - **Pytest & Unittest**: Automated regression and citation verification testing.
        """
    )

st.markdown("---")

# =====================================================================
# 4. Limitations & Medical Disclaimer
# =====================================================================
st.markdown("### ⚠️ Known Limitations & Disclaimers")
st.markdown(
    """
    1. **Abstract-Level Evidence:** EvidenceBot currently indexes and parses peer-reviewed **abstracts** from PubMed. While abstracts summarize key endpoints, full clinical protocols, adverse event profiles, and post-hoc analyses may reside in full-text articles.
    2. **Publication Bias:** PubMed indexes published studies, which historically favor positive or statistically significant outcomes.
    3. **Clinical Judgment:** EvidenceBot synthesizes academic literature for exploration and education. It does not possess medical training or patient context.
    """
)

# Standard Disclaimer
render_disclaimer()
