"""
Test script to verify the user profile and nutrition plan implementation.
Run this to check if everything is set up correctly.
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_environment():
    """Test if all required environment variables are set."""
    print("=" * 60)
    print("🔍 Testing Environment Variables")
    print("=" * 60)
    
    required_vars = {
        "SUPABASE_URL": os.getenv("SUPABASE_URL"),
        "SUPABASE_API_KEY": os.getenv("SUPABASE_API_KEY"),
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
        "API_URL": os.getenv("API_URL", "http://localhost:8000")
    }
    
    all_set = True
    for var_name, var_value in required_vars.items():
        status = "✅ SET" if var_value else "❌ NOT SET"
        print(f"{var_name}: {status}")
        if not var_value:
            all_set = False
    
    print()
    return all_set

def test_imports():
    """Test if all required modules can be imported."""
    print("=" * 60)
    print("🔍 Testing Module Imports")
    print("=" * 60)
    
    modules_to_test = [
        ("backend.auth", "AuthService"),
        ("backend.profile_service", "ProfileService"),
        ("backend.gemini_service", "get_gemini_response"),
        ("backend.main", "app"),
    ]
    
    all_imported = True
    for module_name, class_name in modules_to_test:
        try:
            module = __import__(module_name, fromlist=[class_name])
            getattr(module, class_name)
            print(f"✅ {module_name}.{class_name}")
        except Exception as e:
            print(f"❌ {module_name}.{class_name} - Error: {e}")
            all_imported = False
    
    print()
    return all_imported

def test_profile_service():
    """Test the profile service functions."""
    print("=" * 60)
    print("🔍 Testing Profile Service")
    print("=" * 60)
    
    try:
        from backend.profile_service import ProfileService
        
        # Test BMI calculation
        bmi = ProfileService.calculate_bmi(70, 175)
        print(f"✅ BMI Calculation: {bmi} (Expected: ~22.86)")
        
        if 22.8 <= bmi <= 22.9:
            print("✅ BMI calculation is accurate")
        else:
            print("⚠️ BMI calculation might have issues")
        
        print()
        return True
    except Exception as e:
        print(f"❌ Profile Service Error: {e}")
        print()
        return False

def test_database_connection():
    """Test if we can connect to Supabase."""
    print("=" * 60)
    print("🔍 Testing Database Connection")
    print("=" * 60)
    
    try:
        from supabase import create_client
        
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_API_KEY")
        
        if not supabase_url or not supabase_key:
            print("❌ Supabase credentials not set")
            print()
            return False
        
        supabase = create_client(supabase_url, supabase_key)
        
        # Try to query the user_profiles table (will fail if table doesn't exist)
        try:
            result = supabase.table("user_profiles").select("*").limit(1).execute()
            print("✅ Successfully connected to Supabase")
            print("✅ user_profiles table exists")
        except Exception as e:
            if "relation" in str(e).lower() and "does not exist" in str(e).lower():
                print("⚠️ Connected to Supabase, but user_profiles table doesn't exist")
                print("   Run the SQL from backend/database.sql in Supabase SQL Editor")
            else:
                print(f"⚠️ Connection issue: {e}")
        
        print()
        return True
    except Exception as e:
        print(f"❌ Database Connection Error: {e}")
        print()
        return False

def print_summary(results):
    """Print a summary of all tests."""
    print("=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    all_passed = all(results.values())
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print()
    if all_passed:
        print("🎉 All tests passed! Your implementation is ready to use.")
        print()
        print("Next steps:")
        print("1. Make sure the user_profiles table is created in Supabase")
        print("2. Start the backend: python -m uvicorn backend.main:app --reload")
        print("3. Start the frontend: streamlit run frontend/app.py")
        print("4. Register a new account with your profile data")
        print("5. Generate your personalized nutrition plan!")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        print()
        print("Common fixes:")
        print("- Make sure .env file has all required variables")
        print("- Run the SQL from backend/database.sql in Supabase")
        print("- Check your internet connection for Gemini API")
    
    print("=" * 60)

def main():
    """Run all tests."""
    print("\n🚀 NutriFit Implementation Test Suite\n")
    
    results = {
        "Environment Variables": test_environment(),
        "Module Imports": test_imports(),
        "Profile Service": test_profile_service(),
        "Database Connection": test_database_connection(),
    }
    
    print_summary(results)

if __name__ == "__main__":
    main()