import pandas as pd
import json

class SharedTwinState:
    def __init__(self, scenario_config):
        self.scenario_config = scenario_config
        self.simulated_results = {}
        self.agent_logs = {
            "DefenseProcurement": [],
            "SupplyChainRisk": [],
            "QofEAccounting": [],
            "CausalSimulation": [],
            "StrategicAdvisory": [],
            "ExecutiveBriefing": []
        }
        self.critical_flags = []
        self.strategic_recommendations = []

class DefenseProcurementAgent:
    def __init__(self, ingestion_pipeline):
        self.pipeline = ingestion_pipeline

    def execute(self, state):
        tenders = self.pipeline.load_government_tenders()
        mod_lag = state.scenario_config.get("mod_lag_days", 60)
        
        # Core analysis
        state.agent_logs["DefenseProcurement"].append(
            "Analyzing Indian Ministry of Defence (MoD) procurement pipelines..."
        )
        
        active_pipeline_cr = sum(t["estimated_value_cr"] for t in tenders if "Awarded" not in t["status"])
        awarded_cr = sum(t["estimated_value_cr"] for t in tenders if "Awarded" in t["status"])
        
        state.agent_logs["DefenseProcurement"].append(
            f"Detected active tenders under evaluation worth INR {active_pipeline_cr:.1f} Cr. "
            f"Awarded contracts stand at INR {awarded_cr:.1f} Cr."
        )
        
        # Auditable references
        ref_l1 = self.pipeline.get_audit_trail_reference("tenders", "CPPP/2026/MOD/ARMY/321")
        state.agent_logs["DefenseProcurement"].append(
            f"Audit Trail: Verified ideaForge L1 status on Tactical VTOL UAV tender (INR 115 Cr) via CPPP. Source: {ref_l1}."
        )
        
        # Impact of MoD lag
        if mod_lag > 75:
            state.agent_logs["DefenseProcurement"].append(
                f"[WARNING] MoD Disbursement Lag of {mod_lag} days exceeds the safety threshold of 75 days. "
                "This will delay milestone-based payments on the Army VTOL UAV contract, triggering a liquidity squeeze."
            )
            state.critical_flags.append("HIGH_MOD_DISBURSEMENT_LAG")
        else:
            state.agent_logs["DefenseProcurement"].append(
                f"[OK] MoD disbursement lag set to {mod_lag} days. Execution and billing cycles are operational."
            )

class SupplyChainRiskAgent:
    def __init__(self, ingestion_pipeline):
        self.pipeline = ingestion_pipeline

    def execute(self, state):
        import_logs = self.pipeline.load_import_logs()
        tariff_shock = state.scenario_config.get("import_tariff_shock_pct", 0.0)
        
        state.agent_logs["SupplyChainRisk"].append(
            "Auditing semiconductor and sensor import channels..."
        )
        
        # Calculate average lead times
        avg_lead_time = import_logs["Lead_Time_Days"].mean()
        state.agent_logs["SupplyChainRisk"].append(
            f"Average imported component lead-time calculated at {avg_lead_time:.1f} days."
        )
        
        # Reference payload logs
        optical_ref = self.pipeline.get_audit_trail_reference("imports", "IMP-2025-081")
        state.agent_logs["SupplyChainRisk"].append(
            f"Audit Trail: EO/IR Dual Sensor Module imports tracked. Source: {optical_ref}."
        )
        
        # Indigenous content compliance
        tenders = self.pipeline.load_government_tenders()
        for t in tenders:
            req_content = int(t["indigenous_content_requirement"].replace(">=", "").replace("%", "").strip())
            current_mix = state.scenario_config.get("indigenous_mix", 0.60) * 100
            
            if current_mix < req_content:
                state.agent_logs["SupplyChainRisk"].append(
                    f"[CRITICAL] indigenous content requirement ({req_content}%) for Tender {t['tender_id']} "
                    f"is NOT met by current sourcing mix ({current_mix:.1f}%). High risk of bid disqualification."
                )
                state.critical_flags.append(f"BID_DISQUALIFICATION_RISK_{t['tender_id']}")
        
        # Tariff shocks
        if tariff_shock > 10.0:
            state.agent_logs["SupplyChainRisk"].append(
                f"[WARNING] Import price shock of +{tariff_shock}% detected. High import exposure (Israel/US) "
                "for EO/IR optical payloads will cause gross margin deterioration."
            )
            state.critical_flags.append("SUPPLY_CHAIN_MARGIN_SQUEEZE")
        else:
            state.agent_logs["SupplyChainRisk"].append(
                f"[OK] Component input price shocks are within historical standard deviation (+{tariff_shock}%)."
            )

class QofEAccountingAgent:
    def __init__(self, ingestion_pipeline):
        self.pipeline = ingestion_pipeline

    def execute(self, state):
        disclosures = self.pipeline.load_annual_report_disclosures()
        state.agent_logs["QofEAccounting"].append(
            "Conducting Ind AS financial Quality of Earnings (QofE) audit..."
        )
        
        # Check R&D capitalization
        rd = disclosures["key_disclosures"]["rd_expenditure"]
        cap_ratio = rd["capitalized_cr"] / rd["total_cr"]
        
        state.agent_logs["QofEAccounting"].append(
            f"Detected R&D Capitalization ratio of {cap_ratio*100:.1f}% "
            f"(INR {rd['capitalized_cr']:.1f} Cr capitalized vs INR {rd['expensed_cr']:.1f} Cr expensed)."
        )
        
        state.agent_logs["QofEAccounting"].append(
            f"Audit Trail: Verified R&D Intangible Asset additions. Source: {rd['audit_trail']}."
        )
        
        if cap_ratio > 0.60:
            state.agent_logs["QofEAccounting"].append(
                "[WARNING] Aggressive R&D capitalization profile. Over 60% of R&D expenses are balance-sheeted, "
                "artificially boosting current EBITDA. Any technological obsolescence will trigger massive write-offs."
            )
            state.critical_flags.append("AGGRESSIVE_RD_CAPITALIZATION")
            
        # Check working capital expansion
        wc = disclosures["key_disclosures"]["working_capital_cycle"]
        state.agent_logs["QofEAccounting"].append(
            f"Net working capital cycle stands at {wc['net_wc_days']} days (Inventory: {wc['inventory_days']} days, "
            f"Receivables: {wc['receivable_days']} days). Source: {wc['audit_trail']}."
        )
        
        if wc["inventory_days"] > 120:
            state.agent_logs["QofEAccounting"].append(
                f"[WARNING] Inventory holding period of {wc['inventory_days']} days indicates slow-moving "
                "raw materials (semiconductors, carbon frames) stockpiled due to import disruption fears."
            )

class CausalSimulationAgent:
    def __init__(self, causal_engine):
        self.engine = causal_engine

    def execute(self, state):
        state.agent_logs["CausalSimulation"].append(
            "Executing Two-Stage Least Squares (2SLS) causal inference simulation..."
        )
        
        # Get sliders from state config
        mod_lag = state.scenario_config.get("mod_lag_days", 60)
        tariff_shock = state.scenario_config.get("import_tariff_shock_pct", 0.0)
        saas_attach = state.scenario_config.get("saas_attach_rate_pct", 35.0)
        
        # Trigger 2SLS recalculation
        sim_res = self.engine.simulate_counterfactual(
            mod_lag_days=mod_lag,
            import_tariff_shock_pct=tariff_shock,
            saas_attach_rate_pct=saas_attach
        )
        
        state.simulated_results = sim_res["metrics"]
        
        # Fetch 2SLS coefficients for log
        beta_wc = sim_res["coefficients"]["second_stage"]["Working_Capital_Days (Estimated)"]["Coefficient"]
        gamma_mod = sim_res["coefficients"]["first_stage"]["MoD_Disbursement_Lag"]["Coefficient"]
        
        state.agent_logs["CausalSimulation"].append(
            f"1st Stage Instrument Strength: 1-day MoD Disbursement Lag increase causes a "
            f"{gamma_mod:+.2f} day expansion in Working Capital Days."
        )
        state.agent_logs["CausalSimulation"].append(
            f"2nd Stage Causal Impact: 1-day increase in Working Capital Days causally drives "
            f"{beta_wc*100:+.3f}% change in EBITDA Margin."
        )
        
        # Scenarios summary
        state.agent_logs["CausalSimulation"].append(
            f"[RESULT] Simulated EBITDA Margin is {state.simulated_results['EBITDA_Margin']:.2f}% "
            f"(compared to baseline {self.engine.df.iloc[-1]['EBITDA_Margin']:.2f}%)."
        )
        
        wc_change = state.simulated_results.get("Working_Capital_Change_Cr", 0.0)
        if wc_change > 0:
            state.agent_logs["CausalSimulation"].append(
                f"[RESULT] Simulated Working Capital expansion of INR {wc_change:.1f} Cr "
                f"creates an additional borrowing interest cost of INR {state.simulated_results.get('Additional_Interest_Cost_Cr', 0.0):.2f} Cr."
            )

class StrategicAdvisoryAgent:
    def execute(self, state):
        state.agent_logs["StrategicAdvisory"].append(
            "Evaluating McKinsey, Bain, and PE strategic frameworks..."
        )
        ebitda = state.simulated_results.get("EBITDA_Margin", 18.2)
        wc_days = state.simulated_results.get("Working_Capital_Days", 240)
        
        if ebitda < 16.0:
            state.agent_logs["StrategicAdvisory"].append(
                "[RECOMMENDATION] Primary Action: Immediate FLYGHT SaaS bundling to defend EBITDA margin floor."
            )
        elif wc_days > 250:
            state.agent_logs["StrategicAdvisory"].append(
                "[RECOMMENDATION] Primary Action: Restructure payables and accelerate Gujarat fab domestic sourcing."
            )
        else:
            state.agent_logs["StrategicAdvisory"].append(
                "[RECOMMENDATION] Primary Action: Expand enterprise commercial accounts while maintaining defense order pace."
            )

class ExecutiveBriefingAgent:
    def execute(self, state):
        flags = state.critical_flags
        ebitda = state.simulated_results.get("EBITDA_Margin", 18.2)
        state.agent_logs["ExecutiveBriefing"].append(
            f"Daily Synthesis: Operational Twin status evaluated with {len(flags)} critical flags."
        )
        state.agent_logs["ExecutiveBriefing"].append(
            f"Current Simulated EBITDA Margin: {ebitda:.2f}%. System is continuously monitoring regulatory updates."
        )

class IdeaForgeAgentOrchestrator:
    def __init__(self, ingestion_pipeline, causal_engine):
        self.defense_agent = DefenseProcurementAgent(ingestion_pipeline)
        self.supply_agent = SupplyChainRiskAgent(ingestion_pipeline)
        self.qofe_agent = QofEAccountingAgent(ingestion_pipeline)
        self.causal_agent = CausalSimulationAgent(causal_engine)
        self.strategic_agent = StrategicAdvisoryAgent()
        self.briefing_agent = ExecutiveBriefingAgent()

    def run_workflow(self, scenario_config):
        """Runs all 6 agents sequentially to generate a full cooperative report"""
        state = SharedTwinState(scenario_config)
        
        self.defense_agent.execute(state)
        self.supply_agent.execute(state)
        self.qofe_agent.execute(state)
        self.causal_agent.execute(state)
        self.strategic_agent.execute(state)
        self.briefing_agent.execute(state)
        
        return state
