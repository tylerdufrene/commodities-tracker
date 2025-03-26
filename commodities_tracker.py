import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


# Choose time range
time_ranges = {
    '1mo': 30,
    '3mo': 90,
    '6mo':180,
    '1y':365,
    '5y':365*5
}

commodities = {
    "Natural Gas": "Natural_Gas.csv",
    "Feeder Cattle": "Feeder_Cattle.csv"
}

st.title("📈 Commodity Tracker")

selected_range = st.selectbox('Select time range:', list(time_ranges.keys()), index=1)
days_back = time_ranges[selected_range]
cutoff_date = datetime.today() - timedelta(days=days_back)

for name, filename in commodities.items():

    # Download data
    df = pd.read_csv(f"data/{filename}", index_col="Date", parse_dates=True)
    df = df[df.index >= cutoff_date]
    st.subheader(f"{name}")
    latest = df.iloc[-1]
    st.metric("Price", f"${latest['Close']:.2f}", f"{latest['% Change']:.2f}%")
    st.write(f"Volume: {int(latest['Volume'])}")

    # Plot
    fig, ax = plt.subplots()
    df['Close'].plot(ax=ax, label='Close')
    df['7d MA'].plot(ax=ax, linestyle='--', label='7d MA')
    ax.legend()
    st.pyplot(fig)