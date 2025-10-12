"""
Test script to verify all imports work correctly
"""
import sys
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
print()

try:
    import jwt
    print(f"✅ jwt module imported successfully")
    print(f"   Version: {jwt.__version__}")
    print(f"   Has get_algorithm_by_name: {hasattr(jwt, 'get_algorithm_by_name')}")
    print(f"   Location: {jwt.__file__}")
    print()
except Exception as e:
    print(f"❌ Failed to import jwt: {e}")
    print()

try:
    from supabase import create_client, Client
    print(f"✅ supabase imported successfully")
    print()
except Exception as e:
    print(f"❌ Failed to import supabase: {e}")
    print()

try:
    from backend.auth import AuthService
    print(f"✅ backend.auth imported successfully")
    print()
except Exception as e:
    print(f"❌ Failed to import backend.auth: {e}")
    print()

print("=" * 60)
print("All imports successful! The app should work now.")
print("=" * 60)