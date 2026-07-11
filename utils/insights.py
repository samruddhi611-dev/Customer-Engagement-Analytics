# ==================================================
# AI BUSINESS INSIGHTS GENERATION
# ==================================================

import pandas as pd
from database.models import Database
from typing import List


class InsightsEngine:
    """Generate AI-powered business insights"""

    def __init__(self):
        self.db = Database()

    def generate_dashboard_insights(self) -> List[dict]:
        """Generate insights for dashboard"""
        insights = []
        conn = self.db.get_connection()
        cursor = conn.cursor()

        # High churn risk insight
        cursor.execute(
            "SELECT COUNT(*) as count FROM predictions WHERE risk_level IN ('High', 'Critical')"
        )
        high_risk_count = cursor.fetchone()["count"]
        if high_risk_count > 0:
            insights.append(
                {
                    "type": "alert",
                    "icon": "🚨",
                    "title": "High Risk Customers",
                    "message": f"{high_risk_count} customers at high or critical risk of churn. Immediate retention action recommended.",
                    "color": "#e74c3c",
                }
            )

        # Low engagement insight
        cursor.execute(
            "SELECT COUNT(*) as count FROM predictions WHERE engagement_score < 30"
        )
        low_engagement = cursor.fetchone()["count"]
        if low_engagement > 0:
            insights.append(
                {
                    "type": "warning",
                    "icon": "⚡",
                    "title": "Low Engagement",
                    "message": f"{low_engagement} customers showing low engagement. Consider targeted engagement campaigns.",
                    "color": "#ff9800",
                }
            )

        # High value customers
        cursor.execute(
            "SELECT COUNT(*) as count FROM customers WHERE balance > (SELECT AVG(balance) * 1.5 FROM customers)"
        )
        high_value = cursor.fetchone()["count"]
        if high_value > 0:
            insights.append(
                {
                    "type": "opportunity",
                    "icon": "💎",
                    "title": "High Value Customers",
                    "message": f"{high_value} premium customers identified. Focus on retention and cross-selling.",
                    "color": "#2ecc71",
                }
            )

        # New customers insight
        cursor.execute(
            "SELECT COUNT(*) as count FROM customers WHERE strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now')"
        )
        new_customers = cursor.fetchone()["count"]
        if new_customers > 0:
            insights.append(
                {
                    "type": "info",
                    "icon": "👥",
                    "title": "New Customers",
                    "message": f"{new_customers} customers added this month. Onboarding support recommended.",
                    "color": "#1976d2",
                }
            )

        conn.close()
        return insights

    def generate_customer_insights(self, customer_id: str) -> List[str]:
        """Generate insights for specific customer"""
        insights = []
        customer = self.db.get_customer(customer_id)
        prediction = self.db.get_latest_prediction(customer_id)

        if not customer or not prediction:
            return insights

        # Churn risk insight
        if prediction["churn_probability"] > 70:
            insights.append(
                "🚨 Critical: Immediate retention action required. Consider personalized offers."
            )
        elif prediction["churn_probability"] > 50:
            insights.append(
                "⚠️ High Risk: Increase engagement frequency. Offer premium benefits."
            )
        elif prediction["churn_probability"] > 30:
            insights.append(
                "⚡ Medium Risk: Monitor closely. Provide regular value-added services."
            )
        else:
            insights.append("✅ Low Risk: Maintain regular service quality.")

        # Product cross-sell
        if customer["num_of_products"] <= 1:
            insights.append(
                "🛍️ Cross-sell Opportunity: Customer has only 1 product. Recommend additional products."
            )

        # Balance trend
        if customer["balance"] > 200000:
            insights.append(
                "💰 High Value: Premium customer. Assign dedicated relationship manager."
            )
        elif customer["balance"] < 5000:
            insights.append(
                "💸 Low Balance: Promote savings and investment products."
            )

        # Activity status
        if customer["is_active_member"] == 0:
            insights.append(
                "😴 Inactive: Customer not actively using services. Re-engagement campaign needed."
            )
        else:
            insights.append(
                "✨ Active: Customer regularly uses services. Maintain satisfaction."
            )

        # Tenure based
        if customer["tenure"] < 1:
            insights.append(
                "🎯 New Customer: Focus on onboarding experience and satisfaction."
            )
        elif customer["tenure"] > 10:
            insights.append(
                "⭐ Loyal Customer: Long-term relationship. Prioritize retention."
            )

        return insights

    def generate_segment_insights(self) -> dict:
        """Generate insights by customer segments"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        segments = {}

        # By country
        cursor.execute(
            "SELECT country, COUNT(*) as count, AVG(balance) as avg_balance FROM customers GROUP BY country"
        )
        segments["by_country"] = [dict(row) for row in cursor.fetchall()]

        # By risk level
        cursor.execute(
            "SELECT risk_level, COUNT(*) as count FROM predictions GROUP BY risk_level"
        )
        segments["by_risk"] = [dict(row) for row in cursor.fetchall()]

        # By engagement
        cursor.execute(
            """SELECT 
                CASE 
                    WHEN engagement_score >= 80 THEN 'High'
                    WHEN engagement_score >= 50 THEN 'Medium'
                    ELSE 'Low'
                END as engagement_level,
                COUNT(*) as count
            FROM predictions
            GROUP BY engagement_level"""
        )
        segments["by_engagement"] = [dict(row) for row in cursor.fetchall()]

        conn.close()
        return segments
