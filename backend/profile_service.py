"""
Profile service for managing user profiles in Supabase.
"""
import os
from typing import Optional, Dict, Any
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

if not SUPABASE_URL or not SUPABASE_API_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_API_KEY must be set in environment variables")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)


class ProfileService:
    """Service for handling user profile operations."""
    
    @staticmethod
    def calculate_bmi(weight_kg: float, height_cm: float) -> float:
        """Calculate BMI from weight and height."""
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
        """
        Create a user profile in the database.
        
        Args:
            user_id: User's UUID from auth
            full_name: User's full name
            weight_kg: Weight in kilograms
            height_cm: Height in centimeters
            age: User's age
            gender: User's gender
            fitness_goal: Optional fitness goal
            
        Returns:
            Dict containing success status and profile data or error
        """
        try:
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
            
            if response.data:
                return {
                    "success": True,
                    "profile": response.data[0],
                    "message": "Profile created successfully"
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to create profile"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Error creating profile: {str(e)}"
            }
    
    @staticmethod
    def get_profile(user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user profile from database.
        
        Args:
            user_id: User's UUID
            
        Returns:
            Profile data or None
        """
        try:
            response = supabase.table("user_profiles").select("*").eq("id", user_id).execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
            
        except Exception as e:
            print(f"Error getting profile: {e}")
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
        """
        Update user profile.
        
        Args:
            user_id: User's UUID
            weight_kg: Optional new weight
            height_cm: Optional new height
            age: Optional new age
            gender: Optional new gender
            fitness_goal: Optional new fitness goal
            
        Returns:
            Dict containing success status and updated profile or error
        """
        try:
            # Get current profile
            current_profile = ProfileService.get_profile(user_id)
            if not current_profile:
                return {
                    "success": False,
                    "error": "Profile not found"
                }
            
            # Build update data
            update_data = {}
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
            
            # Recalculate BMI if weight or height changed
            final_weight = weight_kg if weight_kg is not None else current_profile["weight_kg"]
            final_height = height_cm if height_cm is not None else current_profile["height_cm"]
            
            if final_weight and final_height:
                update_data["bmi"] = ProfileService.calculate_bmi(final_weight, final_height)
            
            # Update timestamp
            update_data["updated_at"] = "now()"
            
            response = supabase.table("user_profiles").update(update_data).eq("id", user_id).execute()
            
            if response.data:
                return {
                    "success": True,
                    "profile": response.data[0],
                    "message": "Profile updated successfully"
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to update profile"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Error updating profile: {str(e)}"
            }