import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

from ui import section_header, apply_theme, PALETTE


def render_optimization():
    if not st.session_state.get("ready"):
        return

    returns = st.session_state["returns"]
    tickers = st.session_state["tickers"]

    num_assets = len(tickers)
    ann_return = returns.mean() * 252
    cov_matrix = returns.cov()  * 252

    np.random.seed(42)
    results = []
    for _ in range(3000):
        w  = np.random.dirichlet(np.ones(num_assets))
        pr = np.dot(w, ann_return)
        pv = np.sqrt(w @ cov_matrix @ w)
        sh = pr / pv
        results.append({"Return": pr, "Volatility": pv, "Sharpe": sh, "Weights": w})

    results_df     = pd.DataFrame(results)
    max_sharpe_idx = results_df["Sharpe"].idxmax()
    max_sharpe     = results_df.loc[max_sharpe_idx]
    min_vol_idx    = results_df["Volatility"].idxmin()
    min_vol        = results_df.loc[min_vol_idx]

    section_header(
        "Efficient Frontier",
        "3,000 simulated portfolios — color denotes Sharpe ratio",
    )

    fig_ef = px.scatter(
        results_df, x="Volatility", y="Return", color="Sharpe",
        color_continuous_scale="Blues",
        labels={"Volatility": "Risk (Ann. Volatility)", "Return": "Expected Return"},
    )
    fig_ef.update_traces(marker=dict(size=3, opacity=0.55))
    fig_ef.add_scatter(
        x=[max_sharpe["Volatility"]], y=[max_sharpe["Return"]],
        mode="markers",
        marker=dict(size=14, color="#1533F0", symbol="star",
                    line=dict(color="white", width=1.5)),
        name="Max Sharpe",
    )
    fig_ef.add_scatter(
        x=[min_vol["Volatility"]], y=[min_vol["Return"]],
        mode="markers",
        marker=dict(size=14, color="#14D2C3", symbol="diamond",
                    line=dict(color="white", width=1.5)),
        name="Min Volatility",
    )
    apply_theme(fig_ef, height=480,
                legend=dict(orientation="h", yanchor="bottom", y=1.02),
                coloraxis_colorbar=dict(
                    tickfont=dict(family="Inter", size=10, color="#9CA3AF"),
                    title=dict(text="Sharpe", font=dict(size=10, color="#9CA3AF")),
                ))
    st.plotly_chart(fig_ef, use_container_width=True)

    st.markdown("---")

    section_header(
        "Optimal Portfolio Allocations",
        "Max Sharpe maximizes return per unit of risk — Min Volatility minimizes risk",
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            '<div style="font-size:0.65rem;letter-spacing:0.14em;text-transform:uppercase;'
            'color:#1533F0;font-weight:600;margin-bottom:0.75rem;font-family:Inter,sans-serif;">'
            '★ Max Sharpe</div>', unsafe_allow_html=True,
        )
        ms_w = pd.DataFrame({
            "Ticker":     tickers,
            "Weight (%)": (max_sharpe["Weights"] * 100).round(2),
        }).sort_values("Weight (%)", ascending=False)

        fig_ms = px.bar(ms_w, x="Ticker", y="Weight (%)",
                        color="Ticker", text="Weight (%)",
                        color_discrete_sequence=PALETTE)
        fig_ms.update_traces(textposition="outside", marker_line_width=0,
                             textfont=dict(size=10))
        apply_theme(fig_ms, height=300, showlegend=False,
                    yaxis_title="Weight (%)", xaxis_title="")
        st.plotly_chart(fig_ms, use_container_width=True)

        m1, m2, m3 = st.columns(3)
        m1.metric("Sharpe",     round(float(max_sharpe["Sharpe"]), 3))
        m2.metric("Return",     f"{float(max_sharpe['Return'])*100:.1f}%")
        m3.metric("Volatility", f"{float(max_sharpe['Volatility'])*100:.1f}%")

    with col2:
        st.markdown(
            '<div style="font-size:0.65rem;letter-spacing:0.14em;text-transform:uppercase;'
            'color:#14D2C3;font-weight:600;margin-bottom:0.75rem;font-family:Inter,sans-serif;">'
            '◆ Min Volatility</div>', unsafe_allow_html=True,
        )
        mv_w = pd.DataFrame({
            "Ticker":     tickers,
            "Weight (%)": (min_vol["Weights"] * 100).round(2),
        }).sort_values("Weight (%)", ascending=False)

        fig_mv = px.bar(mv_w, x="Ticker", y="Weight (%)",
                        color="Ticker", text="Weight (%)",
                        color_discrete_sequence=PALETTE)
        fig_mv.update_traces(textposition="outside", marker_line_width=0,
                             textfont=dict(size=10))
        apply_theme(fig_mv, height=300, showlegend=False,
                    yaxis_title="Weight (%)", xaxis_title="")
        st.plotly_chart(fig_mv, use_container_width=True)

        m1, m2, m3 = st.columns(3)
        m1.metric("Sharpe",     round(float(min_vol["Sharpe"]), 3))
        m2.metric("Return",     f"{float(min_vol['Return'])*100:.1f}%")
        m3.metric("Volatility", f"{float(min_vol['Volatility'])*100:.1f}%")

    st.session_state["max_sharpe_weights"] = max_sharpe["Weights"]
    st.session_state["ann_return"]         = ann_return
    st.session_state["cov_matrix"]         = cov_matrix
