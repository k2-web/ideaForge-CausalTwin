import streamlit as st
import pandas as pd
import numpy as np
import os
import json

# Import backend engines (running silently behind the scenes)
from graph_db import IdeaForgeOntologyGraph
from data_ingestion import IdeaForgeIngestionPipeline
from causal_engine import IdeaForgeCausalEngine
from memory_engine import MemoryEngine
from reasoning_loop import StrategicReasoningEngine
from strategic_advisor import StrategicAdvisorEngine
from agents import IdeaForgeAgentOrchestrator

# 1. Page Configuration
st.set_page_config(
    page_title="ideaForge Digital Twin | Interactive Company Human OS",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. ULTRA-HIGH CONTRAST CSS DESIGN SYSTEM
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Orbitron:wght@700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* High contrast dark background */
    .stApp {
        background-color: #050814;
        color: #FFFFFF;
    }

    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Streamlit default text override for ultra-contrast */
    p, span, label, div {
        color: #FFFFFF !important;
    }
    
    .stMarkdown p {
        color: #F1F5F9 !important;
        font-weight: 500;
    }

    /* Top Brand Header */
    .top-brand-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #0F172A;
        border: 2px solid #FF5500;
        border-radius: 16px;
        padding: 16px 28px;
        margin-bottom: 24px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.8);
    }

    .brand-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.6rem;
        font-weight: 900;
        color: #FFFFFF !important;
        letter-spacing: 0.05em;
    }

    .brand-subtitle {
        font-size: 0.9rem;
        color: #38BDF8 !important;
        font-weight: 600;
    }

    .twin-status-pill {
        background: #064E3B;
        color: #34D399 !important;
        border: 1px solid #34D399;
        padding: 6px 14px;
        border-radius: 20px;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.8rem;
        font-weight: 800;
    }

    /* Hero Human Body Avatar Centerpiece */
    .human-body-container {
        background: #0F172A;
        border: 2px solid #38BDF8;
        border-radius: 24px;
        padding: 28px;
        text-align: center;
        box-shadow: 0 0 40px rgba(56, 189, 248, 0.2);
        margin-bottom: 28px;
    }

    .human-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.5rem;
        font-weight: 900;
        color: #FFFFFF !important;
        letter-spacing: 0.06em;
        margin-bottom: 6px;
    }

    .human-desc {
        color: #F1F5F9 !important;
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 20px;
    }

    /* Organ Selection Cards */
    .organ-card {
        background: #1E293B;
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        transition: all 0.2s ease-in-out;
        height: 100%;
    }

    .organ-card:hover {
        border-color: #FF5500;
        transform: translateY(-4px);
        box-shadow: 0 0 25px rgba(255, 85, 0, 0.4);
    }

    .organ-icon {
        font-size: 2.5rem;
        margin-bottom: 8px;
    }

    .organ-name {
        font-family: 'Orbitron', sans-serif;
        font-size: 1rem;
        font-weight: 900;
        color: #FFFFFF !important;
        margin-bottom: 4px;
    }

    .organ-meta {
        font-size: 0.85rem;
        color: #38BDF8 !important;
        font-weight: 700;
    }

    /* Section Content Box */
    .section-content-box {
        background: #0F172A;
        border: 2px solid #38BDF8;
        border-radius: 20px;
        padding: 28px;
        margin-bottom: 28px;
    }

    .section-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.4rem;
        font-weight: 900;
        color: #FF5500 !important;
        margin-bottom: 16px;
    }

    /* Metric Box */
    .metric-pill-box {
        background: #1E293B;
        border: 2px solid #38BDF8;
        border-radius: 14px;
        padding: 18px;
        text-align: center;
    }

    .metric-pill-label {
        font-size: 0.85rem;
        color: #F1F5F9 !important;
        font-weight: 700;
        text-transform: uppercase;
    }

    .metric-pill-val {
        font-size: 1.8rem;
        font-weight: 900;
        color: #00E5FF !important;
        margin-top: 4px;
    }

    /* Simulation Control Drawer */
    .sim-drawer {
        background: #1E1008;
        border: 2px solid #FF5500;
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 0 40px rgba(255, 85, 0, 0.3);
    }

    /* Table styling for ultra contrast */
    .stTable table {
        color: #FFFFFF !important;
        background-color: #0F172A !important;
    }
    .stTable th {
        color: #00E5FF !important;
        font-weight: 800 !important;
        background-color: #1E293B !important;
    }
    .stTable td {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    /* STREAMLIT BUTTON OVERRIDE (Fixes white boxes) */
    div.stButton > button {
        background: linear-gradient(135deg, #FF5500 0%, #FF2200 100%) !important;
        color: #FFFFFF !important;
        border: 2px solid #FF5500 !important;
        border-radius: 10px !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 0.8rem !important;
        font-weight: 800 !important;
        padding: 8px 12px !important;
        width: 100% !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        box-shadow: 0 4px 15px rgba(255, 85, 0, 0.4) !important;
        margin-top: 8px !important;
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, #00E5FF 0%, #0088FF 100%) !important;
        color: #04060C !important;
        border-color: #00E5FF !important;
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.8) !important;
    }
</style>
""", unsafe_allow_html=True)

# Session State Setup
if "selected_organ" not in st.session_state:
    st.session_state["selected_organ"] = "heart"

# Backend Objects
@st.cache_resource
def get_backend():
    pipeline = IdeaForgeIngestionPipeline()
    graph_db = IdeaForgeOntologyGraph()
    financials_df = pipeline.load_quarterly_financials()
    causal_engine = IdeaForgeCausalEngine(financials_df)
    memory_engine = MemoryEngine()
    reasoning_engine = StrategicReasoningEngine(causal_engine, memory_engine)
    strategic_advisor = StrategicAdvisorEngine(causal_engine, memory_engine)
    orchestrator = IdeaForgeAgentOrchestrator(pipeline, causal_engine)
    return pipeline, graph_db, financials_df, causal_engine, memory_engine, reasoning_engine, strategic_advisor, orchestrator

pipeline, graph_db, financials_df, causal_engine, memory_engine, reasoning_engine, strategic_advisor, orchestrator = get_backend()
baseline_data = financials_df.iloc[-1].to_dict()

# ----------------- TOP BRAND BAR -----------------
st.markdown("""
<div class="top-brand-bar">
    <div>
        <div class="brand-title">ideaForge Digital Human OS</div>
        <div class="brand-subtitle">An Interactive Digital Twin of India's Pioneer Drone Company — Built for Everyone</div>
    </div>
    <div>
        <span class="twin-status-pill">🟢 TWIN ONLINE & SYNCED</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------- DIGITAL HUMAN BODY CENTERPIECE -----------------
st.markdown("""
<div class="human-body-container">
    <div class="human-title">👤 THE DIGITAL BODY OF IDEAFORGE</div>
    <div class="human-desc">Click any body part (organ) below to explore that exact section of the company in high-contrast detail:</div>
</div>
""", unsafe_allow_html=True)

# 6 Body Part Organ Selectors
c_brain, c_heart, c_arms, c_lungs, c_eyes, c_legs = st.columns(6)

with c_brain:
    st.markdown("""
    <div class="organ-card">
        <div class="organ-icon">🧠</div>
        <div class="organ-name">BRAIN</div>
        <div class="organ-meta">AI Strategy & Decisions</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("EXPLORE BRAIN 🧠", key="btn_brain", use_container_width=True):
        st.session_state["selected_organ"] = "brain"

with c_heart:
    st.markdown("""
    <div class="organ-card">
        <div class="organ-icon">🫀</div>
        <div class="organ-name">HEART</div>
        <div class="organ-meta">Financial Statements</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("EXPLORE HEART 🫀", key="btn_heart", use_container_width=True):
        st.session_state["selected_organ"] = "heart"

with c_arms:
    st.markdown("""
    <div class="organ-card">
        <div class="organ-icon">🦾</div>
        <div class="organ-name">ARMS & HANDS</div>
        <div class="organ-meta">Manufacturing Plants</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("EXPLORE ARMS 🦾", key="btn_arms", use_container_width=True):
        st.session_state["selected_organ"] = "arms"

with c_lungs:
    st.markdown("""
    <div class="organ-card">
        <div class="organ-icon">🫁</div>
        <div class="organ-name">LUNGS</div>
        <div class="organ-meta">Suppliers & Imports</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("EXPLORE LUNGS 🫁", key="btn_lungs", use_container_width=True):
        st.session_state["selected_organ"] = "lungs"

with c_eyes:
    st.markdown("""
    <div class="organ-card">
        <div class="organ-icon">👁️</div>
        <div class="organ-name">EYES & EARS</div>
        <div class="organ-meta">Customers & Tenders</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("EXPLORE EYES 👁️", key="btn_eyes", use_container_width=True):
        st.session_state["selected_organ"] = "eyes"

with c_legs:
    st.markdown("""
    <div class="organ-card">
        <div class="organ-icon">🦵</div>
        <div class="organ-name">LEGS</div>
        <div class="organ-meta">Drone Fleet Deployment</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("EXPLORE LEGS 🦵", key="btn_legs", use_container_width=True):
        st.session_state["selected_organ"] = "legs"


st.write("---")

# ----------------- ORGAN IN-DEPTH EXPLORER SECTIONS -----------------
organ = st.session_state["selected_organ"]

# ==============================================================================
# ORGAN 1: HEART (FINANCIAL STATEMENTS & CASH FLOW)
# ==============================================================================
if organ == "heart":
    st.markdown("""
    <div class="section-content-box">
        <div class="section-header">🫀 THE HEART OF IDEAFORGE — Financial Statements & Money Flow</div>
        <p style="color:#FFFFFF; font-size:1rem; font-weight:600;">
            Just like a human heart pumps blood throughout the body, ideaForge's financial engine pumps money through its operations. 
            Here is a high-contrast breakdown of revenue, profit, cash, and balance sheet health.
        </p>
    </div>
    """, unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown("""
        <div class="metric-pill-box">
            <div class="metric-pill-label">Annual Revenue (Money Earned)</div>
            <div class="metric-pill-val">₹202 Cr</div>
            <div style="font-size:0.85rem; color:#34D399; font-weight:700; margin-top:4px;">+18.5% YoY Growth</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown("""
        <div class="metric-pill-box">
            <div class="metric-pill-label">Operating Profit Margin</div>
            <div class="metric-pill-val">23.9%</div>
            <div style="font-size:0.85rem; color:#34D399; font-weight:700; margin-top:4px;">₹48.2 Cr EBITDA</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown("""
        <div class="metric-pill-box">
            <div class="metric-pill-label">Cash Collection Speed</div>
            <div class="metric-pill-val">75 Days</div>
            <div style="font-size:0.85rem; color:#F43F5E; font-weight:700; margin-top:4px;">MoD Invoice Lag</div>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        st.markdown("""
        <div class="metric-pill-box">
            <div class="metric-pill-label">Working Capital Tank</div>
            <div class="metric-pill-val">₹41.5 Cr</div>
            <div style="font-size:0.85rem; color:#38BDF8; font-weight:700; margin-top:4px;">Cash Tied in Stock</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.markdown("#### 📊 Income Statement & Revenue Stream Breakdown")
    f_col1, f_col2 = st.columns(2)

    with f_col1:
        st.markdown("**Where the Money Comes From (Revenue Mix):**")
        rev_data = pd.DataFrame({
            "Source": ["Defense Contracts (Army & BSF)", "Government Civil Mapping", "FLYGHT Software Subscriptions", "Spare Parts & Services"],
            "Revenue (₹ Cr)": ["131.3", "40.4", "20.2", "10.1"],
            "Share (%)": ["65%", "20%", "10%", "5%"]
        })
        st.table(rev_data)

    with f_col2:
        st.markdown("**Where the Money Goes (Expense Structure):**")
        exp_data = pd.DataFrame({
            "Category": ["Raw Components & Camera BOMs", "R&D & Engineering Salaries", "Factory Operations & Logistics", "Net Profit After Tax"],
            "Amount (₹ Cr)": ["90.9", "40.4", "22.2", "48.5"],
            "Share (%)": ["45%", "20%", "11%", "24%"]
        })
        st.table(exp_data)

# ==============================================================================
# ORGAN 2: ARMS & HANDS (MANUFACTURING PLANTS & PRODUCTION)
# ==============================================================================
elif organ == "arms":
    st.markdown("""
    <div class="section-content-box">
        <div class="section-header">🦾 ARMS & HANDS — Manufacturing Facilities & Drone Assembly</div>
        <p style="color:#FFFFFF; font-size:1rem; font-weight:600;">
            These are the physical factories and hands that build ideaForge's drones. From raw carbon fiber sheets to high-altitude flight testing, explore how drones are crafted.
        </p>
    </div>
    """, unsafe_allow_html=True)

    p1, p2, p3 = st.columns(3)

    with p1:
        st.markdown("""
        <div style="background:#1E293B; border:2px solid #38BDF8; border-radius:14px; padding:20px;">
            <div style="font-size:1.2rem; font-weight:800; color:#00E5FF;">🏭 Navi Mumbai Main Plant</div>
            <div style="font-size:0.9rem; color:#FFFFFF; margin-top:4px;">Primary Manufacturing Facility</div>
            <hr style="border-color:rgba(255,255,255,0.2);">
            <div style="font-size:0.9rem; color:#FFFFFF;">• Monthly Capacity: <b style="color:#00E5FF;">350 Drones</b></div>
            <div style="font-size:0.9rem; color:#FFFFFF;">• Floor Area: <b style="color:#00E5FF;">45,000 sq ft</b></div>
            <div style="font-size:0.9rem; color:#34D399;">• Utilization Rate: <b>78% Active</b></div>
        </div>
        """, unsafe_allow_html=True)

    with p2:
        st.markdown("""
        <div style="background:#1E293B; border:2px solid #38BDF8; border-radius:14px; padding:20px;">
            <div style="font-size:1.2rem; font-weight:800; color:#00E5FF;">🔬 High-Altitude Testing Bay</div>
            <div style="font-size:0.9rem; color:#FFFFFF; margin-top:4px;">Ladakh & Leh Test Center</div>
            <hr style="border-color:rgba(255,255,255,0.2);">
            <div style="font-size:0.9rem; color:#FFFFFF;">• Test Altitude: <b style="color:#00E5FF;">Up to 20,000 ft</b></div>
            <div style="font-size:0.9rem; color:#FFFFFF;">• Temp Range: <b style="color:#00E5FF;">-20°C to +50°C</b></div>
            <div style="font-size:0.9rem; color:#34D399;">• Quality Pass Rate: <b>99.2%</b></div>
        </div>
        """, unsafe_allow_html=True)

    with p3:
        st.markdown("""
        <div style="background:#1E293B; border:2px solid #38BDF8; border-radius:14px; padding:20px;">
            <div style="font-size:1.2rem; font-weight:800; color:#00E5FF;">🛸 Product Lineup Built</div>
            <div style="font-size:0.9rem; color:#FFFFFF; margin-top:4px;">Flagship Drone Models</div>
            <hr style="border-color:rgba(255,255,255,0.2);">
            <div style="font-size:0.9rem; color:#FFFFFF;">• <b style="color:#FF5500;">SWITCH UAV</b> (Border Patrol)</div>
            <div style="font-size:0.9rem; color:#FFFFFF;">• <b style="color:#FF5500;">NETRA V4</b> (Police Patrol)</div>
            <div style="font-size:0.9rem; color:#FFFFFF;">• <b style="color:#FF5500;">Q6 UAV</b> (Land Mapping)</div>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# ORGAN 3: LUNGS (SUPPLIERS & IMPORT FEEDS)
# ==============================================================================
elif organ == "lungs":
    st.markdown("""
    <div class="section-content-box">
        <div class="section-header">🫁 LUNGS — Suppliers & Global Component Imports</div>
        <p style="color:#FFFFFF; font-size:1rem; font-weight:600;">
            Just like lungs inhale oxygen from the environment, ideaForge inhales critical high-tech components from specialized global suppliers to build its drones.
        </p>
    </div>
    """, unsafe_allow_html=True)

    s1, s2, s3, s4 = st.columns(4)

    with s1:
        st.markdown("""
        <div style="background:#1E293B; border:2px solid #FF5500; border-radius:14px; padding:18px;">
            <div style="font-size:1.6rem;">🇮🇱</div>
            <div style="font-weight:800; color:#FFFFFF; font-size:1rem; margin-top:6px;">Elbit Systems (Israel)</div>
            <div style="font-size:0.85rem; color:#00E5FF; font-weight:700;">EO/IR Optical Cameras</div>
            <div style="font-size:0.85rem; color:#FFFFFF; margin-top:6px;">Cost: ₹8.0 Lakhs / unit</div>
        </div>
        """, unsafe_allow_html=True)

    with s2:
        st.markdown("""
        <div style="background:#1E293B; border:2px solid #FF5500; border-radius:14px; padding:18px;">
            <div style="font-size:1.6rem;">🇹🇼</div>
            <div style="font-weight:800; color:#FFFFFF; font-size:1rem; margin-top:6px;">Taiwan Semi Corp</div>
            <div style="font-size:0.85rem; color:#00E5FF; font-weight:700;">Autopilot Microcontroller</div>
            <div style="font-size:0.85rem; color:#FFFFFF; margin-top:6px;">Cost: ₹2.0 Lakhs / unit</div>
        </div>
        """, unsafe_allow_html=True)

    with s3:
        st.markdown("""
        <div style="background:#1E293B; border:2px solid #FF5500; border-radius:14px; padding:18px;">
            <div style="font-size:1.6rem;">🇯🇵</div>
            <div style="font-weight:800; color:#FFFFFF; font-size:1rem; margin-top:6px;">Japan Carbon Fiber</div>
            <div style="font-size:0.85rem; color:#00E5FF; font-weight:700;">Ultra-Light Body Frame</div>
            <div style="font-size:0.85rem; color:#FFFFFF; margin-top:6px;">Cost: ₹1.5 Lakhs / unit</div>
        </div>
        """, unsafe_allow_html=True)

    with s4:
        st.markdown("""
        <div style="background:#1E293B; border:2px solid #FF5500; border-radius:14px; padding:18px;">
            <div style="font-size:1.6rem;">🇮🇳</div>
            <div style="font-weight:800; color:#FFFFFF; font-size:1rem; margin-top:6px;">Local Indian Suppliers</div>
            <div style="font-size:0.85rem; color:#00E5FF; font-weight:700;">LiPo Batteries & Motors</div>
            <div style="font-size:0.85rem; color:#FFFFFF; margin-top:6px;">Cost: ₹0.8 Lakhs / unit</div>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# ORGAN 4: EYES & EARS (CUSTOMERS & DEFENSE TENDERS)
# ==============================================================================
elif organ == "eyes":
    st.markdown("""
    <div class="section-content-box">
        <div class="section-header">👁️ EYES & EARS — Key Customers & Government Tenders</div>
        <p style="color:#FFFFFF; font-size:1rem; font-weight:600;">
            ideaForge keeps its eyes and ears on defense security tenders and government mapping contracts across India.
        </p>
    </div>
    """, unsafe_allow_html=True)

    e1, e2, e3 = st.columns(3)

    with e1:
        st.markdown("""
        <div style="background:#1E293B; border:2px solid #FF5500; border-radius:14px; padding:20px;">
            <div style="font-size:1.2rem; font-weight:800; color:#FF5500;">🪖 Indian Army (Ministry of Defence)</div>
            <div style="font-size:0.9rem; color:#FFFFFF; margin-top:4px;">Primary Defense Client</div>
            <hr style="border-color:rgba(255,255,255,0.2);">
            <div style="font-size:0.9rem; color:#FFFFFF;">• Revenue Share: <b style="color:#00E5FF;">65%</b></div>
            <div style="font-size:0.9rem; color:#FFFFFF;">• Primary Deployment: <b>High-Altitude Border Surveillance</b></div>
            <div style="font-size:0.9rem; color:#34D399;">• Fast-Track Procurement Active</div>
        </div>
        """, unsafe_allow_html=True)

    with e2:
        st.markdown("""
        <div style="background:#1E293B; border:2px solid #FF5500; border-radius:14px; padding:20px;">
            <div style="font-size:1.2rem; font-weight:800; color:#FF5500;">🛡️ Ministry of Home Affairs (BSF, CRPF)</div>
            <div style="font-size:0.9rem; color:#FFFFFF; margin-top:4px;">Paramilitary & Law Enforcement</div>
            <hr style="border-color:rgba(255,255,255,0.2);">
            <div style="font-size:0.9rem; color:#FFFFFF;">• Revenue Share: <b style="color:#00E5FF;">15%</b></div>
            <div style="font-size:0.9rem; color:#FFFFFF;">• Primary Deployment: <b>Crowd Monitoring & Rescue</b></div>
            <div style="font-size:0.9rem; color:#34D399;">• Multi-Year Service Tenders</div>
        </div>
        """, unsafe_allow_html=True)

    with e3:
        st.markdown("""
        <div style="background:#1E293B; border:2px solid #FF5500; border-radius:14px; padding:20px;">
            <div style="font-size:1.2rem; font-weight:800; color:#FF5500;">🗺️ Survey of India</div>
            <div style="font-size:0.9rem; color:#FFFFFF; margin-top:4px;">Civil Mapping Tenders</div>
            <hr style="border-color:rgba(255,255,255,0.2);">
            <div style="font-size:0.9rem; color:#FFFFFF;">• Revenue Share: <b style="color:#00E5FF;">20%</b></div>
            <div style="font-size:0.9rem; color:#FFFFFF;">• Primary Deployment: <b>SVAMITVA Rural Land Mapping</b></div>
            <div style="font-size:0.9rem; color:#34D399;">• High-Precision Q6 Drone Fleet</div>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# ORGAN 5: LEGS (FLEET DEPLOYMENT & FIELD SERVICES)
# ==============================================================================
elif organ == "legs":
    st.markdown("""
    <div class="section-content-box">
        <div class="section-header">🦵 LEGS — Drone Fleet Deployment & Field Mobility</div>
        <p style="color:#FFFFFF; font-size:1rem; font-weight:600;">
            ideaForge's drones have flown over 950,000 flight missions across difficult terrains, extreme altitudes, and urban environments.
        </p>
    </div>
    """, unsafe_allow_html=True)

    l1, l2, l3 = st.columns(3)
    with l1:
        st.metric("Total Flight Missions Completed", "950,000+", "Across Borders & Cities")
    with l2:
        st.metric("Patents Granted & Filed", "108+", "Proprietary UAS Tech")
    with l3:
        st.metric("FLYGHT SaaS Active Drones", "1,250 Unit Syncs", "Live Real-Time Video Stream")

# ==============================================================================
# ORGAN 6: BRAIN (AI STRATEGY & DECISION SIMULATION)
# ==============================================================================
elif organ == "brain":
    st.markdown("""
    <div class="section-content-box">
        <div class="section-header">🧠 THE BRAIN — AI Leadership & Strategy Simulator</div>
        <p style="color:#FFFFFF; font-size:1rem; font-weight:600;">
            The brain processes complex information, calculates risks, and makes decisions for the company. 
            Use the simulation sliders below to see how executive decisions affect ideaForge in real time.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ----------------- REAL-WORLD SIMULATOR DRAWER FOR EVERY ORGAN -----------------
st.write("---")
st.markdown("""
<div class="sim-drawer">
    <div style="font-family:'Orbitron', sans-serif; font-size:1.3rem; font-weight:900; color:#FF5500; margin-bottom:4px;">
        🎛️ REAL-WORLD SIMULATION STUDIO — Test Factors Affecting the Company
    </div>
    <div style="font-size:0.9rem; color:#FFFFFF; font-weight:600; margin-bottom:16px;">
        Drag the sliders below to simulate how government payment speeds, component import tariffs, and software adoption change ideaForge's profits and cash flow:
    </div>
</div>
""", unsafe_allow_html=True)

s_col1, s_col2 = st.columns([1, 1.2])

with s_col1:
    st.markdown("##### 🎚️ Real-World Factors")

    mod_lag = st.slider(
        "⏳ Government Invoice Clearance Time (Days)",
        min_value=15, max_value=180, value=int(baseline_data["MoD_Disbursement_Lag"]), step=5,
        help="How fast the Ministry of Defence clears invoices for completed drone deliveries."
    )

    import_price_shock = st.slider(
        "📷 Imported Camera / Tariff Price Hike (%)",
        min_value=0, max_value=50, value=0, step=5,
        help="Price increase for optical cameras imported from Israel or microchips from Taiwan."
    )

    saas_attach_rate = st.slider(
        "💻 Software Subscription Adoption (%)",
        min_value=0, max_value=100, value=int(baseline_data["SaaS_Attach_Rate"] * 100), step=5,
        help="Percentage of clients paying for annual FLYGHT software subscriptions."
    )

    scenario_config = {
        "mod_lag_days": mod_lag,
        "import_tariff_shock_pct": import_price_shock,
        "saas_attach_rate_pct": saas_attach_rate,
        "indigenous_mix": 0.60
    }

    agent_state = orchestrator.run_workflow(scenario_config)
    sim_res = agent_state.simulated_results

with s_col2:
    st.markdown("##### 📈 Simulated Company Outcome")

    quarters = ["Q1 FY25", "Q2 FY25", "Q3 FY25", "Q4 FY25", "Q1 FY26", "Q2 FY26", "Q3 FY26", "Q4 FY26 (Simulated)"]
    baseline_trend = [12.8, 8.4, 18.2, 38.6, 15.1, 11.5, 22.1, baseline_data["EBITDA_Margin"]]
    simulated_trend = [12.8, 8.4, 18.2, 38.6, 15.1, 11.5, 22.1, sim_res["EBITDA_Margin"]]

    chart_df = pd.DataFrame({
        "Normal Profit Margin (%)": baseline_trend,
        "Simulated Profit Margin (%)": simulated_trend
    }, index=quarters)

    st.line_chart(chart_df, color=["#00E5FF", "#FF5500"])

    o1, o2 = st.columns(2)
    with o1:
        st.metric("Simulated Profit Margin", f"{sim_res['EBITDA_Margin']:.1f}%", f"{sim_res['EBITDA_Margin'] - baseline_data['EBITDA_Margin']:.1f}% change")
    with o2:
        st.metric("Cash Collection Speed", f"{sim_res['Working_Capital_Days']:.0f} Days", f"{sim_res['Working_Capital_Days'] - baseline_data['Working_Capital_Days']:.0f}d change")

st.markdown("<br><center style='color:#00E5FF; font-family:Orbitron, sans-serif; font-size:0.95rem; font-weight:800;'>ideaForge Digital Human OS — An Autonomous Company Digital Twin Built for Everyone</center>", unsafe_allow_html=True)
