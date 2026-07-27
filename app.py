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
    page_title="ideaForge Digital Twin | Human Avatar Company OS",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. ULTRA-HIGH CONTRAST CSS & HUMAN AVATAR CANVAS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Orbitron:wght@700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background-color: #050814;
        color: #FFFFFF;
    }

    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 3rem;
        max-width: 1350px;
    }

    p, span, label, div {
        color: #FFFFFF !important;
    }

    /* Top Brand Bar */
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
        color: #00E5FF !important;
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

    /* Central Human Avatar Canvas */
    .human-avatar-stage {
        background: linear-gradient(180deg, #0F172A 0%, #050814 100%);
        border: 2px solid #00E5FF;
        border-radius: 24px;
        padding: 30px;
        text-align: center;
        position: relative;
        margin-bottom: 30px;
        box-shadow: 0 0 50px rgba(0, 229, 255, 0.15);
    }

    .avatar-figure-box {
        display: inline-block;
        background: radial-gradient(circle, rgba(0, 229, 255, 0.1) 0%, transparent 70%);
        border: 2px solid rgba(0, 229, 255, 0.4);
        border-radius: 50%;
        width: 200px;
        height: 200px;
        line-height: 200px;
        font-size: 5rem;
        margin: 16px 0;
        box-shadow: 0 0 30px rgba(0, 229, 255, 0.3);
    }

    /* Streamlit Button Override */
    div.stButton > button {
        background: linear-gradient(135deg, #FF5500 0%, #FF2200 100%) !important;
        color: #FFFFFF !important;
        border: 2px solid #FF5500 !important;
        border-radius: 10px !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 0.85rem !important;
        font-weight: 800 !important;
        padding: 10px 14px !important;
        width: 100% !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        box-shadow: 0 4px 15px rgba(255, 85, 0, 0.4) !important;
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, #00E5FF 0%, #0088FF 100%) !important;
        color: #04060C !important;
        border-color: #00E5FF !important;
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.8) !important;
    }

    /* Section Content Box */
    .section-content-box {
        background: #0F172A;
        border: 2px solid #00E5FF;
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
        border: 2px solid #00E5FF;
        border-radius: 14px;
        padding: 18px;
        text-align: center;
    }

    .metric-pill-label {
        font-size: 0.85rem;
        color: #FFFFFF !important;
        font-weight: 700;
        text-transform: uppercase;
    }

    .metric-pill-val {
        font-size: 1.8rem;
        font-weight: 900;
        color: #00E5FF !important;
        margin-top: 4px;
    }

    /* Simulation Box */
    .sim-drawer {
        background: #1E1008;
        border: 2px solid #FF5500;
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 0 40px rgba(255, 85, 0, 0.3);
    }

    /* Clean bullet list item styling */
    .bullet-item {
        background: #1E293B;
        border-left: 4px solid #00E5FF;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 10px;
        font-size: 0.95rem;
        font-weight: 600;
        color: #FFFFFF !important;
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

# ----------------- CENTRAL HUMAN AVATAR STAGE -----------------
st.markdown("""
<div class="human-avatar-stage">
    <div style="font-family:'Orbitron', sans-serif; font-size:1.6rem; font-weight:900; color:#FFFFFF;">
        👤 CENTRAL DIGITAL HUMAN AVATAR OF IDEAFORGE
    </div>
    <div style="font-size:0.95rem; color:#00E5FF; font-weight:600; margin-top:4px;">
        Click any body part below to explore that organ of the company in plain English:
    </div>
    <br>
    <div class="avatar-figure-box">
        👤
    </div>
</div>
""", unsafe_allow_html=True)

# 6 Body Part Organ Selectors directly beneath avatar
c_brain, c_heart, c_arms, c_lungs, c_eyes, c_legs = st.columns(6)

with c_brain:
    if st.button("🧠 1. BRAIN\n(AI Strategy)", key="btn_brain", use_container_width=True):
        st.session_state["selected_organ"] = "brain"

with c_heart:
    if st.button("🫀 2. HEART\n(Financials)", key="btn_heart", use_container_width=True):
        st.session_state["selected_organ"] = "heart"

with c_arms:
    if st.button("🦾 3. ARMS\n(Factories)", key="btn_arms", use_container_width=True):
        st.session_state["selected_organ"] = "arms"

with c_lungs:
    if st.button("🫁 4. LUNGS\n(Suppliers)", key="btn_lungs", use_container_width=True):
        st.session_state["selected_organ"] = "lungs"

with c_eyes:
    if st.button("👁️ 5. EYES\n(Customers)", key="btn_eyes", use_container_width=True):
        st.session_state["selected_organ"] = "eyes"

with c_legs:
    if st.button("🦵 6. LEGS\n(Fleet Ops)", key="btn_legs", use_container_width=True):
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
        <div class="section-header">🫀 THE HEART OF IDEAFORGE — Financial Statements & Cash Flow</div>
        <p style="color:#FFFFFF; font-size:1rem; font-weight:600;">
            Just like a human heart pumps blood throughout the body, ideaForge's financial engine pumps money through its operations. 
            Here are the exact numbers and bullet points explaining the company's financial health:
        </p>
    </div>
    """, unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown("""
        <div class="metric-pill-box">
            <div class="metric-pill-label">Annual Revenue</div>
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
            <div style="font-size:0.85rem; color:#00E5FF; font-weight:700; margin-top:4px;">Cash Tied in Stock</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.markdown("#### 📋 Key Financial Bullet Points & Numbers")
    
    st.markdown("""
    <div class="bullet-item">💵 <b>Total Revenue (₹202 Cr)</b>: 65% comes from Indian Army defense orders, 20% from civil mapping, 10% from FLYGHT software subscriptions, and 5% from spare parts.</div>
    <div class="bullet-item">📈 <b>Profitability (23.9% Margin)</b>: Operating profit stands at ₹48.2 Cr, driven by high-margin defense drone platforms.</div>
    <div class="bullet-item">⏳ <b>Cash Cycle (75 Days)</b>: Ministry of Defence milestone bill clearances take ~60 to 90 days.</div>
    <div class="bullet-item">🏦 <b>Working Capital Requirement (₹41.5 Cr)</b>: Capital required to maintain component stock and cover unpaid government invoices.</div>
    """, unsafe_allow_html=True)

# ==============================================================================
# ORGAN 2: ARMS & HANDS (MANUFACTURING PLANTS & PRODUCTION)
# ==============================================================================
elif organ == "arms":
    st.markdown("""
    <div class="section-content-box">
        <div class="section-header">🦾 ARMS & HANDS — Manufacturing Facilities & Drone Assembly</div>
        <p style="color:#FFFFFF; font-size:1rem; font-weight:600;">
            These are the physical factories and hands that build ideaForge's drones. From raw carbon fiber sheets to high-altitude flight testing, explore how drones are crafted:
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="bullet-item">🏭 <b>Navi Mumbai Main Factory</b>: 45,000 sq ft facility capable of manufacturing <b>350 drones per month</b> (currently running at 78% capacity).</div>
    <div class="bullet-item">🔬 <b>Leh & Ladakh High-Altitude Testing Facility</b>: Tests drones up to <b>20,000 ft altitude</b> in extreme temperatures (-20°C to +50°C) with a 99.2% quality pass rate.</div>
    <div class="bullet-item">🛸 <b>Primary Drone Platforms Built</b>: SWITCH VTOL UAV (Border Defense), NETRA V4 (Police Patrol), Q6 UAV (Rural Land Mapping).</div>
    """, unsafe_allow_html=True)

# ==============================================================================
# ORGAN 3: LUNGS (SUPPLIERS & IMPORT FEEDS)
# ==============================================================================
elif organ == "lungs":
    st.markdown("""
    <div class="section-content-box">
        <div class="section-header">🫁 LUNGS — Suppliers & Global Component Imports</div>
        <p style="color:#FFFFFF; font-size:1rem; font-weight:600;">
            Just like lungs inhale oxygen, ideaForge inhales critical high-tech components from specialized global suppliers:
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="bullet-item">🇮🇱 <b>Elbit Systems (Israel)</b>: Supplies Day/Night EO/IR Optical Cameras (Cost: ₹8.0 Lakhs / unit).</div>
    <div class="bullet-item">🇹🇼 <b>Taiwan Semiconductor Corp</b>: Supplies Autopilot Microcontroller Microchips (Cost: ₹2.0 Lakhs / unit).</div>
    <div class="bullet-item">🇯🇵 <b>Japan Carbon Fiber Corp</b>: Supplies Ultra-Light Carbon Fiber Structural Body Frames (Cost: ₹1.5 Lakhs / unit).</div>
    <div class="bullet-item">🇮🇳 <b>Local Indian Suppliers</b>: Supplies LiPo Battery Packs & Electric Propulsion Motors (Cost: ₹0.8 Lakhs / unit).</div>
    """, unsafe_allow_html=True)

# ==============================================================================
# ORGAN 4: EYES & EARS (CUSTOMERS & DEFENSE TENDERS)
# ==============================================================================
elif organ == "eyes":
    st.markdown("""
    <div class="section-content-box">
        <div class="section-header">👁️ EYES & EARS — Key Customers & Government Tenders</div>
        <p style="color:#FFFFFF; font-size:1rem; font-weight:600;">
            ideaForge keeps its eyes and ears on defense security tenders and government contracts across India:
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="bullet-item">🪖 <b>Indian Army (65% Revenue Share)</b>: Primary defense customer for high-altitude border surveillance under fast-track procurement.</div>
    <div class="bullet-item">🛡️ <b>Ministry of Home Affairs / BSF / CRPF (15% Share)</b>: Paramilitary customer for law enforcement, crowd monitoring, and counter-insurgency.</div>
    <div class="bullet-item">🗺️ <b>Survey of India (20% Share)</b>: Civil customer for rural land mapping under the national SVAMITVA scheme.</div>
    """, unsafe_allow_html=True)

# ==============================================================================
# ORGAN 5: LEGS (FLEET DEPLOYMENT & FIELD SERVICES)
# ==============================================================================
elif organ == "legs":
    st.markdown("""
    <div class="section-content-box">
        <div class="section-header">🦵 LEGS — Drone Fleet Deployment & Field Mobility</div>
        <p style="color:#FFFFFF; font-size:1rem; font-weight:600;">
            ideaForge's drones have flown over 950,000 flight missions across difficult terrains, extreme altitudes, and urban environments:
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="bullet-item">🚀 <b>950,000+ Flight Missions Completed</b>: Across extreme Himalayas, deserts, and cities.</div>
    <div class="bullet-item">📜 <b>108+ Patents Granted & Filed</b>: Proprietary flight control algorithms and battery management tech.</div>
    <div class="bullet-item">💻 <b>1,250 Active FLYGHT SaaS Units</b>: Drones continuously streaming live encrypted video to commanders.</div>
    """, unsafe_allow_html=True)

# ==============================================================================
# ORGAN 6: BRAIN (AI STRATEGY & DECISION SIMULATION)
# ==============================================================================
elif organ == "brain":
    st.markdown("""
    <div class="section-content-box">
        <div class="section-header">🧠 THE BRAIN — AI Leadership & Strategy Simulator</div>
        <p style="color:#FFFFFF; font-size:1rem; font-weight:600;">
            The brain processes complex information, calculates risks, and makes decisions for the company. 
            Use the simulation sliders below to see how executive decisions affect ideaForge in numbers and bullet points:
        </p>
    </div>
    """, unsafe_allow_html=True)

# ----------------- REAL-WORLD SIMULATOR (NUMBERS & BULLET POINTS ONLY — NO MESSY CHARTS!) -----------------
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
    st.markdown("##### 📊 Simulated Outcome (Exact Numbers & Bullet Points)")

    ebitda_diff = sim_res["EBITDA_Margin"] - baseline_data["EBITDA_Margin"]
    wc_diff = sim_res["Working_Capital_Days"] - baseline_data["Working_Capital_Days"]
    req_diff = sim_res["Working_Capital_Requirement_Cr"] - (baseline_data["Revenue"] * (baseline_data["Working_Capital_Days"] / 365.0))

    o1, o2 = st.columns(2)
    with o1:
        st.markdown(f"""
        <div class="metric-pill-box">
            <div class="metric-pill-label">Simulated Profit Margin</div>
            <div class="metric-pill-val">{sim_res['EBITDA_Margin']:.1f}%</div>
            <div style="font-size:0.85rem; color:{'#34D399' if ebitda_diff>=0 else '#F43F5E'}; font-weight:800; margin-top:4px;">
                {'+' if ebitda_diff>=0 else ''}{ebitda_diff:.1f}% vs Normal
            </div>
        </div>
        """, unsafe_allow_html=True)

    with o2:
        st.markdown(f"""
        <div class="metric-pill-box">
            <div class="metric-pill-label">Cash Collection Speed</div>
            <div class="metric-pill-val">{sim_res['Working_Capital_Days']:.0f} Days</div>
            <div style="font-size:0.85rem; color:{'#34D399' if wc_diff<=0 else '#F43F5E'}; font-weight:800; margin-top:4px;">
                {'+' if wc_diff>=0 else ''}{wc_diff:.0f}d vs Normal
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.markdown("**📋 Executive Outcome Bullet Points:**")
    st.markdown(f"""
    <div class="bullet-item">💰 <b>Operating Profit Impact</b>: Operating EBITDA margin changes to <b>{sim_res['EBITDA_Margin']:.1f}%</b> ({'+' if ebitda_diff>=0 else ''}{ebitda_diff:.1f}% shift).</div>
    <div class="bullet-item">⏱️ <b>Cash Collection Cycle</b>: Time taken to collect payments changes to <b>{sim_res['Working_Capital_Days']:.0f} days</b>.</div>
    <div class="bullet-item">🏦 <b>Working Capital Requirement</b>: Required cash buffer in bank changes to <b>₹{sim_res['Working_Capital_Requirement_Cr']:.1f} Cr</b>.</div>
    """, unsafe_allow_html=True)

st.markdown("<br><center style='color:#00E5FF; font-family:Orbitron, sans-serif; font-size:0.95rem; font-weight:800;'>ideaForge Digital Human OS — An Autonomous Company Digital Twin Built for Everyone</center>", unsafe_allow_html=True)
