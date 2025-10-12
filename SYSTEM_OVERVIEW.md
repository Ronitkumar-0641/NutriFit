# 🏗️ NutriFit Authentication System Architecture

## 📐 System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           NUTRIFIT APPLICATION                           │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND (Streamlit)                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                        Main App (app.py)                          │  │
│  │  - Authentication Check                                           │  │
│  │  - Session State Management                                       │  │
│  │  - User Profile Display                                           │  │
│  │  - Logout Functionality                                           │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  ┌─────────────────────────┐  ┌─────────────────────────────────────┐  │
│  │  Login Page             │  │  Register Page                      │  │
│  │  (1_🔐_Login.py)        │  │  (2_📝_Register.py)                 │  │
│  │                         │  │                                     │  │
│  │  - Email Input          │  │  - Full Name Input                  │  │
│  │  - Password Input       │  │  - Email Input                      │  │
│  │  - Login Button         │  │  - Password Input                   │  │
│  │  - Forgot Password      │  │  - Confirm Password                 │  │
│  │  - Link to Register     │  │  - Password Validation              │  │
│  │                         │  │  - Register Button                  │  │
│  │                         │  │  - Link to Login                    │  │
│  └─────────────────────────┘  └─────────────────────────────────────┘  │
│                                                                          │
└────────────────────────────┬─────────────────────────────────────────────┘
                             │
                             │ HTTP Requests
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           BACKEND (FastAPI)                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                      API Endpoints (main.py)                      │  │
│  │                                                                   │  │
│  │  POST /auth/signup        - Register new user                    │  │
│  │  POST /auth/signin        - Login existing user                  │  │
│  │  POST /auth/signout       - Logout user                          │  │
│  │  POST /auth/reset-password - Send password reset email           │  │
│  │                                                                   │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                   Auth Service (auth.py)                          │  │
│  │                                                                   │  │
│  │  - sign_up(email, password, full_name)                           │  │
│  │  - sign_in(email, password)                                      │  │
│  │  - sign_out()                                                    │  │
│  │  - get_user(access_token)                                        │  │
│  │  - reset_password(email)                                         │  │
│  │                                                                   │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                          │
└────────────────────────────┬─────────────────────────────────────────────┘
                             │
                             │ Supabase Client
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          SUPABASE (Cloud)                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                        Supabase Auth                              │  │
│  │                                                                   │  │
│  │  - User Management                                               │  │
│  │  - Password Hashing (bcrypt)                                     │  │
│  │  - JWT Token Generation                                          │  │
│  │  - Email Verification                                            │  │
│  │  - Password Reset                                                │  │
│  │                                                                   │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                      PostgreSQL Database                          │  │
│  │                                                                   │  │
│  │  - auth.users table (managed by Supabase)                        │  │
│  │  - User credentials                                              │  │
│  │  - User metadata                                                 │  │
│  │                                                                   │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Authentication Flow Diagram

### Registration Flow

```
┌─────────┐
│  User   │
└────┬────┘
     │
     │ 1. Fills registration form
     │    (name, email, password)
     ▼
┌─────────────────┐
│ Register Page   │
│ (2_📝_Register) │
└────┬────────────┘
     │
     │ 2. Validates input
     │    - Email format
     │    - Password strength
     │    - Password match
     ▼
┌─────────────────┐
│  AuthService    │
│  sign_up()      │
└────┬────────────┘
     │
     │ 3. Sends registration request
     ▼
┌─────────────────┐
│  Supabase Auth  │
└────┬────────────┘
     │
     │ 4. Creates user account
     │    - Hashes password
     │    - Generates JWT tokens
     │    - Sends verification email (optional)
     ▼
┌─────────────────┐
│  Session State  │
│  - authenticated: true
│  - user: {...}
│  - access_token: "..."
└────┬────────────┘
     │
     │ 5. Redirects to main app
     ▼
┌─────────────────┐
│   Main App      │
│   (Dashboard)   │
└─────────────────┘
```

### Login Flow

```
┌─────────┐
│  User   │
└────┬────┘
     │
     │ 1. Enters credentials
     │    (email, password)
     ▼
┌─────────────────┐
│   Login Page    │
│  (1_🔐_Login)   │
└────┬────────────┘
     │
     │ 2. Validates input
     │    - Email not empty
     │    - Password not empty
     ▼
┌─────────────────┐
│  AuthService    │
│  sign_in()      │
└────┬────────────┘
     │
     │ 3. Sends login request
     ▼
┌─────────────────┐
│  Supabase Auth  │
└────┬────────────┘
     │
     │ 4. Verifies credentials
     │    - Checks email exists
     │    - Validates password hash
     │    - Generates JWT tokens
     ▼
┌─────────────────┐
│  Session State  │
│  - authenticated: true
│  - user: {...}
│  - access_token: "..."
└────┬────────────┘
     │
     │ 5. Redirects to main app
     ▼
┌─────────────────┐
│   Main App      │
│   (Dashboard)   │
└─────────────────┘
```

### Logout Flow

```
┌─────────┐
│  User   │
└────┬────┘
     │
     │ 1. Clicks logout button
     ▼
┌─────────────────┐
│   Main App      │
│   Sidebar       │
└────┬────────────┘
     │
     │ 2. Calls logout
     ▼
┌─────────────────┐
│  AuthService    │
│  sign_out()     │
└────┬────────────┘
     │
     │ 3. Invalidates session
     ▼
┌─────────────────┐
│  Supabase Auth  │
└────┬────────────┘
     │
     │ 4. Clears session state
     ▼
┌─────────────────┐
│  Session State  │
│  - authenticated: false
│  - user: null
│  - access_token: null
└────┬────────────┘
     │
     │ 5. Redirects to welcome screen
     ▼
┌─────────────────┐
│ Welcome Screen  │
│ (Login/Register)│
└─────────────────┘
```

---

## 📁 File Structure

```
NutriFit/
│
├── backend/
│   ├── auth.py                 # ✅ Authentication service
│   ├── main.py                 # ✅ API endpoints (with auth routes)
│   ├── db.py                   # Database connection
│   ├── models.py               # Database models
│   ├── schemas.py              # Pydantic schemas
│   └── ...
│
├── frontend/
│   ├── app.py                  # ✅ Main app (with auth protection)
│   ├── pages/
│   │   ├── 1_🔐_Login.py       # ✅ Login page
│   │   ├── 2_📝_Register.py    # ✅ Register page
│   │   └── README.md           # ✅ Page discovery docs
│   └── requirements.txt        # ✅ Frontend dependencies
│
├── .env                        # ✅ Environment variables (Supabase)
├── requirements.txt            # ✅ Backend dependencies
├── test_auth.py                # ✅ Authentication tests
├── start_app.ps1               # ✅ Startup script
├── START_HERE.md               # ✅ Quick start guide
├── AUTHENTICATION_SETUP.md     # ✅ Detailed setup guide
├── AUTHENTICATION_COMPLETE.md  # ✅ Completion summary
└── SYSTEM_OVERVIEW.md          # ✅ This file
```

---

## 🔐 Security Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    Security Layer 1                          │
│                   Frontend Validation                        │
│  - Email format checking                                     │
│  - Password strength requirements                            │
│  - Password confirmation matching                            │
│  - Input sanitization                                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Security Layer 2                          │
│                  Backend Validation                          │
│  - Pydantic model validation                                 │
│  - Request data validation                                   │
│  - Error handling                                            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Security Layer 3                          │
│                  Supabase Auth                               │
│  - Password hashing (bcrypt)                                 │
│  - JWT token generation                                      │
│  - Token validation                                          │
│  - Email verification (optional)                             │
│  - Rate limiting                                             │
│  - SQL injection prevention                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Session State Management

```
┌─────────────────────────────────────────────────────────────┐
│                  Streamlit Session State                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  authenticated: bool                                         │
│  ├─ true  → User is logged in                               │
│  └─ false → User is not logged in                           │
│                                                              │
│  user: dict                                                  │
│  ├─ id: str           (Supabase user ID)                    │
│  ├─ email: str        (User's email)                        │
│  └─ full_name: str    (User's full name)                    │
│                                                              │
│  access_token: str                                           │
│  └─ JWT token for authenticated API requests                │
│                                                              │
│  Other app state:                                            │
│  ├─ weights: list                                            │
│  ├─ calories: list                                           │
│  ├─ hydration: list                                          │
│  ├─ chat_history: list                                       │
│  ├─ daily_goals: dict                                        │
│  ├─ last_recommendation: dict                                │
│  └─ daily_quote: str                                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow

### User Registration

```
User Input → Frontend Validation → AuthService → Supabase → Database
    ↓              ↓                    ↓           ↓          ↓
  Form         Password            sign_up()    Create     Store
  Data         Strength                         User       User
               Check                            Hash       Data
                                               Password
                                               Generate
                                               Tokens
                                                  ↓
                                            Return to
                                            Frontend
                                                  ↓
                                            Store in
                                            Session
                                            State
                                                  ↓
                                            Redirect
                                            to Main
                                            App
```

### User Login

```
User Input → Frontend Validation → AuthService → Supabase → Database
    ↓              ↓                    ↓           ↓          ↓
  Email        Check Empty          sign_in()    Verify     Query
  Password     Fields                            Password   User
                                                 Hash       Data
                                                 Generate
                                                 Tokens
                                                    ↓
                                              Return to
                                              Frontend
                                                    ↓
                                              Store in
                                              Session
                                              State
                                                    ↓
                                              Redirect
                                              to Main
                                              App
```

### Protected Page Access

```
User Navigates → Check Session State → Authenticated?
                                            ↓
                                    ┌───────┴───────┐
                                   YES             NO
                                    ↓               ↓
                              Show Content    Show Welcome
                              + User Info     + Login Link
                              + Logout Btn    + Register Link
```

---

## 🎨 UI Component Hierarchy

```
Main App (app.py)
│
├─ Authentication Check
│  ├─ If NOT authenticated:
│  │  └─ Welcome Screen
│  │     ├─ Welcome Message
│  │     └─ Navigation Prompt
│  │
│  └─ If authenticated:
│     ├─ Sidebar
│     │  ├─ Logo
│     │  ├─ User Profile
│     │  │  ├─ Welcome Message
│     │  │  └─ Email Display
│     │  ├─ Logout Button
│     │  ├─ Daily Quote
│     │  └─ Navigation Menu
│     │
│     └─ Main Content
│        ├─ Dashboard
│        ├─ Nutrition Plan
│        ├─ Fitness Tracker
│        ├─ AI Chat
│        └─ Medical Report
│
Login Page (1_🔐_Login.py)
│
├─ Login Container
│  ├─ Header
│  │  ├─ Title
│  │  └─ Subtitle
│  │
│  ├─ Login Form
│  │  ├─ Email Input
│  │  ├─ Password Input
│  │  ├─ Login Button
│  │  └─ Forgot Password Button
│  │
│  └─ Footer
│     └─ Register Link
│
Register Page (2_📝_Register.py)
│
└─ Register Container
   ├─ Header
   │  ├─ Title
   │  └─ Subtitle
   │
   ├─ Register Form
   │  ├─ Full Name Input
   │  ├─ Email Input
   │  ├─ Password Input
   │  ├─ Confirm Password Input
   │  ├─ Password Requirements
   │  └─ Register Button
   │
   └─ Footer
      └─ Login Link
```

---

## 🚀 Deployment Considerations

### Environment Variables
```env
# Required for authentication
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_API_KEY=your-anon-key

# Optional
API_URL=http://localhost:8000
JWT_SECRET=your-secret-key
```

### Supabase Configuration
- Email confirmation (optional)
- Password reset redirect URL
- JWT expiration time
- Rate limiting settings

### Security Best Practices
- ✅ Use HTTPS in production
- ✅ Set secure CORS policies
- ✅ Enable rate limiting
- ✅ Use environment variables for secrets
- ✅ Implement token refresh logic
- ✅ Add CSRF protection
- ✅ Enable email verification

---

## 📊 Database Schema (Supabase)

```sql
-- Managed by Supabase Auth
auth.users
├─ id (uuid, primary key)
├─ email (text, unique)
├─ encrypted_password (text)
├─ email_confirmed_at (timestamp)
├─ created_at (timestamp)
├─ updated_at (timestamp)
└─ raw_user_meta_data (jsonb)
   └─ full_name (text)

-- You can extend with custom tables
public.user_profiles
├─ id (uuid, foreign key → auth.users.id)
├─ full_name (text)
├─ avatar_url (text)
├─ preferences (jsonb)
└─ created_at (timestamp)

public.user_nutrition_plans
├─ id (uuid, primary key)
├─ user_id (uuid, foreign key → auth.users.id)
├─ plan_data (jsonb)
├─ created_at (timestamp)
└─ updated_at (timestamp)

public.user_fitness_logs
├─ id (uuid, primary key)
├─ user_id (uuid, foreign key → auth.users.id)
├─ activity (text)
├─ duration (integer)
├─ calories_burned (integer)
└─ logged_at (timestamp)
```

---

## 🎉 Summary

Your NutriFit application now has a **complete, production-ready authentication system** with:

- ✅ Secure user registration and login
- ✅ Beautiful, modern UI
- ✅ Session management
- ✅ Password reset functionality
- ✅ Protected routes
- ✅ User profile display
- ✅ Supabase integration
- ✅ REST API endpoints
- ✅ Comprehensive documentation

**Ready to launch!** 🚀