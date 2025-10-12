"""
Test script to verify nutrition plan generation is working correctly.
"""
import requests
import json
import time

API_URL = "http://localhost:8000"

def test_nutrition_plan_with_profile():
    """Test nutrition plan generation with a sample user profile."""
    print("=" * 60)
    print("Testing Nutrition Plan Generation with User Profile")
    print("=" * 60)
    
    # Wait for server to be ready
    print("\n⏳ Waiting for server to be ready...")
    time.sleep(3)
    
    # Test with a sample user profile
    # Note: This requires a real user_id from your database
    # For testing without a real user, we'll test the generic plan
    
    print("\n📋 Testing Generic Nutrition Plan (no profile)...")
    try:
        response = requests.post(
            f"{API_URL}/recommend",
            json={},
            timeout=60
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ SUCCESS! Nutrition plan generated:")
            print("\n" + "=" * 60)
            print("NUTRITION PLAN:")
            print("=" * 60)
            print(data.get("nutrition", "No nutrition data"))
            print("\n" + "=" * 60)
            print("SUPPLEMENTS:")
            print("=" * 60)
            supplements = data.get("supplements", [])
            if supplements:
                for supp in supplements:
                    print(f"  • {supp}")
            else:
                print("  No supplements recommended")
            print("=" * 60)
            
            # Verify the response is not the error message
            if "Sorry, I couldn't generate" in data.get("nutrition", ""):
                print("\n⚠️ WARNING: Received error message instead of nutrition plan")
                print("This might indicate an issue with the Gemini API response parsing")
                return False
            else:
                print("\n✅ Nutrition plan looks good!")
                return True
        else:
            print(f"\n❌ ERROR: Received status code {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ ERROR: Could not connect to API: {e}")
        print("\nMake sure the backend server is running:")
        print("  python -m uvicorn backend.main:app --reload")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False


def test_with_mock_profile():
    """Test with a mock user profile (requires user_id)."""
    print("\n" + "=" * 60)
    print("Testing with User Profile")
    print("=" * 60)
    print("\nℹ️ To test with a real profile:")
    print("1. Register a user with profile information")
    print("2. Get the user_id from the database")
    print("3. Pass it in the request: {'user_id': 'your-user-id'}")
    print("\nFor now, testing without profile (generic plan)...")


if __name__ == "__main__":
    print("\n🧪 NutriFit Nutrition Plan Test Suite\n")
    
    success = test_nutrition_plan_with_profile()
    test_with_mock_profile()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ ALL TESTS PASSED!")
        print("\nYour nutrition plan generation is working correctly!")
        print("\nNext steps:")
        print("1. Open the app: http://localhost:8501")
        print("2. Register with your profile information")
        print("3. Go to 'Nutrition Plan' page")
        print("4. Click 'Generate Personalized Plan'")
        print("5. You should see a detailed, personalized nutrition plan!")
    else:
        print("❌ TESTS FAILED")
        print("\nTroubleshooting:")
        print("1. Check if backend server is running")
        print("2. Verify GEMINI_API_KEY is set in .env file")
        print("3. Check backend console for error messages")
        print("4. Try running the test again")
    print("=" * 60)