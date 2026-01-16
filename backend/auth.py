"""
Authentication module using Supabase for user management.
"""
import os
from typing import Optional, Dict, Any
from supabase import create_client, Client

# Import profile service
try:
    from .profile_service import ProfileService
except ImportError:
    from profile_service import ProfileService


def get_supabase_client() -> Client:
    """
    Lazily create Supabase client.
    Safe for Streamlit Cloud.
    """
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

    if not SUPABASE_URL or not SUPABASE_API_KEY:
        raise RuntimeError("Supabase credentials are missing")

    return create_client(SUPABASE_URL, SUPABASE_API_KEY)


def login_user(email: str, password: str) -> Dict[str, Any]:
    supabase = get_supabase_client()
    return supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })

supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)


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
        """
        Register a new user with Supabase Auth and create their profile.
        
        Args:
            email: User's email address
            password: User's password
            full_name: Optional full name
            weight_kg: Optional weight in kg
            height_cm: Optional height in cm
            age: Optional age
            gender: Optional gender
            fitness_goal: Optional fitness goal
            
        Returns:
            Dict containing user data and session info or error
        """
        try:
            # Sign up with Supabase Auth
            response = supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "full_name": full_name or ""
                    }
                }
            })
            
            if response.user:
                # Create user profile if additional data provided
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
            else:
                return {
                    "success": False,
                    "error": "Registration failed. Please try again."
                }
                
        except Exception as e:
            error_message = str(e)
            if "already registered" in error_message.lower():
                return {
                    "success": False,
                    "error": "This email is already registered. Please login instead."
                }
            return {
                "success": False,
                "error": f"Registration error: {error_message}"
            }
    
    @staticmethod
    def sign_in(email: str, password: str) -> Dict[str, Any]:
        """
        Sign in an existing user.
        
        Args:
            email: User's email address
            password: User's password
            
        Returns:
            Dict containing user data and session info or error
        """
        try:
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if response.user:
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
            else:
                return {
                    "success": False,
                    "error": "Invalid credentials"
                }
                
        except Exception as e:
            error_message = str(e)
            
            # Check for email not confirmed error
            if "email not confirmed" in error_message.lower():
                return {
                    "success": False,
                    "error": "Email not confirmed. Please check your email inbox (and spam folder) for the confirmation link, or use the 'Resend Confirmation' button below.",
                    "email_not_confirmed": True,
                    "email": email
                }
            
            # Check for invalid credentials
            if "invalid" in error_message.lower() or "credentials" in error_message.lower():
                return {
                    "success": False,
                    "error": "Invalid email or password. Please try again."
                }
            
            return {
                "success": False,
                "error": f"Login error: {error_message}"
            }
    
    @staticmethod
    def sign_out() -> Dict[str, Any]:
        """
        Sign out the current user.
        
        Returns:
            Dict with success status
        """
        try:
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
        """
        Get user information from access token.
        
        Args:
            access_token: JWT access token
            
        Returns:
            User data or None
        """
        try:
            response = supabase.auth.get_user(access_token)
            if response.user:
                return {
                    "id": response.user.id,
                    "email": response.user.email,
                    "full_name": response.user.user_metadata.get("full_name", "")
                }
            return None
        except Exception:
            return None
    
    @staticmethod
    def reset_password(email: str) -> Dict[str, Any]:
        """
        Send password reset email.
        
        Args:
            email: User's email address
            
        Returns:
            Dict with success status
        """
        try:
            supabase.auth.reset_password_email(email)
            return {
                "success": True,
                "message": "Password reset email sent. Please check your inbox."
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error sending reset email: {str(e)}"
            }
    
    @staticmethod
    def resend_confirmation_email(email: str) -> Dict[str, Any]:
        """
        Resend email confirmation link.
        
        Args:
            email: User's email address
            
        Returns:
            Dict with success status
        """
        try:
            # Supabase resends confirmation email when you try to sign up with existing email
            supabase.auth.resend(
                type="signup",
                email=email
            )
            return {
                "success": True,
                "message": "Confirmation email sent! Please check your inbox (and spam folder)."
            }
        except Exception as e:
            error_message = str(e)
            return {
                "success": False,
                "error": f"Error sending confirmation email: {error_message}"
            }
