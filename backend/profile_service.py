"""
Profile service for managing user profiles in Supabase.
Safe for Streamlit Cloud (lazy initialization).
"""

import os
from typing import Optional, Dict, Any
from supabase import create_client, Client


# -------------------------------
# Supabase client (LAZY, SAFE)
# -------------------------------

def get_supabase_client() -> Client:
    """
    Lazily create and return Supabase client.
    Must NOT run at import time.
    """
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_API_KEY")

    if not url or not key:
        raise RuntimeError("Supabase credentials are missing")

    return create_client(url, key)


# -------------------------------
# Profile Service
# -------------------------------

class ProfileService:
    """Service for handling user profile operations."""

    @staticmethod
    def calculate_bmi(weight_kg: float, height_cm: float) -> float:
        height_m = height_cm / 100.0
        return round(weight_kg / (height_m * height_m), 2)

    @staticmethod
    def create_profile(
        user_id: str,
        full_name: str,
        weight_kg: float,
        height_cm: float,
        age: int,
        gender: str,
        fitness_goal: Optional[str] = None
    ) -> Dict[str, Any]:
        try:
            supabase = get_supabase_client()

            bmi = ProfileService.calculate_bmi(weight_kg, height_cm)

            profile_data = {
                "id": user_id,
                "full_name": full_name,
                "weight_kg": weight_kg,
                "height_cm": height_cm,
                "age": age,
                "gender": gender,
                "bmi": bmi,
                "fitness_goal": fitness_goal or "general_health"
            }

            response = supabase.table("user_profiles").insert(profile_data).execute()

            if not response.data:
                return {
                    "success": False,
                    "error": "Failed to create profile"
                }

            return {
                "success": True,
                "profile": response.data[0],
                "message": "Profile created successfully"
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Error creating profile: {str(e)}"
            }

    @staticmethod
    def get_profile(user_id: str) -> Optional[Dict[str, Any]]:
        try:
            supabase = get_supabase_client()

            response = (
                supabase
                .table("user_profiles")
                .select("*")
                .eq("id", user_id)
                .execute()
            )

            if response.data:
                return response.data[0]

            return None

        except Exception:
            return None

    @staticmethod
    def update_profile(
        user_id: str,
        weight_kg: Optional[float] = None,
        height_cm: Optional[float] = None,
        age: Optional[int] = None,
        gender: Optional[str] = None,
        fitness_goal: Optional[str] = None
    ) -> Dict[str, Any]:
        try:
            supabase = get_supabase_client()

            current_profile = ProfileService.get_profile(user_id)
            if not current_profile:
                return {
                    "success": False,
                    "error": "Profile not found"
                }

            update_data: Dict[str, Any] = {}

            if weight_kg is not None:
                update_data["weight_kg"] = weight_kg
            if height_cm is not None:
                update_data["height_cm"] = height_cm
            if age is not None:
                update_data["age"] = age
            if gender is not None:
                update_data["gender"] = gender
            if fitness_goal is not None:
                update_data["fitness_goal"] = fitness_goal

            final_weight = weight_kg if weight_kg is not None else current_profile["weight_kg"]
            final_height = height_cm if height_cm is not None else current_profile["height_cm"]

            if final_weight and final_height:
                update_data["bmi"] = ProfileService.calculate_bmi(
                    final_weight, final_height
                )

            response = (
                supabase
                .table("user_profiles")
                .update(update_data)
                .eq("id", user_id)
                .execute()
            )

            if not response.data:
                return {
                    "success": False,
                    "error": "Failed to update profile"
                }

            return {
                "success": True,
                "profile": response.data[0],
                "message": "Profile updated successfully"
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Error updating profile: {str(e)}"
            }
