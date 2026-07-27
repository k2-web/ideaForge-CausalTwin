import streamlit as st
import pandas as pd
import numpy as np
import os
import json

# Import backend modules
from graph_db import IdeaForgeOntologyGraph
from data_ingestion import IdeaForgeIngestionPipeline
from causal_engine import IdeaForgeCausalEngine
from memory_engine import MemoryEngine
from reasoning_loop import StrategicReasoningEngine
from strategic_advisor import StrategicAdvisorEngine
from agents import IdeaForgeAgentOrchestrator

# 1. Page Configuration
st.set_page_config(
    page_title="AUTONOMOUS FINANCIAL DIGITAL TWIN OS for ideaForge",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Futuristic Human-Avatar & Cyberpunk Design System
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;700;800;900&family=Rajdhani:wght@500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: #04060C;
        background-image: 
            radial-gradient(at 50% 0%, rgba(255, 69, 0, 0.15) 0px, transparent 60%),
            radial-gradient(at 0% 100%, rgba(0, 191, 255, 0.12) 0px, transparent 50%);
        color: #F1F5F9;
    }

    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 3rem;
        max-width: 1350px;
    }

    /* Top Navigation Bar */
    .nav-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 14px 28px;
        background: rgba(10, 15, 26, 0.85);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 69, 0, 0.25);
        border-radius: 14px;
        margin-bottom: 24px;
        box-shadow: 0 4px 25px rgba(0, 0, 0, 0.5);
    }

    .nav-brand {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.4rem;
        font-weight: 900;
        color: #FFFFFF;
        letter-spacing: 0.05em;
    }

    .nav-links {
        display: flex;
        gap: 24px;
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.95rem;
        font-weight: 600;
        color: #94A3B8;
    }

    .nav-btn {
        background: linear-gradient(135deg, #FF4500 0%, #FF2200 100%);
        color: #FFFFFF;
        padding: 6px 18px;
        border-radius: 20px;
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        box-shadow: 0 0 15px rgba(255, 69, 0, 0.4);
    }

    /* Hero Section with Human AI Avatar */
    .hero-center {
        text-align: center;
        margin-bottom: 20px;
    }

    .hero-main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.2rem;
        font-weight: 900;
        letter-spacing: 0.08em;
        color: #FFFFFF;
        text-transform: uppercase;
        margin-bottom: 4px;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.2);
    }

    .hero-sub-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.2rem;
        font-weight: 700;
        color: #FF4500;
        letter-spacing: 0.05em;
        margin-bottom: 20px;
    }

    /* Human Avatar Visual Core */
    .avatar-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 20px 0;
        position: relative;
    }

    .avatar-card {
        background: radial-gradient(circle, rgba(15, 23, 42, 0.9) 0%, rgba(5, 7, 15, 0.95) 100%);
        border: 2px solid rgba(255, 69, 0, 0.4);
        border-radius: 50%;
        width: 180px;
        height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: 0 0 40px rgba(255, 69, 0, 0.3), inset 0 0 20px rgba(0, 191, 255, 0.2);
    }

    .avatar-icon {
        font-size: 3.8rem;
        filter: drop-shadow(0 0 10px #FF4500);
    }

    .avatar-text {
        font-family: 'Orbitron', sans-serif;
        font-size: 0.7rem;
        font-weight: 800;
        color: #00BFFF;
        letter-spacing: 0.08em;
        margin-top: 4px;
    }

    /* Floating Glass Cards */
    .glass-info-card {
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 69, 0, 0.3);
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
        height: 100%;
    }

    .glass-card-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 0.9rem;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .glass-card-text {
        font-size: 0.85rem;
        color: #94A3B8;
        line-height: 1.5;
    }

    /* 7-Step Reasoning Visualizer */
    .reasoning-bar-container {
        background: rgba(10, 15, 26, 0.9);
        border: 1px solid rgba(255, 69, 0, 0.3);
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 28px;
        box-shadow: 0 0 30px rgba(255, 69, 0, 0.15);
    }

    .reasoning-bar-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 1rem;
        font-weight: 800;
        color: #FFFFFF;
        text-align: center;
        letter-spacing: 0.1em;
        margin-bottom: 18px;
    }

    .nodes-flow {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .node-circle {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        background: #0B132B;
        border: 2px solid #00BFFF;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.8rem;
        font-weight: 800;
        color: #00BFFF;
        box-shadow: 0 0 12px rgba(0, 191, 255, 0.5);
    }

    .node-circle.active {
        border-color: #FF4500;
        color: #FF4500;
        box-shadow: 0 0 18px rgba(255, 69, 0, 0.8);
    }

    .node-label {
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.75rem;
        font-weight: 700;
        color: #94A3B8;
        text-align: center;
        margin-top: 6px;
    }

    /* Clean 5-Node Value Chain Cards (No Messy Overlap!) */
    .clean-node-card {
        background: #0F172A;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        padding: 18px;
        text-align: center;
        transition: transform 0.2s, border-color 0.2s;
    }

    .clean-node-card:hover {
        border-color: #FF4500;
        transform: translateY(-3px);
        box-shadow: 0 0 20px rgba(255, 69, 0, 0.2);
    }

    .node-card-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 0.85rem;
        font-weight: 700;
        color: #38BDF8;
        margin-top: 6px;
        margin-bottom: 4px;
    }

    .node-card-desc {
        font-size: 0.8rem;
        color: #94A3B8;
    }

    /* Orange Econometric Monitor Panel */
    .orange-monitor {
        background: linear-gradient(135deg, #1C0A00 0%, #0F0500 100%);
        border: 2px solid #FF4500;
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 0 35px rgba(255, 69, 0, 0.25);
        margin-bottom: 24px;
    }

    .monitor-head {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.1rem;
        font-weight: 900;
        color: #FF4500;
        letter-spacing: 0.08em;
        margin-bottom: 4px;
    }

    .job-status-pill {
        display: inline-block;
        background: rgba(16, 185, 129, 0.2);
        color: #34D399;
        border: 1px solid #10B981;
        padding: 4px 12px;
        border-radius: 6px;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.75rem;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# Session State Setup
if "active_node_inspect" not in st.session_state:
    st.session_state["active_node_inspect"] = "SWITCH_UAV"

# Backend Initialization
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

# ----------------- TOP NAVIGATION BAR -----------------
st.markdown("""
<div class="nav-bar">
    <div class="nav-brand">ideaForge</div>
    <div class="nav-links">
        <span style="color:#FF4500;">Features</span>
        <span>Products</span>
        <span>Descriptions</span>
        <span>Contact</span>
    </div>
    <div>
        <span class="nav-btn">Explore Twin</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------- HERO HEADER & HUMAN AI AVATAR -----------------
st.markdown("""
<div class="hero-center">
    <div class="hero-main-title">AUTONOMOUS FINANCIAL DIGITAL TWIN OS</div>
    <div class="hero-sub-title">for ideaForge</div>
</div>
""", unsafe_allow_html=True)

col_hero_left, col_hero_center, col_hero_right = st.columns([1, 1, 1])

with col_hero_left:
    st.markdown("""
    <div class="glass-info-card">
        <div class="glass-card-title">AUTONOMOUS FINANCIAL DIGITAL TWIN</div>
        <div class="glass-card-text">
            A live digital representation of <b>ideaForge Technology Limited</b> that connects drone manufacturing (BOMs, cameras, lead times) directly to corporate financial outcomes.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_hero_center:
    st.markdown("""
    <div class="avatar-container">
        <div class="avatar-card">
            <div class="avatar-icon">👤</div>
            <div class="avatar-text">AI TWIN CORE</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_hero_right:
    st.markdown("""
    <div class="glass-info-card">
        <div class="glass-card-title">PERSISTENT REASONING ENGINE</div>
        <div class="glass-card-text">
            Ingests defense tenders, tariff updates, and macro-variables to continuously update internal company memory and calculate strategic recommendations.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ----------------- 7-STEP REASONING CYCLE VISUALIZER -----------------
st.markdown("""
<div class="reasoning-bar-container">
    <div class="reasoning-bar-title">7-STEP REASONING CYCLE</div>
    <div class="nodes-flow">
        <div>
            <div class="node-circle active">01</div>
            <div class="node-label">Detection</div>
        </div>
        <div>
            <div class="node-circle">02</div>
            <div class="node-label">Relevance</div>
        </div>
        <div>
            <div class="node-circle">03</div>
            <div class="node-label">15-Dim Impact</div>
        </div>
        <div>
            <div class="node-circle active">04</div>
            <div class="node-label">Severity</div>
        </div>
        <div>
            <div class="node-circle">05</div>
            <div class="node-label">Belief Update</div>
        </div>
        <div>
            <div class="node-circle active">06</div>
            <div class="node-label">Action Trigger</div>
        </div>
        <div>
            <div class="node-circle active">07</div>
            <div class="node-label">Simulate</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------- FLOATING GLASS CONCEPT CARDS -----------------
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.markdown("""
    <div class="glass-info-card" style="border-left: 4px solid #00BFFF;">
        <div class="glass-card-title" style="color: #00BFFF;">CREATING AN EVOLVING, PERSISTENT MODEL</div>
        <div class="glass-card-text">
            Remembers historical operational assumptions, past decision rationales, and belief updates across fiscal quarters.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_g2:
    st.markdown("""
    <div class="glass-info-card" style="border-left: 4px solid #FF4500;">
        <div class="glass-card-title" style="color: #FF4500;">INGESTING STATIC & DYNAMIC DATA</div>
        <div class="glass-card-text">
            Processes Ind AS quarterly filings, BRSR annual reports, GeM defense tenders, and customs cargo BOE logs in real time.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# ----------------- CLEAN 5-NODE VALUE CHAIN MAP (NO MESSY OVERLAP!) -----------------
st.markdown("### 🕸️ Clean Company Value Chain Map")
st.caption("Click any node in the company pipeline to inspect its real-world operational details:")

n_cols = st.columns(5)

with n_cols[0]:
    st.markdown("""
    <div class="clean-node-card">
        <div style="font-size:1.8rem;">🪖</div>
        <div class="node-card-title">1. Defense Clients</div>
        <div class="node-card-desc">Indian Army & BSF (65% Revenue)</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Inspect Clients", use_container_width=True):
        st.session_state["active_node_inspect"] = "Indian_Army"

with n_cols[1]:
    st.markdown("""
    <div class="clean-node-card">
        <div style="font-size:1.8rem;">🚁</div>
        <div class="node-card-title">2. SWITCH Drone</div>
        <div class="node-card-desc">Flagship VTOL Platform</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Inspect Drone", use_container_width=True):
        st.session_state["active_node_inspect"] = "SWITCH_UAV"

with n_cols[2]:
    st.markdown("""
    <div class="clean-node-card">
        <div style="font-size:1.8rem;">📷</div>
        <div class="node-card-title">3. Import Sensors</div>
        <div class="node-card-desc">Israel/US Optical Payloads</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Inspect Sensors", use_container_width=True):
        st.session_state["active_node_inspect"] = "EO_IR_Optical_Payload"

with n_cols[3]:
    st.markdown("""
    <div class="clean-node-card">
        <div style="font-size:1.8rem;">💰</div>
        <div class="node-card-title">4. Operating Profit</div>
        <div class="node-card-desc">EBITDA Margin Target</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Inspect Profit", use_container_width=True):
        st.session_state["active_node_inspect"] = "EBITDA_Margin"

with n_cols[4]:
    st.markdown("""
    <div class="clean-node-card">
        <div style="font-size:1.8rem;">💵</div>
        <div class="node-card-title">5. Cash Cycle</div>
        <div class="node-card-desc">Payment Clearance Speed</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Inspect Cash", use_container_width=True):
        st.session_state["active_node_inspect"] = "Working_Capital_Days"

st.write("")

# Display inspected node summary
inspect_id = st.session_state["active_node_inspect"]
node_data = graph_db.get_node_details(inspect_id)

if node_data:
    st.info(f"🔍 **Selected Value Chain Element**: `{inspect_id}` ({node_data.get('label')})")
    props = {k: v for k, v in node_data.items() if k != "label"}
    st.table(pd.DataFrame(list(props.items()), columns=["Property", "Details"]))

st.write("---")

# ----------------- ORANGE COUNTERFACTUAL SIMULATOR MONITOR -----------------
st.markdown("""
<div class="orange-monitor">
    <div class="monitor-head">d o ( X = x ) &nbsp; COUNTERFACTUAL SIMULATOR MONITOR</div>
    <div style="font-size:0.85rem; color:#FFA07A;">Adjust real-world conditions to simulate financial impacts in real time:</div>
</div>
""", unsafe_allow_html=True)

ctrl_col1, ctrl_col2 = st.columns([1, 1.2])

with ctrl_col1:
    st.markdown("##### 🎛️ Real-World Scenario Sliders")
    
    mod_lag = st.slider(
        "Government Invoice Clearance Time (Days)",
        min_value=15, max_value=180, value=int(baseline_data["MoD_Disbursement_Lag"]), step=5
    )

    import_price_shock = st.slider(
        "Imported Camera / Tariff Price Hike (%)",
        min_value=0, max_value=50, value=0, step=5
    )

    saas_attach_rate = st.slider(
        "Software Subscription Adoption (%)",
        min_value=0, max_value=100, value=int(baseline_data["SaaS_Attach_Rate"] * 100), step=5
    )

    scenario_config = {
        "mod_lag_days": mod_lag,
        "import_tariff_shock_pct": import_price_shock,
        "saas_attach_rate_pct": saas_attach_rate,
        "indigenous_mix": 0.60
    }

    agent_state = orchestrator.run_workflow(scenario_config)
    sim_res = agent_state.simulated_results

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("##### ⚙️ Daily Executive Briefing Worker")
    st.markdown("""
    <div style="background:rgba(0,0,0,0.4); border:1px solid #FF4500; border-radius:10px; padding:16px;">
        <span class="job-status-pill">Job Status: [Running]</span>
        <div style="font-size:0.85rem; color:#FFA07A; margin-top:10px;">
            Automated Nightly Worker is actively monitoring GeM tenders and customs ICES cargo logs.
        </div>
    </div>
    """, unsafe_allow_html=True)

with ctrl_col2:
    st.markdown("##### 📈 Real-Time Profit Trend Simulation")
    
    quarters = ["Q1 FY25", "Q2 FY25", "Q3 FY25", "Q4 FY25", "Q1 FY26", "Q2 FY26", "Q3 FY26", "Q4 FY26 (Simulated)"]
    baseline_trend = [12.8, 8.4, 18.2, 38.6, 15.1, 11.5, 22.1, baseline_data["EBITDA_Margin"]]
    simulated_trend = [12.8, 8.4, 18.2, 38.6, 15.1, 11.5, 22.1, sim_res["EBITDA_Margin"]]
    
    chart_df = pd.DataFrame({
        "Baseline Profit (%)": baseline_trend,
        "Simulated Counterfactual Profit (%)": simulated_trend
    }, index=quarters)
    
    st.line_chart(chart_df, color=["#00BFFF", "#FF4500"])
    
    sc1, sc2 = st.columns(2)
    with sc1:
        st.metric("Simulated Profit Margin", f"{sim_res['EBITDA_Margin']:.1f}%", f"{sim_res['EBITDA_Margin'] - baseline_data['EBITDA_Margin']:.1f}% vs base")
    with sc2:
        st.metric("Cash Collection Speed", f"{sim_res['Working_Capital_Days']:.0f} Days", f"{sim_res['Working_Capital_Days'] - baseline_data['Working_Capital_Days']:.0f}d vs base")

st.markdown("<br><center style='color:#64748B; font-family:Orbitron, sans-serif; font-size:0.9rem;'>A Production-Grade Autonomous Twin</center>", unsafe_allow_html=True)
