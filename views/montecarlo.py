import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from ui import section_header, apply_theme


def render_montecarlo(mc_years: int, initial_investment: int, target_value: int):
    if not st.session_state.get("ready"):
        return

    returns = st.session_state["returns"]
    tickers = st.session_state["tickers"]

    opt_weights = st.session_state.get(
        "max_sharpe_weights",
        np.ones(len(tickers)) / len(tickers),
    )

    port_mu  = np.dot(opt_weights, returns.mean())
    port_sig = np.sqrt(opt_weights @ returns.cov() @ opt_weights)

    trading_days = mc_years * 252
    np.random.seed(42)

    sim_results = []
    for _ in range(1000):
        dr   = np.random.normal(port_mu, port_sig, trading_days)
        path = [initial_investment]
        for r in dr:
            path.append(path[-1] * (1 + r))
        sim_results.append(path)

    sim_df     = pd.DataFrame(sim_results).T
    final_vals = sim_df.iloc[-1]

    section_header(
        "Simulation Summary",
        f"Max-Sharpe portfolio — 1,000 paths over {mc_years}Y horizon",
    )

    prob_goal  = (final_vals >= target_value).mean() * 100
    median_val = final_vals.median()
    p10_val    = final_vals.quantile(0.10)
    p90_val    = final_vals.quantile(0.90)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Median Outcome",                  f"${median_val:,.0f}")
    m2.metric("90th Percentile",                 f"${p90_val:,.0f}")
    m3.metric("10th Percentile",                 f"${p10_val:,.0f}")
    m4.metric(f"Prob. ≥ ${target_value:,.0f}",   f"{prob_goal:.1f}%")

    st.markdown("---")

    section_header(
        "Simulation Paths",
        "200 of 1,000 paths shown — key percentile bands overlaid",
    )

    fig_mc = go.Figure()
    for i in range(200):
        fig_mc.add_trace(go.Scatter(
            x=list(range(trading_days + 1)),
            y=sim_df.iloc[:, i],
            mode="lines",
            line=dict(color="rgba(21,51,240,0.04)", width=1),
            showlegend=False,
        ))

    med_p = sim_df.median(axis=1)
    p10_p = sim_df.quantile(0.10, axis=1)
    p90_p = sim_df.quantile(0.90, axis=1)

    fig_mc.add_trace(go.Scatter(
        x=list(range(trading_days + 1)), y=med_p,
        mode="lines", line=dict(color="#0A0D2C", width=2), name="Median",
    ))
    fig_mc.add_trace(go.Scatter(
        x=list(range(trading_days + 1)), y=p90_p,
        mode="lines", line=dict(color="#10B981", width=1.5, dash="dash"),
        name="90th Pct",
    ))
    fig_mc.add_trace(go.Scatter(
        x=list(range(trading_days + 1)), y=p10_p,
        mode="lines", line=dict(color="#EF4444", width=1.5, dash="dash"),
        name="10th Pct",
    ))
    fig_mc.add_hline(
        y=target_value, line_dash="dot", line_color="#1533F0",
        annotation_text=f"Goal  ${target_value:,.0f}",
        annotation_position="bottom right",
        annotation_font=dict(color="#1533F0", size=10),
    )
    apply_theme(fig_mc, height=480,
                xaxis_title="Trading Days",
                yaxis_title="Portfolio Value ($)",
                legend=dict(orientation="h", yanchor="bottom", y=1.02),
                hovermode="x")
    st.plotly_chart(fig_mc, use_container_width=True)

    st.markdown("---")

    section_header(
        "Distribution of Final Values",
        "Outcome spread across all 1,000 simulations at the horizon",
    )

    fig_dist = px.histogram(
        final_vals, nbins=60,
        labels={"value": "Final Portfolio Value ($)", "count": "Simulations"},
        color_discrete_sequence=["#1533F0"],
    )
    fig_dist.update_traces(opacity=0.75, marker_line_width=0)
    fig_dist.add_vline(
        x=initial_investment, line_dash="dash", line_color="#EF4444",
        annotation_text="Initial",
        annotation_position="top right",
        annotation_font=dict(color="#EF4444", size=10),
    )
    fig_dist.add_vline(
        x=target_value, line_dash="dash", line_color="#10B981",
        annotation_text="Goal",
        annotation_position="top left",
        annotation_font=dict(color="#10B981", size=10),
    )
    apply_theme(fig_dist, height=340, showlegend=False)
    st.plotly_chart(fig_dist, use_container_width=True)
