import streamlit as st
import yfinance as yf
import pandas as pd


@st.cache_data
def load_data(tickers, start, end):
    raw     = yf.download(tickers, start=start, end=end, auto_adjust=True)
    prices  = raw["Close"]
    returns = prices.pct_change().dropna()
    return prices, returns


@st.cache_data
def load_spy(start, end):
    spy_raw = yf.download("SPY", start=start, end=end, auto_adjust=True)
    close = spy_raw["Close"]
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    close.name = "SPY"
    return close


@st.cache_data
def load_fundamentals(tickers):
    import time
    rows = []
    for t in tickers:
        try:
            info = yf.Ticker(t).info
        except Exception:
            info = {}
        rows.append({
            "Ticker":         t,
            "Sector":         info.get("sector",        "N/A"),
            "Market Cap":     info.get("marketCap",     None),
            "P/E Ratio":      info.get("trailingPE",    None),
            "P/B Ratio":      info.get("priceToBook",   None),
            "Profit Margin":  info.get("profitMargins", None),
            "Debt / Equity":  info.get("debtToEquity",  None),
            "Dividend Yield": info.get("dividendYield", None),
        })
        time.sleep(0.5)
    return pd.DataFrame(rows)
