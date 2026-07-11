# ==================================================
# IMPORTS
# ==================================================

import streamlit as st
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

import plotly.express as px

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Customer Engagement Dashboard",
    page_icon="🏦",
    layout="wide"
)


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>
    
    /* Main Background */
    .main {
        background: linear-gradient(135deg, #f5f7fb 0%, #eef2f8 100%);
        padding: 20px;
    }
    
    /* Sidebar Styling */
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a2a4e 0%, #0f1829 100%);
        box-shadow: 2px 0 15px rgba(0, 0, 0, 0.2);
    }
    
    div[data-testid="stSidebar"] * {
        color: #ffffff;
    }
    
    /* Sidebar Headers */
    div[data-testid="stSidebar"] h2 {
        color: #64b5f6;
        font-size: 18px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
        letter-spacing: 0.5px;
    }
    
    /* Metric Cards */
    .stMetric {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
        border-left: 4px solid #1976d2;
        transition: all 0.3s ease;
    }
    
    .stMetric:hover {
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
        transform: translateY(-2px);
    }
    
    /* Headers and Titles */
    h1 {
        color: #0f1829;
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 10px;
        letter-spacing: -0.5px;
    }
    
    h2 {
        color: #1a2a4e;
        font-size: 24px;
        font-weight: 600;
        margin-top: 25px;
        margin-bottom: 15px;
    }
    
    h3 {
        color: #2c3e50;
        font-size: 18px;
        font-weight: 600;
        margin-top: 20px;
    }
    
    /* Dividers */
    .element-container:has(> div[data-testid="stHorizontalBlock"]) {
        margin: 20px 0;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #1976d2 0%, #1565c0 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(25, 118, 210, 0.3);
    }
    
    .stButton > button:hover {
        box-shadow: 0 6px 20px rgba(25, 118, 210, 0.4);
        transform: translateY(-2px);
    }
    
    /* Select Boxes & Input Fields */
    .stSelectbox, .stMultiSelect, .stSlider {
        margin-bottom: 15px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [aria-selected="true"] {
        color: #1976d2;
        border-bottom: 3px solid #1976d2;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #f5f7fb;
        border-radius: 8px;
        padding: 12px 15px;
    }
    
    /* Captions */
    .caption {
        color: #64b5f6;
        font-size: 14px;
        font-weight: 500;
        margin-top: -5px;
        margin-bottom: 20px;
    }
    
    /* Container Styling */
    .element-container {
        margin-bottom: 15px;
    }
    
    /* Success/Error/Warning Messages */
    .stSuccess {
        background-color: #e8f5e9;
        border-radius: 8px;
        padding: 15px;
    }
    
    .stError {
        background-color: #ffebee;
        border-radius: 8px;
        padding: 15px;
    }
    
    .stWarning {
        background-color: #fff3e0;
        border-radius: 8px;
        padding: 15px;
    }
    
    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data
def load_data():

    df = pd.read_csv(
        "data/churn.csv"
    )

    return df


df = load_data()



# ==================================================
# ENGAGEMENT SCORE
# ==================================================

def calculate_engagement_score(df):

    data = df.copy()

    balance_score = (
        data["Balance"] /
        data["Balance"].max()
    ) * 40


    product_score = (
        data["NumOfProducts"] /
        data["NumOfProducts"].max()
    ) * 30


    activity_score = (
        data["IsActiveMember"] * 30
    )


    data["Engagement_Score"] = (
        balance_score +
        product_score +
        activity_score
    )


    return data



df = calculate_engagement_score(df)



# ==================================================
# CHURN MODEL
# ==================================================

@st.cache_resource
def train_churn_model(df):

    data = df.copy()


    data = data.drop(
        [
            "CustomerId",
            "Surname"
        ],
        axis=1,
        errors="ignore"
    )


    encoder = LabelEncoder()


    for col in data.select_dtypes(
        include="object"
    ):

        data[col] = encoder.fit_transform(
            data[col]
        )


    X = data.drop(
        "Exited",
        axis=1
    )


    y = data["Exited"]


    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )


    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )


    model.fit(
        X_train,
        y_train
    )


    predictions = model.predict(
        X_test
    )


    accuracy = accuracy_score(
        y_test,
        predictions
    )


    return (
        model,
        accuracy,
        X_test,
        y_test
    )



model, accuracy, X_test, y_test = train_churn_model(df)



# ==================================================
# BUSINESS RECOMMENDATION
# ==================================================

def generate_recommendation(customer, probability):

    recommendations = []


    if probability > 70:

        recommendations.append(
            "Contact customer with retention offers"
        )

        recommendations.append(
            "Provide personalized relationship manager support"
        )


    elif probability > 40:

        recommendations.append(
            "Send engagement campaigns"
        )

        recommendations.append(
            "Offer additional banking benefits"
        )


    else:

        recommendations.append(
            "Maintain regular engagement"
        )


    if customer["NumOfProducts"] <= 1:

        recommendations.append(
            "Suggest additional banking products"
        )


    if customer["Balance"] < df["Balance"].median():

        recommendations.append(
            "Promote savings and investment plans"
        )


    return recommendations
# ==================================================
# TITLE AND HEADER
# ==================================================

st.markdown(
    """
    <div style='text-align: center; margin-bottom: 10px;'>
        <h1 style='color: #0f1829; margin: 0;'>🏦 Customer Engagement & Retention Intelligence Platform</h1>
        <p style='color: #64b5f6; font-size: 16px; font-weight: 500; margin-top: 8px;'>Advanced Analytics for Customer Behavior & Churn Prediction</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")



# ==================================================
# SIDEBAR NAVIGATION & FILTERS
# ==================================================

st.sidebar.markdown(
    """
    <div style='padding: 20px 0; text-align: center; border-bottom: 2px solid #64b5f6; margin-bottom: 20px;'>
        <h2 style='color: #64b5f6; font-size: 20px; margin: 0;'>📱 Navigation</h2>
    </div>
    """,
    unsafe_allow_html=True
)

page = st.sidebar.radio(
    "Select Module",
    [
        "Dashboard",
        "Engagement Analysis",
        "Product Analysis",
        "High Value Customers",
        "Engagement Score",
        "Churn Prediction",
        "Model Evaluation",
        "Executive Summary"
    ],
    key="page_selector"
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    """
    <div style='margin-top: 20px; margin-bottom: 15px;'>
        <h2 style='color: #64b5f6; font-size: 16px; margin: 0 0 15px 0;'>🎯 Filters</h2>
    </div>
    """,
    unsafe_allow_html=True
)

country = st.sidebar.multiselect(
    "Geography",
    df["Geography"].unique(),
    default=df["Geography"].unique(),
    help="Select countries to filter the data"
)

gender = st.sidebar.multiselect(
    "Gender",
    df["Gender"].unique(),
    default=df["Gender"].unique(),
    help="Select gender categories"
)

st.sidebar.markdown("---")

filtered_df = df[
    (df["Geography"].isin(country)) &
    (df["Gender"].isin(gender))
]

# Display filter summary
st.sidebar.markdown(
    f"""
    <div style='background: #0f1829; padding: 12px; border-radius: 8px; margin-top: 15px;'>
        <p style='color: #64b5f6; font-size: 12px; margin: 0;'>Active Records: <b style="color: #4db8ff">{len(filtered_df):,}</b></p>
    </div>
    """,
    unsafe_allow_html=True
)



# ==================================================
# DASHBOARD PAGE
# ==================================================

if page == "Dashboard":

    st.markdown(
        """
        <h2 style='color: #0f1829; margin-bottom: 20px;'>📊 Customer Overview Dashboard</h2>
        """,
        unsafe_allow_html=True
    )

    total_customers = len(filtered_df)
    churn_rate = (filtered_df["Exited"].mean() * 100)
    retention_rate = (100 - churn_rate)
    avg_balance = (filtered_df["Balance"].mean())
    avg_engagement = (filtered_df["Engagement_Score"].mean())

    col1, col2, col3, col4 = st.columns(4, gap="medium")

    with col1:
        st.metric(
            "👥 Total Customers",
            f"{total_customers:,}",
            delta=f"{len(filtered_df) - len(df)} from all"
        )

    with col2:
        st.metric(
            "📉 Churn Rate",
            f"{churn_rate:.2f}%",
            delta=f"Retention: {retention_rate:.2f}%",
            delta_color="inverse"
        )

    with col3:
        st.metric(
            "💰 Avg Balance",
            f"${avg_balance:,.0f}",
            delta=f"Total: ${filtered_df['Balance'].sum():,.0f}"
        )

    with col4:
        st.metric(
            "📈 Engagement Score",
            f"{avg_engagement:.1f}",
            delta=f"Max: {filtered_df['Engagement_Score'].max():.1f}"
        )

    st.markdown("---")

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.subheader("Customer Churn Distribution")
        churn_chart = px.pie(
            filtered_df,
            names="Exited",
            labels={0: "Retained", 1: "Churned"},
            color_discrete_map={0: "#2ecc71", 1: "#e74c3c"},
            title=None
        )
        churn_chart.update_traces(
            textposition='inside',
            textinfo='label+percent',
            hoverinfo='label+value+percent'
        )
        churn_chart.update_layout(
            height=400,
            showlegend=True,
            font=dict(size=12)
        )
        st.plotly_chart(churn_chart, use_container_width=True, key="dashboard_churn")

    with col2:
        st.subheader("Geographic Distribution")
        geo = (filtered_df["Geography"].value_counts().reset_index())
        geo.columns = ["Geography", "Customers"]
        
        geo_chart = px.bar(
            geo,
            x="Geography",
            y="Customers",
            color="Geography",
            color_discrete_sequence=["#1976d2", "#64b5f6", "#42a5f5"],
            title=None
        )
        geo_chart.update_traces(hovertemplate='<b>%{x}</b><br>Customers: %{y}<extra></extra>')
        geo_chart.update_layout(
            height=400,
            showlegend=False,
            xaxis_title="",
            yaxis_title="Number of Customers",
            font=dict(size=11),
            plot_bgcolor="rgba(245, 247, 251, 0.5)",
            paper_bgcolor="white"
        )
        st.plotly_chart(geo_chart, use_container_width=True, key="dashboard_geo")



# ==================================================
# ENGAGEMENT ANALYSIS
# ==================================================

elif page == "Engagement Analysis":

    st.markdown(
        """
        <h2 style='color: #0f1829; margin-bottom: 20px;'>📈 Customer Engagement Analysis</h2>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([2, 1], gap="medium")

    with col1:
        st.subheader("Correlation Heatmap")
        numeric_df = (filtered_df.select_dtypes(include=np.number))
        corr = numeric_df.corr()

        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(
            corr,
            annot=True,
            fmt=".2f",
            cmap="coolwarm",
            center=0,
            ax=ax,
            cbar_kws={'label': 'Correlation'},
            square=True,
            linewidths=0.5,
            linecolor='white'
        )
        ax.set_title("Feature Correlation Matrix", fontsize=14, fontweight="bold", pad=20)
        plt.tight_layout()
        st.pyplot(fig)

    with col2:
        st.subheader("Key Insights")
        st.markdown(
            """
            <div style='background: #e3f2fd; padding: 15px; border-radius: 8px; border-left: 4px solid #1976d2;'>
                <p style='margin: 8px 0; color: #0f1829;'><b>Engagement Score</b></p>
                <p style='margin: 8px 0; font-size: 12px; color: #1565c0;'>Positive correlation with active membership</p>
                
                <p style='margin: 15px 0 8px 0; color: #0f1829;'><b>Balance & Age</b></p>
                <p style='margin: 8px 0; font-size: 12px; color: #1565c0;'>Age shows relationship with balance levels</p>
                
                <p style='margin: 15px 0 8px 0; color: #0f1829;'><b>Activity Status</b></p>
                <p style='margin: 8px 0; font-size: 12px; color: #1565c0;'>Active members have higher engagement scores</p>
            </div>
            """,
            unsafe_allow_html=True
        )



# ==================================================
# PRODUCT ANALYSIS
# ==================================================

elif page == "Product Analysis":

    st.markdown(
        """
        <h2 style='color: #0f1829; margin-bottom: 20px;'>🛍️ Product Analysis</h2>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([2, 1], gap="medium")

    with col1:
        product = (filtered_df["NumOfProducts"].value_counts().reset_index())
        product.columns = ["Products", "Customers"]
        product = product.sort_values("Products")

        fig = px.bar(
            product,
            x="Products",
            y="Customers",
            color="Customers",
            color_continuous_scale="Blues",
            title=None
        )
        fig.update_traces(
            hovertemplate='<b>%{x} Product(s)</b><br>Customers: %{y}<extra></extra>',
            marker_line_width=1,
            marker_line_color='white'
        )
        fig.update_layout(
            height=400,
            xaxis_title="Number of Products",
            yaxis_title="Number of Customers",
            font=dict(size=11),
            plot_bgcolor="rgba(245, 247, 251, 0.5)",
            paper_bgcolor="white",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True, key="product_chart")

    with col2:
        st.subheader("Product Distribution")
        for idx, row in product.iterrows():
            st.markdown(
                f"""
                <div style='background: white; padding: 10px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #1976d2;'>
                    <p style='margin: 0; font-weight: 600; color: #0f1829;'>{int(row["Products"])} Product{'s' if row["Products"] != 1 else ''}</p>
                    <p style='margin: 5px 0 0 0; font-size: 12px; color: #64b5f6;'>{int(row["Customers"]):,} customers</p>
                </div>
                """,
                unsafe_allow_html=True
            )



# ==================================================
# HIGH VALUE CUSTOMERS
# ==================================================

elif page == "High Value Customers":

    st.markdown(
        """
        <h2 style='color: #0f1829; margin-bottom: 20px;'>⭐ High Value Customer Detector</h2>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        balance_limit = st.slider(
            "Minimum Balance ($)",
            0,
            250000,
            100000,
            step=10000,
            help="Filter customers with balance above this threshold"
        )

    with col2:
        st.markdown(
            f"""
            <div style='background: #e8f5e9; padding: 15px; border-radius: 8px; border-left: 4px solid #2ecc71; margin-top: 25px;'>
                <p style='color: #1b5e20; font-size: 12px; margin: 0 0 5px 0;'>Filter Threshold</p>
                <p style='color: #2ecc71; font-size: 20px; font-weight: bold; margin: 0;'>${balance_limit:,}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        high_value = filtered_df[
            (filtered_df["Balance"] >= balance_limit) &
            (filtered_df["IsActiveMember"] == 0)
        ]
        st.markdown(
            f"""
            <div style='background: #fff3e0; padding: 15px; border-radius: 8px; border-left: 4px solid #ff9800; margin-top: 25px;'>
                <p style='color: #e65100; font-size: 12px; margin: 0 0 5px 0;'>At Risk</p>
                <p style='color: #f57c00; font-size: 20px; font-weight: bold; margin: 0;'>{len(high_value)} Customers</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    if len(high_value) > 0:
        st.subheader(f"High Value At-Risk Customers ({len(high_value)})")
        
        display_cols = ["CustomerId", "Age", "Balance", "NumOfProducts", "IsActiveMember", "Engagement_Score", "Exited"]
        st.dataframe(
            high_value[display_cols].sort_values("Balance", ascending=False),
            use_container_width=True,
            hide_index=True
        )

        csv = high_value.to_csv(index=False)
        st.download_button(
            "📥 Download High-Value Customer Data",
            csv,
            "high_value_customers.csv",
            "text/csv",
            use_container_width=True
        )
    else:
        st.info("✅ No high-value at-risk customers found with the current filters.", icon="ℹ️")



# ==================================================
# ENGAGEMENT SCORE
# ==================================================

elif page == "Engagement Score":

    st.markdown(
        """
        <h2 style='color: #0f1829; margin-bottom: 20px;'>📈 Customer Engagement Score</h2>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1, 2], gap="medium")

    with col1:
        st.subheader("Top 10 Engaged")
        top = (
            filtered_df
            .sort_values("Engagement_Score", ascending=False)
            .head(10)
        )

        for idx, (_, row) in enumerate(top.iterrows(), 1):
            st.markdown(
                f"""
                <div style='background: white; padding: 10px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #1976d2;'>
                    <p style='margin: 0; font-weight: 600; color: #0f1829;'>#{idx} - ID: {int(row["CustomerId"])}</p>
                    <p style='margin: 5px 0 0 0; font-size: 12px; color: #64b5f6;'>Score: {row["Engagement_Score"]:.1f}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    with col2:
        st.subheader("Engagement Score Distribution")
        fig = px.histogram(
            filtered_df,
            x="Engagement_Score",
            nbins=30,
            color_discrete_sequence=["#1976d2"],
            title=None
        )
        fig.update_traces(
            hovertemplate='<b>Score Range: %{x}</b><br>Customers: %{y}<extra></extra>',
            marker_line_width=1,
            marker_line_color='white'
        )
        fig.update_layout(
            height=400,
            xaxis_title="Engagement Score",
            yaxis_title="Number of Customers",
            font=dict(size=11),
            plot_bgcolor="rgba(245, 247, 251, 0.5)",
            paper_bgcolor="white",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True, key="engagement_distribution")

    st.markdown("---")

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.metric(
            "Average Score",
            f"{filtered_df['Engagement_Score'].mean():.1f}",
            delta=f"Median: {filtered_df['Engagement_Score'].median():.1f}"
        )

    with col2:
        st.metric(
            "Highest Score",
            f"{filtered_df['Engagement_Score'].max():.1f}",
            delta=f"Max Customer: {int(filtered_df.loc[filtered_df['Engagement_Score'].idxmax(), 'CustomerId'])}"
        )

    with col3:
        st.metric(
            "Lowest Score",
            f"{filtered_df['Engagement_Score'].min():.1f}",
            delta=f"Min Customer: {int(filtered_df.loc[filtered_df['Engagement_Score'].idxmin(), 'CustomerId'])}"
        )

elif page == "Churn Prediction":

    st.markdown(
        """
        <h2 style='color: #0f1829; margin-bottom: 20px;'>🤖 Customer Churn Prediction</h2>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style='background: #e3f2fd; padding: 15px; border-radius: 8px; border-left: 4px solid #1976d2; margin-bottom: 20px;'>
            <p style='margin: 0; color: #0f1829; font-weight: 600;'>Model Performance</p>
            <p style='margin: 8px 0 0 0; font-size: 14px; color: #1565c0;'>Accuracy: <b>{accuracy*100:.2f}%</b></p>
        </div>
        """,
        unsafe_allow_html=True
    )

    customer_id = st.selectbox(
        "Select Customer for Prediction",
        filtered_df["CustomerId"].unique(),
        help="Choose a customer to predict churn probability"
    )

    customer = filtered_df[
        filtered_df["CustomerId"] == customer_id
    ].iloc[0]

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.metric("Age", f"{int(customer['Age'])} years")

    with col2:
        st.metric("Balance", f"${customer['Balance']:,.0f}")

    with col3:
        st.metric("Products", f"{int(customer['NumOfProducts'])}")

    st.markdown("---")

    if st.button("🔮 Predict Churn Probability", use_container_width=True, type="primary"):

        input_data = customer.drop("Exited")
        input_df = pd.DataFrame([input_data])
        input_df = input_df.drop(["CustomerId", "Surname"], axis=1, errors="ignore")

        encoder = LabelEncoder()

        for col in input_df.select_dtypes(include="object"):
            input_df[col] = encoder.fit_transform(input_df[col])

        probability = model.predict_proba(input_df)[0][1] * 100

        st.markdown("---")

        col1, col2 = st.columns([1, 2], gap="medium")

        with col1:
            if probability > 70:
                st.markdown(
                    f"""
                    <div style='background: #ffebee; padding: 20px; border-radius: 8px; border-left: 4px solid #c62828; text-align: center;'>
                        <p style='margin: 0; color: #c62828; font-size: 28px; font-weight: bold;'>{probability:.1f}%</p>
                        <p style='margin: 10px 0 0 0; color: #b71c1c; font-weight: 600;'>🚨 HIGH RISK</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            elif probability > 40:
                st.markdown(
                    f"""
                    <div style='background: #fff3e0; padding: 20px; border-radius: 8px; border-left: 4px solid #ef6c00; text-align: center;'>
                        <p style='margin: 0; color: #ef6c00; font-size: 28px; font-weight: bold;'>{probability:.1f}%</p>
                        <p style='margin: 10px 0 0 0; color: #e65100; font-weight: 600;'>⚠️ MEDIUM RISK</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div style='background: #e8f5e9; padding: 20px; border-radius: 8px; border-left: 4px solid #2e7d32; text-align: center;'>
                        <p style='margin: 0; color: #2e7d32; font-size: 28px; font-weight: bold;'>{probability:.1f}%</p>
                        <p style='margin: 10px 0 0 0; color: #1b5e20; font-weight: 600;'>✅ LOW RISK</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with col2:
            st.subheader("Recommended Actions")
            recommendations = generate_recommendation(customer, probability)
            for item in recommendations:
                st.markdown(
                    f"""
                    <div style='background: #f5f7fb; padding: 10px; border-radius: 6px; margin-bottom: 8px; border-left: 3px solid #64b5f6;'>
                        <p style='margin: 0; color: #0f1829; font-size: 13px;'>✓ {item}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )





elif page == "Model Evaluation":

    st.markdown(
        """
        <h2 style='color: #0f1829; margin-bottom: 20px;'>📊 Churn Model Evaluation</h2>
        """,
        unsafe_allow_html=True
    )

    predictions = model.predict(X_test)
    report = classification_report(y_test, predictions, output_dict=True)

    col1, col2, col3, col4 = st.columns(4, gap="medium")

    with col1:
        st.metric("Accuracy", f"{accuracy*100:.2f}%")

    with col2:
        st.metric("Precision (Churned)", f"{report['1']['precision']*100:.2f}%")

    with col3:
        st.metric("Recall (Churned)", f"{report['1']['recall']*100:.2f}%")

    with col4:
        st.metric("F1-Score (Churned)", f"{report['1']['f1-score']*100:.2f}%")

    st.markdown("---")

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.subheader("Confusion Matrix")
        cm = confusion_matrix(y_test, predictions)

        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="Blues",
            ax=ax,
            cbar_kws={'label': 'Count'},
            linewidths=1,
            linecolor='white'
        )
        ax.set_xlabel("Predicted Label", fontsize=12, fontweight="bold")
        ax.set_ylabel("True Label", fontsize=12, fontweight="bold")
        ax.set_xticklabels(["Retained", "Churned"])
        ax.set_yticklabels(["Retained", "Churned"], rotation=0)
        plt.tight_layout()
        st.pyplot(fig)

    with col2:
        st.subheader("Feature Importance")
        importance = pd.DataFrame({
            "Feature": X_test.columns,
            "Importance": model.feature_importances_
        })
        importance = importance.sort_values("Importance", ascending=True).tail(10)

        fig = px.barh(
            importance,
            x="Importance",
            y="Feature",
            color="Importance",
            color_continuous_scale="Blues",
            title=None
        )
        fig.update_traces(
            hovertemplate='<b>%{y}</b><br>Importance: %{x:.4f}<extra></extra>',
            marker_line_width=1,
            marker_line_color='white'
        )
        fig.update_layout(
            height=400,
            xaxis_title="Importance Score",
            yaxis_title="",
            font=dict(size=11),
            plot_bgcolor="rgba(245, 247, 251, 0.5)",
            paper_bgcolor="white",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True, key="feature_importance")





elif page == "Executive Summary":

    st.markdown(
        """
        <h2 style='color: #0f1829; margin-bottom: 20px;'>📄 Executive Summary</h2>
        """,
        unsafe_allow_html=True
    )

    total = len(filtered_df)
    churn = (filtered_df["Exited"].mean() * 100)
    engagement = (filtered_df["Engagement_Score"].mean())

    col1, col2 = st.columns([1, 1], gap="medium")

    with col1:
        st.markdown(
            f"""
            <div style='background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%); padding: 25px; border-radius: 12px; color: white;'>
                <p style='margin: 0 0 15px 0; font-size: 14px; font-weight: 500;'>📊 CUSTOMER OVERVIEW</p>
                
                <div style='margin-bottom: 15px;'>
                    <p style='margin: 0; font-size: 12px; opacity: 0.9;'>Total Customers</p>
                    <p style='margin: 5px 0 0 0; font-size: 32px; font-weight: bold;'>{total:,}</p>
                </div>
                
                <div style='margin-bottom: 15px;'>
                    <p style='margin: 0; font-size: 12px; opacity: 0.9;'>Churn Rate</p>
                    <p style='margin: 5px 0 0 0; font-size: 28px; font-weight: bold;'>{churn:.2f}%</p>
                </div>
                
                <div>
                    <p style='margin: 0; font-size: 12px; opacity: 0.9;'>Retention Rate</p>
                    <p style='margin: 5px 0 0 0; font-size: 28px; font-weight: bold;'>{100-churn:.2f}%</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div style='background: linear-gradient(135deg, #42a5f5 0%, #1e88e5 100%); padding: 25px; border-radius: 12px; color: white;'>
                <p style='margin: 0 0 15px 0; font-size: 14px; font-weight: 500;'>🤖 MACHINE LEARNING MODEL</p>
                
                <div style='margin-bottom: 15px;'>
                    <p style='margin: 0; font-size: 12px; opacity: 0.9;'>Model Accuracy</p>
                    <p style='margin: 5px 0 0 0; font-size: 32px; font-weight: bold;'>{accuracy*100:.2f}%</p>
                </div>
                
                <div style='margin-bottom: 15px;'>
                    <p style='margin: 0; font-size: 12px; opacity: 0.9;'>Avg Engagement Score</p>
                    <p style='margin: 5px 0 0 0; font-size: 28px; font-weight: bold;'>{engagement:.1f}/100</p>
                </div>
                
                <div>
                    <p style='margin: 0; font-size: 12px; opacity: 0.9;'>Algorithm</p>
                    <p style='margin: 5px 0 0 0; font-size: 16px; font-weight: 500;'>Random Forest</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    st.markdown(
        """
        <div style='background: #e3f2fd; padding: 20px; border-radius: 8px; border-left: 4px solid #1976d2;'>
            <h3 style='color: #0f1829; margin-top: 0;'>Key Findings & Insights</h3>
            <ul style='color: #1565c0; line-height: 1.8;'>
                <li><b>Customer Intelligence:</b> The platform analyzes deep customer behavior patterns to identify engagement trends and predict churn probability with high accuracy.</li>
                <li><b>Risk Mitigation:</b> Early identification of at-risk customers enables proactive retention strategies and personalized interventions.</li>
                <li><b>Engagement Metrics:</b> Composite engagement scores combine balance, product adoption, and activity status to quantify customer health.</li>
                <li><b>Predictive Capabilities:</b> Advanced machine learning model provides actionable insights for customer retention and product recommendations.</li>
                <li><b>Data-Driven Decisions:</b> Geographic and demographic analysis enables targeted marketing campaigns and resource allocation.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.markdown(
            """
            <div style='background: white; padding: 15px; border-radius: 8px; border: 1px solid #e0e0e0;'>
                <p style='margin: 0 0 10px 0; font-weight: 600; color: #0f1829;'>💡 Recommendations</p>
                <ul style='margin: 0; padding-left: 20px; font-size: 13px; color: #424242;'>
                    <li>Focus retention efforts on high-risk customers</li>
                    <li>Promote product cross-selling opportunities</li>
                    <li>Enhance engagement for inactive members</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div style='background: white; padding: 15px; border-radius: 8px; border: 1px solid #e0e0e0;'>
                <p style='margin: 0 0 10px 0; font-weight: 600; color: #0f1829;'>📈 Opportunities</p>
                <ul style='margin: 0; padding-left: 20px; font-size: 13px; color: #424242;'>
                    <li>Segment customers by engagement level</li>
                    <li>Personalize engagement strategies</li>
                    <li>Monitor model performance continuously</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div style='background: white; padding: 15px; border-radius: 8px; border: 1px solid #e0e0e0;'>
                <p style='margin: 0 0 10px 0; font-weight: 600; color: #0f1829;'>✅ Actions</p>
                <ul style='margin: 0; padding-left: 20px; font-size: 13px; color: #424242;'>
                    <li>Review high-risk customers weekly</li>
                    <li>Test retention campaign effectiveness</li>
                    <li>Optimize product recommendations</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )



# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.markdown(
    """
    <div style='text-align: center; padding: 20px; background: #f5f7fb; border-radius: 8px; margin-top: 20px;'>
        <p style='color: #64b5f6; font-size: 12px; margin: 0;'>🏦 Customer Engagement & Retention Intelligence Platform</p>
        <p style='color: #90a4ae; font-size: 11px; margin: 5px 0 0 0;'>Powered by Streamlit • Random Forest ML • Plotly Analytics</p>
    </div>
    """,
    unsafe_allow_html=True
)