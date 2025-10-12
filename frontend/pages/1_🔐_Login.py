"""
Login page for NutriFit application.
"""
import os
import sys
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv

# Add parent directory to path to import auth module
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from backend.auth import AuthService

load_dotenv()

st.set_page_config(
    page_title="Login - NutriFit",
    page_icon="🔐",
    layout="centered",
)


def inject_login_styles():
    """Apply custom styling for the login page."""
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

            .login-container {
                background: linear-gradient(135deg, rgba(15, 23, 42, 0.9), rgba(30, 41, 59, 0.95));
                border-radius: 24px;
                padding: 3rem 2.5rem;
                box-shadow: 0 20px 60px rgba(2, 6, 23, 0.6);
                border: 1px solid rgba(148, 163, 184, 0.2);
                backdrop-filter: blur(20px);
                max-width: 480px;
                margin: 2rem auto;
            }

            .login-header {
                text-align: center;
                margin-bottom: 2rem;
            }

            .login-header h1 {
                font-size: 2.5rem;
                font-weight: 700;
                color: #f8fafc;
                margin-bottom: 0.5rem;
                background: linear-gradient(120deg, #22d3ee, #3b82f6);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }

            .login-header p {
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
        </style>
        """,
        unsafe_allow_html=True,
    )


def main():
    inject_login_styles()
    
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
    
    # Initialize session state for email confirmation
    if "show_resend_confirmation" not in st.session_state:
        st.session_state.show_resend_confirmation = False
        st.session_state.unconfirmed_email = None
    
    # Login form
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class="login-header">
            <h1>🥗 Welcome Back</h1>
            <p>Login to your NutriFit account</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    with st.form("login_form"):
        email = st.text_input("📧 Email", placeholder="your.email@example.com")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            submit = st.form_submit_button("🔐 Login", use_container_width=True)
        with col2:
            forgot_password = st.form_submit_button("🔑 Forgot Password?", use_container_width=True)
        
        if submit:
            if not email or not password:
                st.error("⚠️ Please fill in all fields")
            else:
                with st.spinner("Logging in..."):
                    result = AuthService.sign_in(email, password)
                    
                    if result["success"]:
                        # Store user info in session state
                        st.session_state.authenticated = True
                        st.session_state.user = result["user"]
                        st.session_state.access_token = result["session"]["access_token"]
                        st.session_state.show_resend_confirmation = False
                        st.session_state.unconfirmed_email = None
                        st.success("✅ Login successful! Redirecting to main app...")
                        st.balloons()
                        # Redirect to main app page
                        st.switch_page("app.py")
                    else:
                        st.error(f"❌ {result['error']}")
                        
                        # Check if it's an email confirmation error
                        if result.get("email_not_confirmed", False):
                            st.session_state.show_resend_confirmation = True
                            st.session_state.unconfirmed_email = result.get("email", email)
        
        if forgot_password:
            if not email:
                st.error("⚠️ Please enter your email address")
            else:
                with st.spinner("Sending reset email..."):
                    result = AuthService.reset_password(email)
                    if result["success"]:
                        st.success(result["message"])
                    else:
                        st.error(f"❌ {result['error']}")
    
    # Show resend confirmation button if needed
    if st.session_state.show_resend_confirmation and st.session_state.unconfirmed_email:
        st.markdown("---")
        st.info("💡 **Tip:** Check your spam/junk folder if you don't see the confirmation email.")
        
        if st.button("📧 Resend Confirmation Email", use_container_width=True):
            with st.spinner("Sending confirmation email..."):
                result = AuthService.resend_confirmation_email(st.session_state.unconfirmed_email)
                if result["success"]:
                    st.success(result["message"])
                else:
                    st.error(f"❌ {result['error']}")
    
    st.markdown('<div class="divider">OR</div>', unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class="link-text">
            Don't have an account? <a href="/Register">Register here</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()