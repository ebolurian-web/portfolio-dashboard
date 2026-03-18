import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from ui import section_header, apply_theme


def render_risk(initial_investment: int):
    if not st.session_state.get("ready"):
        return

    returns = st.session_state["returns"]
    tickers = st.session_state["tickers"]

    opt_weights = st.session_state.get(
        "max_sharpe_weights",
        np.ones(len(tickers)) / len(tickers),
    )

    port_returns = returns @ opt_weights
    ann_ret  = port_returns.mean() * 252
    ann_vol  = port_returns.std()  * np.sqrt(252)
    sharpe   = ann_ret / ann_vol

    downside = port_returns[port_returns < 0]
    sortino  = ann_ret / (downside.std() * np.sqrt(252))

    cumulative  = (1 + port_returns).cumprod()
    rolling_max = cumulative.cummax()
    drawdown    = (cumulative - rolling_max) / rolling_max
    max_dd      = drawdown.min()

    var_95  = np.percentile(port_returns, 5)
    cvar_95 = port_returns[port_returns <= var_95].mean()

    var_dol  = abs(var_95  * initial_investment)
    cvar_dol = abs(cvar_95 * initial_investment)

    section_header(
        "Risk & Return Metrics",
        "Max-Sharpe portfolio weights applied to historical returns",
    )

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Sharpe Ratio",     f"{sharpe:.3f}")
    m2.metric("Sortino Ratio",    f"{sortino:.3f}")
    m3.metric("Max Drawdown",     f"{max_dd*100:.1f}%")
    m4.metric("Daily VaR (95%)",  f"${var_dol:,.0f}")
    m5.metric("Daily CVaR (95%)", f"${cvar_dol:,.0f}")

    st.markdown("---")

    col_l, col_r = st.columns(2)

    with col_l:
        section_header(
            "Drawdown",
            "Distance from rolling peak — underwater periods shaded",
        )
        fig_dd = go.Figure()
        fig_dd.add_trace(go.Scatter(
            x=drawdown.index, y=drawdown * 100,
            mode="lines", fill="tozeroy",
            line=dict(color="#EF4444", width=1),
            fillcolor="rgba(239,68,68,0.10)",
            name="Drawdown",
        ))
        apply_theme(fig_dd, height=300,
                    yaxis_title="Drawdown (%)", xaxis_title="",
                    showlegend=False)
        st.plotly_chart(fig_dd, use_container_width=True)

    with col_r:
        section_header(
            "Rolling 6-Month Sharpe",
            "Risk-adjusted return consistency across 126-day windows",
        )
        rolling_sharpe = (
            port_returns.rolling(126).mean() * 252
        ) / (
            port_returns.rolling(126).std() * np.sqrt(252)
        )
        fig_rs = go.Figure()
        fig_rs.add_trace(go.Scatter(
            x=rolling_sharpe.index, y=rolling_sharpe,
            mode="lines", line=dict(color="#1533F0", width=1.75),
            name="Rolling Sharpe",
        ))
        fig_rs.add_hline(y=1.0, line_dash="dash", line_color="#10B981",
                         annotation_text="1.0",
                         annotation_position="right",
                         annotation_font=dict(color="#10B981", size=9))
        fig_rs.add_hline(y=0.0, line_dash="dash", line_color="#EF4444",
                         annotation_text="0.0",
                         annotation_position="right",
                         annotation_font=dict(color="#EF4444", size=9))
        apply_theme(fig_rs, height=300,
                    yaxis_title="Sharpe Ratio", xaxis_title="",
                    showlegend=False)
        st.plotly_chart(fig_rs, use_container_width=True)

    st.markdown("---")

    section_header(
        "Daily Returns Distribution",
        "Histogram of portfolio daily returns — 95% VaR threshold marked",
    )
    fig_ret = px.histogram(
        port_returns, nbins=80,
        labels={"value": "Daily Return", "count": "Frequency"},
        color_discrete_sequence=["#1533F0"],
    )
    fig_ret.update_traces(opacity=0.75, marker_line_width=0)
    fig_ret.add_vline(
        x=var_95, line_dash="dash", line_color="#EF4444",
        annotation_text="95% VaR",
        annotation_position="top left",
        annotation_font=dict(color="#EF4444", size=10),
    )
    apply_theme(fig_ret, height=320, showlegend=False)
    st.plotly_chart(fig_ret, use_container_width=True)
