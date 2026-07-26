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
    page_title="JARVIS Corporate Digital Twin | Executive Finance OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. JARVIS Futuristic Cyber HUD Styling & CSS Animation
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@500;600;700&family=Inter:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: #05070F;
        background-image: 
            radial-gradient(at 0% 0%, rgba(6, 182, 212, 0.12) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(139, 92, 246, 0.12) 0px, transparent 50%);
        color: #E2E8F0;
    }

    /* JARVIS HUD Top Header */
    .jarvis-header {
        background: linear-gradient(135deg, rgba(11, 15, 25, 0.9) 0%, rgba(5, 7, 15, 0.95) 100%);
        border: 1px solid rgba(6, 182, 212, 0.3);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 0 30px rgba(6, 182, 212, 0.15);
        position: relative;
        overflow: hidden;
    }

    .jarvis-header::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 2px;
        background: linear-gradient(90deg, #06B6D4, #8B5CF6, #3B82F6);
        animation: pulse-glow 3s infinite alternate;
    }

    @keyframes pulse-glow {
        0% { opacity: 0.4; }
        100% { opacity: 1; }
    }

    .jarvis-status-pill {
        display: inline-flex;
        align-items: center;
        background: rgba(6, 182, 212, 0.15);
        border: 1px solid #06B6D4;
        color: #22D3EE;
        padding: 4px 14px;
        border-radius: 20px;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        margin-bottom: 12px;
        box-shadow: 0 0 10px rgba(6, 182, 212, 0.3);
    }

    .jarvis-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.1rem;
        font-weight: 900;
        letter-spacing: 0.02em;
        background: linear-gradient(90deg, #06B6D4 0%, #A855F7 50%, #FFFFFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
    }

    .jarvis-subtitle {
        color: #94A3B8;
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        letter-spacing: 0.05em;
    }

    /* Cyber Metric Cards */
    .hud-card {
        background: rgba(11, 15, 25, 0.85);
        border: 1px solid rgba(6, 182, 212, 0.25);
        border-radius: 14px;
        padding: 20px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }

    .hud-card:hover {
        border-color: #06B6D4;
        box-shadow: 0 0 25px rgba(6, 182, 212, 0.3);
        transform: translateY(-3px);
    }

    .hud-label {
        font-family: 'Rajdhani', sans-serif;
        color: #94A3B8;
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .hud-val {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.9rem;
        font-weight: 900;
        color: #06B6D4;
        text-shadow: 0 0 12px rgba(6, 182, 212, 0.5);
        margin: 8px 0;
    }

    .hud-badge-pos {
        color: #10B981;
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.9rem;
        font-weight: 700;
    }

    .hud-badge-neg {
        color: #F43F5E;
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.9rem;
        font-weight: 700;
    }

    /* Recommendation Glass Cards */
    .rec-glass {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.8) 100%);
        border-left: 4px solid #A855F7;
        border-top: 1px solid rgba(168, 85, 247, 0.2);
        border-right: 1px solid rgba(168, 85, 247, 0.2);
        border-bottom: 1px solid rgba(168, 85, 247, 0.2);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }

    .rec-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.05rem;
        font-weight: 700;
        color: #C084FC;
        margin-bottom: 6px;
    }

    .tag-cyan {
        background: rgba(6, 182, 212, 0.2);
        color: #22D3EE;
        border: 1px solid rgba(6, 182, 212, 0.4);
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 700;
        display: inline-block;
        margin-right: 8px;
    }

    .tag-purple {
        background: rgba(168, 85, 247, 0.2);
        color: #C084FC;
        border: 1px solid rgba(168, 85, 247, 0.4);
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 700;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Session State Setup
if "selected_node" not in st.session_state:
    st.session_state["selected_node"] = None
if "command_input" not in st.session_state:
    st.session_state["command_input"] = ""

# Backend Initializer
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

# ----------------- SIDEBAR CONTROLS -----------------
st.sidebar.markdown("### 🎛️ Simulation Cockpit Controls")
st.sidebar.caption("Adjust macro-variables to test corporate financial resilience")

mod_lag = st.sidebar.slider(
    "MoD Disbursement Lag (Days)",
    min_value=15, max_value=180, value=int(baseline_data["MoD_Disbursement_Lag"]), step=5,
    help="Ministry of Defence capital budget payment release schedule"
)

import_price_shock = st.sidebar.slider(
    "Import Sensor Tariff Shock (%)",
    min_value=0, max_value=50, value=0, step=5,
    help="Customs duty hike on optical payloads & autopilot chips"
)

saas_attach_rate = st.sidebar.slider(
    "FLYGHT SaaS Attach Rate (%)",
    min_value=0, max_value=100, value=int(baseline_data["SaaS_Attach_Rate"] * 100), step=5,
    help="Percentage of drone fleet bundled with recurring software analytics"
)

indigenous_mix = st.sidebar.slider(
    "Indigenous Sourcing Ratio (%)",
    min_value=30, max_value=90, value=int(baseline_data["Indigenous_Sourcing_Mix"] * 100), step=5,
    help="Domestic component assembly content qualifying for PLI incentives"
)

scenario_config = {
    "mod_lag_days": mod_lag,
    "import_tariff_shock_pct": import_price_shock,
    "saas_attach_rate_pct": saas_attach_rate,
    "indigenous_mix": indigenous_mix / 100.0
}

# Run 2SLS Causal & Agentic Orchestration
agent_state = orchestrator.run_workflow(scenario_config)
sim_res = agent_state.simulated_results

# ----------------- JARVIS HUD HEADER -----------------
st.markdown("""
<div class="jarvis-header">
    <div class="jarvis-status-pill">⚡ JARVIS AI DIGITAL TWIN CORE :: ONLINE</div>
    <div class="jarvis-title">ideaForge Technology Limited</div>
    <div class="jarvis-subtitle">Enterprise Financial & Operational Holographic Replica • Corporate Strategy AI Operating System</div>
</div>
""", unsafe_allow_html=True)

# ----------------- JARVIS COMMAND BAR -----------------
st.markdown("##### 💬 JARVIS Interactive Executive Command Console")
cmd_col1, cmd_col2 = st.columns([3, 1])

with cmd_col1:
    user_cmd = st.text_input(
        "Type a command or query for JARVIS...",
        placeholder="e.g., 'Run liquidity crash test' or 'What happens if optical payload tariffs increase by 15%?'",
        key="jarvis_cmd_input"
    )

with cmd_col2:
    quick_cmd = st.selectbox(
        "Preset Commands",
        ["-- Select Preset --", "⚡ Run Liquidity Stress Test", "🛡️ 15% Tariff Shock Mitigation", "🚀 Maximize FLYGHT SaaS Monetization"]
    )

st.write("")

# ----------------- TELEMETRY KPI GAUGES -----------------
k1, k2, k3, k4 = st.columns(4)

def render_cyber_kpi(col, title, current_val, baseline_val, unit="", is_inverse=False):
    diff = current_val - baseline_val
    is_good = (diff <= 0) if is_inverse else (diff >= 0)
    badge_style = "hud-badge-pos" if is_good else "hud-badge-neg"
    sign = "+" if diff >= 0 else ""
    
    if unit == "%":
        val_str = f"{current_val:.1f}%"
        delta_str = f"{sign}{diff:.1f}% vs base"
    elif unit == "days":
        val_str = f"{current_val:.0f} Days"
        delta_str = f"{sign}{diff:.0f}d vs base"
    else:
        val_str = f"₹{current_val:.1f} Cr"
        delta_str = f"{sign}₹{diff:.1f} Cr vs base"

    col.markdown(f"""
    <div class="hud-card">
        <div class="hud-label">{title}</div>
        <div class="hud-val">{val_str}</div>
        <div class="{badge_style}">{delta_display if 'delta_display' in locals() else delta_str}</div>
    </div>
    """, unsafe_allow_html=True)

render_cyber_kpi(k1, "Operating EBITDA Margin", sim_res["EBITDA_Margin"], baseline_data["EBITDA_Margin"], "%")
render_cyber_kpi(k2, "Working Capital Cycle", sim_res["Working_Capital_Days"], baseline_data["Working_Capital_Days"], "days", is_inverse=True)
render_cyber_kpi(k3, "Projected Net Profit", sim_res["Net_Profit"], baseline_data["Net_Profit"], "Cr")
render_cyber_kpi(k4, "Liquidity Requirement", sim_res["Working_Capital_Requirement_Cr"], baseline_data["Revenue"] * (baseline_data["Working_Capital_Days"] / 365.0), "Cr", is_inverse=True)

st.write("")

# ----------------- FINANCE COCKPIT NAVIGATION -----------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🔮 1. JARVIS CFO Co-Pilot & Advice",
    "⚡ 2. Financial Crash-Test Sandbox",
    "🕸️ 3. Interactive Hologram Twin Core",
    "📚 4. Memory Vault & Belief History"
])

# ==============================================================================
# COCKPIT 1: JARVIS CFO CO-PILOT & ADVICE
# ==============================================================================
with tab1:
    c1, c2 = st.columns([1.1, 1])

    with c1:
        st.markdown("### 🎙️ JARVIS Executive Briefing")
        
        events_list = pipeline.load_dynamic_events()
        trace = reasoning_engine.execute_7_step_loop(events_list[0])
        advisor_matrix = strategic_advisor.generate_strategic_recommendations(trace)

        st.markdown(f"""
        <div style="background: rgba(15, 23, 42, 0.85); border:1px solid rgba(6, 182, 212, 0.3); border-radius:14px; padding:22px; box-shadow:0 0 20px rgba(6, 182, 212, 0.1);">
            <div style="font-family:'Orbitron', sans-serif; font-size:1.1rem; color:#22D3EE; font-weight:700; margin-bottom:12px;">
                🤖 Executive Synthesis & Liquidity Diagnosis
            </div>
            <p style="color:#E2E8F0; font-size:0.95rem; line-height:1.6;">
                <b>System Diagnostic</b>: Under the current scenario parameters (MoD Disbursement Lag set to <b>{mod_lag} days</b> and Tariff Shock at <b>+{import_price_shock}%</b>), operating EBITDA margin stands at <b style="color:#34D399;">{sim_res['EBITDA_Margin']:.1f}%</b>.
            </p>
            <p style="color:#E2E8F0; font-size:0.95rem; line-height:1.6;">
                <b>Liquidity Warning</b>: Extended payment cycles require <b>₹{sim_res['Working_Capital_Requirement_Cr']:.1f} Cr</b> in operational capital. Borrowing interest costs are projected at <b>₹{sim_res.get('Additional_Interest_Cost_Cr', 0.0):.2f} Cr</b>.
            </p>
            <p style="color:#A78BFA; font-size:0.95rem; font-weight:600;">
                💡 <b>Primary Recommended Action</b>: {advisor_matrix['recommended_primary_action']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        st.markdown("### 🛡️ Multi-Agent Advisory Radar")
        if agent_state.critical_flags:
            for flag in agent_state.critical_flags:
                st.error(f"🚨 **Alert Flag**: `{flag}` — Action needed to safeguard working capital.")
        else:
            st.success("✅ **Operational Radar Clear**: All procurement, supply chain, and Ind AS accounting indicators are within safety limits.")

    with c2:
        st.markdown("### ⚡ Prescriptive Strategic Action Cards")
        for rec in advisor_matrix["action_matrix"]:
            st.markdown(f"""
            <div class="rec-glass">
                <div>
                    <span class="tag-cyan">{rec['category']}</span>
                    <span class="tag-purple">Lead: {rec['executive_owner']}</span>
                </div>
                <div class="rec-title" style="margin-top:10px;">{rec['title']}</div>
                <div style="font-size:0.88rem; color:#CBD5E1; margin-bottom:8px;">{rec['recommended_action']}</div>
                <div style="font-size:0.88rem; color:#34D399; font-weight:700;">💰 ROI Impact: {rec['financial_impact']}</div>
            </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# COCKPIT 2: FINANCIAL CRASH-TEST SANDBOX (WHAT-IF ANALYSIS)
# ==============================================================================
with tab2:
    st.markdown("### ⚡ What-If Financial Crash-Test Simulator")
    st.caption("Compare how key corporate finance metrics shift across 3 parallel operational strategies:")

    no_action_margin = sim_res["EBITDA_Margin"]
    action_a_margin = min(35.0, no_action_margin + (15.0 - import_price_shock * 0.4))
    action_b_margin = min(38.0, no_action_margin + (saas_attach_rate * 0.15))

    st.markdown(f"""
    <div style="background:#0F172A; border-radius:14px; padding:24px; border:1px solid rgba(6, 182, 212, 0.3);">
        <table style="width:100%; color:#F8FAFC; border-collapse:collapse; font-size:0.95rem;">
            <tr style="border-bottom:2px solid rgba(6, 182, 212, 0.3); font-family:'Orbitron', sans-serif; font-size:0.85rem; color:#94A3B8;">
                <th style="text-align:left; padding:12px 0;">Strategy Option</th>
                <th style="text-align:center;">Operating EBITDA</th>
                <th style="text-align:center;">Working Capital</th>
                <th style="text-align:right;">Projected Net Profit</th>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.08);">
                <td style="padding:16px 0; font-weight:600; color:#94A3B8;">Status Quo (No Intervention)</td>
                <td style="text-align:center; font-weight:700; color:#F43F5E;">{no_action_margin:.1f}%</td>
                <td style="text-align:center;">{sim_res['Working_Capital_Days']:.0f} Days</td>
                <td style="text-align:right; font-weight:700;">₹{sim_res['Net_Profit']:.1f} Cr</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.08);">
                <td style="padding:16px 0; font-weight:600; color:#38BDF8;">Option A: Fast-Track Gujarat Local Sourcing</td>
                <td style="text-align:center; font-weight:700; color:#34D399;">{action_a_margin:.1f}%</td>
                <td style="text-align:center; font-weight:700; color:#34D399;">{max(180, sim_res['Working_Capital_Days'] - 20):.0f} Days</td>
                <td style="text-align:right; font-weight:700; color:#34D399;">₹{sim_res['Net_Profit'] + 4.5:.1f} Cr</td>
            </tr>
            <tr>
                <td style="padding:16px 0; font-weight:600; color:#C084FC;">Option B: Accelerate FLYGHT SaaS Fleet Bundling</td>
                <td style="text-align:center; font-weight:700; color:#34D399;">{action_b_margin:.1f}%</td>
                <td style="text-align:center; font-weight:700; color:#34D399;">{max(165, sim_res['Working_Capital_Days'] - 35):.0f} Days</td>
                <td style="text-align:right; font-weight:700; color:#34D399;">₹{sim_res['Net_Profit'] + 8.2:.1f} Cr</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# COCKPIT 3: INTERACTIVE HOLOGRAM TWIN CORE (NETWORK CANVAS)
# ==============================================================================
with tab3:
    st.markdown("### 🕸️ Interactive Company Hologram Core")
    st.caption("Visual graph mapping ideaForge's platforms, component BOMs, suppliers, and financial metrics:")

    g1, g2 = st.columns([2, 1])

    with g1:
        nodes = graph_db.get_nodes()
        edges = graph_db.get_edges()

        cy_elements = []
        color_map = {
            "BusinessSegment": "#06B6D4",      # Cyan
            "ProductPlatform": "#10B981",      # Emerald
            "SupplyChainComponent": "#F43F5E", # Rose
            "GovernmentPolicy": "#8B5CF6",     # Violet
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
                    "width": "36px",
                    "height": "36px",
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
            selected = cytoscape(cy_elements, stylesheet, layout={"name": "cose"}, height="460px", key="cy_jarvis")
            if selected and selected.get("nodes"):
                st.session_state["selected_node"] = selected["nodes"][0]
        except Exception:
            all_node_ids = [n["id"] for n in nodes]
            chosen = st.selectbox("Select Node to Inspect", ["-- Select Node --"] + all_node_ids)
            if chosen != "-- Select Node --":
                st.session_state["selected_node"] = chosen

    with g2:
        st.markdown("##### 📦 Holographic Node Inspector")
        if st.session_state["selected_node"]:
            n_id = st.session_state["selected_node"]
            details = graph_db.get_node_details(n_id)
            if details:
                st.markdown(f"**Entity**: `{n_id}`")
                st.markdown(f"**Category**: `{details.get('label')}`")
                props = {k: v for k, v in details.items() if k != "label"}
                st.table(pd.DataFrame(list(props.items()), columns=["Property", "Value"]))
        else:
            st.info("Click any node in the Hologram Core network to inspect its underlying BOM cost structure and revenue linkages.")

# ==============================================================================
# COCKPIT 4: MEMORY VAULT & BELIEF HISTORY
# ==============================================================================
with tab4:
    st.markdown("### 📚 Persistent Memory & Belief Revision Ledger")
    st.caption("Auditable timeline tracking how past macro shocks revised company operational beliefs over time:")

    m1, m2 = st.columns(2)
    with m1:
        st.markdown("##### 📜 Belief Revision Timeline")
        beliefs = memory_engine.get_belief_history()
        st.dataframe(pd.DataFrame(beliefs))

    with m2:
        st.markdown("##### 🎯 Historical Executive Decision Lessons")
        decisions = memory_engine.get_decision_history()
        st.dataframe(pd.DataFrame(decisions))
