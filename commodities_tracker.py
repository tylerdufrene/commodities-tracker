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
commodity = st.selectbox('Select a commodity to explore:', ['Natural Gas'])

selected_range = st.selectbox('Select time range:', list(time_ranges.keys()), index=1)
days_back = time_ranges[selected_range]
cutoff_date = datetime.today() - timedelta(days=days_back)

if commodity == 'Natural Gas':
    st.subheader('📊 Price Overview')

    # Download data
    df = pd.read_csv(f"data/Natural_Gas.csv", index_col="Date", parse_dates=True)
    df = df[df.index >= cutoff_date]
    latest = df.iloc[-1]
    st.metric("Price", f"${latest['Close']:.2f}", f"{latest['% Change']:.2f}%")

    # Plot
    fig, ax = plt.subplots()
    df['Close'].plot(ax=ax, label='Close')
    df['7d MA'].plot(ax=ax, linestyle='--', label='7d MA')
    ax.legend()
    st.pyplot(fig)

    tabs = st.tabs(["📦 Storage Levels"])#, "🔁 Imports & Exports", "🌦 Weather & Seasonality", "📰 News & Events"])
    with tabs[0]:
        st.subheader("EIA Storage")
        try:
            eia_df = pd.read_csv("data/eia_storage.csv", parse_dates=["period"], index_col=0)
            eia_df = eia_df[eia_df["period"] >= cutoff_date]
            st.line_chart(eia_df.set_index("period")["value"])
            st.dataframe(eia_df.tail())
        except FileNotFoundError:
            st.warning("Storage data not found. Please run the EIA data update script.")