# correlation.py
"""
Module: correlation.py
Responsibilities:
 - Compute default probabilities from CDS spreads
 - Calculate Basel IRB asset correlations
 - Compute CAPM-based correlations for public tickers
 - Hybrid merging
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm

# CDS PD and Basel IRB

def cds_to_pd(spread_series: pd.Series, recovery_rate: float) -> pd.Series:
    S = spread_series / 10000.0
    lam = S / (1 - recovery_rate)
    pd1y = 1 - np.exp(-lam)
    return pd1y

def basel_irb_corr(pd1y: pd.Series) -> pd.Series:
    num = 1 - np.exp(-50 * pd1y)
    den = 1 - np.exp(-50)
    rho = 0.12 * (num/den) + 0.24 * (1 - num/den)
    return rho

# CAPM-based

def capm_metrics(price_df: pd.DataFrame, market: pd.Series) -> pd.DataFrame:
    betas, sig_i, sig_m = {}, {}, {}
    for t in price_df:
        df = pd.concat([np.log(price_df[t]/price_df[t].shift(1)), np.log(market/market.shift(1))], axis=1).dropna()
        df.columns = ['asset','market']
        X = sm.add_constant(df['market'])
        beta = sm.OLS(df['asset'], X).fit().params['market']
        betas[t] = beta
        sig_i[t] = df['asset'].std(ddof=1)
        sig_m[t] = df['market'].std(ddof=1)
    metrics = pd.DataFrame({'beta':betas,'sigma_asset':sig_i,'sigma_market':sig_m})
    return metrics

# Hybrid merge
def merge_correlations(irb_corr: pd.DataFrame, capm_corr: pd.DataFrame) -> pd.DataFrame:
    combined = irb_corr.copy()
    public = capm_corr.index.intersection(combined.index)
    combined.loc[public, public] = capm_corr.loc[public, public]
    combined = (combined + combined.T)/2
    np.fill_diagonal(combined.values,1.0)
    return combined