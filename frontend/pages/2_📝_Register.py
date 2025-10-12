"""
Registration page for NutriFit application.
"""
import os
import sys
import re
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import requests

# Add parent directory to path to import auth module
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from backend.auth import AuthService
from backend.gemini_service import get_gemini_response

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Register - NutriFit",
    page_icon="📝",
    layout="centered",
)


def inject_register_styles():
    """Apply custom styling for the register page."""
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

            :root {
                color-scheme: dark;
            }

            .stApp {
                background: linear-gradient(130deg, #0f172a, #1e293b, #111827, #0b1120);
                background-size: 400% 400%;
                animation: gradientFlow 24s ease infinite;
                font-family: 'Poppins', sans-serif;
                color: #e2e8f0;
            }

            @keyframes gradientFlow {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }

            .register-container {
                background: linear-gradient(135deg, rgba(15, 23, 42, 0.9), rgba(30, 41, 59, 0.95));
                border-radius: 24px;
                padding: 3rem 2.5rem;
                box-shadow: 0 20px 60px rgba(2, 6, 23, 0.6);
                border: 1px solid rgba(148, 163, 184, 0.2);
                backdrop-filter: blur(20px);
                max-width: 480px;
                margin: 2rem auto;
            }

            .register-header {
                text-align: center;
                margin-bottom: 2rem;
            }

            .register-header h1 {
                font-size: 2.5rem;
                font-weight: 700;
                color: #f8fafc;
                margin-bottom: 0.5rem;
                background: linear-gradient(120deg, #22d3ee, #3b82f6);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }

            .register-header p {
                color: rgba(226, 232, 240, 0.8);
                font-size: 1.1rem;
            }

            .stTextInput > div > div > input {
                background: rgba(15, 23, 42, 0.6) !important;
                border: 1px solid rgba(148, 163, 184, 0.3) !important;
                border-radius: 12px !important;
                color: #f8fafc !important;
                padding: 0.75rem 1rem !important;
                font-size: 1rem !important;
            }

            .stTextInput > div > div > input:focus {
                border-color: #22d3ee !important;
                box-shadow: 0 0 0 2px rgba(34, 211, 238, 0.2) !important;
            }

            .stButton > button {
                background: linear-gradient(120deg, #22d3ee, #3b82f6) !important;
                color: #0f172a !important;
                border: none !important;
                border-radius: 12px !important;
                padding: 0.75rem 2rem !important;
                font-weight: 600 !important;
                font-size: 1.1rem !important;
                width: 100% !important;
                box-shadow: 0 10px 30px rgba(34, 211, 238, 0.3) !important;
                transition: all 0.3s ease !important;
            }

            .stButton > button:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 15px 40px rgba(59, 130, 246, 0.4) !important;
            }

            .divider {
                text-align: center;
                margin: 1.5rem 0;
                color: rgba(226, 232, 240, 0.6);
                position: relative;
            }

            .divider::before,
            .divider::after {
                content: "";
                position: absolute;
                top: 50%;
                width: 40%;
                height: 1px;
                background: rgba(148, 163, 184, 0.3);
            }

            .divider::before {
                left: 0;
            }

            .divider::after {
                right: 0;
            }

            .link-text {
                text-align: center;
                margin-top: 1.5rem;
                color: rgba(226, 232, 240, 0.8);
            }

            .link-text a {
                color: #22d3ee;
                text-decoration: none;
                font-weight: 600;
            }

            .link-text a:hover {
                color: #3b82f6;
                text-decoration: underline;
            }

            /* Label styling */
            .stTextInput > label {
                color: #f8fafc !important;
                font-weight: 500 !important;
                margin-bottom: 0.5rem !important;
            }

            .password-requirements {
                background: rgba(59, 130, 246, 0.1);
                border-left: 3px solid #3b82f6;
                border-radius: 8px;
                padding: 1rem;
                margin: 1rem 0;
                font-size: 0.9rem;
                color: rgba(226, 232, 240, 0.9);
            }

            .password-requirements ul {
                margin: 0.5rem 0 0 0;
                padding-left: 1.5rem;
            }

            .password-requirements li {
                margin: 0.3rem 0;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password: str) -> tuple[bool, str]:
    """
    Validate password strength.
    Returns (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    return True, ""


def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """Calculate BMI from weight and height."""
    if weight_kg > 0 and height_cm > 0:
        height_m = height_cm / 100.0
        return round(weight_kg / (height_m * height_m), 2)
    return 0.0


def get_bmi_category(bmi: float) -> str:
    """Get BMI category and color."""
    if bmi < 18.5:
        return "Underweight", "#3b82f6"
    elif 18.5 <= bmi < 25:
        return "Normal Weight", "#22c55e"
    elif 25 <= bmi < 30:
        return "Overweight", "#f59e0b"
    else:
        return "Obese", "#ef4444"


def get_ai_bmi_advice(bmi: float, age: int, gender: str) -> str:
    """Get AI-powered BMI advice using Gemini."""
    try:
        prompt = f"""
        As a health and nutrition expert, provide brief, encouraging advice (2-3 sentences) for someone with:
        - BMI: {bmi}
        - Age: {age}
        - Gender: {gender}
        
        Focus on positive, actionable health tips. Keep it concise and motivating.
        """
        response = get_gemini_response(prompt)
        return response
    except Exception as e:
        return "Stay healthy with balanced nutrition and regular exercise!"


def main():
    inject_register_styles()
    
    # Check if user is already logged in
    if st.session_state.get("authenticated", False):
        st.success("✅ You are already logged in!")
        st.info("👈 Use the sidebar to navigate to the main app.")
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.access_token = None
            st.rerun()
        return
    
    # Registration form
    st.markdown('<div class="register-container">', unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class="register-header">
            <h1>🥗 Join NutriFit</h1>
            <p>Create your account to get started</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Initialize session state for BMI calculation
    if "reg_weight" not in st.session_state:
        st.session_state.reg_weight = 70.0
    if "reg_height" not in st.session_state:
        st.session_state.reg_height = 170.0
    if "reg_age" not in st.session_state:
        st.session_state.reg_age = 25
    if "reg_gender" not in st.session_state:
        st.session_state.reg_gender = "male"
    
    # Account Information
    st.markdown("### 📋 Account Information")
    full_name = st.text_input("👤 Full Name", placeholder="John Doe")
    email = st.text_input("📧 Email", placeholder="your.email@example.com")
    password = st.text_input("🔒 Password", type="password", placeholder="Create a strong password")
    confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Re-enter your password")
    
    # Password requirements info
    st.markdown(
        """
        <div class="password-requirements">
            <strong>Password Requirements:</strong>
            <ul>
                <li>At least 8 characters long</li>
                <li>Contains uppercase and lowercase letters</li>
                <li>Contains at least one number</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown("---")
    
    # Personal Information
    st.markdown("### 📊 Personal Information")
    st.caption("Help us personalize your nutrition plan")
    
    col1, col2 = st.columns(2)
    with col1:
        weight_kg = st.number_input(
            "⚖️ Weight (kg)", 
            min_value=30.0, 
            max_value=300.0, 
            value=st.session_state.reg_weight,
            step=0.5,
            key="weight_input"
        )
        st.session_state.reg_weight = weight_kg
        
        age = st.number_input(
            "🎂 Age", 
            min_value=13, 
            max_value=120, 
            value=st.session_state.reg_age,
            step=1,
            key="age_input"
        )
        st.session_state.reg_age = age
    
    with col2:
        height_cm = st.number_input(
            "📏 Height (cm)", 
            min_value=100.0, 
            max_value=250.0, 
            value=st.session_state.reg_height,
            step=0.5,
            key="height_input"
        )
        st.session_state.reg_height = height_cm
        
        gender = st.selectbox(
            "⚧️ Gender",
            options=["male", "female", "other", "prefer_not_to_say"],
            index=["male", "female", "other", "prefer_not_to_say"].index(st.session_state.reg_gender),
            key="gender_input"
        )
        st.session_state.reg_gender = gender
    
    # Fitness Goal
    fitness_goal = st.selectbox(
        "🎯 Fitness Goal",
        options=[
            "weight_loss",
            "muscle_gain",
            "maintenance",
            "general_health",
            "athletic_performance"
        ],
        format_func=lambda x: x.replace("_", " ").title(),
        index=3
    )
    
    # Real-time BMI Calculation and AI Advice
    st.markdown("---")
    st.markdown("### 🧮 Your BMI Analysis")
    
    bmi = calculate_bmi(weight_kg, height_cm)
    
    if bmi > 0:
        category, color = get_bmi_category(bmi)
        
        # Display BMI with color
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.metric("BMI", f"{bmi}")
        with col2:
            st.markdown(f"<h3 style='color: {color}; margin-top: 10px;'>{category}</h3>", unsafe_allow_html=True)
        with col3:
            if st.button("🤖 Get AI Advice", key="ai_advice_btn"):
                with st.spinner("Getting personalized advice..."):
                    advice = get_ai_bmi_advice(bmi, age, gender)
                    st.session_state.ai_advice = advice
        
        # Display AI advice if available
        if "ai_advice" in st.session_state:
            st.info(f"💡 **AI Health Tip:** {st.session_state.ai_advice}")
    
    st.markdown("---")
    
    # Submit button
    if st.button("📝 Create Account", use_container_width=True, type="primary"):
        # Validation
        if not full_name or not email or not password or not confirm_password:
            st.error("⚠️ Please fill in all fields")
        elif not validate_email(email):
            st.error("⚠️ Please enter a valid email address")
        elif password != confirm_password:
            st.error("⚠️ Passwords do not match")
        else:
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                st.error(f"⚠️ {error_msg}")
            else:
                with st.spinner("Creating your account..."):
                    result = AuthService.sign_up(
                        email=email,
                        password=password,
                        full_name=full_name,
                        weight_kg=weight_kg,
                        height_cm=height_cm,
                        age=age,
                        gender=gender,
                        fitness_goal=fitness_goal
                    )
                    
                    if result["success"]:
                        st.success(result["message"])
                        st.balloons()
                        
                        # Check if email confirmation is required
                        if result["session"]["access_token"]:
                            # Auto-login if no email confirmation required
                            st.session_state.authenticated = True
                            st.session_state.user = result["user"]
                            st.session_state.access_token = result["session"]["access_token"]
                            st.success("🎉 Account created successfully! Redirecting to main app...")
                            st.balloons()
                            # Redirect to main app page
                            st.switch_page("app.py")
                        else:
                            # Email confirmation required
                            st.info("🎉 Account created successfully!")
                            st.warning("📧 **Important:** Please check your email inbox (and spam folder) to confirm your email address before logging in.")
                            st.info("Once confirmed, you can login using the Login page.")
                    else:
                        st.error(f"❌ {result['error']}")
    
    st.markdown('<div class="divider">OR</div>', unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class="link-text">
            Already have an account? <a href="/Login">Login here</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()