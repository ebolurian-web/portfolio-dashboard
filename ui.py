import streamlit as st

PALETTE = ["#1533F0", "#14D2C3", "#F59E0B", "#10B981", "#8B5CF6", "#EF4444", "#6B7280"]

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


def apply_theme(fig, height=420, **kw):
    layout = {**CHART, "height": height, **kw}
    fig.update_layout(**layout)
    return fig


def section_header(title, caption=None):
    cap = (
        f'<div style="font-size:0.7rem;color:#9CA3AF;margin-top:0.3rem;'
        f'font-family:Inter,sans-serif;letter-spacing:0.02em;">{caption}</div>'
    ) if caption else ""
    st.markdown(
        f'<div style="margin:0.25rem 0 1rem 0;padding-bottom:0.55rem;border-bottom:1px solid #E5E7F0;">'
        f'<span style="font-size:0.68rem;font-weight:600;letter-spacing:0.16em;text-transform:uppercase;'
        f'color:#0A0D2C;font-family:Inter,sans-serif;">{title}</span>{cap}</div>',
        unsafe_allow_html=True,
    )
