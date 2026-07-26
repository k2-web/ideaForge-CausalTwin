import os
import sys

# Ensure current directory is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_ingestion import IdeaForgeIngestionPipeline
from graph_db import IdeaForgeOntologyGraph
from causal_engine import IdeaForgeCausalEngine
from memory_engine import MemoryEngine
from reasoning_loop import StrategicReasoningEngine
from strategic_advisor import StrategicAdvisorEngine
from agents import IdeaForgeAgentOrchestrator

def run_daily_briefing_job(event_id=None):
    """
    Autonomous Daily Executive Briefing Job.
    Runs without requiring human prompts:
    1. Ingests dynamic breaking events.
    2. Executes the 7-Step Strategic Reasoning Loop.
    3. Fits 2SLS Causal Econometric Models.
    4. Synthesizes McKinsey/PE Recommendations.
    5. Saves the report to persistent memory.
    """
    print("==========================================================================")
    print(" 🚀 AUTONOMOUS EXECUTIVE DIGITAL TWIN: DAILY BRIEFING GENERATOR")
    print("==========================================================================")
    
    pipeline = IdeaForgeIngestionPipeline()
    financials_df = pipeline.load_quarterly_financials()
    causal_engine = IdeaForgeCausalEngine(financials_df)
    memory_engine = MemoryEngine()
    reasoning_engine = StrategicReasoningEngine(causal_engine, memory_engine)
    strategic_advisor = StrategicAdvisorEngine(causal_engine, memory_engine)
    
    events = pipeline.load_dynamic_events()
    
    # Pick target event
    target_event = None
    if event_id:
        for e in events:
            if e["event_id"] == event_id:
                target_event = e
                break
                
    if not target_event:
        target_event = events[0] # Default to latest breaking event
        
    print(f"\n[EVENT DETECTED]: {target_event['event_id']} - {target_event['title']}")
    print(f"[CATEGORY]: {target_event['category']}")
    print(f"[TIMESTAMP]: {target_event['timestamp']}")
    
    # Execute 7-Step Strategic Reasoning Loop
    trace = reasoning_engine.execute_7_step_loop(target_event)
    
    # Generate Strategic Consulting Recommendations
    rec_matrix = strategic_advisor.generate_strategic_recommendations(trace)
    
    # Format Executive Briefing Report
    sims = trace["step7_simulations"]["simulations"]
    no_action = sims["Option_No_Action"]
    action_a = sims["Option_A_Supply_Mitigation"]
    action_b = sims["Option_B_SaaS_Accelerate"]
    
    briefing_text = f"""
# 📋 DAILY EXECUTIVE BRIEFING: IDEAFORGE DIGITAL TWIN
**Generated On**: {target_event['timestamp']} | **Source**: {target_event['source']}

---

### 1. Executive Summary & Event Breakdown
**Event**: {target_event['title']}
**Category**: {target_event['category']}
**Relevance**: {trace['step2_relevance']['relevance_type']} — {trace['step2_relevance']['rationale']}
**Severity Assessment**: **{trace['step4_severity']['severity_level']}**

**Description**:
{target_event['description']}

---

### 2. 15-Dimension Business Impact
- **Revenue**: {trace['step3_dimensions']['impacted_dimensions']['Revenue']}
- **EBITDA Margins**: {trace['step3_dimensions']['impacted_dimensions']['Margins']}
- **Supply Chain**: {trace['step3_dimensions']['impacted_dimensions']['Supply Chain']}
- **Cash Flow / Working Capital**: {trace['step3_dimensions']['impacted_dimensions']['Cash Flow']}
- **Regulation**: {trace['step3_dimensions']['impacted_dimensions']['Regulation']}

---

### 3. 2SLS Econometric Counterfactual Simulations
- **Do Nothing (Status Quo)**:
  - EBITDA Margin: **{no_action['ebitda_margin_pct']}%**
  - Working Capital Days: **{no_action['working_capital_days']} days**
  - Working Capital Req.: **₹{no_action['working_capital_req_cr']} Cr**
  - Projected Net Profit: **₹{no_action['net_profit_cr']} Cr**

- **Action A (Fast-Track Sanand Local Sourcing)**:
  - EBITDA Margin: **{action_a['ebitda_margin_pct']}%** (+{round(action_a['ebitda_margin_pct'] - no_action['ebitda_margin_pct'], 2)}% vs status quo)
  - Working Capital Days: **{action_a['working_capital_days']} days**
  - Projected Net Profit: **₹{action_a['net_profit_cr']} Cr**

- **Action B (Accelerate FLYGHT SaaS Bundling)**:
  - EBITDA Margin: **{action_b['ebitda_margin_pct']}%** (+{round(action_b['ebitda_margin_pct'] - no_action['ebitda_margin_pct'], 2)}% vs status quo)
  - Working Capital Days: **{action_b['working_capital_days']} days**
  - Projected Net Profit: **₹{action_b['net_profit_cr']} Cr**

---

### 4. Prioritized McKinsey / PE Executive Action Matrix
**Primary Recommended Strategy**: {rec_matrix['recommended_primary_action']}

"""
    
    key_takeaways = [
        f"Event '{target_event['title']}' categorized as {trace['step4_severity']['severity_level']}.",
        f"Action B (SaaS Bundling) yields highest EBITDA expansion (+{round(action_b['ebitda_margin_pct'] - no_action['ebitda_margin_pct'], 2)}%).",
        f"Action A (Local Sourcing) reduces working capital requirement by ₹{round(abs(action_a['working_capital_req_cr'] - no_action['working_capital_req_cr']), 1)} Cr."
    ]
    
    recommended_actions = [rec['title'] for rec in rec_matrix['action_matrix']]
    
    # Save briefing to persistent memory
    memory_engine.log_executive_briefing(briefing_text, key_takeaways, recommended_actions)
    
    print("\n" + briefing_text)
    print("==========================================================================")
    print(" ✅ DAILY BRIEFING GENERATED & SAVED TO PERSISTENT MEMORY")
    print("==========================================================================")
    return briefing_text

if __name__ == "__main__":
    run_daily_briefing_job()
