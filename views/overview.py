import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from ui import section_header, apply_theme, PALETTE


def render_overview():
    if not st.session_state.get("ready"):
        return

    prices  = st.session_state["prices"]
    returns = st.session_state["returns"]
    spy     = st.session_state["spy"]
    tickers = st.session_state["tickers"]

    section_header(
        "Normalized Price Performance",
        "All assets rebased to 100 at start date — SPY shown as benchmark",
    )

    all_prices = prices.join(spy, how="left")
    normalized = (all_prices / all_prices.iloc[0]) * 100

    fig_norm = go.Figure()
    for i, col in enumerate(tickers):
        fig_norm.add_trace(go.Scatter(
            x=normalized.index, y=normalized[col],
            name=col, mode="lines",
            line=dict(color=PALETTE[i % len(PALETTE)], width=1.75),
        ))
    fig_norm.add_trace(go.Scatter(
        x=normalized.index, y=normalized["SPY"],
        name="SPY", mode="lines",
        line=dict(color="#14D2C3", width=1.5, dash="dot"), opacity=0.8,
    ))
    apply_theme(fig_norm, height=420,
                yaxis_title="Indexed (base 100)",
                legend=dict(orientation="h", yanchor="bottom", y=1.02),
                hovermode="x unified")
    st.plotly_chart(fig_norm, use_container_width=True)

    st.markdown("---")

    section_header(
        "Return & Volatility Summary",
        "Annualized figures — SPY included for benchmark comparison",
    )

    ann_return = returns.mean() * 252
    ann_vol    = returns.std()  * np.sqrt(252)
    sharpe     = ann_return / ann_vol

    spy_returns = spy.pct_change().dropna()
    spy_ar      = spy_returns.mean() * 252
    spy_av      = spy_returns.std()  * np.sqrt(252)
    spy_sh      = spy_ar / spy_av

    stats_df = pd.DataFrame({
        "Ticker":          tickers + ["SPY"],
        "Ann. Return":     [f"{v*100:.1f}%" for v in ann_return] + [f"{spy_ar*100:.1f}%"],
        "Ann. Volatility": [f"{v*100:.1f}%" for v in ann_vol]    + [f"{spy_av*100:.1f}%"],
        "Sharpe Ratio":    [f"{v:.2f}"       for v in sharpe]     + [f"{spy_sh:.2f}"],
    })
    st.dataframe(stats_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    section_header(
        "Correlation Matrix",
        "Lower values indicate better portfolio diversification",
    )

    corr = returns.corr().round(2)
    fig_corr = px.imshow(
        corr, text_auto=True,
        color_continuous_scale="RdBu_r",
        zmin=-1, zmax=1,
    )
    fig_corr.update_traces(
        textfont=dict(family="Inter", size=11, color="#0A0D2C")
    )
    apply_theme(fig_corr, height=420,
                coloraxis_colorbar=dict(
                    tickfont=dict(family="Inter", size=10, color="#9CA3AF"),
                    title=dict(text="", font=dict(size=10)),
                ))
    st.plotly_chart(fig_corr, use_container_width=True)
