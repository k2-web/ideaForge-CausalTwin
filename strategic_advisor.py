class StrategicAdvisorEngine:
    def __init__(self, causal_engine, memory_engine):
        self.causal_engine = causal_engine
        self.memory_engine = memory_engine

    def generate_strategic_recommendations(self, reasoning_trace):
        """
        Synthesizes top-tier management consulting (McKinsey, Bain, BCG) and 
        Private Equity perspectives into a prioritized Executive Action Matrix.
        """
        event_info = reasoning_trace.get("step1_event", {})
        severity = reasoning_trace.get("step4_severity", {}).get("severity_level", "MODERATE")
        sims = reasoning_trace.get("step7_simulations", {}).get("simulations", {})

        no_action = sims.get("Option_No_Action", {})
        action_a = sims.get("Option_A_Supply_Mitigation", {})
        action_b = sims.get("Option_B_SaaS_Accelerate", {})

        recommendations = []

        # --- 1. MCKINSEY OPERATIONAL & SUPPLY CHAIN STRATEGY ---
        rec_supply = {
            "rec_id": "REC-MCK-01",
            "framework": "McKinsey Operational Excellence & Supply Chain Resilience",
            "title": "Accelerate Domestic Component Sourcing & Sanand Fab Supplier Qualifying",
            "category": "Supply Chain & Manufacturing",
            "executive_owner": "Chief Operating Officer (COO)",
            "priority": "HIGH" if "EXISTENTIAL" in severity or "MAJOR" in severity else "MEDIUM",
            "timeline": "30 - 60 Days",
            "problem_statement": "Import dependency on Israeli/US optical sensors and Taiwanese autopilot ICs exposes gross margins to tariff shocks and logistics lead-time bottlenecks.",
            "recommended_action": "Execute fast-track vendor qualification for local assembly under the Indian Semiconductor Mission (ISM) in Sanand, Gujarat. Transition autopilot microcontrollers from 100% import to 60% local assembly.",
            "financial_impact": f"Reclaims +{round(action_a.get('ebitda_margin_pct', 0) - no_action.get('ebitda_margin_pct', 0), 2)}% in EBITDA Margin; saves INR {round(abs(action_a.get('working_capital_req_cr', 0) - no_action.get('working_capital_req_cr', 0)), 1)} Cr in Working Capital.",
            "risk_rating": "Medium (Requires strict DGFT defense certification)",
            "mitigant": "Dual-source critical optical sensors while ramping local IMU testing."
        }
        recommendations.append(rec_supply)

        # --- 2. BAIN & COMPANY SAAS MONETIZATION STRATEGY ---
        rec_saas = {
            "rec_id": "REC-BAIN-02",
            "framework": "Bain & Company SaaS Attach & Customer Retention Engine",
            "title": "Mandate FLYGHT Patrol Software Bundling on SVAMITVA & Commercial Fleets",
            "category": "Software & Recurring Revenue",
            "executive_owner": "Chief Product Officer (CPO) & VP Commercial Sales",
            "priority": "HIGH",
            "timeline": "Immediate (0 - 30 Days)",
            "problem_statement": "Pure hardware manufacturing sales suffer from lumpy procurement cycles and inventory holding costs.",
            "recommended_action": "Bundle 1-year complimentary FLYGHT Patrol SaaS subscriptions with all SWITCH UAV and Q6 civil sales, transitioning to auto-renewing ARR contracts at INR 1.5 Lakhs/drone/year.",
            "financial_impact": f"Boosts EBITDA Margin to {action_b.get('ebitda_margin_pct', 0)}% (+{round(action_b.get('ebitda_margin_pct', 0) - no_action.get('ebitda_margin_pct', 0), 2)}% expansion) and increases Net Profit to ₹{action_b.get('net_profit_cr', 0)} Cr.",
            "risk_rating": "Low (High customer stickiness in GIS drone fleet management)",
            "mitigant": "Provide API integration with Survey of India GIS portals."
        }
        recommendations.append(rec_saas)

        # --- 3. BCG MATRIX PORTFOLIO POSITIONING ---
        rec_bcg = {
            "rec_id": "REC-BCG-03",
            "framework": "BCG Growth-Share Matrix Optimization",
            "title": "Protect 'Cash Cow' (SWITCH UAV) while Scaling 'Star' (FLYGHT SaaS Platform)",
            "category": "Portfolio & Product Strategy",
            "executive_owner": "Chief Executive Officer (CEO) & Head of Strategy",
            "priority": "MEDIUM",
            "timeline": "60 - 90 Days",
            "problem_statement": "SWITCH UAV provides 65% of defense revenue but faces competitive quadcopter pressure in civil markets.",
            "recommended_action": "Reallocate 15% of civil drone R&D spend toward high-margin payload integrations (LIDAR, Thermal IR) for heavy-lift Q6 UAVs targeting industrial port surveillance.",
            "financial_impact": "Stabilizes overall gross margin floor at 46.5% while expanding high-margin enterprise accounts.",
            "risk_rating": "Low",
            "mitigant": "Focus marketing efforts on enterprise infrastructure partners (e.g. Adani Ports, NTPC)."
        }
        recommendations.append(rec_bcg)

        # --- 4. PRIVATE EQUITY CAPITAL ALLOCATION STRATEGY ---
        rec_pe = {
            "rec_id": "REC-PE-04",
            "framework": "Private Equity Working Capital Optimization & Capital Allocation",
            "title": "Establish Milestone-Linked Vendor Credit & Restructure MoD Billing Cycles",
            "category": "Finance & Working Capital",
            "executive_owner": "Chief Financial Officer (CFO)",
            "priority": "HIGH" if "EXISTENTIAL" in severity or "MAJOR" in severity else "MEDIUM",
            "timeline": "30 Days",
            "problem_statement": "MoD disbursement delays expand working capital to 240+ days, incurring 10.5% p.a. borrowing costs on short-term bank debt.",
            "recommended_action": "Negotiate 90-day extended credit terms with carbon fiber and battery suppliers linked back-to-back with Indian Army milestone acceptance certificates.",
            "financial_impact": f"Reduces annual debt interest expense by ₹{round(no_action.get('working_capital_req_cr', 0) * 0.105 * 0.25, 2)} Cr.",
            "risk_rating": "Medium (Supplier resistance to extended terms)",
            "mitigant": "Offer preferred volume purchase guarantees in exchange for extended payables."
        }
        recommendations.append(rec_pe)

        summary_matrix = {
            "event_title": event_info.get("summary", ""),
            "severity_assessment": severity,
            "recommended_primary_action": rec_saas["title"] if action_b.get("ebitda_margin_pct", 0) > action_a.get("ebitda_margin_pct", 0) else rec_supply["title"],
            "action_matrix": recommendations
        }

        return summary_matrix
