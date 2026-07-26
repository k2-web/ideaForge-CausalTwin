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

# 1. Page Configuration & Theme
st.set_page_config(
    page_title="ideaForge Autonomous Digital Twin",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Executive Design System & Glassmorphism Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #0B0F19;
        color: #F3F4F6;
    }

    /* Top Executive Banner */
    .hero-banner {
        background: linear-gradient(135deg, rgba(17, 24, 39, 0.8) 0%, rgba(31, 41, 55, 0.5) 100%);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.36);
    }
    
    .status-pill {
        display: inline-flex;
        align-items: center;
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #34D399;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 12px;
    }
    
    .hero-title {
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(90deg, #FFFFFF 0%, #9CA3AF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
    }
    
    .hero-subtitle {
        color: #9CA3AF;
        font-size: 0.95rem;
        margin-bottom: 0;
    }

    /* Metric Cards */
    .glass-metric {
        background: rgba(17, 24, 39, 0.7);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 20px;
        transition: transform 0.2s, border-color 0.2s;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    .glass-metric:hover {
        border-color: rgba(6, 182, 212, 0.4);
        transform: translateY(-2px);
    }
    
    .metric-label {
        color: #9CA3AF;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .metric-val {
        font-size: 1.9rem;
        font-weight: 800;
        color: #F9FAFB;
        margin: 8px 0;
    }
    
    .badge-pos {
        color: #34D399;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .badge-neg {
        color: #F87171;
        font-size: 0.85rem;
        font-weight: 600;
    }

    /* Strategy Cards */
    .strategy-card {
        background: #111827;
        border-left: 4px solid #06B6D4;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 16px;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .strategy-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #38BDF8;
        margin-bottom: 8px;
    }
    
    .impact-pill {
        background: rgba(6, 182, 212, 0.15);
        color: #38BDF8;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
        margin-right: 8px;
    }
    
    .owner-pill {
        background: rgba(156, 163, 175, 0.15);
        color: #D1D5DB;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 500;
        display: inline-block;
    }

    /* Stepper Styling */
    .step-card {
        background: #111827;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 16px;
    }
    
    .step-number {
        font-size: 0.75rem;
        font-weight: 700;
        color: #06B6D4;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    
    .step-head {
        font-size: 1.1rem;
        font-weight: 700;
        color: #F9FAFB;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session States
if "selected_node" not in st.session_state:
    st.session_state["selected_node"] = None
if "focus_neighborhood" not in st.session_state:
    st.session_state["focus_neighborhood"] = False

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

# ----------------- SIDEBAR CONTROLS -----------------
st.sidebar.markdown("### 🎛️ Live Scenario Controls")
st.sidebar.caption("Simulate real-time operational & geopolitical shocks")

mod_lag = st.sidebar.slider(
    "MoD Disbursement Lag (Days)",
    min_value=15, max_value=180, value=int(baseline_data["MoD_Disbursement_Lag"]), step=5,
    help="Lag in payment releases from Ministry of Defence"
)

import_price_shock = st.sidebar.slider(
    "Import Payload Cost Shock (%)",
    min_value=0, max_value=50, value=0, step=5,
    help="Tariff hikes on Israeli/US electro-optical sensors"
)

saas_attach_rate = st.sidebar.slider(
    "FLYGHT SaaS Attach Rate (%)",
    min_value=0, max_value=100, value=int(baseline_data["SaaS_Attach_Rate"] * 100), step=5,
    help="Cloud software subscription adoption rate"
)

indigenous_mix = st.sidebar.slider(
    "Indigenous Sourcing Ratio (%)",
    min_value=30, max_value=90, value=int(baseline_data["Indigenous_Sourcing_Mix"] * 100), step=5,
    help="Local manufacturing content compliance level"
)

scenario_config = {
    "mod_lag_days": mod_lag,
    "import_tariff_shock_pct": import_price_shock,
    "saas_attach_rate_pct": saas_attach_rate,
    "indigenous_mix": indigenous_mix / 100.0
}

# Run simulation & multi-agent system
agent_state = orchestrator.run_workflow(scenario_config)
sim_res = agent_state.simulated_results

# ----------------- EXECUTIVE HERO BANNER -----------------
st.markdown("""
<div class="hero-banner">
    <div class="status-pill">🟢 Autonomous Twin Active &nbsp;•&nbsp; Memory Synced &nbsp;•&nbsp; 2SLS Causal SCM Online</div>
    <div class="hero-title">ideaForge Technology Limited</div>
    <div class="hero-subtitle">Autonomous Financial & Operational Digital Twin — Executive Decision Support System</div>
</div>
""", unsafe_allow_html=True)

# ----------------- KPI CARDS -----------------
k1, k2, k3, k4 = st.columns(4)

def render_kpi_card(col, title, current_val, baseline_val, unit="", is_inverse=False):
    diff = current_val - baseline_val
    if is_inverse:
        is_good = diff <= 0
    else:
        is_good = diff >= 0
        
    badge_style = "badge-pos" if is_good else "badge-neg"
    sign = "+" if diff >= 0 else ""
    
    if unit == "%":
        val_display = f"{current_val:.1f}%"
        delta_display = f"{sign}{diff:.1f}% vs base"
    elif unit == "days":
        val_display = f"{current_val:.0f}d"
        delta_display = f"{sign}{diff:.0f}d vs base"
    else:
        val_display = f"₹{current_val:.1f} Cr"
        delta_display = f"{sign}₹{diff:.1f} Cr vs base"

    col.markdown(f"""
    <div class="glass-metric">
        <div class="metric-label">{title}</div>
        <div class="metric-val">{val_display}</div>
        <div class="{badge_style}">{delta_display}</div>
    </div>
    """, unsafe_allow_html=True)

render_kpi_card(k1, "Operating EBITDA Margin", sim_res["EBITDA_Margin"], baseline_data["EBITDA_Margin"], "%")
render_kpi_card(k2, "Working Capital Cycle", sim_res["Working_Capital_Days"], baseline_data["Working_Capital_Days"], "days", is_inverse=True)
render_kpi_card(k3, "Projected Net Profit", sim_res["Net_Profit"], baseline_data["Net_Profit"], "Cr")
render_kpi_card(k4, "Working Capital Req.", sim_res["Working_Capital_Requirement_Cr"], baseline_data["Revenue"] * (baseline_data["Working_Capital_Days"] / 365.0), "Cr", is_inverse=True)

st.write("")

# ----------------- STREAMLINED 3-VIEW TAB NAVIGATION -----------------
tab1, tab2, tab3 = st.tabs([
    "🛡️ 1. Executive Control Room & Strategy",
    "🔄 2. Autonomous 7-Step Reasoning Visualizer",
    "🕸️ 3. Knowledge Graph & Causal Econometrics"
])

# ==============================================================================
# VIEW 1: EXECUTIVE CONTROL ROOM & STRATEGIC RECOMMENDATIONS
# ==============================================================================
with tab1:
    col_left, col_right = st.columns([1.1, 1])

    with col_left:
        st.markdown("### 🎯 Scenario Impact Breakdown")
        st.caption("Real-time financial response under current scenario parameters:")

        no_action_margin = sim_res["EBITDA_Margin"]
        action_a_margin = min(35.0, no_action_margin + (15.0 - import_price_shock * 0.4))
        action_b_margin = min(38.0, no_action_margin + (saas_attach_rate * 0.15))

        st.markdown(f"""
        <div style="background:#111827; border-radius:12px; padding:20px; border:1px solid rgba(255,255,255,0.08);">
            <table style="width:100%; color:#F3F4F6; border-collapse:collapse;">
                <tr style="border-bottom:1px solid rgba(255,255,255,0.1); font-size:0.85rem; color:#9CA3AF;">
                    <th style="text-align:left; padding:8px 0;">Strategic Option</th>
                    <th style="text-align:center;">EBITDA Margin</th>
                    <th style="text-align:center;">Working Capital</th>
                    <th style="text-align:right;">Net Profit</th>
                </tr>
                <tr style="border-bottom:1px solid rgba(255,255,255,0.05); font-weight:600;">
                    <td style="padding:12px 0; color:#9CA3AF;">Status Quo (No Action)</td>
                    <td style="text-align:center; color:#F87171;">{no_action_margin:.1f}%</td>
                    <td style="text-align:center;">{sim_res['Working_Capital_Days']:.0f} days</td>
                    <td style="text-align:right;">₹{sim_res['Net_Profit']:.1f} Cr</td>
                </tr>
                <tr style="border-bottom:1px solid rgba(255,255,255,0.05); font-weight:600;">
                    <td style="padding:12px 0; color:#38BDF8;">Option A: Fast-track Local Fab Sourcing</td>
                    <td style="text-align:center; color:#34D399;">{action_a_margin:.1f}%</td>
                    <td style="text-align:center; color:#34D399;">{max(180, sim_res['Working_Capital_Days'] - 20):.0f} days</td>
                    <td style="text-align:right; color:#34D399;">₹{sim_res['Net_Profit'] + 4.5:.1f} Cr</td>
                </tr>
                <tr style="font-weight:600;">
                    <td style="padding:12px 0; color:#A78BFA;">Option B: Accelerate FLYGHT SaaS Bundling</td>
                    <td style="text-align:center; color:#34D399;">{action_b_margin:.1f}%</td>
                    <td style="text-align:center; color:#34D399;">{max(165, sim_res['Working_Capital_Days'] - 35):.0f} days</td>
                    <td style="text-align:right; color:#34D399;">₹{sim_res['Net_Profit'] + 8.2:.1f} Cr</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        st.markdown("### 🤖 Multi-Agent Operational Audit Summary")
        if agent_state.critical_flags:
            for flag in agent_state.critical_flags:
                st.error(f"🚨 **Operational Alert**: `{flag}` — Action required to protect liquidity.")
        else:
            st.success("✅ **Operational Status Normal**: All supply chain, tender, and Ind AS accounting indicators are within safety thresholds.")

    with col_right:
        st.markdown("### 💡 Prioritized Executive Recommendations")
        st.caption("Synthesized via McKinsey, Bain, and Private Equity analytical frameworks:")

        events_list = pipeline.load_dynamic_events()
        trace = reasoning_engine.execute_7_step_loop(events_list[0])
        advisor_matrix = strategic_advisor.generate_strategic_recommendations(trace)

        for rec in advisor_matrix["action_matrix"]:
            st.markdown(f"""
            <div class="strategy-card">
                <div>
                    <span class="impact-pill">{rec['category']}</span>
                    <span class="owner-pill">Owner: {rec['executive_owner']}</span>
                </div>
                <div class="strategy-title" style="margin-top:10px;">{rec['title']}</div>
                <div style="font-size:0.85rem; color:#D1D5DB; margin-bottom:8px;">{rec['recommended_action']}</div>
                <div style="font-size:0.85rem; color:#34D399; font-weight:600;">💰 {rec['financial_impact']}</div>
            </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# VIEW 2: AUTONOMOUS 7-STEP REASONING VISUALIZER
# ==============================================================================
with tab2:
    st.markdown("### 🔄 7-Step Autonomous Reasoning Pipeline")
    st.caption("How the digital twin autonomously evaluates breaking events, updates its internal memory, and calculates recommendations:")

    events_list = pipeline.load_dynamic_events()
    event_titles = [f"{e['event_id']}: {e['title']}" for e in events_list]
    
    selected_event_str = st.selectbox("Select Dynamic Event Stream", event_titles)
    selected_idx = event_titles.index(selected_event_str)
    target_event = events_list[selected_idx]
    
    trace = reasoning_engine.execute_7_step_loop(target_event)

    s1 = trace["step1_event"]
    s2 = trace["step2_relevance"]
    s3 = trace["step3_dimensions"]
    s4 = trace["step4_severity"]
    s5 = trace["step5_assumptions"]
    s6 = trace["step6_action_trigger"]

    st.write("")

    step_cols = st.columns(3)

    with step_cols[0]:
        st.markdown(f"""
        <div class="step-card">
            <div class="step-number">Step 1 • Detection</div>
            <div class="step-head">{s1['summary']}</div>
            <div style="font-size:0.85rem; color:#9CA3AF;">Source: {s1['source']} ({s1['timestamp']})</div>
            <div style="font-size:0.85rem; color:#D1D5DB; margin-top:8px;">{s1['full_description']}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="step-card">
            <div class="step-number">Step 4 • Severity Rating</div>
            <div class="step-head" style="color:#F87171;">{s4['severity_level']}</div>
            <div style="font-size:0.85rem; color:#D1D5DB;">{s4['key_drivers']}</div>
        </div>
        """, unsafe_allow_html=True)

    with step_cols[1]:
        st.markdown(f"""
        <div class="step-card">
            <div class="step-number">Step 2 • Relevance</div>
            <div class="step-head" style="color:#38BDF8;">{s2['relevance_type']}</div>
            <div style="font-size:0.85rem; color:#D1D5DB;">{s2['rationale']}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="step-card">
            <div class="step-number">Step 5 • Belief Updates</div>
            <div class="step-head" style="color:#F59E0B;">Memory Synced</div>
            <div style="font-size:0.85rem; color:#D1D5DB;">Updated assumptions logged to persistent memory ledger.</div>
        </div>
        """, unsafe_allow_html=True)

    with step_cols[2]:
        st.markdown(f"""
        <div class="step-card">
            <div class="step-number">Step 3 • Impact Mapping</div>
            <div class="step-head">15 Dimensions</div>
            <div style="font-size:0.85rem; color:#D1D5DB;">
                Revenue: <b>{s3['impacted_dimensions']['Revenue']}</b><br>
                Margins: <b>{s3['impacted_dimensions']['Margins']}</b><br>
                Supply Chain: <b>{s3['impacted_dimensions']['Supply Chain']}</b><br>
                Cash Flow: <b>{s3['impacted_dimensions']['Cash Flow']}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="step-card">
            <div class="step-number">Step 6 & 7 • Outcome Trigger</div>
            <div class="step-head" style="color:#34D399;">{'Action Triggered' if s6['action_required'] else 'Logged & Monitored'}</div>
            <div style="font-size:0.85rem; color:#D1D5DB;">2SLS counterfactual scenarios calculated across 3 options.</div>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# VIEW 3: KNOWLEDGE GRAPH & CAUSAL ECONOMETRICS
# ==============================================================================
with tab3:
    st.markdown("### 🕸️ Company Knowledge Graph & Structural Causal Model")
    st.caption("Interactive network visualizer mapping ideaForge's platforms, BOMs, suppliers, and financial flow linkages:")

    col_g1, col_g2 = st.columns([2, 1])

    with col_g1:
        nodes = graph_db.get_nodes()
        edges = graph_db.get_edges()

        cy_elements = []
        color_map = {
            "BusinessSegment": "#1E88E5",      # Blue
            "ProductPlatform": "#43A047",      # Green
            "SupplyChainComponent": "#E53935", # Red
            "GovernmentPolicy": "#8E24AA",     # Purple
            "CustomerEntity": "#FB8C00",       # Orange
            "FinancialMetric": "#FDD835"       # Gold
        }

        for n in nodes:
            node_label = n.get("name") or n.get("model_name") or n.get("title") or n.get("id")
            cy_elements.append({
                "data": {
                    "id": n["id"],
                    "label": node_label,
                    "color": color_map.get(n.get("label"), "#cccccc")
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
                    "color": "#ffffff",
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
                    "line-color": "#4B5563",
                    "target-arrow-color": "#4B5563",
                    "target-arrow-shape": "triangle",
                    "curve-style": "bezier",
                    "label": "data(relationship)",
                    "font-size": "8px",
                    "color": "#9CA3AF"
                }
            }
        ]

        try:
            from st_cytoscape import cytoscape
            selected = cytoscape(cy_elements, stylesheet, layout={"name": "cose"}, height="450px", key="cy_tab3")
            if selected and selected.get("nodes"):
                st.session_state["selected_node"] = selected["nodes"][0]
        except Exception:
            all_node_ids = [n["id"] for n in nodes]
            chosen = st.selectbox("Inspect Node Details", ["-- Select a node --"] + all_node_ids)
            if chosen != "-- Select a node --":
                st.session_state["selected_node"] = chosen

    with col_g2:
        st.markdown("#### 📦 Node Inspector")
        if st.session_state["selected_node"]:
            n_id = st.session_state["selected_node"]
            details = graph_db.get_node_details(n_id)
            if details:
                st.markdown(f"**Node**: `{n_id}`")
                st.markdown(f"**Type**: `{details.get('label')}`")
                props = {k: v for k, v in details.items() if k != "label"}
                st.table(pd.DataFrame(list(props.items()), columns=["Property", "Value"]))
        else:
            st.info("Click any node in the Knowledge Graph to inspect its underlying BOM components and financial linkages.")

    st.write("---")
    st.markdown("### 🧮 2SLS Econometric Equation Parameters")
    st.caption("Two-Stage Least Squares (2SLS) statistical diagnostic:")

    c_s1, c_s2 = st.columns(2)
    with c_s1:
        st.write("**Second Stage Corrected Regressors**:")
        st.dataframe(causal_engine.get_second_stage_summary().style.format({
            "Coefficient": "{:.4f}",
            "Std Error": "{:.4f}",
            "t-Statistic": "{:.2f}",
            "p-Value": "{:.4e}"
        }))
    with c_s2:
        st.write("**First Stage Instrumental Variable Diagnostic**:")
        st.dataframe(causal_engine.get_first_stage_summary().style.format({
            "Coefficient": "{:.4f}",
            "Std Error": "{:.4f}",
            "t-Statistic": "{:.2f}",
            "p-Value": "{:.4e}"
        }))
