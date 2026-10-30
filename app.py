"""
EvidenceBot - Biomedical Literature Intelligence Platform
=========================================================
Production-grade scientific discovery and evidence synthesis engine
powered by NCBI PubMed E-Utilities, SentenceTransformers, and FAISS.
"""

import streamlit as st
from utils.ui_components import apply_theme, render_sidebar, render_disclaimer

# Configure page settings
st.set_page_config(
    page_title="EvidenceBot – Biomedical Literature Intelligence",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply unified design theme & sidebar
apply_theme()
render_sidebar(current_page="Home")

# =====================================================================
# 1. Enterprise Hero Header
# =====================================================================
st.markdown(
    """
    <div class="top-banner">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:16px;">
            <div>
                <h1>🧬 EvidenceBot</h1>
                <p>Enterprise Biomedical Literature Intelligence &bull; Synthesizes peer-reviewed consensus and enforces empirical abstention.</p>
            </div>
            <div style="background:rgba(255,255,255,0.12); border:1px solid rgba(255,255,255,0.2); border-radius:10px; padding:10px 16px; font-size:0.85rem; color:#f0f9ff;">
                <span style="font-weight:700;">NCBI Entrez Integration</span><br>
                <span>Live PubMed Retrieval Engine</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Metric Highlight Bar
st.markdown(
    """
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:14px; margin-bottom:28px;">
        <div class="bio-card" style="margin:0; padding:16px 20px;">
            <div style="font-size:0.78rem; text-transform:uppercase; color:#64748b; font-weight:700; letter-spacing:0.04em;">Database Ingestion</div>
            <div style="font-size:1.35rem; font-weight:800; color:#0f172a; margin-top:2px;">36M+ Articles</div>
            <div style="font-size:0.82rem; color:#0284c7;">Direct NCBI PubMed E-Utilities</div>
        </div>
        <div class="bio-card" style="margin:0; padding:16px 20px;">
            <div style="font-size:0.78rem; text-transform:uppercase; color:#64748b; font-weight:700; letter-spacing:0.04em;">Vector Search</div>
            <div style="font-size:1.35rem; font-weight:800; color:#0f172a; margin-top:2px;">FAISS Dense Index</div>
            <div style="font-size:0.82rem; color:#0284c7;">Sub-millisecond Cosine Matching</div>
        </div>
        <div class="bio-card" style="margin:0; padding:16px 20px;">
            <div style="font-size:0.78rem; text-transform:uppercase; color:#64748b; font-weight:700; letter-spacing:0.04em;">Citation Fidelity</div>
            <div style="font-size:1.35rem; font-weight:800; color:#0f172a; margin-top:2px;">100% Deterministic</div>
            <div style="font-size:0.82rem; color:#0284c7;">Zero Hallucinated PMIDs</div>
        </div>
        <div class="bio-card" style="margin:0; padding:16px 20px;">
            <div style="font-size:0.78rem; text-transform:uppercase; color:#64748b; font-weight:700; letter-spacing:0.04em;">Safety Protocol</div>
            <div style="font-size:1.35rem; font-weight:800; color:#0f172a; margin-top:2px;">Empirical Abstention</div>
            <div style="font-size:0.82rem; color:#0284c7;">Withholds Unsubstantiated Claims</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================================================
# 2. Main Question Input Area
# =====================================================================
st.markdown("### 🔍 Query Scientific Literature")
st.caption("Submit a clinical, pharmacological, or biochemical inquiry to retrieve peer-reviewed studies and synthesize findings:")

sample_placeholder = "e.g., Does zinc supplementation reduce the duration or severity of common cold symptoms?"
home_query = st.text_area(
    "Clinical or Scientific Inquiry:",
    height=95,
    placeholder=sample_placeholder,
    label_visibility="collapsed",
    help="Type any clinical inquiry or research topic to search PubMed."
)

col_btn, col_hint = st.columns([1, 4])
with col_btn:
    ask_clicked = st.button("🚀 Synthesize Evidence", type="primary", use_container_width=True)

with col_hint:
    st.markdown(
        "<div style='font-size:0.86rem; color:#64748b; padding-top:10px;'>"
        "⚡ Connects in real time to NCBI ESearch & EFetch &bull; Guarantees zero synthetic citations."
        "</div>",
        unsafe_allow_html=True
    )

if ask_clicked:
    clean_input = home_query.strip()
    if clean_input:
        st.session_state["query_to_run"] = clean_input
        st.switch_page("pages/1_Ask_EvidenceBot.py")
    else:
        st.warning("⚠️ Please enter a clinical or biomedical research inquiry first.")

st.markdown("---")

# =====================================================================
# 3. Curated Biomedical Queries
# =====================================================================
st.markdown("### 🧪 Curated Literature Inquiries")
st.caption("Select a canonical research scenario to execute immediate live retrieval and synthesis:")

col_q1, col_q2 = st.columns(2)

with col_q1:
    if st.button("📌 Zinc Lozenges & Cold Duration (Established Clinical Trial Consensus)", use_container_width=True):
        st.session_state["query_to_run"] = "Does zinc supplementation reduce the duration or severity of common cold symptoms?"
        st.switch_page("pages/1_Ask_EvidenceBot.py")

    if st.button("📌 Metformin Cellular Mechanism in T2D (Molecular Pathway Investigation)", use_container_width=True):
        st.session_state["query_to_run"] = "What is the primary cellular mechanism of action of metformin in type 2 diabetes?"
        st.switch_page("pages/1_Ask_EvidenceBot.py")

with col_q2:
    if st.button("📌 Dietary Omega-3 & Cardiovascular Risk (Conflicting Multi-Trial Outcomes)", use_container_width=True):
        st.session_state["query_to_run"] = "Does dietary omega-3 fatty acid supplementation prevent major adverse cardiovascular events in healthy individuals?"
        st.switch_page("pages/1_Ask_EvidenceBot.py")

    if st.button("📌 Spirulina Curing Multiple Sclerosis (Scientific Abstention Guard)", use_container_width=True):
        st.session_state["query_to_run"] = "Can spirulina microalgae supplementation cure multiple sclerosis in human patients?"
        st.switch_page("pages/1_Ask_EvidenceBot.py")

st.markdown("---")

# =====================================================================
# 4. Enterprise Architecture Cards
# =====================================================================
st.markdown("### 🛡️ Enterprise Core Capabilities")

fc1, fc2, fc3, fc4 = st.columns(4)

with fc1:
    st.markdown(
        """
        <div class="feature-card">
            <span class="feature-icon">📄</span>
            <div class="feature-title">Live PubMed Ingestion</div>
            <div class="feature-desc">
                Direct integration with NCBI E-Utilities API (<code>esearch</code> and <code>efetch</code>) to pull authentic, peer-reviewed biomedical abstracts.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with fc2:
    st.markdown(
        """
        <div class="feature-card">
            <span class="feature-icon">⚡</span>
            <div class="feature-title">Dense FAISS Retrieval</div>
            <div class="feature-desc">
                Sub-millisecond semantic search powered by SentenceTransformers and FAISS Cosine Similarity (<code>IndexFlatIP</code>).
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with fc3:
    st.markdown(
        """
        <div class="feature-card">
            <span class="feature-icon">🛡️</span>
            <div class="feature-title">Zero Citation Hallucination</div>
            <div class="feature-desc">
                Every generated assertion is audited against real PMIDs. Fabricated citations are flagged and blocked automatically.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with fc4:
    st.markdown(
        """
        <div class="feature-card">
            <span class="feature-icon">⚖️</span>
            <div class="feature-title">Scientific Abstention</div>
            <div class="feature-desc">
                When literature is missing or semantic similarity is insufficient, EvidenceBot openly admits it cannot provide a confident answer.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Scientific Disclaimer
render_disclaimer()
