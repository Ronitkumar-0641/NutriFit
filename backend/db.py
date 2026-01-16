"""
Database helpers for meals and activities.
Safe for Streamlit Cloud (lazy Supabase initialization).
"""

import os
from datetime import datetime
from typing import List, Dict, Optional

# In-memory fallback storage
_in_memory_meals: List[Dict] = []
_in_memory_activities: List[Dict] = []


# -------------------------------
# Supabase client (LAZY, SAFE)
# -------------------------------

def get_supabase_client():
    """
    Lazily create Supabase client.
    Returns None if credentials are missing or client cannot be created.
    """
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_API_KEY")

    if not url or not key:
        return None

    try:
        from supabase import create_client
        return create_client(url, key)
    except Exception:
        return None


# -------------------------------
# Meals
# -------------------------------

def create_meal(meal: Dict) -> Dict:
    supabase = get_supabase_client()

    if supabase:
        resp = supabase.table("meals").insert(meal).execute()
        if resp.data:
            return resp.data[0]

    meal_id = len(_in_memory_meals) + 1
    record = {"id": meal_id, **meal}
    _in_memory_meals.append(record)
    return record


def list_meals() -> List[Dict]:
    supabase = get_supabase_client()

    if supabase:
        resp = supabase.table("meals").select("*").execute()
        return resp.data or []

    return list(_in_memory_meals)


# -------------------------------
# Activities
# -------------------------------

def create_activity(activity: Dict) -> Dict:
    supabase = get_supabase_client()

    if supabase:
        resp = supabase.table("activities").insert(activity).execute()
        if resp.data:
            return resp.data[0]

    activity_id = len(_in_memory_activities) + 1
    record = {
        "id": activity_id,
        "timestamp": datetime.utcnow(),
        **activity,
    }
    _in_memory_activities.append(record)
    return record


def list_activities() -> List[Dict]:
    supabase = get_supabase_client()

    if supabase:
        resp = supabase.table("activities").select("*").execute()
        return resp.data or []

    return list(_in_memory_activities)
