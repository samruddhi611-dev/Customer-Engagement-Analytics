# ==================================================
# DATABASE MODELS
# ==================================================

import sqlite3
from datetime import datetime
from typing import List, Optional, Dict, Any
import json
from config import DATABASE_PATH, RiskLevel, CustomerStatus, UserRole


class Database:
    """SQLite Database Manager"""

    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Users table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                name TEXT NOT NULL,
                role TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active INTEGER DEFAULT 1
            )
        """
        )

        # Customers table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id TEXT UNIQUE NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                date_of_birth TEXT,
                gender TEXT,
                country TEXT,
                credit_score INTEGER,
                occupation TEXT,
                annual_income REAL,
                estimated_salary REAL,
                balance REAL,
                tenure INTEGER,
                num_of_products INTEGER,
                has_credit_card INTEGER,
                is_active_member INTEGER,
                risk_preference TEXT,
                account_type TEXT,
                branch TEXT,
                manager TEXT,
                notes TEXT,
                status TEXT DEFAULT 'Active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_by TEXT
            )
        """
        )

        # Predictions table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id TEXT NOT NULL,
                engagement_score REAL,
                churn_probability REAL,
                risk_level TEXT,
                is_churned INTEGER,
                predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                model_version TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
            )
        """
        )

        # Activity logs table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS activity_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_email TEXT,
                action TEXT,
                customer_id TEXT,
                details TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
            )
        """
        )

        # Imported Data Tracking
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS imports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                imported_by TEXT,
                row_count INTEGER,
                imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        conn.commit()
        conn.close()

    # ==================== CUSTOMER OPERATIONS ====================

    def create_customer(self, customer_data: Dict[str, Any]) -> Optional[str]:
        """Create new customer"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO customers (
                    customer_id, first_name, last_name, email, phone,
                    date_of_birth, gender, country, credit_score, occupation,
                    annual_income, estimated_salary, balance, tenure,
                    num_of_products, has_credit_card, is_active_member,
                    risk_preference, account_type, branch, manager, notes,
                    status, created_by
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    customer_data["customer_id"],
                    customer_data["first_name"],
                    customer_data["last_name"],
                    customer_data.get("email"),
                    customer_data.get("phone"),
                    customer_data.get("date_of_birth"),
                    customer_data.get("gender"),
                    customer_data.get("country"),
                    customer_data.get("credit_score"),
                    customer_data.get("occupation"),
                    customer_data.get("annual_income"),
                    customer_data.get("estimated_salary"),
                    customer_data.get("balance"),
                    customer_data.get("tenure"),
                    customer_data.get("num_of_products"),
                    customer_data.get("has_credit_card"),
                    customer_data.get("is_active_member"),
                    customer_data.get("risk_preference"),
                    customer_data.get("account_type"),
                    customer_data.get("branch"),
                    customer_data.get("manager"),
                    customer_data.get("notes"),
                    customer_data.get("status", "Active"),
                    customer_data.get("created_by"),
                ),
            )

            conn.commit()
            conn.close()
            return customer_data["customer_id"]
        except sqlite3.IntegrityError:
            return None

    def get_customer(self, customer_id: str) -> Optional[Dict]:
        """Get customer by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE customer_id = ?", (customer_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def get_all_customers(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Get all customers with pagination"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM customers ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (limit, offset),
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def update_customer(self, customer_id: str, customer_data: Dict[str, Any]) -> bool:
        """Update customer information"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            update_fields = []
            values = []

            for key, value in customer_data.items():
                if key != "customer_id":
                    update_fields.append(f"{key} = ?")
                    values.append(value)

            update_fields.append("updated_at = CURRENT_TIMESTAMP")
            values.append(customer_id)

            query = f"UPDATE customers SET {', '.join(update_fields)} WHERE customer_id = ?"
            cursor.execute(query, values)

            conn.commit()
            conn.close()
            return True
        except Exception:
            return False

    def delete_customer(self, customer_id: str) -> bool:
        """Delete customer"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM customers WHERE customer_id = ?", (customer_id,))
            cursor.execute("DELETE FROM predictions WHERE customer_id = ?", (customer_id,))
            conn.commit()
            conn.close()
            return True
        except Exception:
            return False

    def search_customers(self, query: str) -> List[Dict]:
        """Search customers by name, email, or ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        search_term = f"%{query}%"
        cursor.execute(
            """
            SELECT * FROM customers WHERE
            customer_id LIKE ? OR
            first_name LIKE ? OR
            last_name LIKE ? OR
            email LIKE ?
            ORDER BY created_at DESC
        """,
            (search_term, search_term, search_term, search_term),
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_customer_count(self) -> int:
        """Get total customer count"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM customers")
        result = cursor.fetchone()
        conn.close()
        return result["count"] if result else 0

    # ==================== PREDICTION OPERATIONS ====================

    def save_prediction(self, customer_id: str, prediction_data: Dict[str, Any]) -> bool:
        """Save prediction result"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO predictions (
                    customer_id, engagement_score, churn_probability,
                    risk_level, is_churned, model_version
                ) VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    customer_id,
                    prediction_data.get("engagement_score"),
                    prediction_data.get("churn_probability"),
                    prediction_data.get("risk_level"),
                    prediction_data.get("is_churned"),
                    prediction_data.get("model_version", "1.0"),
                ),
            )
            conn.commit()
            conn.close()
            return True
        except Exception:
            return False

    def get_latest_prediction(self, customer_id: str) -> Optional[Dict]:
        """Get latest prediction for customer"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM predictions WHERE customer_id = ? ORDER BY predicted_at DESC LIMIT 1",
            (customer_id,),
        )
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    # ==================== ACTIVITY LOG OPERATIONS ====================

    def log_activity(self, user_email: str, action: str, customer_id: str = None, details: str = None):
        """Log user activity"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO activity_logs (user_email, action, customer_id, details)
                VALUES (?, ?, ?, ?)
            """,
                (user_email, action, customer_id, details),
            )
            conn.commit()
            conn.close()
        except Exception:
            pass

    def get_activity_logs(self, limit: int = 100) -> List[Dict]:
        """Get recent activity logs"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM activity_logs ORDER BY timestamp DESC LIMIT ?", (limit,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    # ==================== USER OPERATIONS ====================

    def create_user(self, email: str, password: str, name: str, role: str) -> bool:
        """Create new user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (email, password, name, role) VALUES (?, ?, ?, ?)",
                (email, password, name, role),
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_user(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    # ==================== STATISTICS ====================

    def get_dashboard_stats(self) -> Dict[str, Any]:
        """Get dashboard statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Total customers
        cursor.execute("SELECT COUNT(*) as count FROM customers")
        total_customers = cursor.fetchone()["count"]

        # Active customers
        cursor.execute("SELECT COUNT(*) as count FROM customers WHERE is_active_member = 1")
        active_customers = cursor.fetchone()["count"]

        # High risk
        cursor.execute(
            "SELECT COUNT(*) as count FROM predictions WHERE risk_level IN ('High', 'Critical')"
        )
        high_risk = cursor.fetchone()["count"]

        # Average balance
        cursor.execute("SELECT AVG(balance) as avg_balance FROM customers")
        avg_balance = cursor.fetchone()["avg_balance"] or 0

        # Average engagement score
        cursor.execute("SELECT AVG(engagement_score) as avg_score FROM predictions")
        avg_engagement = cursor.fetchone()["avg_score"] or 0

        conn.close()

        return {
            "total_customers": total_customers,
            "active_customers": active_customers,
            "high_risk_customers": high_risk,
            "avg_balance": avg_balance,
            "avg_engagement_score": avg_engagement,
        }
