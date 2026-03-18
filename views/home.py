import streamlit as st
import numpy as np

from ui import section_header


def render_home():
    st.markdown(
        '<div class="cover-hero">'
        '<div class="cover-eyebrow">Portfolio Analytics &nbsp;/&nbsp; Quantitative Research</div>'
        '<h1 class="cover-title">Built for<br>rigorous<br>analysis.</h1>'
        '<p class="cover-desc">An interactive quantitative framework for portfolio construction, '
        'risk decomposition, and forward-looking scenario analysis — '
        'designed to demonstrate institutional-grade analytical capability.</p>'
        '<div class="cover-pills">'
        '<span class="cover-pill"><span class="dot"></span>Price Performance</span>'
        '<span class="cover-pill"><span class="dot"></span>Efficient Frontier</span>'
        '<span class="cover-pill"><span class="dot"></span>Monte Carlo</span>'
        '<span class="cover-pill"><span class="dot"></span>Risk Metrics</span>'
        '<span class="cover-pill"><span class="dot"></span>Fundamentals</span>'
        '</div>'
        '<div class="cover-cta">'
        '<div class="cover-cta-line"></div>'
        '<div class="cover-cta-text">Configure in sidebar &rarr; Run Analysis</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:2.5rem'></div>", unsafe_allow_html=True)
    section_header("What's Inside")

    modules = [
        ("Overview",     "Normalized price chart vs SPY benchmark, annualized return & volatility table, correlation heatmap."),
        ("Optimization", "3,000-simulation efficient frontier with Max-Sharpe and Min-Volatility portfolio weights."),
        ("Monte Carlo",  "1,000-path simulation fan chart, goal-probability metric, and final-value distribution."),
        ("Risk Metrics", "Sharpe, Sortino, Max Drawdown, 95% VaR & CVaR, rolling 6-month Sharpe, returns distribution."),
        ("Fundamentals", "P/E, P/B, profit margin, debt/equity, dividend yield, sector breakdown, allocation vs. valuation bubble chart."),
    ]

    cols = st.columns(len(modules))
    for col, (title, desc) in zip(cols, modules):
        with col:
            st.markdown(
                f'<div class="module-card">'
                f'<div class="module-card-title">{title}</div>'
                f'<div class="module-card-desc">{desc}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    if st.session_state.get("ready"):
        st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
        st.markdown("---")
        section_header("Portfolio at a Glance", "Max-Sharpe weights applied to historical data")

        _ret  = st.session_state["returns"]
        _tick = st.session_state["tickers"]
        _spy  = st.session_state["spy"]

        _ar      = _ret.mean() * 252
        _av      = _ret.std()  * np.sqrt(252)
        _spy_ret = _spy.pct_change().dropna()
        _spy_ar  = _spy_ret.mean() * 252

        cols2 = st.columns(len(_tick) + 1)
        for c, t in zip(cols2[:-1], _tick):
            c.metric(t, f"{_ar[t]*100:.1f}%", f"σ {_av[t]*100:.1f}%")
        cols2[-1].metric("SPY", f"{_spy_ar*100:.1f}%", "benchmark")
