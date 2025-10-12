import os
from datetime import datetime
from typing import Optional, Dict, List
from dataclasses import dataclass

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

_in_memory_meals: List[dict] = []
_in_memory_activities: List[dict] = []


def connect_supabase():
    """Attempt to create a Supabase client if credentials are present.
    Returns None if not configured. This keeps the app runnable without Supabase.
    """
    if not SUPABASE_URL or not SUPABASE_API_KEY:
        return None
    try:
        from supabase import create_client

        client = create_client(SUPABASE_URL, SUPABASE_API_KEY)
        return client
    except Exception:
        return None

# Create a single, reusable client instance when the module is loaded.
_supabase_client = connect_supabase()

def create_meal(meal: dict) -> dict:
    if _supabase_client:
        resp = _supabase_client.table("meals").insert(meal).execute()
        return resp.data[0]
    meal_id = len(_in_memory_meals) + 1
    m = {"id": meal_id, **meal}
    _in_memory_meals.append(m)
    return m


def list_meals() -> List[dict]:
    if _supabase_client:
        resp = _supabase_client.table("meals").select("*").execute()
        return resp.data or []
    return _in_memory_meals


def create_activity(activity: dict) -> dict:
    """Persist a logged activity for the given user."""
    if _supabase_client:
        resp = _supabase_client.table("activities").insert(activity).execute()
        data = resp.data or []
        if data:
            return data[0]
    activity_id = len(_in_memory_activities) + 1
    record = {
        "id": activity_id,
        "timestamp": datetime.utcnow(),
        **activity,
    }
    _in_memory_activities.append(record)
    return record


def list_activities() -> List[dict]:
    """Return activities associated with the specified user."""
    if _supabase_client:
        resp = _supabase_client.table("activities").select("*").execute()
        return resp.data or []
    return _in_memory_activities
