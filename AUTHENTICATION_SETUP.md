# NutriFit Authentication Setup Guide

This guide explains how to set up and use the authentication system in NutriFit using Supabase.

## 🎯 Overview

NutriFit now includes a complete authentication system with:
- User registration with email and password
- User login with session management
- Password reset functionality
- Protected routes (main app requires authentication)
- User profile display
- Logout functionality

## 🔧 Setup

### 1. Supabase Configuration

Your Supabase credentials are already configured in the `.env` file:

```env
SUPABASE_URL="https://tereffehsopjmyxuhnwk.supabase.co"
SUPABASE_API_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 2. Supabase Auth Setup

Make sure your Supabase project has Auth enabled:

1. Go to your Supabase dashboard: https://app.supabase.com
2. Navigate to Authentication > Settings
3. Ensure "Enable Email Confirmations" is configured as needed
4. Configure email templates if desired

### 3. Install Dependencies

Install the required packages:

```bash
# Activate your virtual environment
.\venv\Scripts\activate

# Install frontend dependencies
pip install -r frontend/requirements.txt

# Install backend dependencies
pip install -r requirements.txt
```

## 🚀 Running the Application

### Start the Backend API

```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Start the Frontend

```bash
cd frontend
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📱 Using the Authentication System

### Registration

1. Navigate to the **📝 Register** page from the sidebar
2. Fill in your details:
   - Full Name
   - Email address
   - Password (must meet requirements)
   - Confirm Password
3. Click "Create Account"
4. You'll be automatically logged in after successful registration

### Login

1. Navigate to the **🔐 Login** page from the sidebar
2. Enter your email and password
3. Click "Login"
4. You'll be redirected to the main app

### Password Reset

1. On the Login page, click "Forgot Password?"
2. Enter your email address
3. Check your email for the reset link
4. Follow the link to reset your password

### Logout

1. Once logged in, you'll see a "🚪 Logout" button in the sidebar
2. Click it to log out
3. You'll be redirected to the welcome screen

## 🔒 Password Requirements

Passwords must meet the following criteria:
- At least 8 characters long
- Contains at least one uppercase letter
- Contains at least one lowercase letter
- Contains at least one number

## 📁 File Structure

```
NutriFit/
├── backend/
│   ├── auth.py              # Authentication service with Supabase
│   └── main.py              # FastAPI backend
├── frontend/
│   ├── app.py               # Main Streamlit app (protected)
│   └── pages/
│       ├── 1_🔐_Login.py    # Login page
│       └── 2_📝_Register.py # Registration page
└── .env                     # Environment variables (Supabase credentials)
```

## 🔑 Key Features

### Backend (`backend/auth.py`)

The `AuthService` class provides:
- `sign_up(email, password, full_name)` - Register new users
- `sign_in(email, password)` - Authenticate users
- `sign_out()` - Log out users
- `get_user(access_token)` - Get user info from token
- `reset_password(email)` - Send password reset email

### Frontend Pages

**Main App (`app.py`)**
- Checks authentication status
- Shows welcome screen if not authenticated
- Displays user info and logout button when authenticated
- Protects all main features

**Login Page (`1_🔐_Login.py`)**
- Email and password login
- Password reset functionality
- Link to registration page
- Beautiful gradient UI

**Register Page (`2_📝_Register.py`)**
- User registration form
- Password validation
- Email validation
- Auto-login after registration
- Link to login page

## 🎨 UI Features

Both login and register pages feature:
- Modern gradient backgrounds
- Smooth animations
- Responsive design
- Clear error messages
- Success notifications with balloons 🎈
- Password strength requirements
- Consistent branding with NutriFit theme

## 🔐 Session Management

User sessions are managed using Streamlit's session state:
- `st.session_state.authenticated` - Boolean flag
- `st.session_state.user` - User information (id, email, full_name)
- `st.session_state.access_token` - JWT access token

## 🐛 Troubleshooting

### "Module not found" errors
Make sure you've installed all dependencies:
```bash
pip install -r frontend/requirements.txt
pip install -r requirements.txt
```

### Supabase connection errors
- Verify your `.env` file has the correct credentials
- Check that your Supabase project is active
- Ensure Auth is enabled in your Supabase dashboard

### Login/Registration not working
- Check the browser console for errors
- Verify the backend API is running
- Check Supabase Auth logs in the dashboard

## 🔄 Next Steps

You can extend the authentication system by:
1. Adding social login (Google, GitHub, etc.)
2. Implementing role-based access control
3. Adding user profile editing
4. Creating a user settings page
5. Adding two-factor authentication
6. Storing user-specific data in Supabase database

## 📚 Resources

- [Supabase Auth Documentation](https://supabase.com/docs/guides/auth)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Session State](https://docs.streamlit.io/library/api-reference/session-state)

## 🎉 Success!

Your NutriFit app now has a complete authentication system! Users can register, login, and access personalized features securely.