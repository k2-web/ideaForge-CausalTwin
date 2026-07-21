import numpy as np
import pandas as pd
import statsmodels.api as sm

class IdeaForgeCausalEngine:
    def __init__(self, data_frame):
        self.df = data_frame.copy()
        self.fit_models()

    def fit_models(self):
        """
        Fits a Two-Stage Least Squares (2SLS) Model manually using numpy/statsmodels 
        to ensure mathematically precise residuals and standard errors.
        
        System definition:
        Z (Instrument): MoD_Disbursement_Lag (Days)
        X (Treatment): Working_Capital_Days (Days)
        Y (Outcome): EBITDA_Margin (%)
        W1 (Control): Indigenous_Sourcing_Mix (%)
        W2 (Control): PLI_Subsidy_Receipts (INR Cr)
        S (Control): SaaS_Attach_Rate (%)
        """
        n = len(self.df)
        
        # 1. Prepare variables
        # Endogenous treatment (X)
        self.X_val = self.df["Working_Capital_Days"].values
        # Instrument (Z)
        self.Z_val = self.df["MoD_Disbursement_Lag"].values
        # Controls (W)
        self.W1_val = self.df["Indigenous_Sourcing_Mix"].values
        self.W2_val = self.df["PLI_Subsidy_Receipts"].values
        self.S_val = self.df["SaaS_Attach_Rate"].values
        # Outcome (Y)
        self.Y_val = self.df["EBITDA_Margin"].values
        
        # --- FIRST STAGE: Regress X on Z, W1, S, and Constant ---
        # Matrix of instruments (Z_all)
        self.Z_all = np.column_stack([
            np.ones(n),
            self.Z_val,
            self.W1_val,
            self.S_val
        ])
        
        # Regress X on Z_all
        # X = Z_all * gamma + v
        self.first_stage_model = sm.OLS(self.X_val, self.Z_all).fit()
        self.gamma = self.first_stage_model.params
        
        # Get fitted values of X (X_hat)
        self.X_hat = self.first_stage_model.predict(self.Z_all)
        
        # --- SECOND STAGE: Regress Y on X_hat, W2, S, and Constant ---
        # Matrix of regressors (X_all)
        self.X_all_hat = np.column_stack([
            np.ones(n),
            self.X_hat,
            self.W2_val,
            self.S_val
        ])
        
        # Regress Y on X_all_hat
        # Y = X_all_hat * beta + epsilon
        self.second_stage_model = sm.OLS(self.Y_val, self.X_all_hat).fit()
        self.beta = self.second_stage_model.params
        
        # --- CORRECT THE STANDARD ERRORS FOR 2SLS ---
        # Note: The second stage OLS standard errors are incorrect because they use X_hat residuals.
        # We must calculate residuals using the actual X (X_val) instead of X_hat.
        self.X_all_actual = np.column_stack([
            np.ones(n),
            self.X_val,
            self.W2_val,
            self.S_val
        ])
        
        # True residuals: Y - X_actual * beta
        residuals = self.Y_val - np.dot(self.X_all_actual, self.beta)
        
        # Residual variance s^2 = e'e / (n - k)
        k = self.X_all_actual.shape[1]
        s2 = np.sum(residuals**2) / (n - k)
        
        # Covariance matrix Var(beta) = s^2 * (X_hat' * X_hat)^-1
        x_hat_transpose_x_hat_inv = np.linalg.inv(np.dot(self.X_all_hat.T, self.X_all_hat))
        self.cov_beta = s2 * x_hat_transpose_x_hat_inv
        
        # Standard errors, t-statistics, p-values
        self.se_beta = np.sqrt(np.diag(self.cov_beta))
        self.t_stats = self.beta / self.se_beta
        # Two-tailed p-value from t-distribution
        from scipy import stats
        self.p_values = 2 * (1 - stats.t.cdf(np.abs(self.t_stats), df=n - k))

    def get_first_stage_summary(self):
        """Returns statistics for the first stage instrumental variable regression"""
        params = self.first_stage_model.params
        se = self.first_stage_model.bse
        t_values = self.first_stage_model.tvalues
        p_values = self.first_stage_model.pvalues
        
        index = ["Intercept", "MoD_Disbursement_Lag", "Indigenous_Sourcing_Mix", "SaaS_Attach_Rate"]
        return pd.DataFrame({
            "Coefficient": params,
            "Std Error": se,
            "t-Statistic": t_values,
            "p-Value": p_values
        }, index=index)

    def get_second_stage_summary(self):
        """Returns corrected statistics for the second stage outcome regression"""
        index = ["Intercept", "Working_Capital_Days (Estimated)", "PLI_Subsidy_Receipts", "SaaS_Attach_Rate"]
        return pd.DataFrame({
            "Coefficient": self.beta,
            "Std Error": self.se_beta,
            "t-Statistic": self.t_stats,
            "p-Value": self.p_values
        }, index=index)

    def simulate_counterfactual(self, mod_lag_days=None, import_tariff_shock_pct=0.0, saas_attach_rate_pct=None):
        """
        Executes structural interventions (do-calculus) across operational parameters.
        Returns a dictionary containing simulated financials and key metrics.
        """
        # Baseline (most recent historical quarter, e.g., Q4 FY26)
        baseline = self.df.iloc[-1].copy()
        
        sim = baseline.to_dict()
        sim_log = []
        
        # 1. MoD Disbursement Lag (Z) intervention
        if mod_lag_days is not None:
            sim["MoD_Disbursement_Lag"] = mod_lag_days
            # Calculate counterfactual Working Capital Days (X) using First Stage
            # equation: Working_Capital_Days = gamma_0 + gamma_1 * mod_lag_days + gamma_2 * W1 + gamma_3 * S
            # We preserve historical controls W1 (Indigenous Sourcing) and S (SaaS Attach Rate)
            x_pred = (self.gamma[0] + 
                      self.gamma[1] * mod_lag_days + 
                      self.gamma[2] * sim["Indigenous_Sourcing_Mix"] +
                      self.gamma[3] * sim["SaaS_Attach_Rate"])
            
            wc_delta = x_pred - sim["Working_Capital_Days"]
            sim["Working_Capital_Days"] = x_pred
            sim_log.append(f"MoD Lag changed to {mod_lag_days} days. Working Capital Days simulated at {x_pred:.1f} days (change of {wc_delta:+.1f} days).")
        
        # 2. SaaS Attach Rate (S) intervention
        if saas_attach_rate_pct is not None:
            # saas_attach_rate_pct is in percent (e.g. 35.0 for 35%)
            new_s_fraction = saas_attach_rate_pct / 100.0
            s_delta = new_s_fraction - sim["SaaS_Attach_Rate"]
            sim["SaaS_Attach_Rate"] = new_s_fraction
            sim_log.append(f"SaaS Attach Rate set to {saas_attach_rate_pct}%.")
            
            # Recalculate Working Capital Days based on new SaaS attach rate
            # SaaS clients have faster payment times, which is captured by First Stage gamma[3]
            x_pred = (self.gamma[0] + 
                      self.gamma[1] * sim["MoD_Disbursement_Lag"] + 
                      self.gamma[2] * sim["Indigenous_Sourcing_Mix"] +
                      self.gamma[3] * new_s_fraction)
            sim["Working_Capital_Days"] = x_pred

        # 3. Calculate EBITDA Margin using Second Stage (SCM)
        # EBITDA_Margin = beta_0 + beta_1 * Working_Capital_Days + beta_2 * PLI_Receipts + beta_3 * SaaS_Attach
        ebitda_margin_pred = (self.beta[0] + 
                              self.beta[1] * sim["Working_Capital_Days"] + 
                              self.beta[2] * sim["PLI_Subsidy_Receipts"] + 
                              self.beta[3] * sim["SaaS_Attach_Rate"])
        
        # 4. Supply Chain Tariff / Price Shock intervention
        # This acts directly on COGS, bypassing the OLS linear model for custom accounting flows
        # (reflecting Phase 1 ontology details: Supply Chain Component drives COGS, COGS reduces Gross Margin)
        # Let's say: ideaForge COGS is typically 50-60% of revenue. 
        # Imported optical payloads and autopilot boards make up ~40% of COGS.
        import_share_of_cogs = 0.40
        cogs_baseline_pct = 1 - (sim["Revenue"] - (sim["Revenue"] * 0.55)) / sim["Revenue"] # Baseline COGS fraction (~54%)
        
        # Apply tariff shock to imported component costs
        tariff_multiplier = 1.0 + (import_tariff_shock_pct / 100.0)
        cogs_impact_pct = import_share_of_cogs * (tariff_multiplier - 1.0)
        
        # Adjusted Gross Margin
        sim["Gross_Margin_Pct"] = (1 - cogs_baseline_pct - cogs_impact_pct) * 100
        
        # Apply import cost shock to EBITDA Margin (EBITDA margin drops directly by the COGS increase)
        final_ebitda_margin = ebitda_margin_pred - (cogs_impact_pct * 100)
        sim["EBITDA_Margin"] = final_ebitda_margin
        
        if import_tariff_shock_pct > 0:
            sim_log.append(f"Import cost shock of +{import_tariff_shock_pct}% applied. Gross Margin reduced to {sim['Gross_Margin_Pct']:.1f}%.")

        # 5. Compute actual currency values for Q4 FY26 scale
        # EBITDA = Revenue * EBITDA_Margin
        sim["EBITDA"] = sim["Revenue"] * (sim["EBITDA_Margin"] / 100.0)
        
        # Working Capital impact in Rupees
        # Working Capital Requirement (WCR) = Revenue * (Working Capital Days / 365)
        sim["Working_Capital_Requirement_Cr"] = sim["Revenue"] * (sim["Working_Capital_Days"] / 365.0)
        baseline_wcr = baseline["Revenue"] * (baseline["Working_Capital_Days"] / 365.0)
        sim["Working_Capital_Change_Cr"] = sim["Working_Capital_Requirement_Cr"] - baseline_wcr
        
        # Interest cost on expanded working capital (borrowing cost estimated at 10.5% p.a.)
        borrowing_rate = 0.105
        sim["Additional_Interest_Cost_Cr"] = max(0, sim["Working_Capital_Change_Cr"]) * borrowing_rate
        
        # Net Profit adjusted for interest cost and EBITDA shift
        ebitda_delta = sim["EBITDA"] - baseline["EBITDA"]
        sim["Net_Profit"] = max(0, baseline["Net_Profit"] + ebitda_delta - sim["Additional_Interest_Cost_Cr"])
        
        return {
            "metrics": sim,
            "log": sim_log,
            "coefficients": {
                "first_stage": self.get_first_stage_summary().to_dict(orient="index"),
                "second_stage": self.get_second_stage_summary().to_dict(orient="index")
            }
        }
