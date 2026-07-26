import json

class StrategicReasoningEngine:
    def __init__(self, causal_engine, memory_engine):
        self.causal_engine = causal_engine
        self.memory_engine = memory_engine

    def execute_7_step_loop(self, event_data):
        """
        Executes the formal 7-Step Strategic Reasoning Cycle for any event.
        Returns a structured dictionary with full step-by-step analytical traces.
        """
        event_id = event_data.get("event_id", "EVT-UNKNOWN")
        title = event_data.get("title", "Unspecified Event")
        category = event_data.get("category", "General Operations")
        desc = event_data.get("description", "")
        params = event_data.get("impact_parameters", {})

        # --- STEP 1: What happened? ---
        step1 = {
            "step": "Step 1: Event Identification",
            "question": "What happened?",
            "summary": title,
            "category": category,
            "source": event_data.get("source", "Internal Monitoring"),
            "timestamp": event_data.get("timestamp", ""),
            "full_description": desc
        }

        # --- STEP 2: Does this affect me? ---
        # Determine relevance based on category and parameters
        if any(p in params for p in ["mod_lag_days", "import_tariff_shock_pct", "saas_attach_rate_pct"]):
            relevance = "DIRECT"
            rationale = "Event acts directly on core operational variables (Disbursement Lag, Tariff Sourcing, or SaaS Attach Rate)."
        elif "competitor" in category.lower() or "policy" in category.lower():
            relevance = "INDIRECT"
            rationale = "Event shifts macro competitive dynamics or regulatory frameworks."
        else:
            relevance = "NEGLIGIBLE"
            rationale = "Event is outside ideaForge's core dual-use defense and civil UAV supply network."

        step2 = {
            "step": "Step 2: Relevance Assessment",
            "question": "Does this affect me?",
            "relevance_type": relevance,
            "rationale": rationale
        }

        # --- STEP 3: Which business dimensions are affected? ---
        dimensions = {
            "Revenue": "AFFECTED" if params.get("saas_attach_rate_pct") or params.get("mod_lag_days") else "STABLE",
            "Margins": "CRITICAL" if params.get("import_tariff_shock_pct") else "MONITORED",
            "Operations": "AFFECTED" if params.get("mod_lag_days", 0) > 75 else "STABLE",
            "Manufacturing": "AFFECTED" if params.get("import_tariff_shock_pct", 0) > 10 else "STABLE",
            "Supply Chain": "CRITICAL" if params.get("import_tariff_shock_pct") else "STABLE",
            "Customers": "AFFECTED" if "tenders" in desc.lower() or "svamitva" in desc.lower() else "STABLE",
            "Competition": "MONITORED",
            "Regulation": "CRITICAL" if "tariff" in desc.lower() or "pli" in desc.lower() or "mod" in desc.lower() else "STABLE",
            "Capital Allocation": "AFFECTED" if params.get("mod_lag_days", 0) > 75 else "STABLE",
            "Cash Flow": "CRITICAL" if params.get("mod_lag_days", 0) > 75 else "STABLE",
            "Debt": "AFFECTED" if params.get("mod_lag_days", 0) > 80 else "STABLE",
            "Growth": "POSITIVE" if params.get("saas_attach_rate_pct", 0) > 35 else "MONITORED",
            "Market Perception": "STABLE",
            "Talent": "STABLE",
            "Technology": "POSITIVE" if "semiconductor" in desc.lower() or "analytics" in desc.lower() else "STABLE"
        }

        step3 = {
            "step": "Step 3: 15-Dimension Impact Mapping",
            "question": "Which parts of my business are affected?",
            "impacted_dimensions": dimensions
        }

        # --- STEP 4: How large is the impact? ---
        mod_lag = params.get("mod_lag_days", 60)
        tariff = params.get("import_tariff_shock_pct", 0)
        saas = params.get("saas_attach_rate_pct", 35)

        if tariff > 20 or mod_lag > 110:
            severity = "EXISTENTIAL / SEVERE"
        elif tariff > 10 or mod_lag > 75:
            severity = "MAJOR"
        elif tariff > 0 or mod_lag > 60 or saas > 35:
            severity = "MODERATE"
        else:
            severity = "MINOR"

        step4 = {
            "step": "Step 4: Severity Assessment",
            "question": "How large is the impact?",
            "severity_level": severity,
            "key_drivers": f"MoD Lag: {mod_lag}d | Import Tariff Shock: +{tariff}% | SaaS Attach: {saas}%"
        }

        # --- STEP 5: What assumptions changed? ---
        revisions = []
        if mod_lag != 60:
            revisions.append({
                "key": "MoD_Disbursement_Lag",
                "old": 60,
                "new": mod_lag,
                "reason": f"Updated due to event '{title}'"
            })
            self.memory_engine.revise_belief("MoD_Disbursement_Lag", 60, mod_lag, f"Event {event_id}: {title}", event_id, severity)

        if tariff != 0:
            revisions.append({
                "key": "Import_Tariff_Shock_Pct",
                "old": 0,
                "new": tariff,
                "reason": f"Updated due to event '{title}'"
            })
            self.memory_engine.revise_belief("Import_Tariff_Shock_Pct", 0, tariff, f"Event {event_id}: {title}", event_id, severity)

        if saas != 35:
            revisions.append({
                "key": "FLYGHT_SaaS_Attach_Rate",
                "old": 0.35,
                "new": saas / 100.0,
                "reason": f"Updated due to event '{title}'"
            })
            self.memory_engine.revise_belief("FLYGHT_SaaS_Attach_Rate", 0.35, saas / 100.0, f"Event {event_id}: {title}", event_id, severity)

        step5 = {
            "step": "Step 5: Assumption Revision & Belief Updates",
            "question": "What assumptions changed?",
            "invalidated_beliefs": revisions if revisions else ["No baseline assumptions invalidated."]
        }

        # --- STEP 6: Do I need to act? ---
        if severity in ["MAJOR", "EXISTENTIAL / SEVERE"] or saas > 40:
            act_required = True
            action_rationale = "Material operational impact detected. Immediate executive counter-strategy required."
        else:
            act_required = False
            action_rationale = "Impact is within normal operating buffers. Log event to memory and monitor."

        step6 = {
            "step": "Step 6: Executive Action Trigger",
            "question": "Do I need to act?",
            "action_required": act_required,
            "decision_rationale": action_rationale
        }

        # --- STEP 7: Simulate outcomes & scenarios ---
        # Run 2SLS Causal Counterfactual Simulations for 3 strategic options
        # Baseline simulation (Do Nothing)
        sim_no_action = self.causal_engine.simulate_counterfactual(
            mod_lag_days=mod_lag,
            import_tariff_shock_pct=tariff,
            saas_attach_rate_pct=saas
        )

        # Action Option A: Supply Chain Buffering & Local Sourcing Offsets
        sim_action_a = self.causal_engine.simulate_counterfactual(
            mod_lag_days=max(45, mod_lag - 15), # Negotiate faster milestone release
            import_tariff_shock_pct=max(0, tariff - 10), # Substitute with local Gujarat components
            saas_attach_rate_pct=saas
        )

        # Action Option B: Accelerated SaaS Monetization & Price Adjustments
        sim_action_b = self.causal_engine.simulate_counterfactual(
            mod_lag_days=mod_lag,
            import_tariff_shock_pct=tariff,
            saas_attach_rate_pct=min(100, saas + 15) # Drive FLYGHT SaaS attach to offset hardware margin squeeze
        )

        step7 = {
            "step": "Step 7: Scenario & Outcome Simulation (2SLS Causal Engine)",
            "question": "If we act, what happens?",
            "simulations": {
                "Option_No_Action": {
                    "title": "Do Nothing (Status Quo)",
                    "probability": "0.45",
                    "ebitda_margin_pct": round(sim_no_action["metrics"]["EBITDA_Margin"], 2),
                    "working_capital_days": round(sim_no_action["metrics"]["Working_Capital_Days"], 1),
                    "net_profit_cr": round(sim_no_action["metrics"]["Net_Profit"], 2),
                    "working_capital_req_cr": round(sim_no_action["metrics"]["Working_Capital_Requirement_Cr"], 2)
                },
                "Option_A_Supply_Mitigation": {
                    "title": "Action A: Fast-track Local Sourcing & Milestone Audit",
                    "probability": "0.75",
                    "ebitda_margin_pct": round(sim_action_a["metrics"]["EBITDA_Margin"], 2),
                    "working_capital_days": round(sim_action_a["metrics"]["Working_Capital_Days"], 1),
                    "net_profit_cr": round(sim_action_a["metrics"]["Net_Profit"], 2),
                    "working_capital_req_cr": round(sim_action_a["metrics"]["Working_Capital_Requirement_Cr"], 2)
                },
                "Option_B_SaaS_Accelerate": {
                    "title": "Action B: Accelerate FLYGHT SaaS Fleet Bundling",
                    "probability": "0.85",
                    "ebitda_margin_pct": round(sim_action_b["metrics"]["EBITDA_Margin"], 2),
                    "working_capital_days": round(sim_action_b["metrics"]["Working_Capital_Days"], 1),
                    "net_profit_cr": round(sim_action_b["metrics"]["Net_Profit"], 2),
                    "working_capital_req_cr": round(sim_action_b["metrics"]["Working_Capital_Requirement_Cr"], 2)
                }
            }
        }

        full_trace = {
            "event_id": event_id,
            "step1_event": step1,
            "step2_relevance": step2,
            "step3_dimensions": step3,
            "step4_severity": step4,
            "step5_assumptions": step5,
            "step6_action_trigger": step6,
            "step7_simulations": step7
        }

        return full_trace
