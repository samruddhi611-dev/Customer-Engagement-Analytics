# ==================================================
# ENTERPRISE BANKING ANALYTICS PLATFORM
# ==================================================

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

# Import custom modules
from config import *
from database.models import Database
from ml_pipeline import MLPipeline
from utils.auth import AuthManager, init_session_state
from utils.validators import Validator
from utils.ui_components import *
from utils.insights import InsightsEngine
from utils.data_import import DataImporter
from utils.data_export import DataExporter

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="BankAnalytics Pro | Enterprise Banking Platform",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# INITIALIZE SESSION & GLOBALS
# ==================================================

init_session_state()
db = Database()
ml_pipeline = MLPipeline()
auth_manager = AuthManager()
insights_engine = InsightsEngine()
data_importer = DataImporter()
data_exporter = DataExporter()

# ==================================================
# PROFESSIONAL CSS STYLING
# ==================================================

def load_css():
    st.markdown("""
        <style>
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
        
        .main {
            background: linear-gradient(135deg, #f5f7fb 0%, #eef2f8 100%);
        }
        
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a2a4e 0%, #0f1829 100%);
            box-shadow: 2px 0 20px rgba(0, 0, 0, 0.15);
        }
        
        [data-testid="stSidebar"] * {
            color: #ffffff;
        }
        
        h1 { color: #0f1829; font-size: 32px; font-weight: 700; }
        h2 { color: #1a2a4e; font-size: 24px; font-weight: 600; }
        h3 { color: #2c3e50; font-size: 18px; font-weight: 600; }
        
        .stMetric { 
            background: white; 
            padding: 20px; 
            border-radius: 12px; 
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
            border-left: 4px solid #1976d2;
        }
        
        .stButton > button {
            background: linear-gradient(90deg, #1976d2 0%, #1565c0 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)

load_css()

# ==================================================
# LOGIN PAGE
# ==================================================

def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div style='text-align: center; margin: 50px 0;'><h1 style='color: #1976d2;'>🏦 BankAnalytics Pro</h1><p style='color: #666;'>Enterprise Customer Intelligence Platform</p></div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        email = st.text_input("📧 Email", placeholder="admin@bankanalytics.com")
        password = st.text_input("🔐 Password", type="password", placeholder="Enter password")
        
        if st.button("🔓 Login", use_container_width=True, type="primary"):
            if email and password:
                if auth_manager.login(email, password):
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
            else:
                st.warning("⚠️ Enter email and password")
        
        st.markdown("---")
        st.markdown("""
            <div style='background: #f5f7fb; padding: 15px; border-radius: 8px;'>
                <p style='font-weight: bold;'>📝 Demo Credentials:</p>
                <p><code>admin@bankanalytics.com / admin123</code></p>
                <p><code>manager@bankanalytics.com / manager123</code></p>
                <p><code>employee@bankanalytics.com / employee123</code></p>
            </div>
        """, unsafe_allow_html=True)

# ==================================================
# SIDEBAR NAVIGATION
# ==================================================

def sidebar_navigation():
    with st.sidebar:
        st.markdown("<div style='text-align: center; padding: 20px 0; margin-bottom: 20px; border-bottom: 1px solid rgba(255,255,255,0.2);'><h2 style='color: #64b5f6; margin: 0;'>🏦 BankAnalytics</h2><p style='color: #90caf9; margin: 5px 0 0 0;'>Pro Edition</p></div>", unsafe_allow_html=True)
        
        current_user = auth_manager.get_current_user()
        st.markdown(f"<p style='color: #90caf9; font-size: 12px;'>👤 {current_user['name']} ({current_user['role']})</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown("### 📊 Dashboard")
        if st.button("🎯 Dashboard", use_container_width=True):
            st.session_state.current_page = "Dashboard"
            st.rerun()
        if st.button("📈 Analytics", use_container_width=True):
            st.session_state.current_page = "Analytics"
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 👥 Customers")
        if st.button("➕ Add Customer", use_container_width=True):
            st.session_state.current_page = "Add Customer"
            st.rerun()
        if st.button("🔍 Search Customer", use_container_width=True):
            st.session_state.current_page = "Search Customer"
            st.rerun()
        if st.button("📋 All Customers", use_container_width=True):
            st.session_state.current_page = "All Customers"
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 🤖 ML Predictions")
        if st.button("🔮 Predict Churn", use_container_width=True):
            st.session_state.current_page = "Churn Prediction"
            st.rerun()
        if st.button("📊 Model Performance", use_container_width=True):
            st.session_state.current_page = "Model Performance"
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Reports")
        if st.button("📄 Executive Summary", use_container_width=True):
            st.session_state.current_page = "Executive Summary"
            st.rerun()
        if st.button("📥 Import/Export", use_container_width=True):
            st.session_state.current_page = "Import Export"
            st.rerun()
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            auth_manager.logout()
            st.rerun()
        
        st.markdown(f"<p style='text-align: center; color: #666; font-size: 11px; margin-top: 20px;'>© 2024 BankAnalytics Pro</p>", unsafe_allow_html=True)

# ==================================================
# DASHBOARD PAGE
# ==================================================

def page_dashboard():
    st.markdown("<h1>📊 Dashboard</h1>", unsafe_allow_html=True)
    
    stats = db.get_dashboard_stats()
    
    col1, col2, col3, col4, col5 = st.columns(5, gap="medium")
    
    with col1:
        st.metric("👥 Total Customers", f"{stats['total_customers']:,}")
    with col2:
        st.metric("✅ Active", f"{stats['active_customers']:,}")
    with col3:
        st.metric("🚨 High Risk", f"{stats['high_risk_customers']:,}")
    with col4:
        st.metric("💰 Avg Balance", f"${stats['avg_balance']:,.0f}")
    with col5:
        st.metric("📈 Engagement", f"{stats['avg_engagement_score']:.1f}")
    
    st.markdown("---")
    
    # Insights
    insights = insights_engine.generate_dashboard_insights()
    if insights:
        st.subheader("💡 Business Insights")
        for insight in insights:
            st.markdown(f"""
                <div style='background: {insight["color"]}20; padding: 15px; border-radius: 8px; border-left: 4px solid {insight["color"]}; margin: 10px 0;'>
                    <p style='margin: 0; font-weight: bold;'>{insight["icon"]} {insight["title"]}</p>
                    <p style='margin: 8px 0 0 0; color: #333;'>{insight["message"]}</p>
                </div>
            """, unsafe_allow_html=True)

# ==================================================
# ADD CUSTOMER PAGE
# ==================================================

def page_add_customer():
    if not auth_manager.require_permission("create_customer"):
        return
    
    st.markdown("<h1>➕ Add New Customer</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        first_name = st.text_input("First Name *")
        last_name = st.text_input("Last Name *")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        date_of_birth = st.date_input("Date of Birth")
    
    with col2:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        country = st.selectbox("Country", ["USA", "UK", "Germany", "France", "Spain"])
        credit_score = st.number_input("Credit Score", 300, 850, 650)
        occupation = st.text_input("Occupation")
        annual_income = st.number_input("Annual Income ($)", 0.0)
    
    col3, col4 = st.columns(2, gap="medium")
    
    with col3:
        estimated_salary = st.number_input("Estimated Salary ($)", 0.0)
        balance = st.number_input("Balance ($)", 0.0)
        tenure = st.number_input("Tenure (years)", 0, 50, 5)
        num_products = st.slider("Number of Products", 1, 4, 2)
    
    with col4:
        has_credit_card = st.checkbox("Has Credit Card")
        is_active_member = st.checkbox("Is Active Member")
        risk_preference = st.selectbox("Risk Preference", ["Conservative", "Moderate", "Aggressive"])
        account_type = st.selectbox("Account Type", ACCOUNT_TYPES)
    
    notes = st.text_area("Notes")
    
    if st.button("💾 Save Customer", use_container_width=True, type="primary"):
        customer_data = {
            "customer_id": f"CUST_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "date_of_birth": str(date_of_birth),
            "gender": gender,
            "country": country,
            "credit_score": credit_score,
            "occupation": occupation,
            "annual_income": annual_income,
            "estimated_salary": estimated_salary,
            "balance": balance,
            "tenure": tenure,
            "num_of_products": num_products,
            "has_credit_card": int(has_credit_card),
            "is_active_member": int(is_active_member),
            "risk_preference": risk_preference,
            "account_type": account_type,
            "notes": notes,
            "created_by": st.session_state.user_email,
        }
        
        is_valid, errors = Validator.validate_all_customer_data(customer_data)
        
        if is_valid:
            cust_id = db.create_customer(customer_data)
            if cust_id:
                # Get prediction
                pred = ml_pipeline.predict_churn(customer_data, cust_id)
                if pred:
                    db.save_prediction(cust_id, pred)
                
                db.log_activity(st.session_state.user_email, "CREATE_CUSTOMER", cust_id)
                st.success(f"✅ Customer created: {cust_id}")
            else:
                st.error("❌ Customer already exists")
        else:
            for error in errors:
                st.error(f"❌ {error}")

# ==================================================
# SEARCH CUSTOMER PAGE
# ==================================================

def page_search_customer():
    st.markdown("<h1>🔍 Search Customer</h1>", unsafe_allow_html=True)
    
    search_query = st.text_input("Search by ID, Name, or Email")
    
    if search_query:
        results = db.search_customers(search_query)
        
        if results:
            st.subheader(f"Found {len(results)} customer(s)")
            
            for customer in results:
                with st.expander(f"{customer['first_name']} {customer['last_name']} (ID: {customer['customer_id']})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Email:** {customer['email']}")
                        st.write(f"**Phone:** {customer['phone']}")
                        st.write(f"**Country:** {customer['country']}")
                        st.write(f"**Credit Score:** {customer['credit_score']}")
                    
                    with col2:
                        st.write(f"**Balance:** ${customer['balance']:,.0f}")
                        st.write(f"**Products:** {customer['num_of_products']}")
                        st.write(f"**Tenure:** {customer['tenure']} years")
                        st.write(f"**Status:** {customer['status']}")
                    
                    # Get prediction
                    prediction = db.get_latest_prediction(customer['customer_id'])
                    if prediction:
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Engagement Score", f"{prediction['engagement_score']:.1f}")
                        with col2:
                            st.metric("Churn Risk", f"{prediction['churn_probability']:.1f}%")
                        with col3:
                            st.metric("Risk Level", prediction['risk_level'])
        else:
            st.info("No customers found")

# ==================================================
# ALL CUSTOMERS PAGE
# ==================================================

def page_all_customers():
    st.markdown("<h1>📋 All Customers</h1>", unsafe_allow_html=True)
    
    customers = db.get_all_customers(limit=100)
    
    if customers:
        df = pd.DataFrame(customers)
        # Select relevant columns
        display_cols = ["customer_id", "first_name", "last_name", "email", "country", "balance", "num_of_products", "status"]
        df_display = df[[col for col in display_cols if col in df.columns]]
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        # Export options
        col1, col2, col3 = st.columns(3)
        with col1:
            success, data, filename = data_exporter.export_customers_csv()
            if success:
                st.download_button("📥 Download CSV", data, filename, "text/csv", use_container_width=True)
        with col2:
            success, data, filename = data_exporter.export_customers_excel()
            if success:
                st.download_button("📥 Download Excel", data, filename, "application/vnd.ms-excel", use_container_width=True)
    else:
        st.info("No customers found")

# ==================================================
# CHURN PREDICTION PAGE
# ==================================================

def page_churn_prediction():
    st.markdown("<h1>🔮 Churn Prediction</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Existing Customer", "New Customer"])
    
    with tab1:
        customers = db.get_all_customers(limit=500)
        if customers:
            customer_options = {f"{c['first_name']} {c['last_name']} ({c['customer_id']})": c['customer_id'] for c in customers}
            selected = st.selectbox("Select Customer", list(customer_options.keys()))
            
            if selected:
                customer_id = customer_options[selected]
                customer = db.get_customer(customer_id)
                prediction = db.get_latest_prediction(customer_id)
                
                if prediction:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Engagement Score", f"{prediction['engagement_score']:.1f}")
                    with col2:
                        st.metric("Churn Probability", f"{prediction['churn_probability']:.1f}%")
                    with col3:
                        st.metric("Risk Level", prediction['risk_level'])
                    
                    render_risk_gauge(prediction['churn_probability'], "Churn Risk")
                    
                    insights = insights_engine.generate_customer_insights(customer_id)
                    if insights:
                        render_recommendation_card(insights)
    
    with tab2:
        st.subheader("Create New Customer Prediction")
        
        # Similar form to add customer, but for prediction only
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", 18, 100, 35)
            credit_score = st.number_input("Credit Score", 300, 850, 650)
            tenure = st.number_input("Tenure (years)", 0, 50, 5)
        with col2:
            balance = st.number_input("Balance ($)", 0.0)
            num_products = st.slider("Number of Products", 1, 4, 2)
            is_active = st.checkbox("Is Active Member")
        
        if st.button("🔮 Predict Churn", use_container_width=True, type="primary"):
            prediction_data = {
                "age": age,
                "credit_score": credit_score,
                "tenure": tenure,
                "balance": balance,
                "num_of_products": num_products,
                "is_active_member": int(is_active),
            }
            
            pred = ml_pipeline.predict_churn(prediction_data)
            if pred:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Engagement Score", f"{pred['engagement_score']:.1f}")
                with col2:
                    st.metric("Churn Probability", f"{pred['churn_probability']:.1f}%")
                with col3:
                    st.metric("Risk Level", pred['risk_level'])
                
                render_risk_gauge(pred['churn_probability'], "Churn Risk")

# ==================================================
# MODEL PERFORMANCE PAGE
# ==================================================

def page_model_performance():
    st.markdown("<h1>📊 Model Performance</h1>", unsafe_allow_html=True)
    
    accuracy = ml_pipeline.get_model_accuracy()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Model Accuracy", f"{accuracy*100:.2f}%")
    with col2:
        st.metric("Algorithm", "Random Forest")
    with col3:
        st.metric("Features", len(ml_pipeline.feature_columns or []))
    with col4:
        st.metric("Train/Test Split", "80/20")
    
    st.markdown("---")
    
    st.subheader("📈 Feature Importance")
    importance = ml_pipeline.get_feature_importance()
    if importance is not None:
        fig = px.bar(importance.head(10), x="Importance", y="Feature", orientation="h", color="Importance")
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

# ==================================================
# EXECUTIVE SUMMARY PAGE
# ==================================================

def page_executive_summary():
    st.markdown("<h1>📄 Executive Summary</h1>", unsafe_allow_html=True)
    
    stats = db.get_dashboard_stats()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%); padding: 25px; border-radius: 12px; color: white;'>
                <p style='margin: 0 0 15px 0; font-size: 14px;'>👥 TOTAL CUSTOMERS</p>
                <p style='margin: 0; font-size: 32px; font-weight: bold;'>{stats['total_customers']:,}</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #42a5f5 0%, #1e88e5 100%); padding: 25px; border-radius: 12px; color: white;'>
                <p style='margin: 0 0 15px 0; font-size: 14px;'>🚨 HIGH RISK</p>
                <p style='margin: 0; font-size: 32px; font-weight: bold;'>{stats['high_risk_customers']:,}</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
        ### Key Findings
        - Customer database actively manages retention strategies
        - Machine learning model provides accurate churn predictions
        - Multi-segment analysis enables targeted interventions
        - Real-time dashboards track KPIs and emerging risks
    """)

# ==================================================
# IMPORT/EXPORT PAGE
# ==================================================

def page_import_export():
    if not auth_manager.is_manager():
        st.error("❌ Manager access required")
        return
    
    st.markdown("<h1>📥📤 Import/Export Data</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Import", "Export"])
    
    with tab1:
        st.subheader("Import Customer Data")
        uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])
        
        if uploaded_file:
            if st.button("📤 Import File", use_container_width=True):
                if uploaded_file.name.endswith('.csv'):
                    success, message, count = data_importer.import_csv(uploaded_file, st.session_state.user_email)
                else:
                    success, message, count = data_importer.import_excel(uploaded_file, st.session_state.user_email)
                
                if success:
                    st.success(f"✅ {message}")
                else:
                    st.error(f"❌ {message}")
        
        if st.button("📥 Import Dataset", use_container_width=True):
            success, message, count = data_importer.import_from_csv_dataset(st.session_state.user_email)
            if success:
                st.success(f"✅ {message}")
            else:
                st.error(f"❌ {message}")
    
    with tab2:
        st.subheader("Export Customer Data")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            success, data, filename = data_exporter.export_customers_csv()
            if success:
                st.download_button("📥 Customers CSV", data, filename, "text/csv", use_container_width=True)
        
        with col2:
            success, data, filename = data_exporter.export_predictions_csv()
            if success:
                st.download_button("📥 Predictions CSV", data, filename, "text/csv", use_container_width=True)
        
        with col3:
            success, data, filename = data_exporter.export_high_risk_customers_csv()
            if success:
                st.download_button("📥 High Risk CSV", data, filename, "text/csv", use_container_width=True)

# ==================================================
# MAIN APP LOGIC
# ==================================================

def main():
    if not st.session_state.authenticated:
        login_page()
    else:
        sidebar_navigation()
        
        # Route to pages
        page = st.session_state.current_page
        
        if page == "Dashboard":
            page_dashboard()
        elif page == "Analytics":
            st.markdown("<h1>📈 Analytics</h1>", unsafe_allow_html=True)
            st.info("Advanced analytics dashboard coming soon!")
        elif page == "Add Customer":
            page_add_customer()
        elif page == "Search Customer":
            page_search_customer()
        elif page == "All Customers":
            page_all_customers()
        elif page == "Churn Prediction":
            page_churn_prediction()
        elif page == "Model Performance":
            page_model_performance()
        elif page == "Executive Summary":
            page_executive_summary()
        elif page == "Import Export":
            page_import_export()
        else:
            page_dashboard()
        
        st.markdown("---")
        st.markdown("<p style='text-align: center; color: #999; font-size: 11px;'>🏦 BankAnalytics Pro | Enterprise Banking Platform | Powered by Streamlit & ML</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
