import streamlit as st

from styles import inject_styles
from data import load_data, load_spy, load_fundamentals
from sidebar import render_sidebar
from views.home import render_home
from views.overview import render_overview
from views.optimization import render_optimization
from views.montecarlo import render_montecarlo
from views.risk import render_risk
from views.fundamentals import render_fundamentals

# ── PAGE CONFIG ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="Portfolio Analytics",
    page_icon="◈",
    layout="wide",
)

# ── STYLES + ANIMATION ──────────────────────────────────────────────
inject_styles()

# ── PAGE HEADER ─────────────────────────────────────────────────────
st.markdown(
    '<div class="page-header">'
    '<div>'
    '<div class="page-header-eyebrow">Quantitative Research</div>'
    '<div class="page-header-title">Portfolio Analytics</div>'
    '</div>'
    '<div class="page-header-right">'
    '<div class="page-header-badge">Interactive Suite ◈</div>'
    '<div class="page-header-byline">By Eden Bolurian</div>'
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)

# ── SIDEBAR → config ────────────────────────────────────────────────
cfg = render_sidebar()

tickers = [t.strip().upper() for t in cfg["tickers_input"].split(",") if t.strip()]

# ── DATA LOADING ────────────────────────────────────────────────────
if cfg["run"]:
    with st.spinner("Fetching market data..."):
        prices, returns  = load_data(tickers, cfg["start_date"], cfg["end_date"])
        spy              = load_spy(cfg["start_date"], cfg["end_date"])
        fundamentals     = load_fundamentals(tickers)
    st.session_state["prices"]       = prices
    st.session_state["returns"]      = returns
    st.session_state["spy"]          = spy
    st.session_state["fundamentals"] = fundamentals
    st.session_state["tickers"]      = tickers
    st.session_state["ready"]        = True

# ── TABS ────────────────────────────────────────────────────────────
tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Home",
    "Overview",
    "Optimization",
    "Monte Carlo",
    "Risk Metrics",
    "Fundamentals",
])

if not st.session_state.get("ready"):
    for tab in [tab1, tab2, tab3, tab4, tab5]:
        with tab:
            st.markdown(
                '<div class="sidebar-prompt">'
                '<span>Configure your portfolio in the sidebar and click '
                '<strong>Run Analysis</strong> to begin.</span>'
                '<span class="sidebar-prompt-arrow">&#x203A;</span>'
                '</div>',
                unsafe_allow_html=True,
            )

# ── VIEWS ────────────────────────────────────────────────────────────
with tab0:
    render_home()

with tab1:
    render_overview()

with tab2:
    render_optimization()

with tab3:
    render_montecarlo(
        mc_years=cfg["mc_years"],
        initial_investment=cfg["initial_investment"],
        target_value=cfg["target_value"],
    )

with tab4:
    render_risk(initial_investment=cfg["initial_investment"])

with tab5:
    render_fundamentals()
