import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

from ui import section_header, apply_theme, PALETTE


def render_fundamentals():
    if not st.session_state.get("ready"):
        return

    fundamentals = st.session_state["fundamentals"]
    tickers      = st.session_state["tickers"]

    opt_weights = st.session_state.get(
        "max_sharpe_weights",
        np.ones(len(tickers)) / len(tickers),
    )

    section_header(
        "Fundamental Statistics",
        "Key metrics per holding — sourced from Yahoo Finance",
    )

    display_df = fundamentals.copy()
    display_df["Market Cap"]    = display_df["Market Cap"].apply(
        lambda x: f"${x/1e9:.1f}B" if pd.notna(x) else "—")
    display_df["P/E Ratio"]     = display_df["P/E Ratio"].apply(
        lambda x: f"{x:.1f}x" if pd.notna(x) else "—")
    display_df["P/B Ratio"]     = display_df["P/B Ratio"].apply(
        lambda x: f"{x:.1f}x" if pd.notna(x) else "—")
    display_df["Profit Margin"] = display_df["Profit Margin"].apply(
        lambda x: f"{x*100:.1f}%" if pd.notna(x) else "—")
    display_df["Debt / Equity"] = display_df["Debt / Equity"].apply(
        lambda x: f"{x:.1f}" if pd.notna(x) else "—")
    display_df["Dividend Yield"] = display_df["Dividend Yield"].apply(
        lambda x: f"{x:.2f}%" if pd.notna(x) else "—")

    st.dataframe(display_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    section_header(
        "Sector Breakdown",
        "Portfolio weight by sector — based on Max-Sharpe allocation",
    )

    sector_df = pd.DataFrame({
        "Ticker": tickers,
        "Sector": fundamentals["Sector"].values,
        "Weight": opt_weights,
    })
    sector_grouped = (
        sector_df.groupby("Sector")["Weight"]
        .sum().reset_index()
        .sort_values("Weight", ascending=False)
    )
    sector_grouped["Weight (%)"] = (sector_grouped["Weight"] * 100).round(2)

    col1, col2 = st.columns(2)

    with col1:
        fig_pie = px.pie(
            sector_grouped, names="Sector", values="Weight",
            hole=0.45, color_discrete_sequence=PALETTE,
        )
        fig_pie.update_traces(
            textposition="inside", textinfo="percent+label",
            textfont=dict(family="Inter", size=11),
            marker=dict(line=dict(color="white", width=2)),
        )
        apply_theme(fig_pie, height=360, showlegend=False)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        fig_bar = px.bar(
            sector_grouped, x="Weight (%)", y="Sector",
            orientation="h", color="Sector", text="Weight (%)",
            color_discrete_sequence=PALETTE,
        )
        fig_bar.update_traces(marker_line_width=0, textfont=dict(size=10))
        apply_theme(fig_bar, height=360, showlegend=False, yaxis_title="")
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    section_header(
        "Allocation vs. Valuation",
        "Bubble size = portfolio weight — spot if optimizer is over-weighting expensive stocks",
    )

    val_df = fundamentals.copy()
    val_df["Weight (%)"] = (opt_weights * 100).round(2)
    val_df_clean = val_df.dropna(subset=["P/E Ratio", "Profit Margin"])

    if not val_df_clean.empty:
        fig_bubble = px.scatter(
            val_df_clean,
            x="P/E Ratio", y="Profit Margin",
            size="Weight (%)", color="Ticker", text="Ticker",
            color_discrete_sequence=PALETTE,
            labels={"P/E Ratio": "P/E Ratio", "Profit Margin": "Profit Margin"},
        )
        fig_bubble.update_traces(
            textposition="top center",
            textfont=dict(size=10),
            marker=dict(line=dict(color="white", width=1.5)),
        )
        apply_theme(fig_bubble, height=420, showlegend=False)
        st.plotly_chart(fig_bubble, use_container_width=True)
    else:
        st.info("Insufficient fundamental data to render valuation chart.")
