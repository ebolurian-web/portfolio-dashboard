import re
import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.optimize import minimize
from datetime import date, datetime, timedelta

# ── PAGE CONFIG ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Portfolio Analytics",
    page_icon="◈",
    layout="wide"
)

# ── STYLES ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,700;1,400&family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --blue:    #1533F0;
    --teal:    #14D2C3;
    --bg:      #FFFFFF;
    --border:  #E5E7F0;
    --text:    #0A0D2C;
    --muted:   #9CA3AF;
    --pos:     #10B981;
    --neg:     #EF4444;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}
.stApp {
    background-color: #ffffff !important;
}
/* Hide Streamlit chrome entirely */
#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] {
    background: transparent !important;
    border:     none        !important;
    box-shadow: none        !important;
    height:     0           !important;
    min-height: 0           !important;
    overflow:   hidden      !important;
    padding:    0           !important;
}
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="stMainMenuPopover"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarToggleButton"]   { display: none !important; }

/* Remove top gap on main content */
.block-container, [data-testid="block-container"] {
    padding-top: 0.5rem !important;
}

/* Sidebar always visible — block every CSS-level collapse path */
[data-testid="stSidebar"] {
    transform:   translateX(0) !important;
    display:     block         !important;
    visibility:  visible       !important;
    min-width:   245px         !important;
}
[data-testid="stSidebarContent"],
[data-testid="stSidebarUserContent"] {
    display:    flex    !important;
    visibility: visible !important;
}
/* Hide every native collapse/toggle control */
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarToggleButton"],
[data-testid="stSidebar"] button[aria-label*="ollapse"],
[data-testid="stSidebar"] button[aria-label*="lose"],
[data-testid="stSidebar"] button[kind="header"]   { display: none !important; }

/* ── Layout: flush sidebar / smooth content shift ────────────── */
[data-testid="stAppViewContainer"] {
    gap: 0 !important;
    padding: 0 !important;
}
[data-testid="stMain"] {
    padding-left: 0 !important;
    /* let Streamlit control margin-left; just make it animate smoothly */
    transition: margin-left 0.3s ease !important;
}

/* ── Sidebar ──────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid var(--border) !important;
    box-shadow: 4px 0 32px rgba(21,51,240,.04) !important;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] p {
    font-size: 0.68rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    font-weight: 500 !important;
}
[data-testid="stSidebar"] input {
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 3px !important;
    font-size: 0.85rem !important;
    background: white !important;
    transition: border-color .2s, box-shadow .2s !important;
}
[data-testid="stSidebar"] input:focus {
    border-color: var(--blue) !important;
    box-shadow: 0 0 0 3px rgba(21,51,240,.08) !important;
    outline: none !important;
}
[data-testid="stSidebar"] hr {
    border-color: var(--border) !important;
    margin: 1rem 0 !important;
}
[data-testid="stSidebar"] .stButton > button {
    background: var(--blue) !important;
    border: none !important;
    color: white !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
    border-radius: 2px !important;
    padding: 0.7rem 1rem !important;
    transition: background .2s, box-shadow .2s, transform .15s !important;
    width: 100% !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #0F25C8 !important;
    box-shadow: 0 6px 20px rgba(21,51,240,.3) !important;
    transform: translateY(-1px) !important;
}

/* ── Tabs ─────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
    padding: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    color: var(--muted) !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    font-weight: 500 !important;
    padding: 0.8rem 1.5rem !important;
    transition: color .2s, border-color .2s !important;
}
.stTabs [aria-selected="true"] {
    color: var(--blue) !important;
    border-bottom: 2px solid var(--blue) !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--text) !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab-highlight"] {
    background: var(--blue) !important;
    height: 2px !important;
}
.stTabs [data-baseweb="tab-border"] {
    background: var(--border) !important;
}

/* ── Metric cards ─────────────────────────────────── */
[data-testid="metric-container"] {
    background: white !important;
    border: 1px solid var(--border) !important;
    border-radius: 3px !important;
    padding: 1.1rem 1.25rem !important;
    transition: border-color .25s ease, box-shadow .25s ease, transform .2s ease !important;
    cursor: default !important;
}
[data-testid="metric-container"]:hover {
    border-color: var(--blue) !important;
    box-shadow: 0 6px 28px rgba(21,51,240,.10) !important;
    transform: translateY(-3px) !important;
}
[data-testid="metric-container"] [data-testid="stMetricLabel"] > div {
    font-size: 0.62rem !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    font-weight: 500 !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] > div {
    font-size: 1.5rem !important;
    font-weight: 600 !important;
    color: var(--blue) !important;
    letter-spacing: -0.02em !important;
}

/* ── Headings ─────────────────────────────────────── */
h1, h2, h3, h4 {
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── Dividers ─────────────────────────────────────── */
hr {
    border-color: var(--border) !important;
    margin: 1.75rem 0 !important;
}

/* ── Alerts ───────────────────────────────────────── */
[data-testid="stAlert"] {
    background: rgba(21,51,240,.04) !important;
    border: 1px solid rgba(21,51,240,.15) !important;
    border-radius: 3px !important;
}
[data-testid="stAlert"] p {
    color: var(--blue) !important;
    font-size: 0.82rem !important;
    text-transform: none !important;
    letter-spacing: 0.02em !important;
}

/* ── Spinner ──────────────────────────────────────── */
.stSpinner > div { border-top-color: var(--blue) !important; }

/* ── DataFrames ───────────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 3px !important;
}

/* ── Number / Date inputs ─────────────────────────── */
[data-testid="stNumberInput"] input,
[data-testid="stDateInput"] input {
    border: 1px solid var(--border) !important;
    background: white !important;
    transition: border-color .2s, box-shadow .2s !important;
}
[data-testid="stNumberInput"] input:focus,
[data-testid="stDateInput"] input:focus {
    border-color: var(--blue) !important;
    box-shadow: 0 0 0 3px rgba(21,51,240,.08) !important;
}

/* ── Slider thumb ─────────────────────────────────── */
[data-testid="stSlider"] [role="slider"] {
    background: var(--blue) !important;
    box-shadow: 0 2px 8px rgba(21,51,240,.3) !important;
}

/* ── Cover hero ───────────────────────────────────── */
.cover-hero {
    padding: 5rem 0 4.5rem 0;
    border-bottom: 1px solid #E5E7F0;
    min-height: 68vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.cover-eyebrow {
    font-size: 0.58rem;
    letter-spacing: 0.38em;
    text-transform: uppercase;
    color: #1533F0;
    font-weight: 500;
    margin-bottom: 1.75rem;
    font-family: Inter, sans-serif;
}
.cover-title {
    font-family: 'Playfair Display', Georgia, serif !important;
    font-size: clamp(4rem, 8vw, 7rem) !important;
    font-weight: 400 !important;
    color: #1533F0 !important;
    line-height: 0.93 !important;
    letter-spacing: -0.02em !important;
    margin: 0 0 2.5rem 0 !important;
}
.cover-desc {
    font-family: Inter, sans-serif;
    font-size: 1rem;
    color: #374151;
    max-width: 540px;
    line-height: 1.75;
    font-weight: 400;
    margin-bottom: 3rem;
}
.cover-pills {
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
    margin-bottom: 3.5rem;
}
.cover-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.4rem 0.9rem;
    border: 1px solid #E5E7F0;
    border-radius: 100px;
    font-size: 0.68rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #0A0D2C;
    font-weight: 500;
    transition: border-color .2s, color .2s, background .2s;
    cursor: default;
    font-family: Inter, sans-serif;
}
.cover-pill:hover {
    border-color: #1533F0;
    color: #1533F0;
    background: rgba(21,51,240,.04);
}
.cover-pill .dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #14D2C3;
    flex-shrink: 0;
}
.cover-cta {
    display: flex;
    align-items: center;
    gap: 1rem;
}
.cover-cta-line {
    width: 48px;
    height: 1px;
    background: #1533F0;
    flex-shrink: 0;
}
.cover-cta-text {
    font-family: Inter, sans-serif;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #1533F0;
    font-weight: 500;
}

/* ── Module cards ─────────────────────────────────── */
.module-card {
    border: 1px solid #E5E7F0;
    border-radius: 3px;
    padding: 1.5rem 1.25rem;
    background: white;
    cursor: default;
    transition: border-color .25s ease, box-shadow .25s ease, transform .2s ease;
    height: 100%;
}
.module-card:hover {
    border-color: #1533F0;
    box-shadow: 0 6px 28px rgba(21,51,240,.10);
    transform: translateY(-3px);
}
.module-card-title {
    font-size: 0.6rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #1533F0;
    font-weight: 600;
    margin-bottom: 0.65rem;
    font-family: Inter, sans-serif;
}
.module-card-desc {
    font-size: 0.82rem;
    color: #6B7280;
    line-height: 1.6;
    font-family: Inter, sans-serif;
}

/* ── Page header ──────────────────────────────────── */
.page-header {
    padding: 1.4rem 0 0.9rem 0;
    border-bottom: 1px solid #E5E7F0;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
}
.page-header-eyebrow {
    font-size: 0.54rem;
    letter-spacing: 0.36em;
    text-transform: uppercase;
    color: #1533F0;
    font-weight: 500;
    margin-bottom: 0.35rem;
    font-family: Inter, sans-serif;
}
.page-header-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.55rem;
    font-weight: 400;
    color: #1533F0;
    letter-spacing: -0.01em;
    line-height: 1;
}
.page-header-badge {
    font-size: 0.58rem;
    color: #D1D5DB;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-weight: 500;
    padding-bottom: 0.15rem;
    font-family: Inter, sans-serif;
}

/* ── Sidebar content top padding ─────────────────── */
[data-testid="stSidebarContent"] {
    padding-top: 2rem !important;
}

/* ── Page header byline ───────────────────────────── */
.page-header-right {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 0.3rem;
}
.page-header-byline {
    font-size: 0.54rem;
    color: #9CA3AF;
    letter-spacing: 0.08em;
    font-family: Inter, sans-serif;
    text-align: right;
}

/* ── Sidebar mode toggle ──────────────────────────── */
div[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] > div {
    padding: 0 2px !important;
}
.sb-mode-wrap { display: flex; gap: 6px; margin-bottom: 0.25rem; }

/* Active mode button */
[data-testid="stSidebar"] .stButton button[kind="primary"] {
    font-size: 0.62rem !important;
    letter-spacing: 0.12em !important;
    padding: 0.35rem 0 !important;
    border-radius: 3px !important;
}
/* Inactive mode button */
[data-testid="stSidebar"] .stButton button[kind="secondary"] {
    font-size: 0.62rem !important;
    letter-spacing: 0.12em !important;
    padding: 0.35rem 0 !important;
    border-radius: 3px !important;
    background: white !important;
    color: var(--muted) !important;
    border: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .stButton button[kind="secondary"]:hover {
    border-color: var(--blue) !important;
    color: var(--blue) !important;
}

/* ── Sidebar chat bubbles ─────────────────────────── */
[data-testid="stSidebar"] [data-testid="stChatMessage"] {
    padding: 0.1rem 0 !important;
    background: transparent !important;
}
[data-testid="stSidebar"] [data-testid="stChatMessage"] p {
    font-size: 0.78rem !important;
    line-height: 1.45 !important;
    letter-spacing: 0 !important;
    text-transform: none !important;
    color: var(--text) !important;
    font-weight: 400 !important;
}
/* Disabled run button state */
[data-testid="stSidebar"] .stButton button:disabled {
    opacity: 0.4 !important;
    cursor: not-allowed !important;
}

/* ── Sidebar header ───────────────────────────────── */
.sidebar-header { padding: 0.4rem 0 1.1rem 0; }
.sidebar-header-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.25rem;
    font-weight: 400;
    color: #1533F0;
    margin-bottom: 0.15rem;
    line-height: 1.1;
}
.sidebar-header-sub {
    font-size: 0.6rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #9CA3AF;
    font-weight: 500;
    font-family: Inter, sans-serif;
}

/* ── Sidebar prompt banner ────────────────────────── */
.sidebar-prompt {
    cursor: pointer;
    background: #EEF1FF;
    border: 1px solid #C7D0FB;
    border-radius: 6px;
    padding: 0.85rem 1.25rem;
    color: #1533F0;
    font-size: 0.875rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    transition: background 0.2s, border-color 0.2s, box-shadow 0.2s;
    margin-bottom: 0.5rem;
    user-select: none;
}
.sidebar-prompt:hover {
    background: #DDE2FF;
    border-color: #1533F0;
    box-shadow: 0 2px 12px rgba(21,51,240,0.12);
}
.sidebar-prompt-arrow {
    font-size: 1.1rem;
    opacity: 0.7;
    flex-shrink: 0;
}
</style>
""", unsafe_allow_html=True)


# ── ANIMATION + CUSTOM SIDEBAR TAB ────────────────────────────────
components.html("""
<script>
(function () {
    var canvas, ctx, cells = [], time = 0;
    var mx = -9999, my = -9999, mouseOn = false;

    /* ── constants ── */
    var SPACING  = 38;
    var LINE_LEN = 22;
    var LERP_ON  = 0.12;
    var LERP_OFF = 0.045;
    var MAGNET_R = 160;

    function buildCells(w, h) {
        cells = [];
        var cols = Math.ceil(w / SPACING) + 2;
        var rows = Math.ceil(h / SPACING) + 2;
        for (var c = 0; c < cols; c++) {
            for (var r = 0; r < rows; r++) {
                var ax = c * SPACING, ay = r * SPACING;
                cells.push({
                    ax: ax, ay: ay, tx: ax, ty: ay,
                    hue:   195 + 45 * Math.sin(c * 0.52 + r * 0.37),
                    phase: (c * 0.41 + r * 0.29) % (Math.PI * 2)
                });
            }
        }
    }

    function syncSize(hero) {
        var rect = hero.getBoundingClientRect();
        var w = Math.round(rect.width);
        var h = Math.round(rect.height);
        if (canvas.width !== w || canvas.height !== h) {
            canvas.width  = w;
            canvas.height = h;
            buildCells(w, h);
        }
    }

    function flowAngle(x, y, t) {
        var s = 0.007;
        return (
            Math.sin(x * s * 1.15 + t * 0.38)           +
            Math.cos(y * s         - t * 0.26) * 1.25    +
            Math.sin((x - y) * s * 0.72 + t * 0.44) * 0.6
        ) * Math.PI;
    }

    function draw(hero) {
        syncSize(hero);
        var rect = hero.getBoundingClientRect();
        /* convert page-level mouse coords to canvas-local */
        var lx = mx - rect.left;
        var ly = my - rect.top;

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        time += 0.016;
        ctx.lineWidth = 1.5;
        ctx.lineCap   = 'round';

        for (var i = 0; i < cells.length; i++) {
            var c    = cells[i];
            var dx   = lx - c.ax;
            var dy   = ly - c.ay;
            var dist = Math.sqrt(dx * dx + dy * dy);
            var targetX, targetY, speed;

            if (mouseOn && dist < MAGNET_R && dist > 0.5) {
                var len = Math.min(LINE_LEN, dist * 0.88);
                targetX = c.ax + (dx / dist) * len;
                targetY = c.ay + (dy / dist) * len;
                speed   = LERP_ON;
            } else {
                var angle = flowAngle(c.ax, c.ay, time);
                targetX   = c.ax + Math.cos(angle) * LINE_LEN;
                targetY   = c.ay + Math.sin(angle) * LINE_LEN;
                speed     = LERP_OFF;
            }

            c.tx += (targetX - c.tx) * speed;
            c.ty += (targetY - c.ty) * speed;

            var bright    = 0.5 + 0.5 * Math.sin(
                c.ax * 0.008 - c.ay * 0.005 + time * 0.55 + c.phase * 0.15);
            var lightness = 36 + bright * 42;
            var alpha     = 0.20 + bright * 0.55;

            ctx.beginPath();
            ctx.moveTo(c.ax, c.ay);
            ctx.lineTo(c.tx, c.ty);
            ctx.strokeStyle = 'hsla(' + c.hue.toFixed(1) + ',78%,' +
                              lightness.toFixed(1) + '%,' + alpha.toFixed(2) + ')';
            ctx.stroke();
        }
        requestAnimationFrame(function () { draw(hero); });
    }

    function attachToHero(attempt) {
        var doc  = window.parent.document;
        var hero = doc.querySelector('.cover-hero');
        if (!hero) {
            if (attempt < 20) setTimeout(function () { attachToHero(attempt + 1); }, 300);
            return;
        }
        if (doc.getElementById('mlp-lines')) return;   /* already attached */

        /* ── inject hero-scoped styles ── */
        var style = doc.createElement('style');
        style.id  = 'mlp-style';
        style.textContent =
            /* hero becomes the positioning context; canvas is clipped inside it */
            '.cover-hero { position:relative !important; overflow:hidden !important; }' +
            /* float all hero children above the canvas */
            '.cover-hero > *:not(#mlp-lines) { position:relative !important; z-index:1 !important; }';
        doc.head.appendChild(style);

        /* ── canvas absolutely positioned inside .cover-hero ── */
        canvas = doc.createElement('canvas');
        canvas.id = 'mlp-lines';
        Object.assign(canvas.style, {
            position:      'absolute',
            top:           '0', left: '0',
            width:         '100%', height: '100%',
            pointerEvents: 'none',
            zIndex:        '0'
        });
        hero.insertBefore(canvas, hero.firstChild);
        ctx = canvas.getContext('2d');

        /* ── mouse events — track page coords, convert inside draw() ── */
        doc.addEventListener('mousemove',  function (e) { mx = e.clientX; my = e.clientY; mouseOn = true; });
        doc.addEventListener('mouseleave', function ()  { mouseOn = false; });

        /* ── keep sidebar permanently open ── */
        setInterval(function () {
            var sb = doc.querySelector('[data-testid="stSidebar"]');
            if (!sb) return;
            var r = sb.getBoundingClientRect();
            if (r.right < 60 || r.width < 60) {
                sb.style.setProperty('transform',  'translateX(0)', 'important');
                sb.style.setProperty('display',    'block',         'important');
                sb.style.setProperty('visibility', 'visible',       'important');
                sb.style.setProperty('min-width',  '245px',         'important');
                var inner = sb.querySelector('[data-testid="stSidebarContent"]') ||
                            sb.querySelector('[data-testid="stSidebarUserContent"]') ||
                            sb.firstElementChild;
                if (inner) {
                    inner.style.setProperty('display',    'flex',    'important');
                    inner.style.setProperty('visibility', 'visible', 'important');
                }
            }
        }, 200);

        syncSize(hero);
        draw(hero);
    }

    attachToHero(0);
})();
</script>
""", height=0, scrolling=False)


# ── CHART THEME ────────────────────────────────────────────────────
_F = dict(family="Inter, sans-serif", size=11, color="#9CA3AF")
_AX = dict(
    gridcolor="#F0F1F8",
    linecolor="#E5E7F0",
    tickfont=dict(family="Inter", size=10, color="#9CA3AF"),
    title_font=dict(family="Inter", size=11, color="#9CA3AF"),
    showgrid=True,
    zeroline=False,
)
CHART = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#FAFBFF",
    font=_F,
    xaxis=_AX,
    yaxis=_AX,
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", size=10, color="#9CA3AF"),
        bordercolor="rgba(0,0,0,0)",
    ),
    margin=dict(l=48, r=24, t=36, b=44),
    hoverlabel=dict(
        bgcolor="white",
        bordercolor="#E5E7F0",
        font=dict(family="Inter", size=11, color="#0A0D2C"),
        align="left",
    ),
)
PALETTE = ["#1533F0", "#14D2C3", "#F59E0B", "#10B981", "#8B5CF6", "#EF4444", "#6B7280"]


def apply_theme(fig, height=420, **kw):
    # Merge CHART defaults with caller overrides so duplicate keys don't conflict
    layout = {**CHART, "height": height, **kw}
    fig.update_layout(**layout)
    return fig


def section_header(title, caption=None):
    cap = (f'<div style="font-size:0.7rem;color:#9CA3AF;margin-top:0.3rem;'
           f'font-family:Inter,sans-serif;letter-spacing:0.02em;">{caption}</div>') if caption else ""
    st.markdown(
        f'<div style="margin:0.25rem 0 1rem 0;padding-bottom:0.55rem;border-bottom:1px solid #E5E7F0;">'
        f'<span style="font-size:0.68rem;font-weight:600;letter-spacing:0.16em;text-transform:uppercase;'
        f'color:#0A0D2C;font-family:Inter,sans-serif;">{title}</span>{cap}</div>',
        unsafe_allow_html=True
    )


# ── PAGE HEADER ────────────────────────────────────────────────────
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
    unsafe_allow_html=True
)


# ── CHAT HELPERS ───────────────────────────────────────────────────
_STOP = {'AND','OR','THE','A','I','MY','TO','FOR','IS','IN','OF','WITH',
         'WANT','ANALYZE','PLEASE','SOME','PORTFOLIO','STOCKS','SHARES',
         'FUND','ETF','LIKE','WOULD','CAN','YOU','ME','AT','BY','AS'}

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
        if m.group(2) == 'k': v *= 1_000
        elif m.group(2) == 'm': v *= 1_000_000
        return int(v)
    return None

def _parse_int(text, lo=1, hi=10):
    m = re.search(r'\d+', text)
    if m:
        v = int(m.group())
        if lo <= v <= hi:
            return v
    return None

_Q = {
    "tickers": "Which stocks would you like to analyze? Enter tickers separated by commas — e.g. **AAPL, MSFT, GOOGL**. Crypto works too (BTC-USD).",
    "start":   "What **start date** for the analysis? (e.g. 01/01/2020 or '5 years ago')",
    "end":     "And the **end date**? (e.g. today, or 31/12/2024)",
    "invest":  "What is your **initial investment** amount? (e.g. $100,000 or 50k)",
    "horizon": "How many **years ahead** for the Monte Carlo simulation? Enter a number from 1–10.",
    "goal":    "Finally, what is your **target portfolio value**? (e.g. $200,000)",
}

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


# ── SIDEBAR ────────────────────────────────────────────────────────
_chat_init()
if "sb_mode" not in st.session_state:
    st.session_state.sb_mode = "Chat"

with st.sidebar:
    st.markdown(
        '<div class="sidebar-header">'
        '<div class="sidebar-header-title">Portfolio</div>'
        '<div class="sidebar-header-sub">Configuration</div>'
        '</div>',
        unsafe_allow_html=True
    )

    # ── Mode toggle ────────────────────────────────────
    c1, c2 = st.columns(2)
    with c1:
        if st.button("💬  Chat", use_container_width=True,
                     type="primary" if st.session_state.sb_mode == "Chat" else "secondary",
                     key="btn_chat"):
            st.session_state.sb_mode = "Chat"
            st.rerun()
    with c2:
        if st.button("⚙  Manual", use_container_width=True,
                     type="primary" if st.session_state.sb_mode == "Manual" else "secondary",
                     key="btn_manual"):
            st.session_state.sb_mode = "Manual"
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

        # Restart button
        if st.button("↺  Start over", use_container_width=True, key="chat_restart"):
            for k in ["chat_msgs", "chat_step", "chat_vals", "chat_done"]:
                st.session_state.pop(k, None)
            st.rerun()

        vals = st.session_state.chat_vals
        tickers_input      = vals.get("tickers_str",  "AAPL, MSFT, JPM, JNJ, XOM")
        start_date         = vals.get("start_date",   pd.to_datetime("2020-01-01").date())
        end_date           = vals.get("end_date",     date.today())
        initial_investment = vals.get("investment",   100000)
        mc_years           = vals.get("horizon",      5)
        target_value       = vals.get("goal",         200000)

        st.markdown("---")
        run = st.button("▶  Run Analysis", use_container_width=True,
                        disabled=not st.session_state.chat_done,
                        key="run_chat")

    # ── Manual mode ────────────────────────────────────
    else:
        _v = st.session_state.get("chat_vals", {})
        tickers_input = st.text_input(
            "Tickers (comma separated)",
            value=_v.get("tickers_str", "AAPL, MSFT, JPM, JNJ, XOM"),
            key="man_tickers"
        )
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "Start",
                value=_v.get("start_date", pd.to_datetime("2020-01-01").date()),
                format="DD/MM/YYYY", key="man_start"
            )
        with col2:
            end_date = st.date_input(
                "End",
                value=_v.get("end_date", date.today()),
                format="DD/MM/YYYY", key="man_end"
            )

        initial_investment = st.number_input(
            "Initial Investment ($)",
            value=_v.get("investment", 100000),
            step=10000, key="man_invest"
        )
        mc_years = st.slider(
            "Monte Carlo Horizon (Years)",
            min_value=1, max_value=10,
            value=_v.get("horizon", 5), key="man_horizon"
        )
        target_value = st.number_input(
            "Goal Target Value ($)",
            value=_v.get("goal", 200000),
            step=10000, key="man_goal",
            help="Probability of reaching this value is shown in Monte Carlo"
        )

        st.markdown("---")
        run = st.button("Run Analysis", use_container_width=True, key="run_manual")



# ── DATA LOADING ───────────────────────────────────────────────────
tickers = [t.strip().upper() for t in tickers_input.split(",")]

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
    rows = []
    for t in tickers:
        info = yf.Ticker(t).info
        rows.append({
            "Ticker":        t,
            "Sector":        info.get("sector",         "N/A"),
            "Market Cap":    info.get("marketCap",      None),
            "P/E Ratio":     info.get("trailingPE",     None),
            "P/B Ratio":     info.get("priceToBook",    None),
            "Profit Margin": info.get("profitMargins",  None),
            "Debt / Equity": info.get("debtToEquity",   None),
            "Dividend Yield":info.get("dividendYield",  None),
        })
    return pd.DataFrame(rows)


# ── SESSION STATE ──────────────────────────────────────────────────
if run:
    with st.spinner("Fetching market data..."):
        prices, returns         = load_data(tickers, start_date, end_date)
        spy                     = load_spy(start_date, end_date)
        fundamentals            = load_fundamentals(tickers)
    st.session_state["prices"]       = prices
    st.session_state["returns"]      = returns
    st.session_state["spy"]          = spy
    st.session_state["fundamentals"] = fundamentals
    st.session_state["tickers"]      = tickers
    st.session_state["ready"]        = True


# ── TABS ───────────────────────────────────────────────────────────
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
                '<div class="sidebar-prompt" onclick="mlpToggleSidebar()">'
                '<span>Configure your portfolio in the sidebar and click '
                '<strong>Run Analysis</strong> to begin.</span>'
                '<span class="sidebar-prompt-arrow">&#x203A;</span>'
                '</div>',
                unsafe_allow_html=True
            )


# ── TAB 0: HOME / COVER ────────────────────────────────────────────
with tab0:
    # ── Hero — all styles come from the CSS block above ───
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
        unsafe_allow_html=True
    )

    # ── Module cards ──────────────────────────────────
    st.markdown("<div style='height:2.5rem'></div>", unsafe_allow_html=True)
    section_header("What's Inside")

    modules = [
        ("Overview",      "Normalized price chart vs SPY benchmark, annualized return & volatility table, correlation heatmap."),
        ("Optimization",  "3,000-simulation efficient frontier with Max-Sharpe and Min-Volatility portfolio weights."),
        ("Monte Carlo",   "1,000-path simulation fan chart, goal-probability metric, and final-value distribution."),
        ("Risk Metrics",  "Sharpe, Sortino, Max Drawdown, 95% VaR & CVaR, rolling 6-month Sharpe, returns distribution."),
        ("Fundamentals",  "P/E, P/B, profit margin, debt/equity, dividend yield, sector breakdown, allocation vs. valuation bubble chart."),
    ]

    cols = st.columns(len(modules))
    for col, (title, desc) in zip(cols, modules):
        with col:
            st.markdown(
                f'<div class="module-card">'
                f'<div class="module-card-title">{title}</div>'
                f'<div class="module-card-desc">{desc}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    # ── Show summary stats if data loaded ─────────────
    if st.session_state.get("ready"):
        st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
        st.markdown("---")
        section_header("Portfolio at a Glance", "Max-Sharpe weights applied to historical data")

        _ret  = st.session_state["returns"]
        _tick = st.session_state["tickers"]
        _spy  = st.session_state["spy"]

        _ar  = _ret.mean() * 252
        _av  = _ret.std()  * np.sqrt(252)
        _sh  = _ar / _av
        _spy_ret = _spy.pct_change().dropna()
        _spy_ar  = _spy_ret.mean() * 252

        cols2 = st.columns(len(_tick) + 1)
        for c, t in zip(cols2[:-1], _tick):
            c.metric(t, f"{_ar[t]*100:.1f}%", f"σ {_av[t]*100:.1f}%")
        cols2[-1].metric("SPY", f"{_spy_ar*100:.1f}%", "benchmark")


# ── TAB 1: OVERVIEW ────────────────────────────────────────────────
with tab1:
    if st.session_state.get("ready"):
        prices  = st.session_state["prices"]
        returns = st.session_state["returns"]
        spy     = st.session_state["spy"]
        tickers = st.session_state["tickers"]

        section_header(
            "Normalized Price Performance",
            "All assets rebased to 100 at start date — SPY shown as benchmark"
        )

        all_prices = prices.join(spy, how="left")
        normalized = (all_prices / all_prices.iloc[0]) * 100

        fig_norm = go.Figure()
        for i, col in enumerate(tickers):
            fig_norm.add_trace(go.Scatter(
                x=normalized.index, y=normalized[col],
                name=col, mode="lines",
                line=dict(color=PALETTE[i % len(PALETTE)], width=1.75)
            ))
        fig_norm.add_trace(go.Scatter(
            x=normalized.index, y=normalized["SPY"],
            name="SPY", mode="lines",
            line=dict(color="#14D2C3", width=1.5, dash="dot"), opacity=0.8
        ))
        apply_theme(fig_norm, height=420,
                    yaxis_title="Indexed (base 100)",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02),
                    hovermode="x unified")
        st.plotly_chart(fig_norm, use_container_width=True)

        st.markdown("---")

        section_header(
            "Return & Volatility Summary",
            "Annualized figures — SPY included for benchmark comparison"
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
            "Lower values indicate better portfolio diversification"
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


# ── TAB 2: OPTIMIZATION ────────────────────────────────────────────
with tab2:
    if st.session_state.get("ready"):
        returns = st.session_state["returns"]
        tickers = st.session_state["tickers"]

        num_assets = len(tickers)
        ann_return = returns.mean() * 252
        cov_matrix = returns.cov()  * 252

        np.random.seed(42)
        results = []
        for _ in range(3000):
            w    = np.random.dirichlet(np.ones(num_assets))
            pr   = np.dot(w, ann_return)
            pv   = np.sqrt(w @ cov_matrix @ w)
            sh   = pr / pv
            results.append({"Return": pr, "Volatility": pv, "Sharpe": sh, "Weights": w})

        results_df     = pd.DataFrame(results)
        max_sharpe_idx = results_df["Sharpe"].idxmax()
        max_sharpe     = results_df.loc[max_sharpe_idx]
        min_vol_idx    = results_df["Volatility"].idxmin()
        min_vol        = results_df.loc[min_vol_idx]

        section_header(
            "Efficient Frontier",
            "3,000 simulated portfolios — color denotes Sharpe ratio"
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
            name="Max Sharpe"
        )
        fig_ef.add_scatter(
            x=[min_vol["Volatility"]], y=[min_vol["Return"]],
            mode="markers",
            marker=dict(size=14, color="#14D2C3", symbol="diamond",
                        line=dict(color="white", width=1.5)),
            name="Min Volatility"
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
            "Max Sharpe maximizes return per unit of risk — Min Volatility minimizes risk"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                '<div style="font-size:0.65rem;letter-spacing:0.14em;text-transform:uppercase;'
                'color:#1533F0;font-weight:600;margin-bottom:0.75rem;font-family:Inter,sans-serif;">'
                '★ Max Sharpe</div>', unsafe_allow_html=True
            )
            ms_w = pd.DataFrame({
                "Ticker": tickers,
                "Weight (%)": (max_sharpe["Weights"] * 100).round(2)
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
                '◆ Min Volatility</div>', unsafe_allow_html=True
            )
            mv_w = pd.DataFrame({
                "Ticker": tickers,
                "Weight (%)": (min_vol["Weights"] * 100).round(2)
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


# ── TAB 3: MONTE CARLO ─────────────────────────────────────────────
with tab3:
    if st.session_state.get("ready"):
        returns = st.session_state["returns"]
        tickers = st.session_state["tickers"]

        opt_weights = st.session_state.get(
            "max_sharpe_weights",
            np.ones(len(tickers)) / len(tickers)
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
            f"Max-Sharpe portfolio — 1,000 paths over {mc_years}Y horizon"
        )

        prob_goal  = (final_vals >= target_value).mean() * 100
        median_val = final_vals.median()
        p10_val    = final_vals.quantile(0.10)
        p90_val    = final_vals.quantile(0.90)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Median Outcome",          f"${median_val:,.0f}")
        m2.metric("90th Percentile",         f"${p90_val:,.0f}")
        m3.metric("10th Percentile",         f"${p10_val:,.0f}")
        m4.metric(f"Prob. ≥ ${target_value:,.0f}", f"{prob_goal:.1f}%")

        st.markdown("---")

        section_header(
            "Simulation Paths",
            "200 of 1,000 paths shown — key percentile bands overlaid"
        )

        fig_mc = go.Figure()
        for i in range(200):
            fig_mc.add_trace(go.Scatter(
                x=list(range(trading_days + 1)),
                y=sim_df.iloc[:, i],
                mode="lines",
                line=dict(color="rgba(21,51,240,0.04)", width=1),
                showlegend=False
            ))

        med_p = sim_df.median(axis=1)
        p10_p = sim_df.quantile(0.10, axis=1)
        p90_p = sim_df.quantile(0.90, axis=1)

        fig_mc.add_trace(go.Scatter(
            x=list(range(trading_days + 1)), y=med_p,
            mode="lines", line=dict(color="#0A0D2C", width=2), name="Median"
        ))
        fig_mc.add_trace(go.Scatter(
            x=list(range(trading_days + 1)), y=p90_p,
            mode="lines", line=dict(color="#10B981", width=1.5, dash="dash"),
            name="90th Pct"
        ))
        fig_mc.add_trace(go.Scatter(
            x=list(range(trading_days + 1)), y=p10_p,
            mode="lines", line=dict(color="#EF4444", width=1.5, dash="dash"),
            name="10th Pct"
        ))
        fig_mc.add_hline(
            y=target_value, line_dash="dot", line_color="#1533F0",
            annotation_text=f"Goal  ${target_value:,.0f}",
            annotation_position="bottom right",
            annotation_font=dict(color="#1533F0", size=10)
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
            "Outcome spread across all 1,000 simulations at the horizon"
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
            annotation_font=dict(color="#EF4444", size=10)
        )
        fig_dist.add_vline(
            x=target_value, line_dash="dash", line_color="#10B981",
            annotation_text="Goal",
            annotation_position="top left",
            annotation_font=dict(color="#10B981", size=10)
        )
        apply_theme(fig_dist, height=340, showlegend=False)
        st.plotly_chart(fig_dist, use_container_width=True)


# ── TAB 4: RISK METRICS ────────────────────────────────────────────
with tab4:
    if st.session_state.get("ready"):
        returns = st.session_state["returns"]
        tickers = st.session_state["tickers"]

        opt_weights = st.session_state.get(
            "max_sharpe_weights",
            np.ones(len(tickers)) / len(tickers)
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
            "Max-Sharpe portfolio weights applied to historical returns"
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
                "Distance from rolling peak — underwater periods shaded"
            )
            fig_dd = go.Figure()
            fig_dd.add_trace(go.Scatter(
                x=drawdown.index, y=drawdown * 100,
                mode="lines", fill="tozeroy",
                line=dict(color="#EF4444", width=1),
                fillcolor="rgba(239,68,68,0.10)",
                name="Drawdown"
            ))
            apply_theme(fig_dd, height=300,
                        yaxis_title="Drawdown (%)", xaxis_title="",
                        showlegend=False)
            st.plotly_chart(fig_dd, use_container_width=True)

        with col_r:
            section_header(
                "Rolling 6-Month Sharpe",
                "Risk-adjusted return consistency across 126-day windows"
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
                name="Rolling Sharpe"
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
            "Histogram of portfolio daily returns — 95% VaR threshold marked"
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
            annotation_font=dict(color="#EF4444", size=10)
        )
        apply_theme(fig_ret, height=320, showlegend=False)
        st.plotly_chart(fig_ret, use_container_width=True)


# ── TAB 5: FUNDAMENTALS ────────────────────────────────────────────
with tab5:
    if st.session_state.get("ready"):
        fundamentals = st.session_state["fundamentals"]
        tickers      = st.session_state["tickers"]

        opt_weights = st.session_state.get(
            "max_sharpe_weights",
            np.ones(len(tickers)) / len(tickers)
        )

        section_header(
            "Fundamental Statistics",
            "Key metrics per holding — sourced from Yahoo Finance"
        )

        display_df = fundamentals.copy()
        display_df["Market Cap"] = display_df["Market Cap"].apply(
            lambda x: f"${x/1e9:.1f}B" if pd.notna(x) else "—")
        display_df["P/E Ratio"] = display_df["P/E Ratio"].apply(
            lambda x: f"{x:.1f}x" if pd.notna(x) else "—")
        display_df["P/B Ratio"] = display_df["P/B Ratio"].apply(
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
            "Portfolio weight by sector — based on Max-Sharpe allocation"
        )

        sector_df = pd.DataFrame({
            "Ticker": tickers,
            "Sector": fundamentals["Sector"].values,
            "Weight": opt_weights
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
                marker=dict(line=dict(color="white", width=2))
            )
            apply_theme(fig_pie, height=360, showlegend=False)
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            fig_bar = px.bar(
                sector_grouped, x="Weight (%)", y="Sector",
                orientation="h", color="Sector", text="Weight (%)",
                color_discrete_sequence=PALETTE,
            )
            fig_bar.update_traces(marker_line_width=0,
                                  textfont=dict(size=10))
            apply_theme(fig_bar, height=360, showlegend=False, yaxis_title="")
            st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("---")

        section_header(
            "Allocation vs. Valuation",
            "Bubble size = portfolio weight — spot if optimizer is over-weighting expensive stocks"
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
