import io
import streamlit as st
import pandas as pd
from datetime import date

from chat import _chat_init, _chat_respond


def _parse_robinhood_csv(uploaded_file):
    """Parse a Robinhood portfolio CSV and return a list of ticker symbols."""
    try:
        df = pd.read_csv(io.StringIO(uploaded_file.getvalue().decode("utf-8")))
    except Exception:
        return None

    if "Symbol" not in df.columns:
        return None

    tickers = (
        df["Symbol"]
        .dropna()
        .astype(str)
        .str.strip()
        .str.upper()
        .tolist()
    )
    tickers = [t for t in tickers if t and 1 <= len(t) <= 10]
    return tickers if tickers else None


def render_sidebar() -> dict:
    _chat_init()
    if "sb_mode" not in st.session_state:
        st.session_state.sb_mode = "Chat"

    with st.sidebar:
        st.markdown(
            '<div class="sidebar-header">'
            '<div class="sidebar-header-title">Portfolio</div>'
            '<div class="sidebar-header-sub">Configuration</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        # ── Mode toggle ────────────────────────────────────
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button(
                "💬 Chat",
                use_container_width=True,
                type="primary" if st.session_state.sb_mode == "Chat" else "secondary",
                key="btn_chat",
            ):
                st.session_state.sb_mode = "Chat"
                st.rerun()
        with c2:
            if st.button(
                "⚙ Manual",
                use_container_width=True,
                type="primary" if st.session_state.sb_mode == "Manual" else "secondary",
                key="btn_manual",
            ):
                st.session_state.sb_mode = "Manual"
                st.rerun()
        with c3:
            if st.button(
                "📄 CSV",
                use_container_width=True,
                type="primary" if st.session_state.sb_mode == "CSV" else "secondary",
                key="btn_csv",
            ):
                st.session_state.sb_mode = "CSV"
                st.rerun()

        st.markdown("---")

        # ── Chat mode ──────────────────────────────────────
        if st.session_state.sb_mode == "Chat":
            msg_box = st.container(height=400, border=False)
            with msg_box:
                for m in st.session_state.chat_msgs:
                    with st.chat_message(m["role"]):
                        st.markdown(m["content"])

            if not st.session_state.chat_done:
                user_inp = st.chat_input("Type your answer…")
                if user_inp:
                    _chat_respond(user_inp)
                    st.rerun()

            if st.button("↺  Start over", use_container_width=True, key="chat_restart"):
                for k in ["chat_msgs", "chat_step", "chat_vals", "chat_done"]:
                    st.session_state.pop(k, None)
                st.rerun()

            vals = st.session_state.chat_vals
            tickers_input      = vals.get("tickers_str",  "AAPL, MSFT, JPM, JNJ, XOM")
            start_date         = vals.get("start_date",   pd.to_datetime("2020-01-01").date())
            end_date           = vals.get("end_date",     date.today())
            initial_investment = vals.get("investment",   100_000)
            mc_years           = vals.get("horizon",      5)
            target_value       = vals.get("goal",         200_000)

            st.markdown("---")
            run = st.button(
                "▶  Run Analysis",
                use_container_width=True,
                disabled=not st.session_state.chat_done,
                key="run_chat",
            )

        # ── Manual mode ────────────────────────────────────
        elif st.session_state.sb_mode == "Manual":
            _v = st.session_state.get("chat_vals", {})
            tickers_input = st.text_input(
                "Tickers (comma separated)",
                value=_v.get("tickers_str", "AAPL, MSFT, JPM, JNJ, XOM"),
                key="man_tickers",
            )
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input(
                    "Start",
                    value=_v.get("start_date", pd.to_datetime("2020-01-01").date()),
                    format="DD/MM/YYYY",
                    key="man_start",
                )
            with col2:
                end_date = st.date_input(
                    "End",
                    value=_v.get("end_date", date.today()),
                    format="DD/MM/YYYY",
                    key="man_end",
                )
            initial_investment = st.number_input(
                "Initial Investment ($)",
                value=_v.get("investment", 100_000),
                step=10_000,
                key="man_invest",
            )
            mc_years = st.slider(
                "Monte Carlo Horizon (Years)",
                min_value=1, max_value=10,
                value=_v.get("horizon", 5),
                key="man_horizon",
            )
            target_value = st.number_input(
                "Goal Target Value ($)",
                value=_v.get("goal", 200_000),
                step=10_000,
                key="man_goal",
                help="Probability of reaching this value is shown in Monte Carlo",
            )

            st.markdown("---")
            run = st.button("Run Analysis", use_container_width=True, key="run_manual")

        # ── CSV mode ───────────────────────────────────────
        else:
            st.markdown(
                '<p style="font-size:0.68rem;color:#9CA3AF;letter-spacing:0.08em;'
                'text-transform:uppercase;font-weight:500;margin-bottom:0.25rem;">'
                'Robinhood CSV Import</p>',
                unsafe_allow_html=True,
            )
            st.caption(
                "**How to export from Robinhood:** "
                "Open Robinhood → tap your Account icon → scroll to "
                "**Statements & History** → tap **Download** (web) or "
                "**Export to CSV**. Upload the downloaded file below. "
                "Dates and investment amount must still be set manually."
            )

            uploaded = st.file_uploader("Upload CSV", type=["csv"], key="csv_upload")

            csv_tickers = None
            if uploaded is not None:
                csv_tickers = _parse_robinhood_csv(uploaded)
                if csv_tickers:
                    st.success(f"Found {len(csv_tickers)} tickers: {', '.join(csv_tickers)}")
                else:
                    st.error(
                        "Could not find a 'Symbol' column. "
                        "Make sure you're uploading a Robinhood portfolio holdings CSV."
                    )

            st.markdown("---")

            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input(
                    "Start",
                    value=pd.to_datetime("2020-01-01").date(),
                    format="DD/MM/YYYY",
                    key="csv_start",
                )
            with col2:
                end_date = st.date_input(
                    "End",
                    value=date.today(),
                    format="DD/MM/YYYY",
                    key="csv_end",
                )
            initial_investment = st.number_input(
                "Initial Investment ($)",
                value=100_000,
                step=10_000,
                key="csv_invest",
            )
            mc_years = st.slider(
                "Monte Carlo Horizon (Years)",
                min_value=1, max_value=10,
                value=5,
                key="csv_horizon",
            )
            target_value = st.number_input(
                "Goal Target Value ($)",
                value=200_000,
                step=10_000,
                key="csv_goal",
                help="Probability of reaching this value is shown in Monte Carlo",
            )

            tickers_input = ", ".join(csv_tickers) if csv_tickers else ""
            st.markdown("---")
            run = st.button(
                "Run Analysis",
                use_container_width=True,
                disabled=(csv_tickers is None),
                key="run_csv",
            )

    return {
        "run":                run,
        "tickers_input":      tickers_input,
        "start_date":         start_date,
        "end_date":           end_date,
        "initial_investment": initial_investment,
        "mc_years":           mc_years,
        "target_value":       target_value,
    }
