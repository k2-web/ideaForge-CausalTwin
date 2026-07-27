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
    page_title="ideaForge Digital Twin | Executive Cockpit",
    page_icon="🚁",
    layout="wide",
    initial_sidebar_state="collapsed" # Hide clutter sidebar by default
)

# 2. Modern Glassmorphism CSS & Clean UI Tokens
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background-color: #090D16;
        color: #F1F5F9;
    }

    /* Main Container Padding */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Top Executive Header */
    .exec-header {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.7) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 20px 28px;
        margin-bottom: 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .status-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        background-color: #10B981;
        border-radius: 50%;
        margin-right: 6px;
        box-shadow: 0 0 8px #10B981;
    }

    .status-badge {
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    /* Metric Cards */
    .metric-card-clean {
        background: #0F172A;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 20px;
        transition: all 0.2s ease-in-out;
    }

    .metric-card-clean:hover {
        border-color: #3B82F6;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.15);
    }

    .metric-title {
        color: #94A3B8;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #F8FAFC;
        margin: 6px 0;
    }

    .metric-sub-pos {
        color: #34D399;
        font-size: 0.82rem;
        font-weight: 600;
    }

    .metric-sub-neg {
        color: #F43F5E;
        font-size: 0.82rem;
        font-weight: 600;
    }

    /* Product Cards */
    .product-card-ui {
        background: #0F172A;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 20px;
        height: 100%;
    }

    .product-badge-blue {
        background: rgba(59, 130, 246, 0.15);
        color: #60A5FA;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
    }

    .product-badge-green {
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
    }

    /* Scenario Control Panel */
    .control-box {
        background: #0F172A;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
    }

    /* Action Recommendation Card */
    .action-card-ui {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.8) 100%);
        border-left: 4px solid #10B981;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)

# Session State Setup
if "selected_product" not in st.session_state:
    st.session_state["selected_product"] = "SWITCH_UAV"
if "selected_node" not in st.session_state:
    st.session_state["selected_node"] = None
if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "Overview"

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

# ----------------- TOP EXECUTIVE HEADER -----------------
st.markdown("""
<div class="exec-header">
    <div>
        <div style="font-size: 1.5rem; font-weight: 800; color: #FFFFFF;">ideaForge Technology Limited</div>
        <div style="font-size: 0.9rem; color: #94A3B8;">Live Enterprise Digital Twin • Dual-Use Defense & Civil UAS</div>
    </div>
    <div>
        <span class="status-badge"><span class="status-dot"></span>DIGITAL TWIN LIVE & SYNCED</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------- INTERACTIVE CONTROL PANEL ON MAIN PAGE -----------------
with st.container():
    st.markdown("""
    <div class="control-box">
        <div style="font-size: 1.1rem; font-weight: 700; color: #F8FAFC; margin-bottom: 4px;">
            🎛️ Simulation Studio — Test Real-World Shocks
        </div>
        <div style="font-size: 0.85rem; color: #94A3B8; margin-bottom: 16px;">
            Move the sliders below to simulate how government payment delays and component import tariffs change ideaForge's profit margins and cash flow.
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        mod_lag = st.slider(
            "⏳ Government Invoice Clearance Time",
            min_value=15, max_value=180, value=int(baseline_data["MoD_Disbursement_Lag"]), step=5,
            help="Days taken by the Ministry of Defence to pay milestone bills."
        )

    with c2:
        import_price_shock = st.slider(
            "📷 Imported Camera / Tariff Price Shock",
            min_value=0, max_value=50, value=0, step=5,
            help="Import cost surge on Israeli EO/IR sensors & Taiwanese chips."
        )

    with c3:
        saas_attach_rate = st.slider(
            "💻 FLYGHT Software Adoption Rate",
            min_value=0, max_value=100, value=int(baseline_data["SaaS_Attach_Rate"] * 100), step=5,
            help="Percentage of drone clients subscribing to cloud mapping software."
        )

scenario_config = {
    "mod_lag_days": mod_lag,
    "import_tariff_shock_pct": import_price_shock,
    "saas_attach_rate_pct": saas_attach_rate,
    "indigenous_mix": 0.60
}

# Run 2SLS Causal & Agent calculation
agent_state = orchestrator.run_workflow(scenario_config)
sim_res = agent_state.simulated_results

st.write("")

# ----------------- LIVE METRIC CARDS -----------------
m1, m2, m3, m4 = st.columns(4)

def render_metric_card(col, label, val_str, delta_str, is_good=True):
    sub_class = "metric-sub-pos" if is_good else "metric-sub-neg"
    col.markdown(f"""
    <div class="metric-card-clean">
        <div class="metric-title">{label}</div>
        <div class="metric-value">{val_str}</div>
        <div class="{sub_class}">{delta_str}</div>
    </div>
    """, unsafe_allow_html=True)

ebitda_diff = sim_res["EBITDA_Margin"] - baseline_data["EBITDA_Margin"]
wc_diff = sim_res["Working_Capital_Days"] - baseline_data["Working_Capital_Days"]
profit_diff = sim_res["Net_Profit"] - baseline_data["Net_Profit"]
req_diff = sim_res["Working_Capital_Requirement_Cr"] - (baseline_data["Revenue"] * (baseline_data["Working_Capital_Days"] / 365.0))

render_metric_card(m1, "Operating EBITDA Margin", f"{sim_res['EBITDA_Margin']:.1f}%", f"{'+' if ebitda_diff>=0 else ''}{ebitda_diff:.1f}% vs baseline", is_good=ebitda_diff>=0)
render_metric_card(m2, "Cash Flow Collection Time", f"{sim_res['Working_Capital_Days']:.0f} Days", f"{'+' if wc_diff>=0 else ''}{wc_diff:.0f}d vs baseline", is_good=wc_diff<=0)
render_metric_card(m3, "Projected Net Profit", f"₹{sim_res['Net_Profit']:.1f} Cr", f"{'+' if profit_diff>=0 else ''}₹{profit_diff:.1f} Cr vs base", is_good=profit_diff>=0)
render_metric_card(m4, "Required Working Capital", f"₹{sim_res['Working_Capital_Requirement_Cr']:.1f} Cr", f"{'+' if req_diff>=0 else ''}₹{req_diff:.1f} Cr vs base", is_good=req_diff<=0)

st.write("---")

# ----------------- MAIN INTERACTIVE TAB NAVIGATION -----------------
nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)

with nav_col1:
    if st.button("💬 Ask Digital Twin", use_container_width=True, type="primary" if st.session_state["active_tab"] == "Ask" else "secondary"):
        st.session_state["active_tab"] = "Ask"
        st.rerun()

with nav_col2:
    if st.button("🚁 Products & BOM Explorer", use_container_width=True, type="primary" if st.session_state["active_tab"] == "Products" else "secondary"):
        st.session_state["active_tab"] = "Products"
        st.rerun()

with nav_col3:
    if st.button("💡 Strategic Recommendations", use_container_width=True, type="primary" if st.session_state["active_tab"] == "Strategy" else "secondary"):
        st.session_state["active_tab"] = "Strategy"
        st.rerun()

with nav_col4:
    if st.button("🕸️ Value Chain Network Map", use_container_width=True, type="primary" if st.session_state["active_tab"] == "Map" else "secondary"):
        st.session_state["active_tab"] = "Map"
        st.rerun()

st.write("")

# ----------------- TAB 1: ASK DIGITAL TWIN -----------------
if st.session_state["active_tab"] in ["Overview", "Ask"]:
    st.markdown("### 💬 Ask ideaForge Anything")
    st.caption("Type any question about ideaForge's business, customers, products, or financial risks:")

    q_col1, q_col2, q_col3, q_col4 = st.columns(4)
    asked_q = None
    if q_col1.button("❓ What does ideaForge build?"): asked_q = "What does ideaForge build?"
    if q_col2.button("💰 How does ideaForge make money?"): asked_q = "How does ideaForge make money?"
    if q_col3.button("⚠️ What is the biggest risk?"): asked_q = "What is the biggest risk?"
    if q_col4.button("🚀 What is FLYGHT software?"): asked_q = "What is FLYGHT software?"

    custom_q = st.text_input("Type your own question:", placeholder="e.g. Who are their main customers? What is SWITCH UAV?")
    if custom_q: asked_q = custom_q

    if asked_q:
        q_lower = asked_q.lower()
        if "build" in q_lower or "product" in q_lower:
            ans = ("**ideaForge builds dual-use unmanned aircraft systems (drones):**\n\n"
                   "1. **SWITCH VTOL UAV**: Fixed-wing + VTOL drone used by the Indian Army for high-altitude surveillance.\n"
                   "2. **NETRA V4**: Compact quadcopter used by police & paramilitary for law enforcement.\n"
                   "3. **Q6 UAV**: Heavy-payload drone for land mapping under the SVAMITVA scheme.\n"
                   "4. **FLYGHT Platform**: Cloud software for live drone fleet tracking and map analytics.")
        elif "money" in q_lower or "revenue" in q_lower:
            ans = (f"**ideaForge revenue mix:**\n\n"
                   f"- **Defense ISR (65%)**: Contracts from Indian Army & Ministry of Home Affairs.\n"
                   f"- **Civil Mapping (20%)**: Government tenders (Survey of India).\n"
                   f"- **FLYGHT SaaS (10%)**: Recurring annual software subscriptions.\n"
                   f"- **Current Operating Margin**: {sim_res['EBITDA_Margin']:.1f}%.")
        elif "risk" in q_lower or "tariff" in q_lower:
            ans = (f"**Key Operational Risks:**\n\n"
                   f"1. **Government Payment Delays**: Clearance takes ~60–90 days, tying up ₹{sim_res['Working_Capital_Requirement_Cr']:.1f} Cr in capital.\n"
                   f"2. **Import Dependencies**: High-tech cameras imported from Israel/US face tariff risks.")
        else:
            ans = f"ideaForge is India's leading drone maker. Current simulated EBITDA margin is {sim_res['EBITDA_Margin']:.1f}% with working capital cycle of {sim_res['Working_Capital_Days']:.0f} days."

        st.info(f"🤖 **Digital Twin Answer**: {ans}")

# ----------------- TAB 2: PRODUCTS & BOM EXPLORER -----------------
elif st.session_state["active_tab"] == "Products":
    st.markdown("### 🚁 Product Platforms & Bill of Materials")
    st.caption("Click a drone platform to inspect its cost structure and target customers:")

    p1, p2, p3, p4 = st.columns(4)

    with p1:
        st.markdown("""
        <div class="product-card-ui">
            <span class="product-badge-green">65% Revenue</span>
            <div style="font-size:1.2rem; font-weight:700; color:#F8FAFC; margin-top:10px;">SWITCH VTOL UAV</div>
            <div style="font-size:0.85rem; color:#94A3B8; margin-top:4px;">Indian Army Border Surveillance</div>
            <div style="font-size:0.85rem; color:#38BDF8; font-weight:600; margin-top:10px;">Price: ₹25 Lakhs / unit</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Inspect SWITCH UAV", use_container_width=True): st.session_state["selected_product"] = "SWITCH_UAV"

    with p2:
        st.markdown("""
        <div class="product-card-ui">
            <span class="product-badge-blue">15% Revenue</span>
            <div style="font-size:1.2rem; font-weight:700; color:#F8FAFC; margin-top:10px;">NETRA V4 Quadcopter</div>
            <div style="font-size:0.85rem; color:#94A3B8; margin-top:4px;">Police & Paramilitary Patrol</div>
            <div style="font-size:0.85rem; color:#38BDF8; font-weight:600; margin-top:10px;">Price: ₹12 Lakhs / unit</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Inspect NETRA V4", use_container_width=True): st.session_state["selected_product"] = "NETRA_V4"

    with p3:
        st.markdown("""
        <div class="product-card-ui">
            <span class="product-badge-blue">10% Revenue</span>
            <div style="font-size:1.2rem; font-weight:700; color:#F8FAFC; margin-top:10px;">Q6 Heavy Payload</div>
            <div style="font-size:0.85rem; color:#94A3B8; margin-top:4px;">SVAMITVA Rural Land Mapping</div>
            <div style="font-size:0.85rem; color:#38BDF8; font-weight:600; margin-top:10px;">Price: ₹35 Lakhs / unit</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Inspect Q6 UAV", use_container_width=True): st.session_state["selected_product"] = "Q6_UAV"

    with p4:
        st.markdown("""
        <div class="product-card-ui">
            <span class="product-badge-green">High Growth</span>
            <div style="font-size:1.2rem; font-weight:700; color:#F8FAFC; margin-top:10px;">FLYGHT SaaS Software</div>
            <div style="font-size:0.85rem; color:#94A3B8; margin-top:4px;">Cloud Analytics & Fleet Stream</div>
            <div style="font-size:0.85rem; color:#38BDF8; font-weight:600; margin-top:10px;">ARR: ₹1.5 Lakh / drone / yr</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Inspect FLYGHT SaaS", use_container_width=True): st.session_state["selected_product"] = "FLYGHT_Patrol"

    st.write("")
    prod_id = st.session_state["selected_product"]
    st.markdown(f"#### 🔍 Detailed Component Cost Breakdown: `{prod_id}`")

    b1, b2 = st.columns(2)
    with b1:
        st.markdown("**Component Bill of Materials (BOM):**")
        if prod_id == "SWITCH_UAV":
            st.markdown("- 📷 **EO/IR Optical Payload Camera** (Elbit Systems, Israel) — **₹8.0 Lakhs**")
            st.markdown("- 🧭 **Autopilot Microcontroller Board** (Taiwan) — **₹2.0 Lakhs**")
            st.markdown("- ✈️ **Carbon Fiber Frame** (Japan) — **₹1.5 Lakhs**")
            st.markdown("- 🔋 **LiPo Battery Pack** (India Assembly) — **₹0.8 Lakhs**")
        else:
            st.markdown("- 📷 **Thermal Camera Sensor** — **₹4.5 Lakhs**")
            st.markdown("- 🧭 **Autopilot Board** — **₹1.5 Lakhs**")
            st.markdown("- 🔋 **Battery Pack** — **₹0.6 Lakhs**")

    with b2:
        st.markdown("**Key Customer Accounts:**")
        st.markdown("- 🪖 **Indian Army** (Fast-Track Defense Procurement)")
        st.markdown("- 🛡️ **Ministry of Home Affairs** (BSF, CRPF)")

# ----------------- TAB 3: STRATEGIC RECOMMENDATIONS -----------------
elif st.session_state["active_tab"] == "Strategy":
    st.markdown("### 💡 Recommended Counter-Strategies")
    st.caption("Synthesized by AI agents to protect profit margins and cash flow under current scenario:")

    events_list = pipeline.load_dynamic_events()
    trace = reasoning_engine.execute_7_step_loop(events_list[0])
    advisor_matrix = strategic_advisor.generate_strategic_recommendations(trace)

    for rec in advisor_matrix["action_matrix"]:
        st.markdown(f"""
        <div class="action-card-ui">
            <div style="font-size: 1.1rem; font-weight: 700; color: #34D399;">💡 {rec['title']}</div>
            <div style="font-size: 0.85rem; color: #94A3B8; margin: 4px 0;">Category: <b>{rec['category']}</b> | Owner: <b>{rec['executive_owner']}</b></div>
            <p style="color: #E2E8F0; margin: 8px 0;"><b>Action</b>: {rec['recommended_action']}</p>
            <p style="color: #60A5FA; font-weight: 700; margin-bottom:0;">💰 ROI Impact: {rec['financial_impact']}</p>
        </div>
        """, unsafe_allow_html=True)

# ----------------- TAB 4: VALUE CHAIN NETWORK MAP -----------------
elif st.session_state["active_tab"] == "Map":
    st.markdown("### 🕸️ Company Value Chain Network Map")
    st.caption("Interactive network visualizer connecting Customers ➔ Products ➔ Components ➔ Financial Profitability:")

    nodes = graph_db.get_nodes()
    edges = graph_db.get_edges()

    cy_elements = []
    color_map = {
        "BusinessSegment": "#3B82F6",      # Blue
        "ProductPlatform": "#10B981",      # Emerald
        "SupplyChainComponent": "#EF4444", # Red
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
        selected = cytoscape(cy_elements, stylesheet, layout={"name": "cose"}, height="440px", key="cy_map_clean")
        if selected and selected.get("nodes"):
            st.session_state["selected_node"] = selected["nodes"][0]
    except Exception:
        all_node_ids = [n["id"] for n in nodes]
        chosen = st.selectbox("Inspect Network Node", ["-- Select Node --"] + all_node_ids)
        if chosen != "-- Select Node --":
            st.session_state["selected_node"] = chosen

    if st.session_state["selected_node"]:
        n_id = st.session_state["selected_node"]
        details = graph_db.get_node_details(n_id)
        if details:
            st.info(f"🔍 **Inspecting Node `{n_id}`** ({details.get('label')})")
            props = {k: v for k, v in details.items() if k != "label"}
            st.table(pd.DataFrame(list(props.items()), columns=["Property", "Value"]))
