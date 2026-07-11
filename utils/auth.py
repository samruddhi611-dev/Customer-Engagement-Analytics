# ==================================================
# AUTHENTICATION & AUTHORIZATION
# ==================================================

import streamlit as st
from datetime import datetime, timedelta
import hashlib
from config import UserRole, DEMO_CREDENTIALS, ROLE_PERMISSIONS
from database.models import Database


class AuthManager:
    """Authentication & Authorization Manager"""

    def __init__(self):
        self.db = Database()
        self.init_demo_users()

    def init_demo_users(self):
        """Initialize demo users if not exists"""
        for email, creds in DEMO_CREDENTIALS.items():
            if self.db.get_user(email) is None:
                self.db.create_user(
                    email=email,
                    password=self._hash_password(creds["password"]),
                    name=creds["name"],
                    role=creds["role"].value,
                )

    @staticmethod
    def _hash_password(password: str) -> str:
        """Hash password (simple - use bcrypt in production)"""
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self, email: str, password: str) -> bool:
        """Authenticate user"""
        user = self.db.get_user(email)
        if user and user["password"] == self._hash_password(password) and user["is_active"]:
            st.session_state.authenticated = True
            st.session_state.user_email = email
            st.session_state.user_name = user["name"]
            st.session_state.user_role = user["role"]
            st.session_state.login_time = datetime.now()
            return True
        return False

    def logout(self):
        """Logout user"""
        st.session_state.authenticated = False
        st.session_state.user_email = None
        st.session_state.user_name = None
        st.session_state.user_role = None
        st.session_state.login_time = None

    def has_permission(self, permission: str) -> bool:
        """Check if user has permission"""
        if not st.session_state.get("authenticated"):
            return False

        role = st.session_state.get("user_role")
        permissions = ROLE_PERMISSIONS.get(role, {})
        return permissions.get(permission, False)

    def require_permission(self, permission: str):
        """Enforce permission requirement"""
        if not self.has_permission(permission):
            st.error("❌ You don't have permission to access this feature.")
            return False
        return True

    def is_admin(self) -> bool:
        """Check if user is admin"""
        return st.session_state.get("user_role") == UserRole.ADMIN.value

    def is_manager(self) -> bool:
        """Check if user is manager"""
        return st.session_state.get("user_role") in [
            UserRole.MANAGER.value,
            UserRole.ADMIN.value,
        ]

    def get_current_user(self) -> dict:
        """Get current user info"""
        return {
            "email": st.session_state.get("user_email"),
            "name": st.session_state.get("user_name"),
            "role": st.session_state.get("user_role"),
        }


def init_session_state():
    """Initialize session state variables"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_email" not in st.session_state:
        st.session_state.user_email = None
    if "user_name" not in st.session_state:
        st.session_state.user_name = None
    if "user_role" not in st.session_state:
        st.session_state.user_role = None
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Dashboard"
    if "login_time" not in st.session_state:
        st.session_state.login_time = None
