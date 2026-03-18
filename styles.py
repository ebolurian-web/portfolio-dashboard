import streamlit as st
import streamlit.components.v1 as components

CSS_BLOCK = """
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
"""

JS_BLOCK = """
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
        if (doc.getElementById('mlp-lines')) return;

        var style = doc.createElement('style');
        style.id  = 'mlp-style';
        style.textContent =
            '.cover-hero { position:relative !important; overflow:hidden !important; }' +
            '.cover-hero > *:not(#mlp-lines) { position:relative !important; z-index:1 !important; }';
        doc.head.appendChild(style);

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

        doc.addEventListener('mousemove',  function (e) { mx = e.clientX; my = e.clientY; mouseOn = true; });
        doc.addEventListener('mouseleave', function ()  { mouseOn = false; });

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
"""


def inject_styles():
    st.markdown(CSS_BLOCK, unsafe_allow_html=True)
    components.html(JS_BLOCK, height=0, scrolling=False)
