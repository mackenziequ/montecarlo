# monte_carlo.py
"""
Module: monte_carlo.py
Responsibilities:
 - Simulate default times via Gaussian copula
 - Price CDO tranches and compute fair spreads
 - Sensitivity analysis
"""
import numpy as np
import pandas as pd
from scipy.stats import norm, expon

def price_cdo_tranches(tenor, corr, intensity, recovery_rate, tranches, steps=100_000, seed=20250330) -> pd.DataFrame:
    np.random.seed(seed)
    N = len(intensity)
    Z = np.random.multivariate_normal(np.zeros(N), corr, size=steps)
    U = norm.cdf(Z)
    taus = expon(scale=1/intensity).ppf(U)
    results = []
    for a,d in tranches:
        q_sims = []
        for i in range(steps):
            tau = np.sort(taus[i])
            events = np.concatenate(([0], tau[tau<=tenor], [tenor]))
            tranche_loss=0; prem=0; default_leg=0
            for k in range(1,len(events)):
                t0,t1 = events[k-1],events[k]
                num0 = np.searchsorted(tau,t0,'right'); L0 = num0*(1-recovery_rate)/N
                O0 = np.clip((d-L0)/(d-a),0,1); prem += O0*(t1-t0)
                for td in tau[(tau>t0)&(tau<=t1)]:
                    numd = np.searchsorted(tau,td,'right'); Ld = numd*(1-recovery_rate)/N
                    ntl= np.clip((Ld-a)/(d-a),0,1)
                    default_leg += (ntl-tranche_loss); tranche_loss=ntl
            q_sims.append(default_leg/prem)
        q=np.mean(q_sims); se=np.std(q_sims,ddof=1)/np.sqrt(steps)
        results.append((a,d,q,se))
    return pd.DataFrame(results,columns=['attach','detach','fair_spread','stderr'])
