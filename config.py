# ==================================================
# ENTERPRISE CONFIGURATION
# ==================================================

import os
from enum import Enum
from pathlib import Path

# Environment
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_DIR = BASE_DIR / "database"
DB_DIR.mkdir(exist_ok=True)

MODELS_DIR = BASE_DIR / "models"
MODELS_DIR.mkdir(exist_ok=True)

# Database
DATABASE_URL = f"sqlite:///{DB_DIR}/banking_crm.db"
DATABASE_PATH = str(DB_DIR / "banking_crm.db")

# ML Model
MODEL_PATH = str(MODELS_DIR / "churn_model.pkl")
MODEL_ENCODER_PATH = str(MODELS_DIR / "label_encoders.pkl")

# CSV Dataset
CSV_DATA_PATH = str(DATA_DIR / "churn.csv")

# Color Palette - Banking Professional
COLOR_PRIMARY = "#1976d2"
COLOR_PRIMARY_DARK = "#1565c0"
COLOR_SECONDARY = "#64b5f6"
COLOR_SUCCESS = "#2ecc71"
COLOR_WARNING = "#ff9800"
COLOR_DANGER = "#e74c3c"
COLOR_LIGHT_BG = "#f5f7fb"
COLOR_DARK_BG = "#0f1829"

# Theme
THEME_COLORS = {
    "primary": COLOR_PRIMARY,
    "secondary": COLOR_SECONDARY,
    "success": COLOR_SUCCESS,
    "warning": COLOR_WARNING,
    "danger": COLOR_DANGER,
    "light_bg": COLOR_LIGHT_BG,
    "dark_bg": COLOR_DARK_BG,
}

# Risk Levels
class RiskLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

# Customer Status
class CustomerStatus(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    DORMANT = "Dormant"
    FLAGGED = "Flagged"

# Account Types
ACCOUNT_TYPES = [
    "Checking",
    "Savings",
    "Money Market",
    "CD",
    "Premium",
]

# User Roles
class UserRole(str, Enum):
    ADMIN = "Admin"
    MANAGER = "Manager"
    EMPLOYEE = "Employee"

# Role Permissions
ROLE_PERMISSIONS = {
    UserRole.ADMIN: {
        "view_all_customers": True,
        "create_customer": True,
        "edit_customer": True,
        "delete_customer": True,
        "view_reports": True,
        "manage_users": True,
        "system_settings": True,
    },
    UserRole.MANAGER: {
        "view_all_customers": True,
        "create_customer": True,
        "edit_customer": True,
        "delete_customer": False,
        "view_reports": True,
        "manage_users": False,
        "system_settings": False,
    },
    UserRole.EMPLOYEE: {
        "view_all_customers": True,
        "create_customer": True,
        "edit_customer": True,
        "delete_customer": False,
        "view_reports": False,
        "manage_users": False,
        "system_settings": False,
    },
}

# Default Credentials (for demo)
DEMO_CREDENTIALS = {
    "admin@bankanalytics.com": {
        "password": "admin123",
        "role": UserRole.ADMIN,
        "name": "Admin User",
    },
    "manager@bankanalytics.com": {
        "password": "manager123",
        "role": UserRole.MANAGER,
        "name": "Manager User",
    },
    "employee@bankanalytics.com": {
        "password": "employee123",
        "role": UserRole.EMPLOYEE,
        "name": "Employee User",
    },
}

# Pagination
PAGES_PER_RECORD = 10

# Cache Settings
CACHE_TTL = 300  # 5 minutes
