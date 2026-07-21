import os
import pandas as pd
import json

class IdeaForgeIngestionPipeline:
    def __init__(self, data_dir=None):
        if data_dir is None:
            # Default to local directory in project
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.data_dir = os.path.join(current_dir, "mock_data")
        else:
            self.data_dir = data_dir
            
        os.makedirs(self.data_dir, exist_ok=True)
        self._generate_mock_files_if_missing()

    def _generate_mock_files_if_missing(self):
        # 1. Quarterly Ind AS filings (Q1 FY24 to Q4 FY26)
        bse_file = os.path.join(self.data_dir, "bse_filings_quarterly.csv")
        if not os.path.exists(bse_file):
            # Let's create realistic time-series data for ideaForge
            # Demonstrating lumpy payment cycles, Q4 spikes, and working capital shifts
            quarters_data = {
                "Quarter": ["Q1 FY24", "Q2 FY24", "Q3 FY24", "Q4 FY24", 
                            "Q1 FY25", "Q2 FY25", "Q3 FY25", "Q4 FY25",
                            "Q1 FY26", "Q2 FY26", "Q3 FY26", "Q4 FY26"],
                "Revenue": [68.5, 48.2, 90.1, 142.4, 75.1, 56.4, 98.6, 161.2, 85.3, 71.2, 121.8, 202.4],
                "EBITDA": [13.2, 7.8, 16.5, 34.2, 12.8, 8.4, 18.2, 38.6, 15.1, 11.5, 22.1, 48.5],
                "Net_Profit": [6.8, 3.1, 8.9, 21.4, 5.2, 3.5, 9.8, 23.1, 8.2, 5.4, 12.6, 30.1],
                "MoD_Disbursement_Lag": [45, 60, 90, 110, 40, 50, 75, 95, 30, 45, 60, 80],
                "Working_Capital_Days": [210, 225, 260, 290, 205, 215, 245, 275, 195, 208, 228, 248],
                "Indigenous_Sourcing_Mix": [0.45, 0.46, 0.48, 0.50, 0.52, 0.54, 0.55, 0.58, 0.60, 0.61, 0.62, 0.65],
                "PLI_Subsidy_Receipts": [0.0, 4.2, 0.0, 8.5, 0.0, 5.0, 0.0, 10.2, 2.5, 6.0, 0.0, 12.0],
                "SaaS_Attach_Rate": [0.12, 0.14, 0.15, 0.17, 0.20, 0.22, 0.23, 0.25, 0.28, 0.30, 0.32, 0.35]
            }
            df = pd.DataFrame(quarters_data)
            df.to_csv(bse_file, index=False)
            print(f"Created mock BSE filings at {bse_file}")

        # 2. Annual Reports (Form MGT-7 & BRSR Disclosures)
        brsr_file = os.path.join(self.data_dir, "annual_report_brsr_fy25.json")
        if not os.path.exists(brsr_file):
            brsr_data = {
                "company_name": "ideaForge Technology Limited",
                "fiscal_year": "FY2024-25",
                "document_reference": "BRSR/FY25/AR-01",
                "key_disclosures": {
                    "indigenous_sourcing_pct": {
                        "value": 58.0,
                        "unit": "%",
                        "audit_trail": "BRSR Section C, Principle 3, Page 22"
                    },
                    "rd_expenditure": {
                        "capitalized_cr": 24.5,
                        "expensed_cr": 12.8,
                        "total_cr": 37.3,
                        "audit_trail": "Notes to Ind AS Accounts, Note 14 (Intangible Assets), Page 84"
                    },
                    "working_capital_cycle": {
                        "inventory_days": 135,
                        "receivable_days": 110,
                        "payable_days": 40,
                        "net_wc_days": 205,
                        "audit_trail": "Management Discussion & Analysis (MD&A), Section 4, Page 41"
                    },
                    "employee_benefit_expenses": {
                        "total_cr": 45.2,
                        "share_based_payments_esop_cr": 8.4,
                        "audit_trail": "Profit & Loss Account Schedule 22, Page 68"
                    }
                }
            }
            with open(brsr_file, "w") as f:
                json.dump(brsr_data, f, indent=4)
            print(f"Created mock BRSR annual disclosures at {brsr_file}")

        # 3. Government Procurement Notices (GeM & MoD CPPP)
        tenders_file = os.path.join(self.data_dir, "gem_defense_tenders.json")
        if not os.path.exists(tenders_file):
            tenders_data = [
                {
                    "tender_id": "GEM/2026/B/99812",
                    "authority": "Ministry of Defence (Indian Army)",
                    "portal": "Government e-Marketplace (GeM)",
                    "publish_date": "2026-02-15",
                    "product_category": "Micro UAV / VTOL Drone Platforms",
                    "quantity": 180,
                    "estimated_value_cr": 45.0,
                    "indigenous_content_requirement": ">= 60%",
                    "technical_specs": {
                        "flight_endurance": ">= 90 mins",
                        "payload": "Day/Night EO/IR Optical sensor",
                        "operational_altitude": "Up to 4500m"
                    },
                    "status": "Under Evaluation (Bid opened Mar 10, 2026)",
                    "audit_trail": "GeM Portal Tender Summary Sheet - ID 99812, Page 1"
                },
                {
                    "tender_id": "CPPP/2026/MOD/ARMY/321",
                    "authority": "Indian Army Aviation Corps",
                    "portal": "CPPP (Central Public Procurement Portal)",
                    "publish_date": "2026-04-01",
                    "product_category": "High-End ISR UAV (Tactical VTOL)",
                    "quantity": 120,
                    "estimated_value_cr": 115.0,
                    "indigenous_content_requirement": ">= 50%",
                    "technical_specs": {
                        "flight_endurance": ">= 120 mins",
                        "payload": "Dual EO/IR sensor + Laser Range Finder",
                        "range": ">= 15 km"
                    },
                    "status": "Financial Bid Opened (ideaForge L1 bidder)",
                    "audit_trail": "CPPP Bid Opening Report, Ref CPPP/2026/321, Page 3"
                },
                {
                    "tender_id": "GEM/2026/B/88219",
                    "authority": "Survey of India (SVAMITVA Scheme)",
                    "portal": "GeM Tenders",
                    "publish_date": "2026-05-12",
                    "product_category": "Survey Grade Quadcopters",
                    "quantity": 300,
                    "estimated_value_cr": 36.0,
                    "indigenous_content_requirement": ">= 60%",
                    "technical_specs": {
                        "flight_endurance": ">= 45 mins",
                        "payload": "24MP RGB Mapping Camera & RTK GPS"
                    },
                    "status": "Awarded to ideaForge (Contract signed Jun 01, 2026)",
                    "audit_trail": "SVAMITVA Contract Award Registry - SoI/2026/88219, Page 2"
                }
            ]
            with open(tenders_file, "w") as f:
                json.dump(tenders_data, f, indent=4)
            print(f"Created mock GeM tenders at {tenders_file}")

        # 4. Custom Import logs (Customs ICES API)
        import_file = os.path.join(self.data_dir, "customs_import_logs.csv")
        if not os.path.exists(import_file):
            import_data = {
                "Log_ID": ["IMP-2025-081", "IMP-2025-095", "IMP-2025-112", "IMP-2026-004", "IMP-2026-021", "IMP-2026-042"],
                "Date": ["2025-10-12", "2025-11-20", "2025-12-15", "2026-01-22", "2026-02-28", "2026-03-18"],
                "Consignee": "ideaForge Technology Ltd",
                "HS_Code": [85258900, 90142000, 85423100, 85258900, 85423100, 90142000],
                "Item_Description": [
                    "EO/IR Optical Payload Dual Sensor Module",
                    "High-Accuracy IMU Inertial Sensors",
                    "Autopilot Microcontrollers (STM32H7 series)",
                    "EO/IR Optical Payload Dual Sensor Module",
                    "Autopilot Microcontrollers (STM32H7 series)",
                    "High-Accuracy IMU Inertial Sensors"
                ],
                "Supplier": ["Elbit Systems Ltd (Israel)", "Honeywell Aerospace (USA)", "STMicroelectronics (Taiwan)", "Elbit Systems Ltd (Israel)", "STMicroelectronics (Taiwan)", "Honeywell Aerospace (USA)"],
                "Declared_Value_INR_Lakhs": [12.4, 1.8, 0.45, 14.2, 0.52, 2.1],
                "Lead_Time_Days": [115, 65, 88, 130, 92, 70],
                "Tariff_Rate_Pct": [10.0, 7.5, 7.5, 15.0, 7.5, 7.5],
                "Audit_Trail": [
                    "ICES Export-Import Cargo Logs, Chennai Port Bill of Entry #882103",
                    "ICES Air Cargo Logs, Bangalore Customs Port BOE #771204",
                    "ICES Air Cargo Logs, Mumbai Customs Port BOE #991209",
                    "ICES Export-Import Cargo Logs, Chennai Port BOE #110294",
                    "ICES Air Cargo Logs, Mumbai Customs Port BOE #220194",
                    "ICES Air Cargo Logs, Bangalore Customs Port BOE #330291"
                ]
            }
            df_imp = pd.DataFrame(import_data)
            df_imp.to_csv(import_file, index=False)
            print(f"Created mock custom import logs at {import_file}")

    def load_quarterly_financials(self):
        file_path = os.path.join(self.data_dir, "bse_filings_quarterly.csv")
        df = pd.read_csv(file_path)
        if "EBITDA_Margin" not in df.columns:
            df["EBITDA_Margin"] = (df["EBITDA"] / df["Revenue"]) * 100.0
        return df

    def load_annual_report_disclosures(self):
        file_path = os.path.join(self.data_dir, "annual_report_brsr_fy25.json")
        with open(file_path, "r") as f:
            return json.load(f)

    def load_government_tenders(self):
        file_path = os.path.join(self.data_dir, "gem_defense_tenders.json")
        with open(file_path, "r") as f:
            return json.load(f)

    def load_import_logs(self):
        file_path = os.path.join(self.data_dir, "customs_import_logs.csv")
        return pd.read_csv(file_path)

    def get_audit_trail_reference(self, domain, key):
        """Returns the specific document name and page number for audits"""
        if domain == "financials":
            if key == "indigenous_sourcing_pct":
                return "ideaForge BRSR Disclosure FY25, Section C, Principle 3, Page 22"
            elif key == "rd_capitalized":
                return "ideaForge Annual Report FY25, Notes to Ind AS Accounts, Note 14, Page 84"
            elif key == "esop_benefit":
                return "ideaForge Annual Report FY25, P&L Account Schedule 22, Page 68"
            elif key == "working_capital":
                return "ideaForge Annual Report FY25, Management Discussion & Analysis (MD&A), Page 41"
            else:
                return "BSE filings (Q1 FY24 - Q4 FY26), Financial Disclosure Notes"
        elif domain == "tenders":
            tenders = self.load_government_tenders()
            for t in tenders:
                if t["tender_id"] == key:
                    return f"{t['authority']} Tender {t['tender_id']}, {t['audit_trail']}"
            return "GeM Procurement Portal Notification Registry"
        elif domain == "imports":
            imports = self.load_import_logs()
            match = imports[imports["Log_ID"] == key]
            if not match.empty:
                return f"Chennai/Mumbai Custom House Bill of Entry, {match.iloc[0]['Audit_Trail']}"
            return "ICES Indian Custom House Cargo logs"
        return "Regulatory Disclosure Summary Sheet"
