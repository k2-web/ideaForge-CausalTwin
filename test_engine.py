import os
import sys

# Ensure current directory is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_ingestion import IdeaForgeIngestionPipeline
from graph_db import IdeaForgeOntologyGraph
from causal_engine import IdeaForgeCausalEngine
from agents import IdeaForgeAgentOrchestrator

def test_ingestion_pipeline():
    print("Testing Ingestion Pipeline...")
    pipeline = IdeaForgeIngestionPipeline()
    financials_df = pipeline.load_quarterly_financials()
    tenders = pipeline.load_government_tenders()
    imports = pipeline.load_import_logs()
    
    assert financials_df is not None and not financials_df.empty, "Quarterly financials df is empty!"
    assert len(tenders) > 0, "No tenders loaded!"
    assert not imports.empty, "Import logs df is empty!"
    
    ref = pipeline.get_audit_trail_reference("financials", "indigenous_sourcing_pct")
    assert "BRSR" in ref, "Invalid audit trail reference format!"
    print("Ingestion Pipeline Test passed successfully.\n")
    return pipeline, financials_df

def test_graph_ontology():
    print("Testing Graph Ontology Design...")
    graph = IdeaForgeOntologyGraph()
    nodes = graph.get_nodes()
    edges = graph.get_edges()
    
    assert len(nodes) > 0, "No nodes in ontology!"
    assert len(edges) > 0, "No edges in ontology!"
    
    # Check node details
    switch_details = graph.get_node_details("SWITCH_UAV")
    assert switch_details is not None, "SWITCH_UAV node not found!"
    assert switch_details["label"] == "ProductPlatform", "Invalid class label for SWITCH UAV!"
    
    # Check 2-hop neighborhood
    neighborhood = graph.get_2_hop_neighborhood("SWITCH_UAV")
    assert len(neighborhood["nodes"]) > 0, "2-hop neighborhood is empty!"
    print("Graph Ontology Test passed successfully.\n")
    return graph

def test_causal_engine(financials_df):
    print("Testing 2SLS Causal Engine...")
    engine = IdeaForgeCausalEngine(financials_df)
    
    # Verify coefficients exist
    assert len(engine.beta) > 0, "2nd stage coefficients are missing!"
    assert len(engine.gamma) > 0, "1st stage coefficients are missing!"
    
    # Run counterfactual simulation
    sim_res = engine.simulate_counterfactual(mod_lag_days=90, import_tariff_shock_pct=15.0, saas_attach_rate_pct=40.0)
    metrics = sim_res["metrics"]
    
    assert metrics["MoD_Disbursement_Lag"] == 90, "Scenario lag value did not update!"
    assert metrics["EBITDA_Margin"] > 0, "Simulated EBITDA margin is non-positive or missing!"
    assert "coefficients" in sim_res, "Coefficients summaries missing in simulation output!"
    print("Causal Engine Test passed successfully.\n")
    return engine

def test_agent_orchestrator(pipeline, engine):
    print("Testing LangGraph Agent Orchestrator...")
    orchestrator = IdeaForgeAgentOrchestrator(pipeline, engine)
    
    scenario_config = {
        "mod_lag_days": 100,
        "import_tariff_shock_pct": 20.0,
        "saas_attach_rate_pct": 45.0,
        "indigenous_mix": 0.55
    }
    
    state = orchestrator.run_workflow(scenario_config)
    
    # Verify each agent executed and wrote logs
    assert len(state.agent_logs["DefenseProcurement"]) > 0, "Defense Procurement Agent logs are empty!"
    assert len(state.agent_logs["SupplyChainRisk"]) > 0, "Supply Chain Risk Agent logs are empty!"
    assert len(state.agent_logs["QofEAccounting"]) > 0, "QofE Accounting Agent logs are empty!"
    assert len(state.agent_logs["CausalSimulation"]) > 0, "Causal Simulation Agent logs are empty!"
    
    # Check if flags were raised
    assert "HIGH_MOD_DISBURSEMENT_LAG" in state.critical_flags, "Expected lag flag was not raised!"
    assert "SUPPLY_CHAIN_MARGIN_SQUEEZE" in state.critical_flags, "Expected tariff flag was not raised!"
    
    print("Agent Orchestrator Test passed successfully.\n")

if __name__ == "__main__":
    print("==================================================")
    print("   RUNNING CAUSAL TWIN BACKEND INTEGRATION TESTS  ")
    print("==================================================")
    pipeline, financials_df = test_ingestion_pipeline()
    graph = test_graph_ontology()
    engine = test_causal_engine(financials_df)
    test_agent_orchestrator(pipeline, engine)
    print("==================================================")
    print("            ALL VERIFICATION TESTS PASSED          ")
    print("==================================================")
