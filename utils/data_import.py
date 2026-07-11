# ==================================================
# DATA IMPORT FUNCTIONALITY
# ==================================================

import pandas as pd
from typing import Tuple, List
import io
from database.models import Database
from config import CSV_DATA_PATH


class DataImporter:
    """Import customer data from CSV/Excel"""

    def __init__(self):
        self.db = Database()

    def import_csv(self, file_path: str, user_email: str) -> Tuple[bool, str, int]:
        """Import customers from CSV file"""
        try:
            df = pd.read_csv(file_path)
            return self._process_import(df, file_path, user_email)
        except Exception as e:
            return False, f"Error reading CSV: {str(e)}", 0

    def import_excel(self, file_path: str, user_email: str) -> Tuple[bool, str, int]:
        """Import customers from Excel file"""
        try:
            df = pd.read_excel(file_path)
            return self._process_import(df, file_path, user_email)
        except Exception as e:
            return False, f"Error reading Excel: {str(e)}", 0

    def import_from_csv_dataset(self, user_email: str) -> Tuple[bool, str, int]:
        """Import from original CSV dataset"""
        try:
            df = pd.read_csv(CSV_DATA_PATH)
            # Map CSV columns to database columns
            df = df.rename(
                columns={
                    "CustomerId": "customer_id",
                    "Surname": "last_name",
                    "CreditScore": "credit_score",
                    "Age": "age",
                    "Tenure": "tenure",
                    "Balance": "balance",
                    "NumOfProducts": "num_of_products",
                    "HasCrCard": "has_credit_card",
                    "IsActiveMember": "is_active_member",
                    "EstimatedSalary": "estimated_salary",
                }
            )
            df["first_name"] = df["last_name"].apply(lambda x: "Customer")
            return self._process_import(df, "churn.csv", user_email)
        except Exception as e:
            return False, f"Error importing dataset: {str(e)}", 0

    def _process_import(self, df: pd.DataFrame, filename: str, user_email: str) -> Tuple[bool, str, int]:
        """Process imported data"""
        try:
            imported_count = 0
            errors = []

            for idx, row in df.iterrows():
                customer_data = {
                    "customer_id": str(row.get("customer_id", f"IMP_{idx}")),
                    "first_name": str(row.get("first_name", "Customer")),
                    "last_name": str(row.get("last_name", "")),
                    "email": str(row.get("email", "")),
                    "phone": str(row.get("phone", "")),
                    "date_of_birth": str(row.get("date_of_birth", "")),
                    "gender": str(row.get("gender", "")),
                    "country": str(row.get("country", "Geography")),
                    "credit_score": int(row.get("credit_score", 0)) if row.get("credit_score") else 0,
                    "occupation": str(row.get("occupation", "")),
                    "annual_income": float(row.get("annual_income", 0)) if row.get("annual_income") else 0,
                    "estimated_salary": float(row.get("estimated_salary", 0)) if row.get("estimated_salary") else 0,
                    "balance": float(row.get("balance", 0)) if row.get("balance") else 0,
                    "tenure": int(row.get("tenure", 0)) if row.get("tenure") else 0,
                    "num_of_products": int(row.get("num_of_products", 1)) if row.get("num_of_products") else 1,
                    "has_credit_card": int(row.get("has_credit_card", 0)) if row.get("has_credit_card") else 0,
                    "is_active_member": int(row.get("is_active_member", 0)) if row.get("is_active_member") else 0,
                    "risk_preference": str(row.get("risk_preference", "Moderate")),
                    "account_type": str(row.get("account_type", "Checking")),
                    "branch": str(row.get("branch", "")),
                    "manager": str(row.get("manager", "")),
                    "notes": str(row.get("notes", "")),
                    "status": str(row.get("status", "Active")),
                    "created_by": user_email,
                }

                # Try to create customer
                result = self.db.create_customer(customer_data)
                if result:
                    imported_count += 1
                    self.db.log_activity(user_email, "IMPORT_CUSTOMER", result, filename)
                else:
                    errors.append(f"Row {idx + 1}: Duplicate or invalid customer")

            message = f"Successfully imported {imported_count} customers"
            if errors:
                message += f" with {len(errors)} errors"

            return True, message, imported_count
        except Exception as e:
            return False, f"Error processing import: {str(e)}", 0
