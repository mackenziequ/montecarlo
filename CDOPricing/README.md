# CDO Pricing Pipeline

# Monte Carlo CDO Pricing and Correlation Impact

## Overview
This project implements a hybrid Monte Carlo framework to price a five-year, four-tranche Collateralized Debt Obligation (CDO) referencing a high-yield North American CDX index. The model combines empirical equity correlations for public firms with regulatory correlation floors for private issuers to simulate default dynamics and calculate fair tranche spreads.

## Key Features
- **Hybrid Correlation Framework**: 
  - Public firms: CAPM-beta derived correlations from weekly equity returns (2010-2024)
  - Private firms: Basel II/III IRB PD-driven correlation floors (12%-24% range)
- **Default Probability Calibration**: Flat-hazard assumption with 40% recovery rate
- **Monte Carlo Simulation**: 100,000 default-time paths using one-factor Gaussian copula
- **Tranche Sensitivity Analysis**: Uniform correlation stress testing (±10%)

## Tranche Pricing Results
| Tranche | Attachment | Detachment | Fair Spread | Standard Error |
|---------|------------|------------|-------------|----------------|
| Equity | 0% | 5% | 90.0 bp | 0.69 bp |
| Mezzanine | 5% | 15% | 11.0 bp | 0.08 bp |
| Senior | 15% | 25% | 1.3 bp | 0.02 bp |
| Super Senior | 25% | 100% | 0.015 bp | 0.001 bp |

## Correlation Sensitivity
- **Equity Tranche**: Highly sensitive (+19 bp for +10% correlation bump)
- **Mezzanine**: Moderate sensitivity (+3 bp)
- **Senior/Super Senior**: Minimal sensitivity (<1 bp)

## Methodology Highlights
1. **Data Processing**: 92-name high-yield CDX universe with CDS spreads
2. **Default Intensity**: λ = S/(1-R) with R=40\% recovery rate
3. **Correlation Matrix**:
   - Public firms: CAPM-based equity correlations (0.0458-0.4955 range)
   - Private firms: Basel IRB formula ρ = 0.12×(1-e^(-50PD))/(1-e^(-50)) + 0.24×(1 - ...)
4. **Monte Carlo Engine**: Simulates default times, tranche losses, and premium accruals

## Limitations
- One-factor Gaussian copula may understate tail risk
- Flat-hazard assumption ignores term structure
- Uniform 40\% recovery rate across all names
- No discounting in cash flow calculations

## Dependencies
- Python with pandas, numpy, scipy
- yfinance for equity data
- Standard scientific computing stack


## Structure

- `data_processing.py`: Load CDS and price data
- `correlation.py`: Compute IRB and CAPM correlations, merge hybrid matrix
- `monte_carlo.py`: Price CDO tranches via simulation
- `main.ipynb`: Orchestrates the workflow, generates results and figures

## Requirements
- Python 3.9+
- pandas, numpy, scipy, statsmodels, yfinance, matplotlib

## Usage
1. Adjust paths in `main.ipynb`
2. Run `main.ipynb` end-to-end
3. Inspect outputs: tranche spreads, sensitivity graphs

## Notes
- Assumes flat hazard with constant recovery (40%) and zero discounting
- Modify `tranches`, `tenor`, and correlation settings as needed
"""

## References
- Hull (2022) - Derivatives pricing
- Basel Committee on Banking Supervision (2005) - IRB framework
- Li (2000) - Gaussian copula model
- Moody's Ultimate Recovery Database & S&P Global recovery studies
