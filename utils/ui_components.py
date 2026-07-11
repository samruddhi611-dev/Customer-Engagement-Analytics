# ==================================================
# REUSABLE UI COMPONENTS
# ==================================================

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from config import THEME_COLORS, RiskLevel
import pandas as pd


def render_kpi_card(
    title: str,
    value: str,
    delta: str = None,
    icon: str = "📊",
    color: str = "#1976d2",
    delta_color: str = "normal",
):
    """Render professional KPI card"""
    col1, col2 = st.columns([4, 1])
    with col1:
        st.metric(title, value, delta=delta, delta_color=delta_color)
    with col2:
        st.markdown(
            f"<div style='font-size: 32px; text-align: center; padding: 10px;'>{icon}</div>",
            unsafe_allow_html=True,
        )


def render_risk_gauge(risk_percentage: float, label: str = "Risk Level"):
    """Render risk gauge chart"""
    if risk_percentage > 70:
        color = "#e74c3c"
        status = "🚨 CRITICAL"
    elif risk_percentage > 50:
        color = "#ff9800"
        status = "⚠️ HIGH"
    elif risk_percentage > 30:
        color = "#f39c12"
        status = "⚡ MEDIUM"
    else:
        color = "#2ecc71"
        status = "✅ LOW"

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=risk_percentage,
            title={"text": label},
            delta={"reference": 50},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": color},
                "steps": [
                    {"range": [0, 30], "color": "#e8f5e9"},
                    {"range": [30, 70], "color": "#fff3e0"},
                    {"range": [70, 100], "color": "#ffebee"},
                ],
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": 90,
                },
            },
        )
    )
    fig.update_layout(height=300, font={"size": 12})
    st.plotly_chart(fig, use_container_width=True, key=f"gauge_{label}")
    st.markdown(f"<p style='text-align: center; font-size: 16px; font-weight: bold;'>{status}</p>", unsafe_allow_html=True)


def render_recommendation_card(recommendations: list):
    """Render recommendation card"""
    st.markdown(
        f"""
        <div style='background: #e3f2fd; padding: 20px; border-radius: 12px; border-left: 4px solid #1976d2;'>
            <p style='font-weight: bold; margin-top: 0;'>💡 Recommendations</p>
            {''.join([f'<p style="margin: 8px 0;">• {rec}</p>' for rec in recommendations])}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_profile_card(customer: dict, prediction: dict):
    """Render customer profile card"""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Age",
            f"{customer.get('age', 'N/A')} yrs"
            if customer.get('age')
            else "N/A",
        )

    with col2:
        st.metric(
            "Balance",
            f"${customer.get('balance', 0):,.0f}"
            if customer.get('balance')
            else "$0",
        )

    with col3:
        st.metric(
            "Products",
            customer.get('num_of_products', 0) or 0,
        )

    with col4:
        st.metric(
            "Engagement",
            f"{prediction.get('engagement_score', 0):.1f}"
            if prediction
            else "N/A",
        )


def render_professional_table(df: pd.DataFrame, title: str = None):
    """Render professional data table with sorting and pagination"""
    if title:
        st.subheader(title)

    # Display with enhanced styling
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            col: st.column_config.Column()
            for col in df.columns
        },
    )


def render_status_badge(status: str):
    """Render status badge"""
    colors = {
        "Active": "#2ecc71",
        "Inactive": "#95a5a6",
        "Dormant": "#e74c3c",
        "Flagged": "#ff9800",
    }
    color = colors.get(status, "#95a5a6")
    return f'<span style="background: {color}; color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold;">{status}</span>'


def render_confirmation_dialog(title: str, message: str) -> bool:
    """Render confirmation dialog"""
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Confirm", use_container_width=True, key="confirm"):
            return True
    with col2:
        if st.button("❌ Cancel", use_container_width=True, key="cancel"):
            return False
    return None


def render_donut_chart(data: pd.DataFrame, names: str, values: str, title: str):
    """Render professional donut chart"""
    fig = px.pie(
        data,
        names=names,
        values=values,
        hole=0.3,
        title=title,
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig.update_traces(textposition="inside", textinfo="label+percent")
    fig.update_layout(height=400, showlegend=True)
    st.plotly_chart(fig, use_container_width=True, key=f"donut_{title}")


def render_treemap(data: pd.DataFrame, labels: str, parents: str, values: str, title: str):
    """Render treemap visualization"""
    fig = px.treemap(
        data,
        labels=labels,
        parents=parents,
        values=values,
        title=title,
        color=values,
        color_continuous_scale="RdYlGn_r",
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True, key=f"treemap_{title}")


def render_sunburst(data: pd.DataFrame, labels: str, parents: str, values: str, title: str):
    """Render sunburst visualization"""
    fig = px.sunburst(
        data,
        labels=labels,
        parents=parents,
        values=values,
        title=title,
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True, key=f"sunburst_{title}")


def render_scatter_plot(data: pd.DataFrame, x: str, y: str, color: str, title: str):
    """Render scatter plot"""
    fig = px.scatter(
        data,
        x=x,
        y=y,
        color=color,
        title=title,
        size_max=60,
    )
    fig.update_layout(height=400, hovermode="closest")
    st.plotly_chart(fig, use_container_width=True, key=f"scatter_{title}")


def render_bubble_chart(data: pd.DataFrame, x: str, y: str, size: str, color: str, title: str):
    """Render bubble chart"""
    fig = px.scatter(
        data,
        x=x,
        y=y,
        size=size,
        color=color,
        title=title,
        hover_name=data.index,
    )
    fig.update_layout(height=400, hovermode="closest")
    st.plotly_chart(fig, use_container_width=True, key=f"bubble_{title}")


def render_area_chart(data: pd.DataFrame, title: str):
    """Render area chart"""
    fig = px.area(data, title=title)
    fig.update_layout(height=400, hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True, key=f"area_{title}")


def render_waterfall_chart(data: pd.DataFrame, x: str, y: str, title: str):
    """Render waterfall chart"""
    fig = go.Figure(go.Waterfall(
        x=data[x],
        y=data[y],
        connector={"line": {"color": "rgba(63, 63, 63, 0.5)"}},
    ))
    fig.update_layout(title=title, height=400)
    st.plotly_chart(fig, use_container_width=True, key=f"waterfall_{title}")


def render_radar_chart(data: pd.DataFrame, title: str):
    """Render radar chart"""
    fig = px.line_polar(data, title=title)
    fig.update_traces(fill="toself")
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True, key=f"radar_{title}")
