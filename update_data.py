# update_data.py
import yfinance as yf
import pandas as pd
from datetime import datetime

commodities = {
    "Natural Gas": "NG=F",
    "Feeder Cattle": "GF=F"
}

for name, ticker in commodities.items():
    df = yf.download(ticker, period="6mo", interval="1d", progress=False, multi_level_index=False)
    df["% Change"] = df["Close"].pct_change() * 100
    df["7d MA"] = df["Close"].rolling(window=7).mean()
    fname = f"data/{name.replace(' ', '_')}.csv"
    df.to_csv(fname)
    print(f"Updated: {fname}")
