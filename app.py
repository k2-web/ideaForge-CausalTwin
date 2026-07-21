import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
import os

# Import custom modules
from graph_db import IdeaForgeOntologyGraph
from data_ingestion import IdeaForgeIngestionPipeline
from causal_engine import IdeaForgeCausalEngine
from agents import IdeaForgeAgentOrchestrator

# 1. Page Configuration and Theme Injection
st.set_page_config(
    page_title="ideaForge Causal Twin",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom sleek dark CSS styling for premium look
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
if "simulation_run" not in st.session_state:
    st.session_state["simulation_run"] = False

# Initialize pipeline, graph database, and causal engine
@st.cache_resource
def get_backend_objects():
    pipeline = IdeaForgeIngestionPipeline()
    graph_db = IdeaForgeOntologyGraph()
    financials_df = pipeline.load_quarterly_financials()
    causal_engine = IdeaForgeCausalEngine(financials_df)
    orchestrator = IdeaForgeAgentOrchestrator(pipeline, causal_engine)
    return pipeline, graph_db, financials_df, causal_engine, orchestrator

pipeline, graph_db, financials_df, causal_engine, orchestrator = get_backend_objects()

# Baseline numbers (latest quarter: Q4 FY26)
baseline_data = financials_df.iloc[-1].to_dict()

# Sidebar: Controls
st.sidebar.image("https://img.icons8.com/nolan/96/drone.png", width=64)
st.sidebar.title("Causal Twin Controls")
st.sidebar.write("Simulate operational interventions below:")

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

# Slider 4: Indigenous Sourcing Mix (displays current compliance level)
indigenous_mix = st.sidebar.slider(
    "Indigenous Sourcing Ratio (%)",
    min_value=30,
    max_value=90,
    value=int(baseline_data["Indigenous_Sourcing_Mix"] * 100),
    step=5,
    help="Level of local manufacturing and assembly sourcing, qualifying for PLI incentives and tenders."
)

# Run button
run_simulation = st.sidebar.button("RUN COUNTERFACTUAL SIMULATION", type="primary", use_container_width=True)

# Generate current config
scenario_config = {
    "mod_lag_days": mod_lag,
    "import_tariff_shock_pct": import_price_shock,
    "saas_attach_rate_pct": saas_attach_rate,
    "indigenous_mix": indigenous_mix / 100.0
}

# Run agents workflow
agent_state = orchestrator.run_workflow(scenario_config)
sim_res = agent_state.simulated_results

# ----------------- MAIN PANEL -----------------
st.title("⚡ ideaForge Technology Limited: Enterprise Causal Digital Twin")
st.markdown("Mathematical simulation and multi-agent audit of India's leading UAS manufacturer under supply shocks and defense disbursement delays.")

# Row 1: KPI Metrics
kpi_cols = st.columns(4)

def render_kpi(col, title, val_fmt, baseline_val, simulated_val, unit=""):
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

    # Flip color logic for working capital days (less is better)
    if title == "Working Capital" and diff != 0:
        delta_class = "metric-delta-neg" if diff > 0 else "metric-delta-pos"

    col.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{val_str}</div>
        <div class="{delta_class}">{delta_str} vs baseline</div>
    </div>
    """, unsafe_allow_html=True)

# Fill KPI row
render_kpi(kpi_cols[0], "EBITDA Margin", "pct", baseline_data["EBITDA_Margin"], sim_res["EBITDA_Margin"])
render_kpi(kpi_cols[1], "Working Capital", "days", baseline_data["Working_Capital_Days"], sim_res["Working_Capital_Days"])
render_kpi(kpi_cols[2], "Net Profit", "currency", baseline_data["Net_Profit"], sim_res["Net_Profit"])
render_kpi(kpi_cols[3], "Working Capital Req.", "currency", 
           baseline_data["Revenue"] * (baseline_data["Working_Capital_Days"] / 365.0), 
           sim_res["Working_Capital_Requirement_Cr"])

st.write("---")

# Row 2: Graph Visualization & Node Details
left_graph_col, right_details_col = st.columns([2, 1])

with left_graph_col:
    st.subheader("🕸️ Operational Directed Acyclic Graph (DAG) Ontology")
    st.caption("Bidirectional graph mapping ideaForge's business divisions, product units, supply chain links, and Ind AS financial flow dependencies.")
    
    # Reset Graph View button
    if st.session_state["focus_neighborhood"]:
        if st.button("Clear Neighborhood Focus"):
            st.session_state["focus_neighborhood"] = False
            st.session_state["selected_node"] = None
            st.rerun()

    # Query graph nodes and edges
    if st.session_state["focus_neighborhood"] and st.session_state["selected_node"]:
        neighborhood = graph_db.get_2_hop_neighborhood(st.session_state["selected_node"])
        nodes = neighborhood["nodes"]
        edges = neighborhood["edges"]
    else:
        nodes = graph_db.get_nodes()
        edges = graph_db.get_edges()

    # Format nodes & edges for Cytoscape.js
    cy_elements = []
    
    # Define colors for different node classes
    color_map = {
        "BusinessSegment": "#1E88E5",      # Blue
        "ProductPlatform": "#43A047",      # Green
        "SupplyChainComponent": "#E53935", # Red
        "GovernmentPolicy": "#8E24AA",     # Purple
        "CustomerEntity": "#FB8C00",       # Orange
        "FinancialMetric": "#FDD835"       # Gold/Yellow
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

    # Style sheet for st-cytoscape
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
        },
        {
            "selector": ":selected",
            "style": {
                "border-width": "3px",
                "border-color": "#63b3ed",
                "width": "42px",
                "height": "42px"
            }
        }
    ]

    layout = {"name": "cose", "nodeRepulsion": 8000, "idealEdgeLength": 100}

    # Render Cytoscape Graph with fallback handling
    try:
        from st_cytoscape import cytoscape
        selected = cytoscape(
            cy_elements,
            stylesheet,
            layout=layout,
            height="480px",
            selection_type="single",
            key="cy_graph"
        )
        
        # Intercept selections
        if selected and selected.get("nodes"):
            clicked = selected["nodes"][0]
            if clicked != st.session_state["selected_node"]:
                st.session_state["selected_node"] = clicked
                st.session_state["focus_neighborhood"] = True
                st.rerun()
    except Exception as e:
        # Fallback iframe using direct HTML injection in case of libraries issue
        st.error(f"Render failed: {e}. Injecting embedded Cytoscape visualizer.")
        st.info("Interactive nodes are supported in pure HTML mode below.")
        
        # Simple list select fallback for node focus since iframe doesn't bubble up events natively
        all_node_ids = [n["id"] for n in nodes]
        chosen = st.selectbox("Direct Node Inspector", ["-- Select a node to expand --"] + all_node_ids)
        if chosen != "-- Select a node to expand --" and chosen != st.session_state["selected_node"]:
            st.session_state["selected_node"] = chosen
            st.session_state["focus_neighborhood"] = True
            st.rerun()

with right_details_col:
    st.subheader("🔍 Node Properties & 2-Hop Details")
    if st.session_state["selected_node"]:
        node_id = st.session_state["selected_node"]
        details = graph_db.get_node_details(node_id)
        
        if details:
            st.markdown(f"### 📦 `{node_id}`")
            st.markdown(f"**Classification**: `{details.get('label')}`")
            
            # Format properties into a readable table
            props = {k: v for k, v in details.items() if k != "label"}
            st.table(pd.DataFrame(list(props.items()), columns=["Property", "Value"]))
            
            # Show neighbors
            adj_nodes = list(graph_db.graph.neighbors(node_id))
            pre_nodes = list(graph_db.graph.predecessors(node_id))
            
            if adj_nodes:
                st.markdown("**Downstream Outflows:**")
                for n in adj_nodes:
                    st.markdown(f"- `{n}` via `[{graph_db.graph[node_id][n]['relationship']}]`")
            if pre_nodes:
                st.markdown("**Upstream Inflows:**")
                for n in pre_nodes:
                    st.markdown(f"- `{n}` via `[{graph_db.graph[n][node_id]['relationship']}]`")
        else:
            st.write("No details found.")
    else:
        st.info("Click a node in the network graph above to inspect its BOM, supply constraints, and financial flows.")

st.write("---")

# Row 3: Econometric Modeling Detail & Agent Reports
left_math_col, right_agent_col = st.columns([1, 1])

with left_math_col:
    st.subheader("📊 2SLS Causal Equations & Model Statistics")
    st.markdown("Standard observational models suffer from backdoor confounding due to macroeconomic and funding cycles. We resolve this by using a **Two-Stage Least Squares (2SLS)** structure:")
    
    st.latex(r"""
    \text{1st Stage: } \text{Working Capital Days} = \gamma_0 + \gamma_1 (\text{MoD Disbursement Lag}) + \mathbf{W}\boldsymbol{\Gamma} + v
    """)
    st.latex(r"""
    \text{2nd Stage: } \text{EBITDA Margin} = \beta_0 + \beta_1 (\widehat{\text{Working Capital Days}}) + \mathbf{W}\boldsymbol{\mathbf{B}} + \varepsilon
    """)
    
    st.write("**Second Stage Corrected Regressor Parameters**:")
    stage2_df = causal_engine.get_second_stage_summary()
    st.dataframe(stage2_df.style.format({
        "Coefficient": "{:.5f}",
        "Std Error": "{:.5f}",
        "t-Statistic": "{:.3f}",
        "p-Value": "{:.5e}"
    }))
    
    st.write("**First Stage Instrument Diagnostic**:")
    stage1_df = causal_engine.get_first_stage_summary()
    st.dataframe(stage1_df.style.format({
        "Coefficient": "{:.4f}",
        "Std Error": "{:.4f}",
        "t-Statistic": "{:.3f}",
        "p-Value": "{:.5e}"
    }))
    
    st.caption("Note: Working Capital Days is highly endogenous. Using MoD Disbursement Lag as an IV satisfies exclusion restrictions, isolating true operational performance drivers.")

with right_agent_col:
    st.subheader("🤖 LangGraph Analytical Debate Transcript")
    st.caption("Four autonomous agent instances auditing this scenario's structural validity and checking for Indian Accounting Standards compliance:")
    
    # 1. Defense Procurement
    st.markdown(f"""
    <div class="agent-bubble">
        <div class="agent-header">🪖 Defense Procurement Agent</div>
        <div class="agent-body">
            {"<br>".join(agent_state.agent_logs["DefenseProcurement"])}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. Supply Chain Risk
    st.markdown(f"""
    <div class="agent-bubble">
        <div class="agent-header">⚙️ Supply Chain Risk Agent</div>
        <div class="agent-body">
            {"<br>".join(agent_state.agent_logs["SupplyChainRisk"])}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 3. Quality of Earnings (QofE)
    st.markdown(f"""
    <div class="agent-bubble">
        <div class="agent-header">🔍 QofE Accounting Agent (Ind AS Compliance)</div>
        <div class="agent-body">
            {"<br>".join(agent_state.agent_logs["QofEAccounting"])}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 4. Causal Simulation
    st.markdown(f"""
    <div class="agent-bubble" style="border-left-color: #48bb78;">
        <div class="agent-header">📈 Causal Simulation Agent</div>
        <div class="agent-body">
            {"<br>".join(agent_state.agent_logs["CausalSimulation"])}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Critical flags banner
    if agent_state.critical_flags:
        st.error(f"🚨 **Critical Operational Flags Triggered**: {', '.join(agent_state.critical_flags)}")
    else:
        st.success("✅ **All Operational Thresholds Within Normal Tolerances**")
