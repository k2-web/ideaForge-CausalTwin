import os
import json
from datetime import datetime

class MemoryEngine:
    def __init__(self, storage_dir=None):
        if storage_dir is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.storage_dir = os.path.join(current_dir, "mock_data")
        else:
            self.storage_dir = storage_dir
            
        os.makedirs(self.storage_dir, exist_ok=True)
        self.memory_file = os.path.join(self.storage_dir, "persistent_memory.json")
        self._load_or_initialize_memory()

    def _load_or_initialize_memory(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r") as f:
                    self.memory_data = json.load(f)
                return
            except Exception as e:
                print(f"Error loading memory file ({e}), re-initializing.")
                
        # Initialize default persistent memory structure
        self.memory_data = {
            "company_name": "ideaForge Technology Limited",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "belief_ledger": [
                {
                    "timestamp": "2025-04-15 10:00:00",
                    "assumption_key": "MoD_Disbursement_Lag",
                    "old_value": 45,
                    "new_value": 60,
                    "reason": "MoD defense budget allocation delay announced in Parliament",
                    "event_id": "EVT-2025-001",
                    "impact_severity": "Moderate"
                },
                {
                    "timestamp": "2025-09-20 14:30:00",
                    "assumption_key": "EO_IR_Optical_Payload_Lead_Time",
                    "old_value": 90,
                    "new_value": 120,
                    "reason": "Middle East cargo logistics bottleneck and customs clearance delay",
                    "event_id": "EVT-2025-014",
                    "impact_severity": "Major"
                },
                {
                    "timestamp": "2026-01-10 11:15:00",
                    "assumption_key": "FLYGHT_SaaS_Attach_Rate",
                    "old_value": 0.25,
                    "new_value": 0.35,
                    "reason": "SVAMITVA civil mapping mandate required cloud portal analytics",
                    "event_id": "EVT-2026-003",
                    "impact_severity": "Positive Growth"
                }
            ],
            "decision_history": [
                {
                    "decision_id": "DEC-2025-Q2-01",
                    "date": "2025-06-30",
                    "context": "MoD Disbursement Lag increased to 60 days causing cash flow tension",
                    "chosen_action": "Buffered raw material inventory and arranged working capital line from SBI (INR 30 Cr)",
                    "predicted_outcome": "EBITDA margin maintained at 18.2%, Working Capital expanded to 240 days",
                    "actual_outcome": "Working Capital reached 245 days; interest expense increased by INR 0.8 Cr",
                    "lessons_learned": "Inventory buffering without vendor extended credit line increases net borrowing costs by 10.5% p.a."
                },
                {
                    "decision_id": "DEC-2025-Q4-02",
                    "date": "2025-12-15",
                    "context": "Foreign drone import ban enforced by DGFT",
                    "chosen_action": "Accelerated SWITCH UAV production for Indian Army fast-track tender",
                    "predicted_outcome": "Quarterly revenue surge to INR 160+ Cr",
                    "actual_outcome": "Revenue reached INR 161.2 Cr in Q4 FY25; gross margin expanded to 48%",
                    "lessons_learned": "Sovereign protection policy significantly increases win rate in defense tenders."
                }
            ],
            "state_snapshots": [
                {
                    "quarter": "Q4 FY25",
                    "revenue_cr": 161.2,
                    "ebitda_margin_pct": 23.9,
                    "working_capital_days": 275,
                    "saas_attach_rate": 0.25,
                    "key_highlight": "Record Q4 execution driven by Army SWITCH UAV deliveries"
                },
                {
                    "quarter": "Q3 FY26",
                    "revenue_cr": 121.8,
                    "ebitda_margin_pct": 18.1,
                    "working_capital_days": 228,
                    "saas_attach_rate": 0.32,
                    "key_highlight": "SVAMITVA civil mapping expansion offsets seasonal defense dip"
                }
            ],
            "executive_briefings": []
        }
        self._save_memory()

    def _save_memory(self):
        self.memory_data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.memory_file, "w") as f:
            json.dump(self.memory_data, f, indent=4)

    def revise_belief(self, key, old_val, new_val, reason, event_id="EVT-LIVE", severity="Moderate"):
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "assumption_key": key,
            "old_value": old_val,
            "new_value": new_val,
            "reason": reason,
            "event_id": event_id,
            "impact_severity": severity
        }
        self.memory_data["belief_ledger"].insert(0, entry)
        self._save_memory()

    def log_decision_and_forecast(self, decision_id, context, chosen_action, predicted_outcome, rationale):
        entry = {
            "decision_id": decision_id,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "context": context,
            "chosen_action": chosen_action,
            "predicted_outcome": predicted_outcome,
            "actual_outcome": "Pending Evaluation",
            "lessons_learned": rationale
        }
        self.memory_data["decision_history"].insert(0, entry)
        self._save_memory()

    def log_executive_briefing(self, briefing_text, key_takeaways, recommended_actions):
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "briefing_text": briefing_text,
            "key_takeaways": key_takeaways,
            "recommended_actions": recommended_actions
        }
        self.memory_data["executive_briefings"].insert(0, entry)
        self._save_memory()

    def get_belief_history(self):
        return self.memory_data.get("belief_ledger", [])

    def get_decision_history(self):
        return self.memory_data.get("decision_history", [])

    def get_state_snapshots(self):
        return self.memory_data.get("state_snapshots", [])

    def get_latest_executive_briefing(self):
        briefings = self.memory_data.get("executive_briefings", [])
        if briefings:
            return briefings[0]
        return None

    def get_all_executive_briefings(self):
        return self.memory_data.get("executive_briefings", [])
