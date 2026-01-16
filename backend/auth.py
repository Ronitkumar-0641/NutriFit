"""
Authentication module using Supabase for user management.
Safe for Streamlit Cloud (lazy initialization).
"""

import os
from typing import Optional, Dict, Any
from supabase import create_client, Client

# Import profile service
try:
    from .profile_service import ProfileService
except ImportError:
    from profile_service import ProfileService


# -------------------------------
# Supabase client (LAZY, SAFE)
# -------------------------------

def get_supabase_client() -> Client:
    """
    Lazily create and return Supabase client.
    This MUST NOT run at import time.
    """
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_API_KEY")

    if not url or not key:
        raise RuntimeError("Supabase credentials are missing")

    return create_client(url, key)


# -------------------------------
# Simple login helper (used by UI)
# -------------------------------

def login_user(email: str, password: str) -> Dict[str, Any]:
    supabase = get_supabase_client()
    return supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })


# -------------------------------
# Auth Service Class
# -------------------------------

class AuthService:
    """Service for handling authentication operations with Supabase."""

    @staticmethod
    def sign_up(
        email: str,
        password: str,
        full_name: Optional[str] = None,
        weight_kg: Optional[float] = None,
        height_cm: Optional[float] = None,
        age: Optional[int] = None,
        gender: Optional[str] = None,
        fitness_goal: Optional[str] = None
    ) -> Dict[str, Any]:
        try:
            supabase = get_supabase_client()

            response = supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "full_name": full_name or ""
                    }
                }
            })

            if not response.user:
                return {
                    "success": False,
                    "error": "Registration failed. Please try again."
                }

            profile_created = False
            if weight_kg and height_cm and age and gender:
                profile_result = ProfileService.create_profile(
                    user_id=response.user.id,
                    full_name=full_name or "",
                    weight_kg=weight_kg,
                    height_cm=height_cm,
                    age=age,
                    gender=gender,
                    fitness_goal=fitness_goal
                )
                profile_created = profile_result.get("success", False)

            return {
                "success": True,
                "user": {
                    "id": response.user.id,
                    "email": response.user.email,
                    "full_name": full_name
                },
                "session": {
                    "access_token": response.session.access_token if response.session else None,
                    "refresh_token": response.session.refresh_token if response.session else None
                },
                "profile_created": profile_created,
                "message": "Registration successful! Please check your email to verify your account."
            }

        except Exception as e:
            msg = str(e).lower()
            if "already registered" in msg:
                return {
                    "success": False,
                    "error": "This email is already registered. Please login instead."
                }
            return {
                "success": False,
                "error": f"Registration error: {str(e)}"
            }

    @staticmethod
    def sign_in(email: str, password: str) -> Dict[str, Any]:
        try:
            supabase = get_supabase_client()

            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            if not response.user:
                return {
                    "success": False,
                    "error": "Invalid email or password."
                }

            return {
                "success": True,
                "user": {
                    "id": response.user.id,
                    "email": response.user.email,
                    "full_name": response.user.user_metadata.get("full_name", "")
                },
                "session": {
                    "access_token": response.session.access_token,
                    "refresh_token": response.session.refresh_token
                },
                "message": "Login successful!"
            }

        except Exception as e:
            msg = str(e).lower()

            if "email not confirmed" in msg:
                return {
                    "success": False,
                    "error": "Email not confirmed. Please check your inbox.",
                    "email_not_confirmed": True,
                    "email": email
                }

            if "invalid" in msg or "credentials" in msg:
                return {
                    "success": False,
                    "error": "Invalid email or password."
                }

            return {
                "success": False,
                "error": f"Login error: {str(e)}"
            }

    @staticmethod
    def sign_out() -> Dict[str, Any]:
        try:
            supabase = get_supabase_client()
            supabase.auth.sign_out()
            return {
                "success": True,
                "message": "Logged out successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Logout error: {str(e)}"
            }

    @staticmethod
    def get_user(access_token: str) -> Optional[Dict[str, Any]]:
        try:
            supabase = get_supabase_client()
            response = supabase.auth.get_user(access_token)

            if not response.user:
                return None

            return {
                "id": response.user.id,
                "email": response.user.email,
                "full_name": response.user.user_metadata.get("full_name", "")
            }

        except Exception:
            return None

    @staticmethod
    def reset_password(email: str) -> Dict[str, Any]:
        try:
            supabase = get_supabase_client()
            supabase.auth.reset_password_email(email)
            return {
                "success": True,
                "message": "Password reset email sent."
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Reset error: {str(e)}"
            }

    @staticmethod
    def resend_confirmation_email(email: str) -> Dict[str, Any]:
        try:
            supabase = get_supabase_client()
            supabase.auth.resend(
                type="signup",
                email=email
            )
            return {
                "success": True,
                "message": "Confirmation email sent."
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Resend error: {str(e)}"
            }
