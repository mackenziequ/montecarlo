# data_processing.py
"""
Module: data_processing.py
Responsibilities:
 - Load and clean CDS and ticker data
 - Download historical price data for public tickers
 - Handle missing tickers mapping
"""
import pandas as pd
import yfinance as yf

def load_cdx_data(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df = df.dropna(subset=['CDS Spread'])
    df[['ticker','CountryCode']] = df['parent ticker exchange'].str.split(' ',1,expand=True)
    return df

def download_prices(tickers: list[str], start: str, end: str, freq: str='W') -> pd.DataFrame:
    prices = {}
    for t in tickers:
        hist = yf.download(t, start=start, end=end, progress=False, auto_adjust=False)
        if hist.empty or 'Close' not in hist:
            continue
        adj = hist['Close'].resample(freq).last().dropna()
        prices[t] = adj
    price_df = pd.DataFrame(prices)
    return price_df
