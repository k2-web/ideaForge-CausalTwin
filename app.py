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

# 2. Ultra-Futuristic Cyberpunk CSS Design System matching Digital Human Body Concept
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Orbitron:wght@700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background-color: #04060C;
        background-image: 
            radial-gradient(at 50% 10%, rgba(255, 69, 0, 0.15) 0px, transparent 60%),
            radial-gradient(at 10% 90%, rgba(0, 191, 255, 0.12) 0px, transparent 50%),
            radial-gradient(at 90% 90%, rgba(139, 92, 246, 0.12) 0px, transparent 50%);
        color: #F8FAFC;
    }

    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Top Brand Header */
    .top-brand-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 69, 0, 0.3);
        border-radius: 16px;
        padding: 16px 28px;
        margin-bottom: 24px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.6);
    }

    .brand-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.5rem;
        font-weight: 900;
        color: #FFFFFF;
        letter-spacing: 0.05em;
    }

    .brand-subtitle {
        font-size: 0.85rem;
        color: #94A3B8;
    }

    .twin-status-pill {
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 6px 14px;
        border-radius: 20px;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.75rem;
        font-weight: 700;
    }

    /* Hero Human Body Avatar Centerpiece */
    .human-body-container {
        background: radial-gradient(circle, rgba(15, 23, 42, 0.95) 0%, rgba(4, 6, 12, 0.98) 100%);
        border: 2px solid rgba(255, 69, 0, 0.35);
        border-radius: 24px;
        padding: 28px;
        text-align: center;
        box-shadow: 0 0 50px rgba(255, 69, 0, 0.15);
        margin-bottom: 28px;
    }

    .human-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.4rem;
        font-weight: 900;
        color: #FFFFFF;
        letter-spacing: 0.06em;
        margin-bottom: 6px;
    }

    .human-desc {
        color: #94A3B8;
        font-size: 0.9rem;
        margin-bottom: 24px;
    }

    /* Organ Selection Cards */
    .organ-card {
        background: #0F172A;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        transition: all 0.2s ease-in-out;
        cursor: pointer;
        height: 100%;
    }

    .organ-card:hover {
        border-color: #FF4500;
        transform: translateY(-4px);
        box-shadow: 0 0 25px rgba(255, 69, 0, 0.25);
    }

    .organ-card.active {
        border-color: #00BFFF;
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        box-shadow: 0 0 30px rgba(0, 191, 255, 0.3);
    }

    .organ-icon {
        font-size: 2.5rem;
        margin-bottom: 8px;
    }

    .organ-name {
        font-family: 'Orbitron', sans-serif;
        font-size: 0.95rem;
        font-weight: 800;
        color: #F8FAFC;
        margin-bottom: 4px;
    }

    .organ-meta {
        font-size: 0.8rem;
        color: #38BDF8;
        font-weight: 600;
    }

    /* Section Content Box */
    .section-content-box {
        background: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 69, 0, 0.3);
        border-radius: 20px;
        padding: 28px;
        margin-bottom: 28px;
    }

    .section-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.3rem;
        font-weight: 800;
        color: #FF4500;
        margin-bottom: 16px;
    }

    /* Metric Box */
    .metric-pill-box {
        background: #1E293B;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
    }

    .metric-pill-label {
        font-size: 0.8rem;
        color: #94A3B8;
        font-weight: 600;
        text-transform: uppercase;
    }

    .metric-pill-val {
        font-size: 1.6rem;
        font-weight: 800;
        color: #38BDF8;
        margin-top: 4px;
    }

    /* Simulation Control Drawer */
    .sim-drawer {
        background: linear-gradient(135deg, #1C0A00 0%, #0F0500 100%);
        border: 2px solid #FF4500;
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 0 40px rgba(255, 69, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Session State Setup
if "selected_organ" not in st.session_state:
    st.session_state["selected_organ"] = "heart"  # Default: Heart (Financial Statements)

# Backend Objects (Calculations run silently behind the scenes)
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
    <div class="human-desc">Click any body part (organ) below to explore that exact section of the company in depth:</div>
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
    if st.button("Explore Brain", key="btn_brain", use_container_width=True):
        st.session_state["selected_organ"] = "brain"

with c_heart:
    st.markdown("""
    <div class="organ-card">
        <div class="organ-icon">🫀</div>
        <div class="organ-name">HEART</div>
        <div class="organ-meta">Financial Statements</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Explore Heart", key="btn_heart", use_container_width=True):
        st.session_state["selected_organ"] = "heart"

with c_arms:
    st.markdown("""
    <div class="organ-card">
        <div class="organ-icon">🦾</div>
        <div class="organ-name">ARMS & HANDS</div>
        <div class="organ-meta">Manufacturing Plants</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Explore Arms", key="btn_arms", use_container_width=True):
        st.session_state["selected_organ"] = "arms"

with c_lungs:
    st.markdown("""
    <div class="organ-card">
        <div class="organ-icon">🫁</div>
        <div class="organ-name">LUNGS</div>
        <div class="organ-meta">Suppliers & Imports</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Explore Lungs", key="btn_lungs", use_container_width=True):
        st.session_state["selected_organ"] = "lungs"

with c_eyes:
    st.markdown("""
    <div class="organ-card">
        <div class="organ-icon">👁️</div>
        <div class="organ-name">EYES & EARS</div>
        <div class="organ-meta">Customers & Tenders</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Explore Eyes", key="btn_eyes", use_container_width=True):
        st.session_state["selected_organ"] = "eyes"

with c_legs:
    st.markdown("""
    <div class="organ-card">
        <div class="organ-icon">🦵</div>
        <div class="organ-name">LEGS</div>
        <div class="organ-meta">Drone Fleet Deployment</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Explore Legs", key="btn_legs", use_container_width=True):
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
        <p style="color:#CBD5E1;">
            Just like a human heart pumps blood throughout the body, ideaForge's financial engine pumps money through its operations. 
            Here is a simple breakdown of the company's revenue, profit, cash, and financial health.
        </p>
    </div>
    """, unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown("""
        <div class="metric-pill-box">
            <div class="metric-pill-label">Annual Revenue (Money Earned)</div>
            <div class="metric-pill-val">₹202 Cr</div>
            <div style="font-size:0.8rem; color:#34D399; margin-top:4px;">+18.5% YoY Growth</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown("""
        <div class="metric-pill-box">
            <div class="metric-pill-label">Operating Profit Margin</div>
            <div class="metric-pill-val">23.9%</div>
            <div style="font-size:0.8rem; color:#34D399; margin-top:4px;">₹48.2 Cr EBITDA</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown("""
        <div class="metric-pill-box">
            <div class="metric-pill-label">Cash Collection Speed</div>
            <div class="metric-pill-val">75 Days</div>
            <div style="font-size:0.8rem; color:#F43F5E; margin-top:4px;">MoD Invoice Lag</div>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        st.markdown("""
        <div class="metric-pill-box">
            <div class="metric-pill-label">Working Capital Tank</div>
            <div class="metric-pill-val">₹41.5 Cr</div>
            <div style="font-size:0.8rem; color:#60A5FA; margin-top:4px;">Cash Tied in Stock</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.markdown("#### 📊 Income Statement & Revenue Stream Breakdown")
    f_col1, f_col2 = st.columns(2)

    with f_col1:
        st.markdown("**Where the Money Comes From (Revenue Mix):**")
        rev_data = pd.DataFrame({
            "Source": ["Defense Contracts (Army & BSF)", "Government Civil Mapping", "FLYGHT Software Subscriptions", "Spare Parts & Services"],
            "Revenue (₹ Cr)": [131.3, 40.4, 20.2, 10.1],
            "Share (%)": ["65%", "20%", "10%", "5%"]
        })
        st.table(rev_data)

    with f_col2:
        st.markdown("**Where the Money Goes (Expense Structure):**")
        exp_data = pd.DataFrame({
            "Category": ["Raw Components & Camera BOMs", "R&D & Engineering Salaries", "Factory Operations & Logistics", "Net Profit After Tax"],
            "Amount (₹ Cr)": [90.9, 40.4, 22.2, 48.5],
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
        <p style="color:#CBD5E1;">
            These are the physical factories and hands that build ideaForge's drones. From raw carbon fiber sheets to high-altitude flight testing, explore how drones are crafted.
        </p>
    </div>
    """, unsafe_allow_html=True)

    p1, p2, p3 = st.columns(3)

    with p1:
        st.markdown("""
        <div style="background:#0F172A; border:1px solid rgba(255,255,255,0.1); border-radius:14px; padding:20px;">
            <div style="font-size:1.1rem; font-weight:800; color:#38BDF8;">🏭 Navi Mumbai Main Plant</div>
            <div style="font-size:0.85rem; color:#94A3B8; margin-top:4px;">Primary Manufacturing Facility</div>
            <hr style="border-color:rgba(255,255,255,0.1);">
            <div style="font-size:0.85rem; color:#E2E8F0;">• Monthly Capacity: <b>350 Drones</b></div>
            <div style="font-size:0.85rem; color:#E2E8F0;">• Floor Area: <b>45,000 sq ft</b></div>
            <div style="font-size:0.85rem; color:#34D399;">• Utilization Rate: <b>78% Active</b></div>
        </div>
        """, unsafe_allow_html=True)

    with p2:
        st.markdown("""
        <div style="background:#0F172A; border:1px solid rgba(255,255,255,0.1); border-radius:14px; padding:20px;">
            <div style="font-size:1.1rem; font-weight:800; color:#38BDF8;">🔬 High-Altitude Testing Bay</div>
            <div style="font-size:0.85rem; color:#94A3B8; margin-top:4px;">Ladakh & Leh Test Center</div>
            <hr style="border-color:rgba(255,255,255,0.1);">
            <div style="font-size:0.85rem; color:#E2E8F0;">• Test Altitude: <b>Up to 20,000 ft</b></div>
            <div style="font-size:0.85rem; color:#E2E8F0;">• Temp Range: <b>-20°C to +50°C</b></div>
            <div style="font-size:0.85rem; color:#34D399;">• Quality Pass Rate: <b>99.2%</b></div>
        </div>
        """, unsafe_allow_html=True)

    with p3:
        st.markdown("""
        <div style="background:#0F172A; border:1px solid rgba(255,255,255,0.1); border-radius:14px; padding:20px;">
            <div style="font-size:1.1rem; font-weight:800; color:#38BDF8;">🛸 Product Lineup Built</div>
            <div style="font-size:0.85rem; color:#94A3B8; margin-top:4px;">Flagship Drone Models</div>
            <hr style="border-color:rgba(255,255,255,0.1);">
            <div style="font-size:0.85rem; color:#E2E8F0;">• <b>SWITCH UAV</b> (Border Patrol)</div>
            <div style="font-size:0.85rem; color:#E2E8F0;">• <b>NETRA V4</b> (Police Patrol)</div>
            <div style="font-size:0.85rem; color:#E2E8F0;">• <b>Q6 UAV</b> (Land Mapping)</div>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# ORGAN 3: LUNGS (SUPPLIERS & IMPORT FEEDS)
# ==============================================================================
elif organ == "lungs":
    st.markdown("""
    <div class="section-content-box">
        <div class="section-header">🫁 LUNGS — Suppliers & Global Component Imports</div>
        <p style="color:#CBD5E1;">
            Just like lungs inhale oxygen from the environment, ideaForge inhales critical high-tech components from specialized global suppliers to build its drones.
        </p>
    </div>
    """, unsafe_allow_html=True)

    s1, s2, s3, s4 = st.columns(4)

    with s1:
        st.markdown("""
        <div style="background:#0F172A; border:1px solid rgba(255,255,255,0.1); border-radius:14px; padding:18px;">
            <div style="font-size:1.5rem;">🇮🇱</div>
            <div style="font-weight:700; color:#F8FAFC; margin-top:6px;">Elbit Systems (Israel)</div>
            <div style="font-size:0.8rem; color:#38BDF8;">EO/IR Optical Cameras</div>
            <div style="font-size:0.8rem; color:#94A3B8; margin-top:6px;">Cost: ₹8.0 Lakhs / unit</div>
        </div>
        """, unsafe_allow_html=True)

    with s2:
        st.markdown("""
        <div style="background:#0F172A; border:1px solid rgba(255,255,255,0.1); border-radius:14px; padding:18px;">
            <div style="font-size:1.5rem;">🇹🇼</div>
            <div style="font-weight:700; color:#F8FAFC; margin-top:6px;">Taiwan Semi Corp</div>
            <div style="font-size:0.8rem; color:#38BDF8;">Autopilot Microcontroller</div>
            <div style="font-size:0.8rem; color:#94A3B8; margin-top:6px;">Cost: ₹2.0 Lakhs / unit</div>
        </div>
        """, unsafe_allow_html=True)

    with s3:
        st.markdown("""
        <div style="background:#0F172A; border:1px solid rgba(255,255,255,0.1); border-radius:14px; padding:18px;">
            <div style="font-size:1.5rem;">🇯🇵</div>
            <div style="font-weight:700; color:#F8FAFC; margin-top:6px;">Japan Carbon Fiber</div>
            <div style="font-size:0.8rem; color:#38BDF8;">Ultra-Light Body Frame</div>
            <div style="font-size:0.8rem; color:#94A3B8; margin-top:6px;">Cost: ₹1.5 Lakhs / unit</div>
        </div>
        """, unsafe_allow_html=True)

    with s4:
        st.markdown("""
        <div style="background:#0F172A; border:1px solid rgba(255,255,255,0.1); border-radius:14px; padding:18px;">
            <div style="font-size:1.5rem;">🇮🇳</div>
            <div style="font-weight:700; color:#F8FAFC; margin-top:6px;">Local Indian Suppliers</div>
            <div style="font-size:0.8rem; color:#38BDF8;">LiPo Batteries & Motors</div>
            <div style="font-size:0.8rem; color:#94A3B8; margin-top:6px;">Cost: ₹0.8 Lakhs / unit</div>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# ORGAN 4: EYES & EARS (CUSTOMERS & DEFENSE TENDERS)
# ==============================================================================
elif organ == "eyes":
    st.markdown("""
    <div class="section-content-box">
        <div class="section-header">👁️ EYES & EARS — Key Customers & Government Tenders</div>
        <p style="color:#CBD5E1;">
            ideaForge keeps its eyes and ears on defense security tenders and government mapping contracts across India.
        </p>
    </div>
    """, unsafe_allow_html=True)

    e1, e2, e3 = st.columns(3)

    with e1:
        st.markdown("""
        <div style="background:#0F172A; border:1px solid rgba(255,255,255,0.1); border-radius:14px; padding:20px;">
            <div style="font-size:1.1rem; font-weight:800; color:#F59E0B;">🪖 Indian Army (Ministry of Defence)</div>
            <div style="font-size:0.85rem; color:#94A3B8; margin-top:4px;">Primary Defense Client</div>
            <hr style="border-color:rgba(255,255,255,0.1);">
            <div style="font-size:0.85rem; color:#E2E8F0;">• Revenue Share: <b>65%</b></div>
            <div style="font-size:0.85rem; color:#E2E8F0;">• Primary Deployment: <b>High-Altitude Border Surveillance</b></div>
            <div style="font-size:0.85rem; color:#60A5FA;">• Fast-Track Procurement Active</div>
        </div>
        """, unsafe_allow_html=True)

    with e2:
        st.markdown("""
        <div style="background:#0F172A; border:1px solid rgba(255,255,255,0.1); border-radius:14px; padding:20px;">
            <div style="font-size:1.1rem; font-weight:800; color:#F59E0B;">🛡️ Ministry of Home Affairs (BSF, CRPF)</div>
            <div style="font-size:0.85rem; color:#94A3B8; margin-top:4px;">Paramilitary & Law Enforcement</div>
            <hr style="border-color:rgba(255,255,255,0.1);">
            <div style="font-size:0.85rem; color:#E2E8F0;">• Revenue Share: <b>15%</b></div>
            <div style="font-size:0.85rem; color:#E2E8F0;">• Primary Deployment: <b>Crowd Monitoring & Rescue</b></div>
            <div style="font-size:0.85rem; color:#60A5FA;">• Multi-Year Service Tenders</div>
        </div>
        """, unsafe_allow_html=True)

    with e3:
        st.markdown("""
        <div style="background:#0F172A; border:1px solid rgba(255,255,255,0.1); border-radius:14px; padding:20px;">
            <div style="font-size:1.1rem; font-weight:800; color:#F59E0B;">🗺️ Survey of India</div>
            <div style="font-size:0.85rem; color:#94A3B8; margin-top:4px;">Civil Mapping Tenders</div>
            <hr style="border-color:rgba(255,255,255,0.1);">
            <div style="font-size:0.85rem; color:#E2E8F0;">• Revenue Share: <b>20%</b></div>
            <div style="font-size:0.85rem; color:#E2E8F0;">• Primary Deployment: <b>SVAMITVA Rural Land Mapping</b></div>
            <div style="font-size:0.85rem; color:#60A5FA;">• High-Precision Q6 Drone Fleet</div>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# ORGAN 5: LEGS (FLEET DEPLOYMENT & FIELD SERVICES)
# ==============================================================================
elif organ == "legs":
    st.markdown("""
    <div class="section-content-box">
        <div class="section-header">🦵 LEGS — Drone Fleet Deployment & Field Mobility</div>
        <p style="color:#CBD5E1;">
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
        <p style="color:#CBD5E1;">
            The brain processes complex information, calculates risks, and makes decisions for the company. 
            Use the simulation sliders below to see how executive decisions affect ideaForge in real time.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ----------------- REAL-WORLD SIMULATOR DRAWER FOR EVERY ORGAN -----------------
st.write("---")
st.markdown("""
<div class="sim-drawer">
    <div style="font-family:'Orbitron', sans-serif; font-size:1.2rem; font-weight:900; color:#FF4500; margin-bottom:4px;">
        🎛️ REAL-WORLD SIMULATION STUDIO — Test Factors Affecting the Company
    </div>
    <div style="font-size:0.85rem; color:#FFA07A; margin-bottom:16px;">
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

    st.line_chart(chart_df, color=["#00BFFF", "#FF4500"])

    o1, o2 = st.columns(2)
    with o1:
        st.metric("Simulated Profit Margin", f"{sim_res['EBITDA_Margin']:.1f}%", f"{sim_res['EBITDA_Margin'] - baseline_data['EBITDA_Margin']:.1f}% change")
    with o2:
        st.metric("Cash Collection Speed", f"{sim_res['Working_Capital_Days']:.0f} Days", f"{sim_res['Working_Capital_Days'] - baseline_data['Working_Capital_Days']:.0f}d change")

st.markdown("<br><center style='color:#64748B; font-family:Orbitron, sans-serif; font-size:0.9rem;'>ideaForge Digital Human OS — An Autonomous Company Digital Twin Built for Everyone</center>", unsafe_allow_html=True)
