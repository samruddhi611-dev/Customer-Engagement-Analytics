# ==================================================
# DATA EXPORT FUNCTIONALITY
# ==================================================

import pandas as pd
from typing import Tuple
from database.models import Database
from io import BytesIO
import datetime


class DataExporter:
    """Export customer data to CSV/Excel/PDF"""

    def __init__(self):
        self.db = Database()

    def export_customers_csv(self) -> Tuple[bool, BytesIO, str]:
        """Export all customers to CSV"""
        try:
            conn = self.db.get_connection()
            df = pd.read_sql_query("SELECT * FROM customers", conn)
            conn.close()

            csv_buffer = BytesIO()
            df.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)

            filename = f"customers_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            return True, csv_buffer.getvalue(), filename
        except Exception as e:
            return False, None, str(e)

    def export_customers_excel(self) -> Tuple[bool, BytesIO, str]:
        """Export all customers to Excel"""
        try:
            conn = self.db.get_connection()
            df = pd.read_sql_query("SELECT * FROM customers", conn)
            conn.close()

            excel_buffer = BytesIO()
            df.to_excel(excel_buffer, index=False, sheet_name="Customers")
            excel_buffer.seek(0)

            filename = f"customers_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            return True, excel_buffer.getvalue(), filename
        except Exception as e:
            return False, None, str(e)

    def export_predictions_csv(self) -> Tuple[bool, BytesIO, str]:
        """Export all predictions to CSV"""
        try:
            conn = self.db.get_connection()
            df = pd.read_sql_query(
                """
                SELECT p.*, c.first_name, c.last_name, c.email, c.balance
                FROM predictions p
                LEFT JOIN customers c ON p.customer_id = c.customer_id
            """,
                conn,
            )
            conn.close()

            csv_buffer = BytesIO()
            df.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)

            filename = f"predictions_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            return True, csv_buffer.getvalue(), filename
        except Exception as e:
            return False, None, str(e)

    def export_high_risk_customers_csv(self) -> Tuple[bool, BytesIO, str]:
        """Export high-risk customers to CSV"""
        try:
            conn = self.db.get_connection()
            df = pd.read_sql_query(
                """
                SELECT c.*, p.churn_probability, p.risk_level, p.engagement_score
                FROM customers c
                LEFT JOIN predictions p ON c.customer_id = p.customer_id
                WHERE p.risk_level IN ('High', 'Critical')
                ORDER BY p.churn_probability DESC
            """,
                conn,
            )
            conn.close()

            csv_buffer = BytesIO()
            df.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)

            filename = f"high_risk_customers_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            return True, csv_buffer.getvalue(), filename
        except Exception as e:
            return False, None, str(e)

    def export_activity_log_csv(self) -> Tuple[bool, BytesIO, str]:
        """Export activity logs to CSV"""
        try:
            conn = self.db.get_connection()
            df = pd.read_sql_query("SELECT * FROM activity_logs ORDER BY timestamp DESC", conn)
            conn.close()

            csv_buffer = BytesIO()
            df.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)

            filename = f"activity_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            return True, csv_buffer.getvalue(), filename
        except Exception as e:
            return False, None, str(e)
