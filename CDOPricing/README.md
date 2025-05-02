# CDO Pricing Pipeline

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
