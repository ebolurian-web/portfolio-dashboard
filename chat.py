import re
import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta

_STOP = {
    'AND', 'OR', 'THE', 'A', 'I', 'MY', 'TO', 'FOR', 'IS', 'IN', 'OF', 'WITH',
    'WANT', 'ANALYZE', 'PLEASE', 'SOME', 'PORTFOLIO', 'STOCKS', 'SHARES',
    'FUND', 'ETF', 'LIKE', 'WOULD', 'CAN', 'YOU', 'ME', 'AT', 'BY', 'AS',
}

_Q = {
    "tickers": "Which stocks would you like to analyze? Enter tickers separated by commas — e.g. **AAPL, MSFT, GOOGL**. Crypto works too (BTC-USD).",
    "start":   "What **start date** for the analysis? (e.g. 01/01/2020 or '5 years ago')",
    "end":     "And the **end date**? (e.g. today, or 31/12/2024)",
    "invest":  "What is your **initial investment** amount? (e.g. $100,000 or 50k)",
    "horizon": "How many **years ahead** for the Monte Carlo simulation? Enter a number from 1–10.",
    "goal":    "Finally, what is your **target portfolio value**? (e.g. $200,000)",
}


def _parse_tickers(text):
    hits = re.findall(r'\b([A-Za-z]{1,5}(?:-[A-Za-z]{2,4})?)\b', text)
    out  = [h.upper() for h in hits if h.upper() not in _STOP]
    return out if out else None


def _parse_date(text):
    t = text.strip().lower()
    if t in ('today', 'now', 'present'):
        return date.today()
    m = re.search(r'(\d+)\s*(year|yr)', t)
    if m:
        return (datetime.today() - timedelta(days=365 * int(m.group(1)))).date()
    m = re.search(r'(\d+)\s*(month|mo)', t)
    if m:
        return (datetime.today() - timedelta(days=30 * int(m.group(1)))).date()
    try:
        return pd.to_datetime(text, dayfirst=True).date()
    except Exception:
        return None


def _parse_money(text):
    t = text.lower().replace(',', '').replace('$', '').replace(' ', '')
    m = re.search(r'(\d+(?:\.\d+)?)\s*([km]?)', t)
    if m:
        v = float(m.group(1))
        if m.group(2) == 'k':
            v *= 1_000
        elif m.group(2) == 'm':
            v *= 1_000_000
        return int(v)
    return None


def _parse_int(text, lo=1, hi=10):
    m = re.search(r'\d+', text)
    if m:
        v = int(m.group())
        if lo <= v <= hi:
            return v
    return None


def _chat_init():
    if "chat_msgs" not in st.session_state:
        st.session_state.chat_msgs = [
            {"role": "assistant", "content":
             "Hi! I'll set up your portfolio analysis through a few quick questions.\n\n" + _Q["tickers"]}
        ]
        st.session_state.chat_step = "tickers"
        st.session_state.chat_vals = {}
        st.session_state.chat_done = False


def _chat_respond(user_input):
    msgs = st.session_state.chat_msgs
    step = st.session_state.chat_step
    vals = st.session_state.chat_vals
    msgs.append({"role": "user", "content": user_input})

    if step == "tickers":
        t = _parse_tickers(user_input)
        if t:
            vals["tickers_str"] = ", ".join(t)
            st.session_state.chat_step = "start"
            msgs.append({"role": "assistant", "content":
                f"Got it — analyzing **{', '.join(t)}**.\n\n" + _Q["start"]})
        else:
            msgs.append({"role": "assistant", "content":
                "I couldn't find any tickers. Try something like: AAPL, MSFT, GOOGL"})

    elif step == "start":
        d = _parse_date(user_input)
        if d:
            vals["start_date"] = d
            st.session_state.chat_step = "end"
            msgs.append({"role": "assistant", "content":
                f"Start date: **{d.strftime('%d/%m/%Y')}**.\n\n" + _Q["end"]})
        else:
            msgs.append({"role": "assistant", "content":
                "Couldn't parse that date. Try: 01/01/2020 or '5 years ago'"})

    elif step == "end":
        d = _parse_date(user_input)
        if d:
            vals["end_date"] = d
            st.session_state.chat_step = "invest"
            msgs.append({"role": "assistant", "content":
                f"End date: **{d.strftime('%d/%m/%Y')}**.\n\n" + _Q["invest"]})
        else:
            msgs.append({"role": "assistant", "content":
                "Couldn't parse that. Try: today, or 18/03/2026"})

    elif step == "invest":
        v = _parse_money(user_input)
        if v and v > 0:
            vals["investment"] = v
            st.session_state.chat_step = "horizon"
            msgs.append({"role": "assistant", "content":
                f"Investment: **${v:,}**.\n\n" + _Q["horizon"]})
        else:
            msgs.append({"role": "assistant", "content":
                "Try a number like $100,000 or 50k"})

    elif step == "horizon":
        v = _parse_int(user_input, 1, 10)
        if v:
            vals["horizon"] = v
            st.session_state.chat_step = "goal"
            msgs.append({"role": "assistant", "content":
                f"Horizon: **{v} year{'s' if v > 1 else ''}**.\n\n" + _Q["goal"]})
        else:
            msgs.append({"role": "assistant", "content":
                "Please enter a whole number between 1 and 10."})

    elif step == "goal":
        v = _parse_money(user_input)
        if v and v > 0:
            vals["goal"] = v
            st.session_state.chat_done = True
            msgs.append({"role": "assistant", "content":
                f"All set! Here's your configuration:\n\n"
                f"**Tickers:** {vals['tickers_str']}\n\n"
                f"**Period:** {vals['start_date'].strftime('%d/%m/%Y')} → {vals['end_date'].strftime('%d/%m/%Y')}\n\n"
                f"**Investment:** ${vals['investment']:,}\n\n"
                f"**Horizon:** {vals['horizon']} year{'s' if vals['horizon'] > 1 else ''}\n\n"
                f"**Goal:** ${v:,}\n\n"
                "Click **Run Analysis** below to begin."})
        else:
            msgs.append({"role": "assistant", "content":
                "Try a number like $200,000 or 200k"})
