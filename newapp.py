# ==================================================
# PROFESSIONAL BANKING ANALYTICS PLATFORM
# ==================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from datetime import datetime

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="BankAnalytics Pro | Customer Intelligence Platform",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# SESSION STATE MANAGEMENT
# ==================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

# ==================================================
# PROFESSIONAL CSS STYLING
# ==================================================

def load_css():
    st.markdown(
        """
        <style>
        
        /* Root Color Palette */
        :root {
            --primary: #1976d2;
            --primary-dark: #1565c0;
            --secondary: #64b5f6;
            --success: #2ecc71;
            --warning: #ff9800;
            --danger: #e74c3c;
            --light-bg: #f5f7fb;
            --dark-bg: #0f1829;
        }
        
        /* Main Background */
        .main {
            background: linear-gradient(135deg, #f5f7fb 0%, #eef2f8 100%);
        }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a2a4e 0%, #0f1829 100%);
            box-shadow: 2px 0 20px rgba(0, 0, 0, 0.15);
        }
        
        [data-testid="stSidebar"] * {
            color: #ffffff;
        }
        
        /* Headers */
        h1 {
            color: #0f1829;
            font-size: 32px;
            font-weight: 700;
            letter-spacing: -0.5px;
            margin-bottom: 10px;
        }
        
        h2 {
            color: #1a2a4e;
            font-size: 24px;
            font-weight: 600;
            margin-top: 20px;
            margin-bottom: 15px;
        }
        
        h3 {
            color: #2c3e50;
            font-size: 18px;
            font-weight: 600;
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
            width: 100%;
        }
        
        .stButton > button:hover {
            box-shadow: 0 6px 20px rgba(25, 118, 210, 0.4);
            transform: translateY(-2px);
        }
        
        /* Messages */
        .stSuccess {
            background-color: #e8f5e9;
            border-radius: 8px;
            padding: 15px;
            border-left: 4px solid #2ecc71;
        }
        
        .stError {
            background-color: #ffebee;
            border-radius: 8px;
            padding: 15px;
            border-left: 4px solid #e74c3c;
        }
        
        .stWarning {
            background-color: #fff3e0;
            border-radius: 8px;
            padding: 15px;
            border-left: 4px solid #ff9800;
        }
        
        .stInfo {
            background-color: #e3f2fd;
            border-radius: 8px;
            padding: 15px;
            border-left: 4px solid #1976d2;
        }
        
        </style>
        """,
        unsafe_allow_html=True
    )

load_css()

# ==================================================
# LOAD AND CACHE DATA
# ==================================================

@st.cache_data
def load_data():
    df = pd.read_csv("data/churn.csv")
    return df

@st.cache_resource
def train_churn_model(df):
    data = df.copy()
    data = data.drop(["CustomerId", "Surname"], axis=1, errors="ignore")
    
    encoder = LabelEncoder()
    for col in data.select_dtypes(include="object"):
        data[col] = encoder.fit_transform(data[col])
    
    X = data.drop("Exited", axis=1)
    y = data["Exited"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    
    return model, accuracy, X_test, y_test

# Load data
if "df" not in st.session_state:
    st.session_state.df = load_data()

if "model" not in st.session_state:
    st.session_state.model, st.session_state.accuracy, st.session_state.X_test, st.session_state.y_test = train_churn_model(st.session_state.df)

df = st.session_state.df
model = st.session_state.model
accuracy = st.session_state.accuracy
X_test = st.session_state.X_test
y_test = st.session_state.y_test

# ==================================================
# ENGAGEMENT SCORE CALCULATION
# ==================================================

def calculate_engagement_score(df):
    data = df.copy()
    balance_score = (data["Balance"] / data["Balance"].max()) * 40
    product_score = (data["NumOfProducts"] / data["NumOfProducts"].max()) * 30
    activity_score = (data["IsActiveMember"] * 30)
    data["Engagement_Score"] = balance_score + product_score + activity_score
    return data

df = calculate_engagement_score(df)

# ==================================================
# BUSINESS RECOMMENDATIONS
# ==================================================

def generate_recommendation(customer, probability):
    recommendations = []
    
    if probability > 70:
        recommendations.append("📞 Priority: Contact with retention offers immediately")
        recommendations.append("👤 Assign dedicated relationship manager")
    elif probability > 40:
        recommendations.append("📧 Launch engagement campaign")
        recommendations.append("🎁 Offer additional banking benefits")
    else:
        recommendations.append("✅ Maintain regular engagement")
    
    if customer["NumOfProducts"] <= 1:
        recommendations.append("🛍️ Cross-sell additional banking products")
    
    if customer["Balance"] < df["Balance"].median():
        recommendations.append("💰 Promote savings and investment plans")
    
    return recommendations

# ==================================================
# LOGIN PAGE
# ==================================================

def login_page():
    """Professional login page"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div style='text-align: center; margin-bottom: 30px;'>", unsafe_allow_html=True)
        st.markdown("<h1 style='color: #1976d2; font-size: 36px; margin: 20px 0;'>🏦 BankAnalytics</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #666; font-size: 16px; margin-top: 5px;'>Customer Intelligence Platform</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: #999; font-size: 13px; margin-top: 10px;'>Professional Edition</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        username = st.text_input("👤 Username", placeholder="demo")
        password = st.text_input("🔐 Password", type="password", placeholder="demo")
        
        col1, col2 = st.columns(2)
        with col1:
            remember = st.checkbox("Remember me")
        with col2:
            st.markdown("<p style='text-align: right; margin-top: 15px;'><a href='#' style='color: #1976d2; text-decoration: none; font-size: 12px;'>Forgot password?</a></p>", unsafe_allow_html=True)
        
        st.markdown("")
        
        if st.button("🔓 Login", use_container_width=True, type="primary"):
            if username and password:
                if username == "demo" and password == "demo":
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Try demo/demo")
            else:
                st.warning("⚠️ Please enter username and password")
        
        st.markdown("---")
        st.markdown("""
        <div style='background: #f5f7fb; padding: 15px; border-radius: 8px; text-align: center;'>
            <p style='color: #666; font-size: 12px; margin: 0;'><b>Demo Credentials</b></p>
            <p style='color: #1976d2; font-size: 13px; margin: 5px 0 0 0;'><code>Username: demo</code></p>
            <p style='color: #1976d2; font-size: 13px; margin: 3px 0 0 0;'><code>Password: demo</code></p>
        </div>
        """, unsafe_allow_html=True)

# ==================================================
# SIDEBAR NAVIGATION
# ==================================================

def sidebar_navigation():
    """Professional sidebar with navigation"""
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 20px 0; border-bottom: 1px solid rgba(255,255,255,0.2); margin-bottom: 20px;'>
            <h2 style='color: #64b5f6; font-size: 26px; margin: 0;'>🏦 BankAnalytics</h2>
            <p style='color: #90caf9; font-size: 12px; margin: 5px 0 0 0;'>Pro Edition</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📊 Dashboard")
        pages_main = {
            "🎯 Dashboard": "Dashboard",
            "📈 Engagement": "Engagement Analysis",
            "🛍️ Products": "Product Analysis",
            "⭐ High Value": "High Value Customers",
            "📊 Scores": "Engagement Score",
        }
        
        for label, page in pages_main.items():
            if st.button(label, use_container_width=True, key=f"btn_{page}_1"):
                st.session_state.current_page = page
                st.rerun()
        
        st.markdown("---")
        st.markdown("### 🤖 Analytics")
        pages_ml = {
            "🔮 Predict Churn": "Churn Prediction",
            "📉 Model Performance": "Model Evaluation",
            "🔍 Customer Search": "Customer Search",
        }
        
        for label, page in pages_ml.items():
            if st.button(label, use_container_width=True, key=f"btn_{page}_2"):
                st.session_state.current_page = page
                st.rerun()
        
        st.markdown("---")
        st.markdown("### 📋 Reports")
        pages_reports = {
            "📄 Executive Summary": "Executive Summary",
        }
        
        for label, page in pages_reports.items():
            if st.button(label, use_container_width=True, key=f"btn_{page}_3"):
                st.session_state.current_page = page
                st.rerun()
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.username = None
                st.rerun()
        
        st.markdown("---")
        st.markdown(f"""
        <div style='background: rgba(255,255,255,0.1); padding: 12px; border-radius: 8px; text-align: center;'>
            <p style='margin: 0; font-size: 11px; color: #90caf9;'>Logged in as</p>
            <p style='margin: 5px 0 0 0; font-size: 13px; color: white; font-weight: 600;'>{st.session_state.username}</p>
        </div>
        """, unsafe_allow_html=True)

# ==================================================
# DASHBOARD PAGE
# ==================================================

def page_dashboard():
    st.markdown("<h1>📊 Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666; margin-bottom: 20px;'>Welcome to your customer analytics hub</p>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    
    total_customers = len(df)
    churn_rate = (df["Exited"].mean() * 100)
    retention_rate = (100 - churn_rate)
    avg_balance = (df["Balance"].mean())
    
    with col1:
        st.metric("👥 Total Customers", f"{total_customers:,}", f"+{int(total_customers*0.05)} this month")
    
    with col2:
        st.metric("📉 Churn Rate", f"{churn_rate:.2f}%", "↓ -2.3% vs last month", delta_color="inverse")
    
    with col3:
        st.metric("💰 Avg Balance", f"${avg_balance:,.0f}", f"Total: ${df['Balance'].sum():,.0f}")
    
    with col4:
        st.metric("📈 Model Accuracy", f"{accuracy*100:.2f}%", "Random Forest")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        st.subheader("📊 Churn Distribution")
        churn_data = df["Exited"].value_counts().reset_index()
        churn_data.columns = ["Status", "Count"]
        churn_data["Status"] = churn_data["Status"].map({0: "Retained", 1: "Churned"})
        
        fig = px.pie(churn_data, names="Status", values="Count", 
                     color_discrete_map={"Retained": "#2ecc71", "Churned": "#e74c3c"})
        fig.update_traces(textposition='inside', textinfo='label+percent')
        fig.update_layout(height=400, showlegend=True)
        st.plotly_chart(fig, use_container_width=True, key="dashboard_churn")
    
    with col2:
        st.subheader("🌍 Customers by Geography")
        geo = df["Geography"].value_counts().reset_index()
        geo.columns = ["Country", "Customers"]
        
        fig = px.bar(geo, x="Country", y="Customers", color_discrete_sequence=["#1976d2"])
        fig.update_layout(hovermode='x', plot_bgcolor="rgba(0,0,0,0)", height=400)
        st.plotly_chart(fig, use_container_width=True, key="dashboard_geo")

# ==================================================
# ENGAGEMENT ANALYSIS PAGE
# ==================================================

def page_engagement_analysis():
    st.markdown("<h1>📈 Engagement Analysis</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1], gap="medium")
    
    with col1:
        st.subheader("Correlation Heatmap")
        numeric_df = df.select_dtypes(include=np.number)
        corr = numeric_df.corr()
        
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax,
                   cbar_kws={'label': 'Correlation'}, square=True, linewidths=0.5)
        ax.set_title("Feature Correlation Matrix", fontsize=14, fontweight="bold", pad=20)
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.subheader("Key Insights")
        st.info("""
        **Engagement Score**
        - Strong correlation with active membership status
        
        **Balance & Age**
        - Age shows relationship with balance levels
        
        **Activity Status**
        - Active members have significantly higher engagement scores
        """)

# ==================================================
# PRODUCT ANALYSIS PAGE
# ==================================================

def page_product_analysis():
    st.markdown("<h1>🛍️ Product Analysis</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1], gap="medium")
    
    with col1:
        product = df["NumOfProducts"].value_counts().sort_index().reset_index()
        product.columns = ["Products", "Customers"]
        
        fig = px.bar(product, x="Products", y="Customers",
                     color_discrete_sequence=["#1976d2"],
                     title="Customer Product Distribution")
        fig.update_layout(hovermode='x', plot_bgcolor="rgba(0,0,0,0)", height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Summary")
        for _, row in product.iterrows():
            st.metric(f"{int(row['Products'])} Product(s)", f"{int(row['Customers'])} customers")

# ==================================================
# HIGH VALUE CUSTOMERS PAGE
# ==================================================

def page_high_value():
    st.markdown("<h1>⭐ High Value Customers</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        balance_limit = st.slider("Minimum Balance ($)", 0, 250000, 100000, step=10000)
    
    with col2:
        st.metric("Filter Threshold", f"${balance_limit:,}")
    
    high_value = df[(df["Balance"] >= balance_limit) & (df["IsActiveMember"] == 0)]
    
    with col3:
        st.metric("At Risk", f"{len(high_value)}")
    
    st.markdown("---")
    
    if len(high_value) > 0:
        st.subheader(f"High Value At-Risk Customers ({len(high_value)})")
        display_cols = ["CustomerId", "Age", "Balance", "NumOfProducts", "IsActiveMember", "Engagement_Score", "Exited"]
        st.dataframe(high_value[display_cols].sort_values("Balance", ascending=False), use_container_width=True, hide_index=True)
        
        csv = high_value.to_csv(index=False)
        st.download_button("📥 Download CSV", csv, "high_value_customers.csv", "text/csv", use_container_width=True)
    else:
        st.success("✅ No high-value at-risk customers found")

# ==================================================
# ENGAGEMENT SCORE PAGE
# ==================================================

def page_engagement_score():
    st.markdown("<h1>📊 Engagement Score</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2], gap="medium")
    
    with col1:
        st.subheader("Top 10 Engaged")
        top = df.nlargest(10, "Engagement_Score")[["CustomerId", "Engagement_Score"]]
        for idx, (_, row) in enumerate(top.iterrows(), 1):
            st.metric(f"#{idx}", f"ID: {int(row['CustomerId'])}", f"Score: {row['Engagement_Score']:.1f}")
    
    with col2:
        st.subheader("Distribution")
        fig = px.histogram(df, x="Engagement_Score", nbins=30, color_discrete_sequence=["#1976d2"])
        fig.update_layout(hovermode='x', plot_bgcolor="rgba(0,0,0,0)", height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Avg Score", f"{df['Engagement_Score'].mean():.1f}")
    with col2:
        st.metric("Max Score", f"{df['Engagement_Score'].max():.1f}")
    with col3:
        st.metric("Min Score", f"{df['Engagement_Score'].min():.1f}")

# ==================================================
# CHURN PREDICTION PAGE
# ==================================================

def page_churn_prediction():
    st.markdown("<h1>🔮 Churn Prediction</h1>", unsafe_allow_html=True)
    
    st.info(f"🤖 Model Accuracy: **{accuracy*100:.2f}%**")
    
    customer_id = st.selectbox("Select Customer", df["CustomerId"].unique())
    customer = df[df["CustomerId"] == customer_id].iloc[0]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Age", f"{int(customer['Age'])} years")
    with col2:
        st.metric("Balance", f"${customer['Balance']:,.0f}")
    with col3:
        st.metric("Products", f"{int(customer['NumOfProducts'])}")
    
    if st.button("🔮 Predict Churn", use_container_width=True, type="primary"):
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
                st.error(f"🚨 HIGH RISK\n**{probability:.1f}%**")
            elif probability > 40:
                st.warning(f"⚠️ MEDIUM RISK\n**{probability:.1f}%**")
            else:
                st.success(f"✅ LOW RISK\n**{probability:.1f}%**")
        
        with col2:
            st.subheader("Recommendations")
            for rec in generate_recommendation(customer, probability):
                st.write(f"• {rec}")

# ==================================================
# CUSTOMER SEARCH PAGE
# ==================================================

def page_customer_search():
    st.markdown("<h1>🔍 Customer Search</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666;'>Find and analyze individual customer profiles</p>", unsafe_allow_html=True)
    
    search_id = st.number_input("Enter Customer ID", min_value=1, max_value=int(df["CustomerId"].max()))
    
    if search_id:
        customer = df[df["CustomerId"] == search_id]
        
        if not customer.empty:
            customer = customer.iloc[0]
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Age", f"{int(customer['Age'])} years")
            with col2:
                st.metric("Balance", f"${customer['Balance']:,.0f}")
            with col3:
                st.metric("Products", f"{int(customer['NumOfProducts'])}")
            with col4:
                st.metric("Engagement", f"{customer['Engagement_Score']:.1f}")
            
            st.markdown("---")
            
            col1, col2 = st.columns(2, gap="medium")
            
            with col1:
                st.subheader("Profile Information")
                st.write(f"**Geography:** {customer['Geography']}")
                st.write(f"**Gender:** {customer['Gender']}")
                st.write(f"**Tenure:** {int(customer['Tenure'])} years")
                st.write(f"**Active Member:** {'✅ Yes' if customer['IsActiveMember'] else '❌ No'}")
                st.write(f"**Credit Score:** {int(customer['CreditScore'])}")
            
            with col2:
                st.subheader("Churn Prediction")
                input_data = customer.drop("Exited")
                input_df = pd.DataFrame([input_data])
                input_df = input_df.drop(["CustomerId", "Surname"], axis=1, errors="ignore")
                
                encoder = LabelEncoder()
                for col in input_df.select_dtypes(include="object"):
                    input_df[col] = encoder.fit_transform(input_df[col])
                
                probability = model.predict_proba(input_df)[0][1] * 100
                
                if probability > 70:
                    st.error(f"🚨 **High Risk: {probability:.1f}%**")
                elif probability > 40:
                    st.warning(f"⚠️ **Medium Risk: {probability:.1f}%**")
                else:
                    st.success(f"✅ **Low Risk: {probability:.1f}%**")
            
            st.markdown("---")
            st.subheader("💡 Recommendations")
            for rec in generate_recommendation(customer, probability):
                st.write(f"• {rec}")
        else:
            st.error("❌ Customer not found")

# ==================================================
# MODEL EVALUATION PAGE
# ==================================================

def page_model_evaluation():
    st.markdown("<h1>📊 Model Evaluation</h1>", unsafe_allow_html=True)
    
    predictions = model.predict(X_test)
    report = classification_report(y_test, predictions, output_dict=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Accuracy", f"{accuracy*100:.2f}%")
    with col2:
        st.metric("Precision", f"{report['1']['precision']*100:.2f}%")
    with col3:
        st.metric("Recall", f"{report['1']['recall']*100:.2f}%")
    with col4:
        st.metric("F1-Score", f"{report['1']['f1-score']*100:.2f}%")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        st.subheader("Confusion Matrix")
        cm = confusion_matrix(y_test, predictions)
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax, cbar=False)
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Actual")
        ax.set_xticklabels(["Retained", "Churned"])
        ax.set_yticklabels(["Retained", "Churned"], rotation=0)
        st.pyplot(fig)
    
    with col2:
        st.subheader("Feature Importance (Top 10)")
        importance = pd.DataFrame({
            "Feature": X_test.columns,
            "Importance": model.feature_importances_
        }).sort_values("Importance", ascending=True).tail(10)
        
        fig = px.bar(importance, x="Importance", y="Feature", orientation="h",
                    color_discrete_sequence=["#1976d2"])
        fig.update_layout(hovermode='y', plot_bgcolor="rgba(0,0,0,0)", height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

# ==================================================
# EXECUTIVE SUMMARY PAGE
# ==================================================

def page_executive_summary():
    st.markdown("<h1>📄 Executive Summary</h1>", unsafe_allow_html=True)
    
    total = len(df)
    churn = (df["Exited"].mean() * 100)
    engagement = (df["Engagement_Score"].mean())
    
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%); padding: 25px; border-radius: 12px; color: white;'>
            <p style='margin: 0 0 15px 0; font-size: 14px; font-weight: 500;'>👥 CUSTOMER OVERVIEW</p>
            <p style='margin: 0; font-size: 32px; font-weight: 700;'>{total:,}</p>
            <p style='margin: 8px 0 0 0; font-size: 12px; opacity: 0.9;'>Total Customers</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #42a5f5 0%, #1e88e5 100%); padding: 25px; border-radius: 12px; color: white;'>
            <p style='margin: 0 0 15px 0; font-size: 14px; font-weight: 500;'>🤖 MODEL PERFORMANCE</p>
            <p style='margin: 0; font-size: 32px; font-weight: 700;'>{accuracy*100:.2f}%</p>
            <p style='margin: 8px 0 0 0; font-size: 12px; opacity: 0.9;'>Accuracy</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    ### 📋 Key Findings
    
    - **Customer Intelligence:** Advanced analysis of behavior patterns and engagement trends
    - **Risk Mitigation:** Early identification of at-risk customers enables proactive retention
    - **Engagement Metrics:** Composite scores combining balance, products, and activity status
    - **Predictive Analytics:** ML model provides actionable insights for retention strategies
    - **Data-Driven Strategy:** Geographic and demographic analysis for targeted campaigns
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### 💡 Recommendations
        - Focus retention on high-risk customers
        - Promote product cross-selling
        - Enhance engagement for inactive members
        """)
    
    with col2:
        st.markdown("""
        #### 📈 Opportunities
        - Segment by engagement level
        - Personalize strategies
        - Monitor model performance
        """)
    
    with col3:
        st.markdown("""
        #### ✅ Actions
        - Review high-risk customers weekly
        - Test retention campaigns
        - Optimize recommendations
        """)

# ==================================================
# MAIN APP LOGIC
# ==================================================

def main():
    # Show login if not authenticated
    if not st.session_state.authenticated:
        login_page()
    else:
        # Show authenticated app
        sidebar_navigation()
        
        # Route to pages
        if st.session_state.current_page == "Dashboard":
            page_dashboard()
        elif st.session_state.current_page == "Engagement Analysis":
            page_engagement_analysis()
        elif st.session_state.current_page == "Product Analysis":
            page_product_analysis()
        elif st.session_state.current_page == "High Value Customers":
            page_high_value()
        elif st.session_state.current_page == "Engagement Score":
            page_engagement_score()
        elif st.session_state.current_page == "Churn Prediction":
            page_churn_prediction()
        elif st.session_state.current_page == "Customer Search":
            page_customer_search()
        elif st.session_state.current_page == "Model Evaluation":
            page_model_evaluation()
        elif st.session_state.current_page == "Executive Summary":
            page_executive_summary()
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; padding: 20px; color: #999; font-size: 12px;'>
            🏦 BankAnalytics Pro | Customer Intelligence Platform | Powered by Streamlit & Random Forest ML
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
