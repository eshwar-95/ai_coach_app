"""Authentication and session management module."""
import streamlit as st
import pandas as pd
from src.config import hash_password, verify_password
from src.databricks_client import DatabricksClient


class AuthenticationManager:
    """Manages user authentication and session."""

    @staticmethod
    def get_roles_data() -> pd.DataFrame:
        """Fetch roles data from Databricks."""
        try:
            client = DatabricksClient()
            return client.get_roles_data()
        except Exception as e:
            st.error(f"Error fetching roles data: {str(e)}")
            return pd.DataFrame()

    @staticmethod
    def authenticate_user(email_or_username: str, password: str) -> dict:
        """
        Authenticate user against roles.csv.

        Args:
            email_or_username: User email or username
            password: User password

        Returns:
            Dictionary with user info if authenticated, None otherwise
        """
        roles_df = AuthenticationManager.get_roles_data()

        if roles_df.empty:
            return None

        # Search for user by email or username (case-insensitive)
        user_record = roles_df[
            (
                roles_df["email"].str.lower() == email_or_username.lower()
            )
            | (roles_df["username"].str.lower() == email_or_username.lower())
        ]

        if user_record.empty:
            return None

        user_record = user_record.iloc[0]

        # Verify password (plain text comparison)
        if password != user_record["password"]:
            return None

        return {
            "id": str(user_record.get("id", "")),
            "username": user_record.get("username", ""),
            "email": user_record.get("email", ""),
            "role": user_record.get("role", "mentee"),
            "name": user_record.get("name", ""),
        }

    @staticmethod
    def initialize_session():
        """Initialize session state variables."""
        if "authenticated" not in st.session_state:
            st.session_state.authenticated = False
        if "user" not in st.session_state:
            st.session_state.user = None
        if "current_page" not in st.session_state:
            st.session_state.current_page = "login"

    @staticmethod
    def login(email_or_username: str, password: str) -> bool:
        """
        Log in a user.

        Args:
            email_or_username: User email or username
            password: User password

        Returns:
            True if login successful, False otherwise
        """
        user = AuthenticationManager.authenticate_user(email_or_username, password)
        if user:
            st.session_state.authenticated = True
            st.session_state.user = user
            st.session_state.current_page = "home"
            return True
        return False

    @staticmethod
    def logout():
        """Log out the current user."""
        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.current_page = "login"

    @staticmethod
    def is_authenticated() -> bool:
        """Check if user is authenticated."""
        return st.session_state.get("authenticated", False)

    @staticmethod
    def get_current_user() -> dict:
        """Get current authenticated user."""
        return st.session_state.get("user", None)

    @staticmethod
    def get_user_role() -> str:
        """Get current user's role."""
        user = AuthenticationManager.get_current_user()
        return user["role"] if user else None

    @staticmethod
    def is_mentor() -> bool:
        """Check if current user is a mentor."""
        return AuthenticationManager.get_user_role() == "mentor"

    @staticmethod
    def is_mentee() -> bool:
        """Check if current user is a mentee."""
        return AuthenticationManager.get_user_role() == "mentee"
