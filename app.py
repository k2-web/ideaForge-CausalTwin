import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
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

# 2. Futuristic Cyberpunk / Glassmorphism Design System matching reference image
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;700;800;900&family=Rajdhani:wght@500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: #04060C;
        background-image: 
            radial-gradient(at 50% 0%, rgba(255, 69, 0, 0.12) 0px, transparent 60%),
            radial-gradient(at 0% 100%, rgba(0, 191, 255, 0.1) 0px, transparent 50%);
        color: #F1F5F9;
    }

    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 3rem;
        max-width: 1400px;
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

    .nav-link-item {
        cursor: pointer;
        transition: color 0.2s;
    }
    .nav-link-item:hover {
        color: #FF4500;
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

    /* Hero Section */
    .hero-center {
        text-align: center;
        margin-bottom: 28px;
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
        margin-bottom: 24px;
    }

    /* Glass Info Cards */
    .glass-info-card {
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 69, 0, 0.3);
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
        margin-bottom: 16px;
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

    /* 7-Step Reasoning Node Visualizer */
    .reasoning-bar-container {
        background: rgba(10, 15, 26, 0.9);
        border: 1px solid rgba(255, 69, 0, 0.3);
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 32px;
        box-shadow: 0 0 30px rgba(255, 69, 0, 0.15);
    }

    .reasoning-bar-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 1rem;
        font-weight: 800;
        color: #FFFFFF;
        text-align: center;
        letter-spacing: 0.1em;
        margin-bottom: 20px;
    }

    .nodes-flow {
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: relative;
    }

    .node-circle {
        width: 42px;
        height: 42px;
        border-radius: 50%;
        background: #0B132B;
        border: 2px solid #00BFFF;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.85rem;
        font-weight: 800;
        color: #00BFFF;
        box-shadow: 0 0 15px rgba(0, 191, 255, 0.5);
        z-index: 2;
    }

    .node-circle.active {
        border-color: #FF4500;
        color: #FF4500;
        box-shadow: 0 0 20px rgba(255, 69, 0, 0.8);
    }

    .node-label {
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.75rem;
        font-weight: 700;
        color: #94A3B8;
        text-align: center;
        margin-top: 6px;
    }

    /* Orange Econometric Monitor Panel */
    .orange-monitor {
        background: linear-gradient(135deg, #1C0A00 0%, #0F0500 100%);
        border: 2px solid #FF4500;
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 0 40px rgba(255, 69, 0, 0.25);
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

    .monitor-sub {
        font-size: 0.8rem;
        color: #FFA07A;
        margin-bottom: 16px;
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
if "selected_node" not in st.session_state:
    st.session_state["selected_node"] = None
if "selected_product" not in st.session_state:
    st.session_state["selected_product"] = "SWITCH_UAV"

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
        <span class="nav-link-item">Features</span>
        <span class="nav-link-item">Products</span>
        <span class="nav-link-item">Descriptions</span>
        <span class="nav-link-item">Contact</span>
    </div>
    <div>
        <span class="nav-btn">Explore Twin</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------- SECTION 1: HERO TITLE -----------------
st.markdown("""
<div class="hero-center">
    <div class="hero-main-title">AUTONOMOUS FINANCIAL DIGITAL TWIN OS</div>
    <div class="hero-sub-title">for ideaForge</div>
</div>
""", unsafe_allow_html=True)

col_h1, col_h2 = st.columns(2)

with col_h1:
    st.markdown("""
    <div class="glass-info-card">
        <div class="glass-card-title">AUTONOMOUS FINANCIAL DIGITAL TWIN</div>
        <div class="glass-card-text">
            ideaForge is a live mathematical replica that connects physical UAS operations (BOMs, lead times) directly to financial metrics (EBITDA, working capital, free cash flow).
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_h2:
    st.markdown("""
    <div class="glass-info-card">
        <div class="glass-card-title">PERSISTENT REASONING ENGINE</div>
        <div class="glass-card-text">
            Ingests breaking news, defense tenders, and customs disclosures to continuously update internal operational beliefs and forecast multi-year counterfactual outcomes.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ----------------- SECTION 2: 7-STEP REASONING CYCLE FLOW -----------------
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

# ----------------- SECTION 3: HOLOGRAM SPHERE CARDS -----------------
col_s1, col_s2 = st.columns(2)

with col_s1:
    st.markdown("""
    <div class="glass-info-card" style="border-left: 4px solid #00BFFF;">
        <div class="glass-card-title" style="color: #00BFFF;">CREATING AN EVOLVING, PERSISTENT MODEL</div>
        <div class="glass-card-text">
            Maintains an auditable memory ledger tracking historical assumptions, past decision rationales, and belief revisions across fiscal quarters.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_s2:
    st.markdown("""
    <div class="glass-info-card" style="border-left: 4px solid #FF4500;">
        <div class="glass-card-title" style="color: #FF4500;">INGESTING STATIC & DYNAMIC DATA</div>
        <div class="glass-card-text">
            Processes Ind AS quarterly filings, BRSR annual disclosures, GeM procurement portal tenders, and customs cargo BOE import logs.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ----------------- SECTION 4: ORANGE ECONOMETRIC MONITOR PANEL -----------------
st.markdown("""
<div class="orange-monitor">
    <div class="monitor-head">d o ( X = x ) &nbsp; COUNTERFACTUAL OUTCOMES</div>
    <div class="monitor-sub">Two-Stage Least Squares (2SLS) Econometric SCM Engine & Dynamic Simulation Studio</div>
</div>
""", unsafe_allow_html=True)

# Live Controls & Simulation Output
ctrl_col1, ctrl_col2 = st.columns([1, 1.2])

with ctrl_col1:
    st.markdown("##### 🎛️ Simulation Controls")
    
    mod_lag = st.slider(
        "MoD Disbursement Lag (Days)",
        min_value=15, max_value=180, value=int(baseline_data["MoD_Disbursement_Lag"]), step=5
    )

    import_price_shock = st.slider(
        "Import Payload Cost Shock (%)",
        min_value=0, max_value=50, value=0, step=5
    )

    saas_attach_rate = st.slider(
        "FLYGHT SaaS Attach Rate (%)",
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
            Automated Nightly Worker is actively monitoring GeM tender notices and customs ICES BOE logs.
        </div>
    </div>
    """, unsafe_allow_html=True)

with ctrl_col2:
    st.markdown("##### 📈 Econometric Counterfactual Projections")
    
    # Generate realistic trend curve for chart based on slider values
    quarters = ["Q1 FY25", "Q2 FY25", "Q3 FY25", "Q4 FY25", "Q1 FY26", "Q2 FY26", "Q3 FY26", "Q4 FY26 (Simulated)"]
    
    baseline_trend = [12.8, 8.4, 18.2, 38.6, 15.1, 11.5, 22.1, baseline_data["EBITDA_Margin"]]
    simulated_trend = [12.8, 8.4, 18.2, 38.6, 15.1, 11.5, 22.1, sim_res["EBITDA_Margin"]]
    
    chart_df = pd.DataFrame({
        "Baseline EBITDA (%)": baseline_trend,
        "Simulated Counterfactual EBITDA (%)": simulated_trend
    }, index=quarters)
    
    st.line_chart(chart_df, color=["#00BFFF", "#FF4500"])
    
    # Summary Cards
    sc1, sc2 = st.columns(2)
    with sc1:
        st.metric("Simulated EBITDA Margin", f"{sim_res['EBITDA_Margin']:.1f}%", f"{sim_res['EBITDA_Margin'] - baseline_data['EBITDA_Margin']:.1f}% vs base")
    with sc2:
        st.metric("Working Capital Cycle", f"{sim_res['Working_Capital_Days']:.0f} Days", f"{sim_res['Working_Capital_Days'] - baseline_data['Working_Capital_Days']:.0f}d vs base")

st.write("---")

# ----------------- SECTION 5: INTERACTIVE KNOWLEDGE GRAPH -----------------
st.markdown("### 🕸️ Company Value Chain Knowledge Graph")
st.caption("Interactive network visualizer mapping ideaForge's platforms, component BOMs, suppliers, and financial flow linkages:")

g1, g2 = st.columns([2, 1])

with g1:
    nodes = graph_db.get_nodes()
    edges = graph_db.get_edges()

    cy_elements = []
    color_map = {
        "BusinessSegment": "#00BFFF",      # Cyan
        "ProductPlatform": "#10B981",      # Emerald
        "SupplyChainComponent": "#FF4500", # Orange/Red
        "GovernmentPolicy": "#8B5CF6",     # Purple
        "CustomerEntity": "#F59E0B",       # Amber
        "FinancialMetric": "#EAB308"       # Yellow
    }

    for n in nodes:
        node_label = n.get("name") or n.get("model_name") or n.get("title") or n.get("id")
        cy_elements.append({
            "data": {
                "id": n["id"],
                "label": node_label,
                "color": color_map.get(n.get("label"), "#CCCCCC")
            }
        })

    for e in edges:
        cy_elements.append({
            "data": {
                "source": e["source"],
                "target": e["target"],
                "relationship": e.get("relationship", "")
            }
        })

    stylesheet = [
        {
            "selector": "node",
            "style": {
                "label": "data(label)",
                "background-color": "data(color)",
                "color": "#FFFFFF",
                "font-size": "11px",
                "width": "35px",
                "height": "35px",
                "text-valign": "center",
                "text-halign": "bottom"
            }
        },
        {
            "selector": "edge",
            "style": {
                "width": "2px",
                "line-color": "#475569",
                "target-arrow-color": "#475569",
                "target-arrow-shape": "triangle",
                "curve-style": "bezier",
                "label": "data(relationship)",
                "font-size": "8px",
                "color": "#94A3B8"
            }
        }
    ]

    try:
        from st_cytoscape import cytoscape
        selected = cytoscape(cy_elements, stylesheet, layout={"name": "cose"}, height="440px", key="cy_ref")
        if selected and selected.get("nodes"):
            st.session_state["selected_node"] = selected["nodes"][0]
    except Exception:
        all_node_ids = [n["id"] for n in nodes]
        chosen = st.selectbox("Inspect Graph Node", ["-- Select Node --"] + all_node_ids)
        if chosen != "-- Select Node --":
            st.session_state["selected_node"] = chosen

with g2:
    st.markdown("##### 📦 Node Inspector")
    if st.session_state["selected_node"]:
        n_id = st.session_state["selected_node"]
        details = graph_db.get_node_details(n_id)
        if details:
            st.markdown(f"**Entity**: `{n_id}`")
            st.markdown(f"**Type**: `{details.get('label')}`")
            props = {k: v for k, v in details.items() if k != "label"}
            st.table(pd.DataFrame(list(props.items()), columns=["Property", "Value"]))
    else:
        st.info("Click any node in the Knowledge Graph to inspect its underlying BOM components and financial linkages.")

st.markdown("<br><center style='color:#64748B; font-family:Orbitron, sans-serif; font-size:0.9rem;'>A Production-Grade Autonomous Twin</center>", unsafe_allow_html=True)
