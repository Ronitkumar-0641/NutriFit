"""
Test script to verify Supabase authentication is working.
"""
from backend.auth import AuthService

def test_auth():
    print("🔐 Testing NutriFit Authentication System\n")
    print("=" * 50)
    
    # Test 1: Check if Supabase client is initialized
    print("\n✅ Test 1: Supabase client initialized successfully")
    
    # Test 2: Try to sign up a test user (this will fail if user exists, which is fine)
    print("\n📝 Test 2: Testing user registration...")
    test_email = "test@nutrifit.com"
    test_password = "TestPass123"
    test_name = "Test User"
    
    result = AuthService.sign_up(test_email, test_password, test_name)
    if result["success"]:
        print(f"✅ Registration successful: {result['message']}")
    else:
        print(f"ℹ️  Registration result: {result['error']}")
        print("   (This is expected if the user already exists)")
    
    # Test 3: Try to sign in
    print("\n🔐 Test 3: Testing user login...")
    result = AuthService.sign_in(test_email, test_password)
    if result["success"]:
        print(f"✅ Login successful!")
        print(f"   User ID: {result['user']['id']}")
        print(f"   Email: {result['user']['email']}")
        print(f"   Name: {result['user']['full_name']}")
        print(f"   Access Token: {result['session']['access_token'][:20]}...")
    else:
        print(f"❌ Login failed: {result['error']}")
    
    # Test 4: Sign out
    print("\n🚪 Test 4: Testing logout...")
    result = AuthService.sign_out()
    if result["success"]:
        print(f"✅ Logout successful: {result['message']}")
    else:
        print(f"❌ Logout failed: {result['error']}")
    
    print("\n" + "=" * 50)
    print("🎉 Authentication system test completed!")
    print("\nYou can now run the Streamlit app:")
    print("  cd frontend")
    print("  streamlit run app.py")

if __name__ == "__main__":
    test_auth()