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

    .main {
        background-color:#f5f7fb;
    }

    .stMetric {
        background:white;
        padding:15px;
        border-radius:10px;
        box-shadow:0px 2px 8px rgba(0,0,0,0.1);
    }

    div[data-testid="stSidebar"] {
        background:#0f172a;
    }

    div[data-testid="stSidebar"] * {
        color:white;
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
# TITLE
# ==================================================

st.title(
    "🏦 Customer Engagement & Retention Intelligence Platform"
)

st.caption(
    "Analytics dashboard for customer behavior analysis and churn insights"
)



# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title(
    "Navigation"
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
    ]
)



# ==================================================
# FILTERS
# ==================================================

st.sidebar.header(
    "Filters"
)


country = st.sidebar.multiselect(
    "Geography",
    df["Geography"].unique(),
    default=df["Geography"].unique()
)


gender = st.sidebar.multiselect(
    "Gender",
    df["Gender"].unique(),
    default=df["Gender"].unique()
)



filtered_df = df[
    (df["Geography"].isin(country)) &
    (df["Gender"].isin(gender))
]



# ==================================================
# DASHBOARD PAGE
# ==================================================

if page == "Dashboard":


    st.header(
        "📊 Customer Overview"
    )


    total_customers = len(filtered_df)


    churn_rate = (
        filtered_df["Exited"].mean()
        * 100
    )


    retention_rate = (
        100 - churn_rate
    )


    avg_balance = (
        filtered_df["Balance"].mean()
    )


    avg_engagement = (
        filtered_df["Engagement_Score"].mean()
    )



    col1,col2,col3,col4 = st.columns(4)


    col1.metric(
        "👥 Customers",
        total_customers
    )


    col2.metric(
        "📉 Churn Rate",
        f"{churn_rate:.2f}%"
    )


    col3.metric(
        "💰 Avg Balance",
        f"${avg_balance:,.0f}"
    )


    col4.metric(
        "📈 Engagement",
        f"{avg_engagement:.1f}"
    )



    st.divider()



    st.subheader(
        "Customer Churn"
    )


    churn_chart = px.pie(
        filtered_df,
        names="Exited",
        title="Churn Distribution"
    )


    st.plotly_chart(
        churn_chart,
        use_container_width=True,
        key="dashboard_churn"
    )



    st.subheader(
        "Geography Distribution"
    )


    geo = (
        filtered_df["Geography"]
        .value_counts()
        .reset_index()
    )


    geo.columns=[
        "Geography",
        "Customers"
    ]


    geo_chart = px.bar(
        geo,
        x="Geography",
        y="Customers",
        color="Geography"
    )


    st.plotly_chart(
        geo_chart,
        use_container_width=True,
        key="dashboard_geo"
    )



# ==================================================
# ENGAGEMENT ANALYSIS
# ==================================================

elif page == "Engagement Analysis":


    st.header(
        "📈 Customer Engagement Analysis"
    )


    st.subheader(
        "Correlation Heatmap"
    )


    numeric_df = (
        filtered_df
        .select_dtypes(
            include=np.number
        )
    )


    corr = numeric_df.corr()



    fig,ax = plt.subplots(
        figsize=(10,6)
    )


    sns.heatmap(
        corr,
        annot=True,
        cmap="coolwarm",
        ax=ax
    )


    st.pyplot(
        fig
    )



# ==================================================
# PRODUCT ANALYSIS
# ==================================================

elif page == "Product Analysis":


    st.header(
        "🛍 Product Analysis"
    )


    product = (
        filtered_df["NumOfProducts"]
        .value_counts()
        .reset_index()
    )


    product.columns=[
        "Products",
        "Customers"
    ]


    fig = px.bar(
        product,
        x="Products",
        y="Customers",
        color="Products"
    )


    st.plotly_chart(
        fig,
        use_container_width=True,
        key="product_chart"
    )



# ==================================================
# HIGH VALUE CUSTOMERS
# ==================================================

elif page == "High Value Customers":


    st.header(
        "⭐ High Value Customer Detector"
    )


    balance_limit = st.slider(
        "Minimum Balance",
        0,
        250000,
        100000
    )


    high_value = filtered_df[
        (filtered_df["Balance"] >= balance_limit)
        &
        (filtered_df["IsActiveMember"] == 0)
    ]



    st.metric(
        "High Risk Customers",
        len(high_value)
    )


    st.dataframe(
        high_value
    )


    csv = high_value.to_csv(
        index=False
    )


    st.download_button(
        "📥 Download Data",
        csv,
        "high_value_customers.csv",
        "text/csv"
    )



# ==================================================
# ENGAGEMENT SCORE
# ==================================================

elif page == "Engagement Score":


    st.header(
        "📈 Customer Engagement Score"
    )


    top = (
        filtered_df
        .sort_values(
            "Engagement_Score",
            ascending=False
        )
        .head(10)
    )


    st.subheader(
        "Top Engaged Customers"
    )


    st.dataframe(
        top[
            [
                "CustomerId",
                "Balance",
                "NumOfProducts",
                "IsActiveMember",
                "Engagement_Score"
            ]
        ]
    )


    fig = px.histogram(
        filtered_df,
        x="Engagement_Score"
    )


    st.plotly_chart(
        fig,
        use_container_width=True,
        key="engagement_distribution"
    )
    # ==================================================
# CHURN PREDICTION
# ==================================================

elif page == "Churn Prediction":

    st.header(
        "🤖 Customer Churn Prediction"
    )


    st.metric(
        "Model Accuracy",
        f"{accuracy*100:.2f}%"
    )


    st.divider()


    customer_id = st.selectbox(
        "Select Customer ID",
        filtered_df["CustomerId"].unique()
    )


    customer = filtered_df[
        filtered_df["CustomerId"] == customer_id
    ].iloc[0]



    col1,col2,col3 = st.columns(3)


    col1.metric(
        "Age",
        customer["Age"]
    )


    col2.metric(
        "Balance",
        f"${customer['Balance']:,.0f}"
    )


    col3.metric(
        "Products",
        customer["NumOfProducts"]
    )



    if st.button(
        "Predict Churn"
    ):


        input_data = customer.drop(
            "Exited"
        )


        input_df = pd.DataFrame(
            [input_data]
        )


        # Remove columns not used by model

        input_df = input_df.drop(
            [
                "CustomerId",
                "Surname"
            ],
            axis=1,
            errors="ignore"
        )


        encoder = LabelEncoder()


        for col in input_df.select_dtypes(
            include="object"
        ):

            input_df[col] = encoder.fit_transform(
                input_df[col]
            )



        probability = model.predict_proba(
            input_df
        )[0][1] * 100



        st.subheader(
            "Prediction Result"
        )


        st.metric(
            "Churn Probability",
            f"{probability:.2f}%"
        )



        if probability > 70:

            st.error(
                "🚨 High Risk Customer"
            )


        elif probability > 40:

            st.warning(
                "⚠️ Medium Risk Customer"
            )


        else:

            st.success(
                "✅ Low Risk Customer"
            )



        st.subheader(
            "💡 Recommended Actions"
        )


        recommendations = generate_recommendation(
            customer,
            probability
        )


        for item in recommendations:

            st.write(
                "✅ " + item
            )





# ==================================================
# MODEL EVALUATION
# ==================================================

elif page == "Model Evaluation":


    st.header(
        "📈 Churn Model Evaluation"
    )



    predictions = model.predict(
        X_test
    )



    report = classification_report(
        y_test,
        predictions,
        output_dict=True
    )



    col1,col2,col3 = st.columns(3)


    col1.metric(
        "Accuracy",
        f"{accuracy*100:.2f}%"
    )


    col2.metric(
        "Precision",
        f"{report['1']['precision']*100:.2f}%"
    )


    col3.metric(
        "Recall",
        f"{report['1']['recall']*100:.2f}%"
    )



    st.subheader(
        "Confusion Matrix"
    )


    cm = confusion_matrix(
        y_test,
        predictions
    )


    fig,ax = plt.subplots()


    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        ax=ax
    )


    ax.set_xlabel(
        "Predicted"
    )


    ax.set_ylabel(
        "Actual"
    )


    st.pyplot(
        fig
    )



    st.subheader(
        "Feature Importance"
    )


    importance = pd.DataFrame({

        "Feature":
        X_test.columns,

        "Importance":
        model.feature_importances_

    })



    importance = importance.sort_values(
        "Importance",
        ascending=False
    )



    fig = px.bar(
        importance,
        x="Importance",
        y="Feature",
        orientation="h"
    )



    st.plotly_chart(
        fig,
        use_container_width=True,
        key="feature_importance"
    )





# ==================================================
# EXECUTIVE SUMMARY
# ==================================================

elif page == "Executive Summary":


    st.header(
        "📄 Executive Summary"
    )


    total = len(filtered_df)


    churn = (
        filtered_df["Exited"].mean()
        *100
    )


    engagement = (
        filtered_df["Engagement_Score"]
        .mean()
    )



    st.success(
        f"""
        **Customer Overview**

        👥 Total Customers: {total}

        📉 Churn Rate: {churn:.2f}%

        📈 Average Engagement Score: {engagement:.2f}

        🤖 ML Model Accuracy: {accuracy*100:.2f}%

        The platform analyzes customer behavior,
        identifies high-risk customers, and provides
        retention recommendations.
        """
    )



# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "Customer Engagement & Retention Intelligence Platform | Streamlit + Machine Learning"
)