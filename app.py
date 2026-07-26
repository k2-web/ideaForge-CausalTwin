import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
import os
import json

# Import custom modules
from graph_db import IdeaForgeOntologyGraph
from data_ingestion import IdeaForgeIngestionPipeline
from causal_engine import IdeaForgeCausalEngine
from memory_engine import MemoryEngine
from reasoning_loop import StrategicReasoningEngine
from strategic_advisor import StrategicAdvisorEngine
from agents import IdeaForgeAgentOrchestrator

# 1. Page Configuration and Theme Injection
st.set_page_config(
    page_title="ideaForge Autonomous Financial Digital Twin",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom sleek dark CSS styling for executive command center
st.markdown("""
<style>
    /* Main layout styling */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    
    /* Header card styling */
    .metric-card {
        background-color: #1a1f2c;
        border: 1px solid #2d3748;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }
    
    .metric-title {
        font-size: 0.85rem;
        color: #a0aec0;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 5px;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 5px 0;
    }
    
    .metric-delta-pos {
        color: #48bb78;
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    .metric-delta-neg {
        color: #f56565;
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    /* Reasoning step cards */
    .reasoning-box {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 14px;
        margin-bottom: 12px;
    }
    .reasoning-step-title {
        font-weight: 700;
        color: #58a6ff;
        font-size: 1rem;
        margin-bottom: 6px;
    }
    
    /* Recommendation card */
    .rec-card {
        background-color: #1c2128;
        border-left: 4px solid #38d9a9;
        border-radius: 4px;
        padding: 15px;
        margin-bottom: 15px;
    }
    .rec-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #63e6be;
    }
    
    /* Agent speech bubbles */
    .agent-bubble {
        background-color: #1e2530;
        border-left: 4px solid #4299e1;
        border-radius: 4px;
        padding: 12px;
        margin-bottom: 12px;
    }
    .agent-header {
        font-weight: 700;
        font-size: 0.9rem;
        color: #63b3ed;
        margin-bottom: 4px;
    }
    .agent-body {
        font-size: 0.85rem;
        color: #e2e8f0;
        line-height: 1.4;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session States
if "selected_node" not in st.session_state:
    st.session_state["selected_node"] = None
if "focus_neighborhood" not in st.session_state:
    st.session_state["focus_neighborhood"] = False
if "current_event_idx" not in st.session_state:
    st.session_state["current_event_idx"] = 0

# Initialize backend objects
@st.cache_resource
def get_backend_objects():
    pipeline = IdeaForgeIngestionPipeline()
    graph_db = IdeaForgeOntologyGraph()
    financials_df = pipeline.load_quarterly_financials()
    causal_engine = IdeaForgeCausalEngine(financials_df)
    memory_engine = MemoryEngine()
    reasoning_engine = StrategicReasoningEngine(causal_engine, memory_engine)
    strategic_advisor = StrategicAdvisorEngine(causal_engine, memory_engine)
    orchestrator = IdeaForgeAgentOrchestrator(pipeline, causal_engine)
    return pipeline, graph_db, financials_df, causal_engine, memory_engine, reasoning_engine, strategic_advisor, orchestrator

pipeline, graph_db, financials_df, causal_engine, memory_engine, reasoning_engine, strategic_advisor, orchestrator = get_backend_objects()

# Baseline numbers (latest quarter: Q4 FY26)
baseline_data = financials_df.iloc[-1].to_dict()

# Sidebar: Global Digital Twin Controls
st.sidebar.image("https://img.icons8.com/nolan/96/drone.png", width=64)
st.sidebar.title("Autonomous Twin Controls")
st.sidebar.caption("Digital Operating System for Corporate Strategy")

# Slider 1: MoD Disbursement Lag
mod_lag = st.sidebar.slider(
    "MoD Disbursement Lag (Days)",
    min_value=15,
    max_value=180,
    value=int(baseline_data["MoD_Disbursement_Lag"]),
    step=5,
    help="Macro-economic instrumental variable representing lag in payment releases from Ministry of Defence."
)

# Slider 2: Import Payload Price Shock
import_price_shock = st.sidebar.slider(
    "Import Payload Cost Shock (%)",
    min_value=0,
    max_value=50,
    value=0,
    step=5,
    help="Simulates tariff hikes or supply chain restrictions on electro-optical/infrared payloads."
)

# Slider 3: FLYGHT SaaS Attach Rate
saas_attach_rate = st.sidebar.slider(
    "FLYGHT SaaS Attach Rate (%)",
    min_value=0,
    max_value=100,
    value=int(baseline_data["SaaS_Attach_Rate"] * 100),
    step=5,
    help="Attach rate of software platform (recurring cloud subscription) across defense/civil fleets."
)

# Slider 4: Indigenous Sourcing Mix
indigenous_mix = st.sidebar.slider(
    "Indigenous Sourcing Ratio (%)",
    min_value=30,
    max_value=90,
    value=int(baseline_data["Indigenous_Sourcing_Mix"] * 100),
    step=5,
    help="Level of local manufacturing and assembly sourcing, qualifying for PLI incentives and tenders."
)

scenario_config = {
    "mod_lag_days": mod_lag,
    "import_tariff_shock_pct": import_price_shock,
    "saas_attach_rate_pct": saas_attach_rate,
    "indigenous_mix": indigenous_mix / 100.0
}

# Run multi-agent workflow
agent_state = orchestrator.run_workflow(scenario_config)
sim_res = agent_state.simulated_results

# ----------------- MAIN TITLE & HEADER -----------------
st.title("⚡ ideaForge Technology Limited: Autonomous Financial Digital Twin")
st.markdown("**AI Operating System for Corporate Strategy** | Persistent Memory • 7-Step Causal Reasoning • 2SLS Econometrics • McKinsey/PE Advisory")

# KPI Summary Cards
kpi_cols = st.columns(4)

def render_kpi(col, title, val_fmt, baseline_val, simulated_val):
    diff = simulated_val - baseline_val
    delta_class = "metric-delta-pos" if diff >= 0 else "metric-delta-neg"
    sign = "+" if diff >= 0 else ""
    
    if val_fmt == "pct":
        val_str = f"{simulated_val:.2f}%"
        delta_str = f"{sign}{diff:.2f}%"
    elif val_fmt == "days":
        val_str = f"{simulated_val:.1f}"
        delta_str = f"{sign}{diff:.1f}"
    else: # currency
        val_str = f"₹{simulated_val:.2f} Cr"
        delta_str = f"{sign}₹{diff:.2f} Cr"

    if title == "Working Capital" and diff != 0:
        delta_class = "metric-delta-neg" if diff > 0 else "metric-delta-pos"

    col.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{val_str}</div>
        <div class="{delta_class}">{delta_str} vs baseline</div>
    </div>
    """, unsafe_allow_html=True)

render_kpi(kpi_cols[0], "EBITDA Margin", "pct", baseline_data["EBITDA_Margin"], sim_res["EBITDA_Margin"])
render_kpi(kpi_cols[1], "Working Capital", "days", baseline_data["Working_Capital_Days"], sim_res["Working_Capital_Days"])
render_kpi(kpi_cols[2], "Net Profit", "currency", baseline_data["Net_Profit"], sim_res["Net_Profit"])
render_kpi(kpi_cols[3], "Working Capital Req.", "currency", 
           baseline_data["Revenue"] * (baseline_data["Working_Capital_Days"] / 365.0), 
           sim_res["Working_Capital_Requirement_Cr"])

st.write("---")

# Navigation Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌐 1. Digital Twin Knowledge Graph",
    "🔄 2. 7-Step Strategic Reasoning Loop",
    "📊 3. 2SLS Econometric Causal Engine",
    "🧠 4. Strategic Recommendation Workbench",
    "📚 5. Persistent Memory & Briefing Archive"
])

# ==============================================================================
# TAB 1: KNOWLEDGE GRAPH ONTOLOGY
# ==============================================================================
with tab1:
    st.subheader("🕸️ Operational Knowledge Graph & Node Subgraph Inspector")
    st.caption("Bidirectional graph mapping ideaForge's business divisions, product platforms, supply chain nodes, and Ind AS financial metrics.")
    
    col_g1, col_g2 = st.columns([2, 1])
    
    with col_g1:
        if st.session_state["focus_neighborhood"]:
            if st.button("Clear Neighborhood Focus"):
                st.session_state["focus_neighborhood"] = False
                st.session_state["selected_node"] = None
                st.rerun()

        if st.session_state["focus_neighborhood"] and st.session_state["selected_node"]:
            neighborhood = graph_db.get_2_hop_neighborhood(st.session_state["selected_node"])
            nodes = neighborhood["nodes"]
            edges = neighborhood["edges"]
        else:
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
                    "class": n.get("label"),
                    "color": color_map.get(n.get("label"), "#cccccc")
                }
            })
            
        for e in edges:
            cy_elements.append({
                "data": {
                    "source": e["source"],
                    "target": e["target"],
                    "id": f"{e['source']}_{e['target']}",
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
                    "text-halign": "bottom",
                    "text-wrap": "wrap",
                    "text-max-width": "90px",
                    "border-width": "1px",
                    "border-color": "#ffffff"
                }
            },
            {
                "selector": "edge",
                "style": {
                    "width": "2px",
                    "line-color": "#4a5568",
                    "target-arrow-color": "#4a5568",
                    "target-arrow-shape": "triangle",
                    "curve-style": "bezier",
                    "label": "data(relationship)",
                    "font-size": "8px",
                    "color": "#a0aec0",
                    "text-rotation": "autorotate",
                    "text-margin-y": "-10px"
                }
            }
        ]
        layout = {"name": "cose", "nodeRepulsion": 8000, "idealEdgeLength": 100}

        try:
            from st_cytoscape import cytoscape
            selected = cytoscape(cy_elements, stylesheet, layout=layout, height="480px", selection_type="single", key="cy_graph_tab1")
            if selected and selected.get("nodes"):
                clicked = selected["nodes"][0]
                if clicked != st.session_state["selected_node"]:
                    st.session_state["selected_node"] = clicked
                    st.session_state["focus_neighborhood"] = True
                    st.rerun()
        except Exception:
            all_node_ids = [n["id"] for n in nodes]
            chosen = st.selectbox("Direct Node Inspector", ["-- Select a node to expand --"] + all_node_ids)
            if chosen != "-- Select a node to expand --" and chosen != st.session_state["selected_node"]:
                st.session_state["selected_node"] = chosen
                st.session_state["focus_neighborhood"] = True
                st.rerun()

    with col_g2:
        st.subheader("🔍 Node Inspector")
        if st.session_state["selected_node"]:
            node_id = st.session_state["selected_node"]
            details = graph_db.get_node_details(node_id)
            if details:
                st.markdown(f"### 📦 `{node_id}`")
                st.markdown(f"**Classification**: `{details.get('label')}`")
                props = {k: v for k, v in details.items() if k != "label"}
                st.table(pd.DataFrame(list(props.items()), columns=["Property", "Value"]))
        else:
            st.info("Click any node in the Cytoscape graph to inspect its underlying BOM, supply chain links, and financial dependencies.")

# ==============================================================================
# TAB 2: 7-STEP STRATEGIC REASONING LOOP
# ==============================================================================
with tab2:
    st.subheader("🔄 Autonomous 7-Step Strategic Reasoning Engine")
    st.caption("Select a dynamic breaking news event or inject a custom event to watch the twin execute its internal 7-step reasoning cycle.")

    events_list = pipeline.load_dynamic_events()
    event_options = [f"{e['event_id']}: {e['title']}" for e in events_list]
    
    col_r1, col_r2 = st.columns([2, 1])
    with col_r1:
        selected_event_str = st.selectbox("Select Ingested Event Feed", event_options)
        selected_idx = event_options.index(selected_event_str)
        target_event = events_list[selected_idx]
        
    with col_r2:
        st.write("")
        st.write("")
        if st.button("➕ Inject Custom Breaking Event"):
            with st.form("custom_event_form"):
                st.write("Inject Custom Operational/Macro Shock")
                c_title = st.text_input("Event Title", "Middle East Air Cargo Embargo Pushes EO/IR Sensor Lead Time to 180 Days")
                c_cat = st.selectbox("Category", ["Supply Chain & Logistics", "Macroeconomic & Interest Rates", "Government Policy & Defense Finance", "Competitor Activity"])
                c_desc = st.text_area("Description", "Regional escalation closes primary air freight routes from Tel Aviv, stalling optical payload imports for SWITCH UAV build.")
                c_mod = st.number_input("MoD Disbursement Lag (Days)", 15, 180, 75)
                c_tariff = st.number_input("Import Tariff Cost Shock (%)", 0, 100, 25)
                c_saas = st.number_input("SaaS Attach Rate (%)", 0, 100, 35)
                submit_custom = st.form_submit_button("Inject Event to Digital Twin")
                if submit_custom:
                    new_e = pipeline.inject_custom_event(c_title, c_cat, c_desc, {
                        "mod_lag_days": c_mod,
                        "import_tariff_shock_pct": c_tariff,
                        "saas_attach_rate_pct": c_saas
                    })
                    st.success(f"Injected custom event `{new_e['event_id']}`!")
                    st.rerun()

    # Execute 7-Step Reasoning Loop
    reasoning_trace = reasoning_engine.execute_7_step_loop(target_event)

    st.write("---")
    st.markdown(f"### ⚙️ Executive Reasoning Trace for Event: `{target_event['event_id']}`")

    # Render Steps 1 to 7
    s1 = reasoning_trace["step1_event"]
    s2 = reasoning_trace["step2_relevance"]
    s3 = reasoning_trace["step3_dimensions"]
    s4 = reasoning_trace["step4_severity"]
    s5 = reasoning_trace["step5_assumptions"]
    s6 = reasoning_trace["step6_action_trigger"]
    s7 = reasoning_trace["step7_simulations"]

    r_col1, r_col2 = st.columns(2)

    with r_col1:
        st.markdown(f"""
        <div class="reasoning-box">
            <div class="reasoning-step-title">{s1['step']}</div>
            <b>Q: {s1['question']}</b><br>
            <b>Summary</b>: {s1['summary']}<br>
            <b>Source</b>: {s1['source']} ({s1['timestamp']})<br>
            <i>{s1['full_description']}</i>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="reasoning-box">
            <div class="reasoning-step-title">{s2['step']}</div>
            <b>Q: {s2['question']}</b><br>
            <b>Relevance Rating</b>: <span style="color:#58a6ff; font-weight:bold;">{s2['relevance_type']}</span><br>
            <b>Rationale</b>: {s2['rationale']}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="reasoning-box">
            <div class="reasoning-step-title">{s4['step']}</div>
            <b>Q: {s4['question']}</b><br>
            <b>Severity Level</b>: <span style="color:#f56565; font-weight:bold;">{s4['severity_level']}</span><br>
            <b>Key Drivers</b>: {s4['key_drivers']}
        </div>
        """, unsafe_allow_html=True)

    with r_col2:
        st.markdown(f"""
        <div class="reasoning-box">
            <div class="reasoning-step-title">{s5['step']}</div>
            <b>Q: {s5['question']}</b><br>
            <b>Belief Ledger Revisions</b>: {json.dumps(s5['invalidated_beliefs'], indent=2)}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="reasoning-box">
            <div class="reasoning-step-title">{s6['step']}</div>
            <b>Q: {s6['question']}</b><br>
            <b>Action Required?</b>: <span style="color:{'#48bb78' if s6['action_required'] else '#a0aec0'}; font-weight:bold;">{'YES - EXECUTE STRATEGY' if s6['action_required'] else 'NO - STORE & MONITOR'}</span><br>
            <b>Rationale</b>: {s6['decision_rationale']}
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="reasoning-box">
        <div class="reasoning-step-title">{s3['step']}</div>
        <b>Q: {s3['question']}</b><br>
    </div>
    """, unsafe_allow_html=True)
    st.json(s3['impacted_dimensions'])

    st.markdown(f"""
    <div class="reasoning-box">
        <div class="reasoning-step-title">{s7['step']}</div>
        <b>Q: {s7['question']}</b>
    </div>
    """, unsafe_allow_html=True)
    
    sim_table_data = []
    for k, v in s7["simulations"].items():
        sim_table_data.append({
            "Option Name": v["title"],
            "Probability": v["probability"],
            "EBITDA Margin (%)": v["ebitda_margin_pct"],
            "Working Capital (Days)": v["working_capital_days"],
            "Net Profit (₹ Cr)": v["net_profit_cr"],
            "Working Capital Req (₹ Cr)": v["working_capital_req_cr"]
        })
    st.table(pd.DataFrame(sim_table_data))

# ==============================================================================
# TAB 3: 2SLS ECONOMETRIC CAUSAL TWIN
# ==============================================================================
with tab3:
    st.subheader("📊 Two-Stage Least Squares (2SLS) Econometric Causal Model")
    st.markdown("Isolates true operating drivers of EBITDA margin volatility under MoD budget disbursement lags:")
    
    st.latex(r"\text{1st Stage: } \text{Working Capital Days} = \gamma_0 + \gamma_1 (\text{MoD Disbursement Lag}) + \mathbf{W}\boldsymbol{\Gamma} + v")
    st.latex(r"\text{2nd Stage: } \text{EBITDA Margin} = \beta_0 + \beta_1 (\widehat{\text{Working Capital Days}}) + \mathbf{W}\boldsymbol{\mathbf{B}} + \varepsilon")
    
    c_m1, c_m2 = st.columns(2)
    with c_m1:
        st.write("**Second Stage Corrected Outcome Regressors**:")
        st.dataframe(causal_engine.get_second_stage_summary().style.format({
            "Coefficient": "{:.5f}",
            "Std Error": "{:.5f}",
            "t-Statistic": "{:.3f}",
            "p-Value": "{:.5e}"
        }))
    with c_m2:
        st.write("**First Stage Instrument Diagnostic**:")
        st.dataframe(causal_engine.get_first_stage_summary().style.format({
            "Coefficient": "{:.4f}",
            "Std Error": "{:.4f}",
            "t-Statistic": "{:.3f}",
            "p-Value": "{:.5e}"
        }))

# ==============================================================================
# TAB 4: STRATEGIC RECOMMENDATION WORKBENCH
# ==============================================================================
with tab4:
    st.subheader("🧠 McKinsey / Bain / PE Executive Recommendation Workbench")
    st.caption("Top-tier management consulting and private equity counter-strategies synthesized for the current digital twin state.")

    advisor_matrix = strategic_advisor.generate_strategic_recommendations(reasoning_trace)

    st.info(f"💡 **Primary Recommended Strategy**: {advisor_matrix['recommended_primary_action']}")

    for rec in advisor_matrix["action_matrix"]:
        st.markdown(f"""
        <div class="rec-card">
            <div class="rec-title">[{rec['framework']}] {rec['title']}</div>
            <p style="margin: 4px 0;"><b>Category</b>: {rec['category']} | <b>Owner</b>: {rec['executive_owner']} | <b>Timeline</b>: {rec['timeline']}</p>
            <p><b>Problem</b>: {rec['problem_statement']}</p>
            <p><b>Recommended Action</b>: {rec['recommended_action']}</p>
            <p style="color:#38d9a9; font-weight:bold;">💰 Financial Impact: {rec['financial_impact']}</p>
            <p style="color:#ffa8a8;">⚠️ Risk & Mitigant: {rec['risk_rating']} — {rec['mitigant']}</p>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# TAB 5: PERSISTENT MEMORY & BRIEFING ARCHIVE
# ==============================================================================
with tab5:
    st.subheader("📚 Persistent Memory & Executive Briefing Archive")
    st.caption("Auditable ledger of historical assumptions, belief revisions, past decision lessons, and proactive daily executive briefings.")

    m_col1, m_col2 = st.columns(2)

    with m_col1:
        st.markdown("### 📜 Belief Revision Ledger")
        beliefs = memory_engine.get_belief_history()
        st.dataframe(pd.DataFrame(beliefs))

        st.markdown("### 🎯 Decision & Forecast History")
        decisions = memory_engine.get_decision_history()
        st.dataframe(pd.DataFrame(decisions))

    with m_col2:
        st.markdown("### 📋 Proactive Daily Executive Briefings")
        briefings = memory_engine.get_all_executive_briefings()
        if briefings:
            for b in briefings:
                with st.expander(f"Briefing Date: {b['date']}"):
                    st.markdown(b["briefing_text"])
        else:
            st.info("No saved briefings found. Run `python3 daily_briefing_job.py` in your terminal to generate automated daily briefings!")
