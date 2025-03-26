import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


# Choose time range
period = st.selectbox("Select time range:", ["1mo", "3mo", "6mo", "1y"])

commodities = {
    "Natural Gas": "Natural_Gas.csv",
    "Feeder Cattle": "Feeder_Cattle.csv"
}

st.title("📈 Commodity Tracker")

for name, filename in commodities.items():

    # Download data
    df = pd.read_csv(f"data/{filename}", index_col="Date", parse_dates=True)
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