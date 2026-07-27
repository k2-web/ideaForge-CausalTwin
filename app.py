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
    page_title="ideaForge Digital Twin | Interactive Company Explorer",
    page_icon="🚁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Sleek, Clean & Friendly UI Styling (No Jargon, High Readability)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: #0B0F17;
        color: #E2E8F0;
    }

    /* Main Welcome Card */
    .company-hero {
        background: linear-gradient(135deg, #111827 0%, #1F2937 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 28px;
        margin-bottom: 24px;
    }
    
    .company-tag {
        display: inline-block;
        background: rgba(59, 130, 246, 0.2);
        color: #60A5FA;
        border: 1px solid rgba(59, 130, 246, 0.3);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 12px;
    }
    
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #FFFFFF;
        margin-bottom: 8px;
    }
    
    .hero-desc {
        color: #9CA3AF;
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 0;
    }

    /* Metric Cards */
    .stat-card {
        background: #111827;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 16px;
    }
    
    .stat-label {
        color: #9CA3AF;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .stat-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #F9FAFB;
        margin: 6px 0;
    }
    
    .stat-sub {
        font-size: 0.8rem;
        color: #60A5FA;
    }

    /* Interactive Product Cards */
    .product-box {
        background: #1F2937;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        transition: transform 0.2s;
    }
    .product-box:hover {
        border-color: #3B82F6;
        transform: translateY(-2px);
    }
    
    .product-name {
        font-size: 1.2rem;
        font-weight: 700;
        color: #38BDF8;
        margin-bottom: 6px;
    }

    /* Chat bubble */
    .chat-bubble-twin {
        background: #1E293B;
        border-left: 4px solid #3B82F6;
        border-radius: 8px;
        padding: 16px;
        margin: 12px 0;
    }
</style>
""", unsafe_allow_html=True)

# Session State Setup
if "selected_product" not in st.session_state:
    st.session_state["selected_product"] = "SWITCH_UAV"
if "selected_node" not in st.session_state:
    st.session_state["selected_node"] = None
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


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
st.sidebar.markdown("### 🎛️ Real-World Simulator")
st.sidebar.caption("Adjust real-world conditions to see how the company responds:")

mod_lag = st.sidebar.slider(
    "Government Payment Speed",
    min_value=15, max_value=180, value=int(baseline_data["MoD_Disbursement_Lag"]), step=5,
    help="Days taken by the Ministry of Defence to clear invoices. Lower is faster cash flow."
)

import_price_shock = st.sidebar.slider(
    "Imported Sensor Tariffs / Price Hike (%)",
    min_value=0, max_value=50, value=0, step=5,
    help="Cost increase for optical cameras and chips imported from Israel/USA."
)

saas_attach_rate = st.sidebar.slider(
    "Software Subscription Adoption (%)",
    min_value=0, max_value=100, value=int(baseline_data["SaaS_Attach_Rate"] * 100), step=5,
    help="Percentage of drone clients subscribing to FLYGHT cloud analytics software."
)

scenario_config = {
    "mod_lag_days": mod_lag,
    "import_tariff_shock_pct": import_price_shock,
    "saas_attach_rate_pct": saas_attach_rate,
    "indigenous_mix": 0.60
}

# Run backend calculations
agent_state = orchestrator.run_workflow(scenario_config)
sim_res = agent_state.simulated_results

# ----------------- HERO WELCOME BANNER -----------------
st.markdown("""
<div class="company-hero">
    <div class="company-tag">🌐 LIVE DIGITAL TWIN OF IDEAFORGE TECHNOLOGY LTD</div>
    <div class="hero-title">Welcome to ideaForge's Digital Twin</div>
    <div class="hero-desc">
        This is a live, interactive digital copy of <b>ideaForge Technology Limited</b>—India's pioneer market leader in defense and civil drones. 
        Explore how the company makes money, builds its drones, manages supply chain risks, and deals with government payments.
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------- TALK TO THE DIGITAL TWIN (CHAT & Q&A) -----------------
st.markdown("### 💬 Talk to the Company Digital Twin")
st.caption("Ask any question in plain English, or click a quick question below:")

q_col1, q_col2, q_col3, q_col4 = st.columns(4)

asked_q = None
if q_col1.button("❓ What does ideaForge build?"):
    asked_q = "What does ideaForge build?"
if q_col2.button("💰 How does the company make money?"):
    asked_q = "How does the company make money?"
if q_col3.button("⚠️ What is ideaForge's biggest risk?"):
    asked_q = "What is ideaForge's biggest risk?"
if q_col4.button("🚀 What is the FLYGHT platform?"):
    asked_q = "What is the FLYGHT platform?"

custom_user_q = st.text_input("Or ask your own question about ideaForge:", placeholder="e.g., Who are their main customers? Where do they buy cameras?")
if custom_user_q:
    asked_q = custom_user_q

if asked_q:
    st.markdown(f"**You asked**: *\"{asked_q}\"*")
    
    # Generate conversational plain English answers
    q_lower = asked_q.lower()
    if "build" in q_lower or "product" in q_lower:
        ans = ("**ideaForge builds high-performance Unmanned Aircraft Systems (drones).**\n\n"
               "1. **SWITCH UAV**: Their flagship flagship VTOL drone used by the Indian Army for border surveillance.\n"
               "2. **NETRA V4**: Quadcopter drone used by police & paramilitary for crowd control and rescue missions.\n"
               "3. **Q6 UAV**: Heavy-payload drone used by Survey of India for mapping rural land under the SVAMITVA scheme.\n"
               "4. **FLYGHT Platform**: Cloud software for fleet tracking & AI map analytics.")
    elif "money" in q_lower or "revenue" in q_lower:
        ans = (f"**ideaForge generates revenue primarily by selling drone hardware and software subscriptions:**\n\n"
               f"- **Defense Orders (65%)**: Large contracts from the Indian Army & Ministry of Home Affairs.\n"
               f"- **Civil Mapping (20%)**: Government mapping tenders (e.g. Survey of India).\n"
               f"- **FLYGHT Software (10%)**: Recurring annual subscriptions for GIS mapping analytics.\n"
               f"- **Current Annual Revenue**: ~₹202 Cr | **Operating Profit Margin**: ~{sim_res['EBITDA_Margin']:.1f}%.")
    elif "risk" in q_lower or "tariff" in q_lower or "component" in q_lower:
        ans = (f"**ideaForge's 2 biggest operational risks are:**\n\n"
               f"1. **Government Payment Delays**: Defense contracts take ~60–90 days to clear invoices, tying up ₹{sim_res['Working_Capital_Requirement_Cr']:.1f} Cr in working capital.\n"
               f"2. **Import Component Reliance**: High-tech cameras (EO/IR sensors) are imported from Israel/USA. A tariff increase or supply bottleneck raises build costs.")
    elif "flyght" in q_lower or "software" in q_lower:
        ans = ("**FLYGHT is ideaForge's proprietary cloud software.**\n\n"
               "Instead of just selling a physical drone once, ideaForge bundles FLYGHT software subscriptions. "
               "It allows drone pilots to stream live video to commanders, process 3D terrain maps, and run AI detection automatically. "
               "It provides high-margin recurring income.")
    else:
        ans = f"**Digital Twin Analysis**: ideaForge operates across Defense ISR and Civil Mapping. Current simulated EBITDA margin is {sim_res['EBITDA_Margin']:.1f}% with working capital cycle of {sim_res['Working_Capital_Days']:.0f} days. All operations are actively monitored."

    st.markdown(f"""
    <div class="chat-bubble-twin">
        <b>🤖 ideaForge Digital Twin Response:</b><br><br>
        {ans}
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# ----------------- 3 SIMPLE INTERACTIVE VIEWS -----------------
tab1, tab2, tab3 = st.tabs([
    "🚁 1. Inside ideaForge (Products & Value Chain)",
    "🎛️ 2. Real-World Scenario Simulator",
    "🕸️ 3. Company Network Map"
])

# ==============================================================================
# VIEW 1: INSIDE IDEAFORGE (PRODUCTS & VALUE CHAIN)
# ==============================================================================
with tab1:
    st.subheader("🚁 Explore ideaForge's Product Platforms")
    st.caption("Click a product platform to see what goes inside it and how it contributes to revenue:")

    p_cols = st.columns(4)

    with p_cols[0]:
        st.markdown("""
        <div class="product-box">
            <div class="product-name">SWITCH VTOL UAV</div>
            <div style="font-size:0.85rem; color:#9CA3AF; margin-bottom:8px;">Flagship Defense Surveillance</div>
            <div style="font-size:0.9rem; font-weight:700; color:#34D399;">65% of Revenue</div>
            <div style="font-size:0.8rem; color:#D1D5DB; margin-top:6px;">Flight Endurance: 120 mins | Price: ₹25 Lakhs</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Inspect SWITCH UAV Details"):
            st.session_state["selected_product"] = "SWITCH_UAV"

    with p_cols[1]:
        st.markdown("""
        <div class="product-box">
            <div class="product-name">NETRA V4 Quadcopter</div>
            <div style="font-size:0.85rem; color:#9CA3AF; margin-bottom:8px;">Paramilitary & Police Patrol</div>
            <div style="font-size:0.9rem; font-weight:700; color:#34D399;">15% of Revenue</div>
            <div style="font-size:0.8rem; color:#D1D5DB; margin-top:6px;">Flight Endurance: 45 mins | Price: ₹12 Lakhs</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Inspect NETRA V4 Details"):
            st.session_state["selected_product"] = "NETRA_V4"

    with p_cols[2]:
        st.markdown("""
        <div class="product-box">
            <div class="product-name">Q6 Heavy Payload UAV</div>
            <div style="font-size:0.85rem; color:#9CA3AF; margin-bottom:8px;">Civil Mapping & Surveying</div>
            <div style="font-size:0.9rem; font-weight:700; color:#34D399;">10% of Revenue</div>
            <div style="font-size:0.8rem; color:#D1D5DB; margin-top:6px;">Payload Capacity: 5 kg | Price: ₹35 Lakhs</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Inspect Q6 UAV Details"):
            st.session_state["selected_product"] = "Q6_UAV"

    with p_cols[3]:
        st.markdown("""
        <div class="product-box">
            <div class="product-name">FLYGHT SaaS Software</div>
            <div style="font-size:0.85rem; color:#9CA3AF; margin-bottom:8px;">Cloud Mapping & AI Portal</div>
            <div style="font-size:0.9rem; font-weight:700; color:#34D399;">10% (High Growth)</div>
            <div style="font-size:0.8rem; color:#D1D5DB; margin-top:6px;">Recurring ARR | Price: ₹1.5 Lakh/drone/yr</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Inspect FLYGHT SaaS Details"):
            st.session_state["selected_product"] = "FLYGHT_Patrol"

    st.write("")
    
    # Show selected product breakdown
    prod_id = st.session_state["selected_product"]
    st.markdown(f"### 📦 Selected Platform Breakdown: `{prod_id}`")
    
    b_col1, b_col2 = st.columns(2)
    with b_col1:
        st.markdown("**Key Sub-Components (Bill of Materials):**")
        if prod_id == "SWITCH_UAV":
            st.markdown("- 📷 **EO/IR Optical Payload** (Imported from Elbit Systems, Israel) — ₹8.0 Lakhs")
            st.markdown("- 🧭 **Autopilot Microcontroller Board** (Imported from Taiwan) — ₹2.0 Lakhs")
            st.markdown("- ✈️ **Carbon Fiber Structural Frame** (Japan Carbon Fiber Corp) — ₹1.5 Lakhs")
            st.markdown("- 🔋 **LiPo Battery Pack** (Assembled locally in India) — ₹0.8 Lakhs")
        elif prod_id == "NETRA_V4":
            st.markdown("- 📷 **Day/Night Thermal Camera** — ₹4.5 Lakhs")
            st.markdown("- 🧭 **Autopilot Board** — ₹1.5 Lakhs")
            st.markdown("- 🔋 **LiPo Battery Pack** — ₹0.6 Lakhs")
        else:
            st.markdown("- 🗺️ **RTK GPS & 24MP Mapping Sensor** — ₹6.0 Lakhs")
            st.markdown("- 💻 **FLYGHT Cloud Portal Sync Module** — ₹1.5 Lakhs")

    with b_col2:
        st.markdown("**Primary Customer Accounts:**")
        if prod_id in ["SWITCH_UAV", "NETRA_V4"]:
            st.markdown("- 🪖 **Indian Army** (Fast-Track Procurement)")
            st.markdown("- 🛡️ **Ministry of Home Affairs** (Border Security Force, CRPF)")
        else:
            st.markdown("- 🗺️ **Survey of India** (SVAMITVA Rural Land Mapping)")
            st.markdown("- 🏢 **Enterprise Clients** (Adani Ports, NTPC Infrastructure Inspection)")

# ==============================================================================
# VIEW 2: REAL-WORLD SCENARIO SIMULATOR
# ==============================================================================
with tab2:
    st.subheader("🎛️ Real-World Scenario Simulator (What-If Engine)")
    st.caption("Adjust the sliders in the left sidebar to see how real-world shocks affect ideaForge's finances in plain English:")

    s_col1, s_col2, s_col3 = st.columns(3)

    with s_col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">OPERATING PROFIT MARGIN</div>
            <div class="stat-value">{sim_res['EBITDA_Margin']:.1f}%</div>
            <div class="stat-sub">{"Healthy Margin" if sim_res['EBITDA_Margin'] > 18 else "Compressed Margin (Tariff Impact)"}</div>
        </div>
        """, unsafe_allow_html=True)

    with s_col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">CASH FLOW CYCLE SPEED</div>
            <div class="stat-value">{sim_res['Working_Capital_Days']:.0f} Days</div>
            <div class="stat-sub">Time taken to collect cash from customers</div>
        </div>
        """, unsafe_allow_html=True)

    with s_col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">WORKING CAPITAL REQUIRED</div>
            <div class="stat-value">₹{sim_res['Working_Capital_Requirement_Cr']:.1f} Cr</div>
            <div class="stat-sub">Capital tied up in raw materials & unpaid bills</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.markdown("### 💡 Recommended Counter-Strategy for Current Scenario")
    
    events_list = pipeline.load_dynamic_events()
    trace = reasoning_engine.execute_7_step_loop(events_list[0])
    advisor_matrix = strategic_advisor.generate_strategic_recommendations(trace)
    
    rec_primary = advisor_matrix["action_matrix"][0]

    st.markdown(f"""
    <div style="background:#1E293B; border-left:4px solid #10B981; border-radius:10px; padding:20px;">
        <div style="font-size:1.1rem; font-weight:700; color:#34D399;">💡 {rec_primary['title']}</div>
        <p style="color:#CBD5E1; margin:8px 0;"><b>Problem Statement</b>: {rec_primary['problem_statement']}</p>
        <p style="color:#CBD5E1; margin:8px 0;"><b>Recommended Action</b>: {rec_primary['recommended_action']}</p>
        <p style="color:#60A5FA; font-weight:700;">💰 Expected Return: {rec_primary['financial_impact']}</p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# VIEW 3: COMPANY NETWORK MAP
# ==============================================================================
with tab3:
    st.subheader("🕸️ Visual Company Network Map")
    st.caption("How ideaForge's customers, products, components, and money flow together:")

    g1, g2 = st.columns([2, 1])

    with g1:
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
                    "line-color": "#4B5563",
                    "target-arrow-color": "#4B5563",
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
            selected = cytoscape(cy_elements, stylesheet, layout={"name": "cose"}, height="440px", key="cy_simple")
            if selected and selected.get("nodes"):
                st.session_state["selected_node"] = selected["nodes"][0]
        except Exception:
            all_node_ids = [n["id"] for n in nodes]
            chosen = st.selectbox("Inspect Network Node", ["-- Select Node --"] + all_node_ids)
            if chosen != "-- Select Node --":
                st.session_state["selected_node"] = chosen

    with g2:
        st.markdown("##### 🔍 Network Element Details")
        if st.session_state["selected_node"]:
            n_id = st.session_state["selected_node"]
            details = graph_db.get_node_details(n_id)
            if details:
                st.markdown(f"**Entity**: `{n_id}`")
                st.markdown(f"**Category**: `{details.get('label')}`")
                props = {k: v for k, v in details.items() if k != "label"}
                st.table(pd.DataFrame(list(props.items()), columns=["Property", "Value"]))
        else:
            st.info("Click any node in the Network Map to see its operational details.")
