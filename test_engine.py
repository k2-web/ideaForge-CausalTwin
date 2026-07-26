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
from daily_briefing_job import run_daily_briefing_job

def test_ingestion_pipeline():
    print("Testing Ingestion Pipeline...")
    pipeline = IdeaForgeIngestionPipeline()
    financials_df = pipeline.load_quarterly_financials()
    tenders = pipeline.load_government_tenders()
    imports = pipeline.load_import_logs()
    events = pipeline.load_dynamic_events()
    
    assert financials_df is not None and not financials_df.empty, "Quarterly financials df is empty!"
    assert len(tenders) > 0, "No tenders loaded!"
    assert not imports.empty, "Import logs df is empty!"
    assert len(events) > 0, "No dynamic events loaded!"
    
    ref = pipeline.get_audit_trail_reference("financials", "indigenous_sourcing_pct")
    assert "BRSR" in ref, "Invalid audit trail reference format!"
    print("Ingestion Pipeline Test passed successfully.\n")
    return pipeline, financials_df, events

def test_graph_ontology():
    print("Testing Graph Ontology Design...")
    graph = IdeaForgeOntologyGraph()
    nodes = graph.get_nodes()
    edges = graph.get_edges()
    
    assert len(nodes) > 0, "No nodes in ontology!"
    assert len(edges) > 0, "No edges in ontology!"
    
    switch_details = graph.get_node_details("SWITCH_UAV")
    assert switch_details is not None, "SWITCH_UAV node not found!"
    assert switch_details["label"] == "ProductPlatform", "Invalid class label for SWITCH UAV!"
    
    neighborhood = graph.get_2_hop_neighborhood("SWITCH_UAV")
    assert len(neighborhood["nodes"]) > 0, "2-hop neighborhood is empty!"
    print("Graph Ontology Test passed successfully.\n")
    return graph

def test_causal_engine(financials_df):
    print("Testing 2SLS Causal Engine...")
    engine = IdeaForgeCausalEngine(financials_df)
    
    assert len(engine.beta) > 0, "2nd stage coefficients are missing!"
    assert len(engine.gamma) > 0, "1st stage coefficients are missing!"
    
    sim_res = engine.simulate_counterfactual(mod_lag_days=90, import_tariff_shock_pct=15.0, saas_attach_rate_pct=40.0)
    metrics = sim_res["metrics"]
    
    assert metrics["MoD_Disbursement_Lag"] == 90, "Scenario lag value did not update!"
    assert metrics["EBITDA_Margin"] > 0, "Simulated EBITDA margin is non-positive or missing!"
    assert "coefficients" in sim_res, "Coefficients summaries missing in simulation output!"
    print("Causal Engine Test passed successfully.\n")
    return engine

def test_memory_engine():
    print("Testing Persistent Memory & Belief Revision Engine...")
    memory = MemoryEngine()
    memory.revise_belief("TEST_KEY", 10, 20, "Unit Test Revision", "EVT-TEST")
    
    beliefs = memory.get_belief_history()
    assert len(beliefs) > 0, "Belief ledger is empty!"
    assert beliefs[0]["assumption_key"] == "TEST_KEY", "Belief revision not logged at top!"
    print("Persistent Memory Engine Test passed successfully.\n")
    return memory

def test_reasoning_and_advisor(causal_engine, memory_engine, events):
    print("Testing 7-Step Strategic Reasoning Loop & McKinsey Advisor...")
    reasoning_engine = StrategicReasoningEngine(causal_engine, memory_engine)
    advisor_engine = StrategicAdvisorEngine(causal_engine, memory_engine)
    
    trace = reasoning_engine.execute_7_step_loop(events[0])
    assert "step1_event" in trace, "Step 1 trace missing!"
    assert "step7_simulations" in trace, "Step 7 simulations missing!"
    
    rec_matrix = advisor_engine.generate_strategic_recommendations(trace)
    assert len(rec_matrix["action_matrix"]) >= 4, "Expected at least 4 McKinsey/PE recommendations!"
    print("7-Step Reasoning & Strategic Advisor Test passed successfully.\n")

def test_daily_briefing_job():
    print("Testing Autonomous Daily Briefing Job...")
    briefing_text = run_daily_briefing_job()
    assert "DAILY EXECUTIVE BRIEFING" in briefing_text, "Executive briefing title missing!"
    assert "2SLS Econometric Counterfactual Simulations" in briefing_text, "Simulations missing from briefing text!"
    print("Daily Briefing Job Test passed successfully.\n")

if __name__ == "__main__":
    print("==================================================")
    print("   RUNNING AUTONOMOUS DIGITAL TWIN BACKEND TESTS ")
    print("==================================================")
    pipeline, financials_df, events = test_ingestion_pipeline()
    graph = test_graph_ontology()
    causal_engine = test_causal_engine(financials_df)
    memory_engine = test_memory_engine()
    test_reasoning_and_advisor(causal_engine, memory_engine, events)
    test_daily_briefing_job()
    print("==================================================")
    print("         ALL AUTONOMOUS TWIN TESTS PASSED          ")
    print("==================================================")
