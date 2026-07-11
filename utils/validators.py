# ==================================================
# FIELD VALIDATION
# ==================================================

import re
from datetime import datetime
from typing import Tuple


class Validator:
    """Customer data validation"""

    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """Validate email format"""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if re.match(pattern, email):
            return True, ""
        return False, "Invalid email format"

    @staticmethod
    def validate_phone(phone: str) -> Tuple[bool, str]:
        """Validate phone number"""
        phone = phone.replace("-", "").replace(" ", "")
        if len(phone) >= 10 and phone.isdigit():
            return True, ""
        return False, "Phone number must be at least 10 digits"

    @staticmethod
    def validate_age(dob: str) -> Tuple[bool, str]:
        """Validate age (18-100)"""
        try:
            birth_date = datetime.strptime(dob, "%Y-%m-%d")
            age = (datetime.now() - birth_date).days // 365
            if 18 <= age <= 100:
                return True, ""
            return False, "Age must be between 18 and 100"
        except ValueError:
            return False, "Invalid date format (use YYYY-MM-DD)"

    @staticmethod
    def validate_credit_score(score: int) -> Tuple[bool, str]:
        """Validate credit score (300-850)"""
        if 300 <= score <= 850:
            return True, ""
        return False, "Credit score must be between 300 and 850"

    @staticmethod
    def validate_balance(balance: float) -> Tuple[bool, str]:
        """Validate balance (non-negative)"""
        if balance >= 0:
            return True, ""
        return False, "Balance cannot be negative"

    @staticmethod
    def validate_tenure(tenure: int) -> Tuple[bool, str]:
        """Validate tenure (0-50 years)"""
        if 0 <= tenure <= 50:
            return True, ""
        return False, "Tenure must be between 0 and 50 years"

    @staticmethod
    def validate_products(num_products: int) -> Tuple[bool, str]:
        """Validate number of products (1-4)"""
        if 1 <= num_products <= 4:
            return True, ""
        return False, "Number of products must be between 1 and 4"

    @staticmethod
    def validate_name(name: str) -> Tuple[bool, str]:
        """Validate name (2-50 chars, letters only)"""
        if 2 <= len(name) <= 50 and name.replace(" ", "").isalpha():
            return True, ""
        return False, "Name must be 2-50 characters, letters only"

    @staticmethod
    def validate_all_customer_data(data: dict) -> Tuple[bool, list]:
        """Validate all customer data"""
        errors = []

        # Required fields
        if not data.get("first_name"):
            errors.append("First name is required")
        else:
            is_valid, msg = Validator.validate_name(data["first_name"])
            if not is_valid:
                errors.append(f"First name: {msg}")

        if not data.get("last_name"):
            errors.append("Last name is required")
        else:
            is_valid, msg = Validator.validate_name(data["last_name"])
            if not is_valid:
                errors.append(f"Last name: {msg}")

        if data.get("email"):
            is_valid, msg = Validator.validate_email(data["email"])
            if not is_valid:
                errors.append(f"Email: {msg}")

        if data.get("phone"):
            is_valid, msg = Validator.validate_phone(data["phone"])
            if not is_valid:
                errors.append(f"Phone: {msg}")

        if data.get("date_of_birth"):
            is_valid, msg = Validator.validate_age(data["date_of_birth"])
            if not is_valid:
                errors.append(f"Date of Birth: {msg}")

        if data.get("credit_score"):
            is_valid, msg = Validator.validate_credit_score(data["credit_score"])
            if not is_valid:
                errors.append(f"Credit Score: {msg}")

        if data.get("balance") is not None:
            is_valid, msg = Validator.validate_balance(data["balance"])
            if not is_valid:
                errors.append(f"Balance: {msg}")

        if data.get("tenure") is not None:
            is_valid, msg = Validator.validate_tenure(data["tenure"])
            if not is_valid:
                errors.append(f"Tenure: {msg}")

        if data.get("num_of_products"):
            is_valid, msg = Validator.validate_products(data["num_of_products"])
            if not is_valid:
                errors.append(f"Number of Products: {msg}")

        return len(errors) == 0, errors
