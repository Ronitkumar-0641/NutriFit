import os
import sys
import random
from datetime import datetime
from typing import List, Tuple

import streamlit as st
import plotly.express as px

# --- Path fix ---
ROOT_DIR = os.path.abspath(".")
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# --- Backend imports (MATCH FIXED BACKEND) ---
from backend.auth import AuthService
from backend.profile_service import ProfileService
from backend.gemini_service import get_gemini_response


st.set_page_config(
    page_title="NutriFit Wellness Hub",
    page_icon="🥗",
    layout="wide",
)

# -------------------------------
# SESSION STATE
# -------------------------------

def _ensure_session_state():
    defaults = {
        "weights": [70.0, 69.5, 69.0, 68.8],
        "calories": [2200, 2100, 2000, 2300],
        "hydration": [1.6, 1.8, 2.0, 2.1],
        "chat_history": [],
        "daily_goals": {
            "2L Water": False,
            "30 min Cardio": False,
            "Log Meals": False,
        },
        "authenticated": False,
        "user": None,
        "access_token": None,
        "daily_quote": random.choice([
            "💪 The only bad workout is the one that didn’t happen.",
            "🥗 Let food be thy medicine.",
            "🏃 Take care of your body. It's the only place you have to live.",
            "🌟 Fitness is about being better than yesterday.",
        ])
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# -------------------------------
# UI HELPERS
# -------------------------------

def _render_page_header(title, subtitle, icon):
    st.markdown(
        f"""
        <div style="background:#0f172a;padding:20px;border-radius:16px;">
            <h1>{icon} {title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -------------------------------
# DASHBOARD
# -------------------------------

def dashboard_page():
    _render_page_header(
        "Daily Wellness Snapshot",
        "Track your health trends at a glance.",
        "📊"
    )

    latest_weight = st.session_state.weights[-1]
    height_cm = st.session_state.user.get("height_cm", 175) if st.session_state.user else 175
    bmi = round(latest_weight / ((height_cm / 100) ** 2), 2)

    c1, c2, c3 = st.columns(3)
    c1.metric("Weight", f"{latest_weight} kg")
    c2.metric("BMI", bmi)
    c3.metric("Hydration", f"{st.session_state.hydration[-1]} L")

    fig = px.line(y=st.session_state.weights, title="Weight Trend")
    st.plotly_chart(fig, use_container_width=True)


# -------------------------------
# NUTRITION PLAN (GEMINI)
# -------------------------------

def nutrition_plan_page():
    _render_page_header(
        "Personalized Nutrition Plan",
        "AI-powered diet guidance",
        "🥗"
    )

    if st.button("Generate Nutrition Plan"):
        with st.spinner("Generating plan..."):
            prompt = "Create a healthy balanced diet plan."
            response = get_gemini_response(prompt)
            st.success("Plan ready!")
            st.markdown(response)


# -------------------------------
# AI CHAT (GEMINI)
# -------------------------------

def ai_chat_page():
    _render_page_header(
        "AI Wellness Coach",
        "Chat with your nutrition assistant",
        "🤖"
    )

    for role, msg in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(msg)

    prompt = st.chat_input("Ask NutriFit AI...")
    if prompt:
        st.session_state.chat_history.append(("user", prompt))
        reply = get_gemini_response(prompt)
        st.session_state.chat_history.append(("assistant", reply))
        st.rerun()


# -------------------------------
# FITNESS TRACKER
# -------------------------------

def fitness_tracker_page():
    _render_page_header(
        "Fitness Tracker",
        "Log activities and hydration",
        "🏃"
    )
    st.info("Coming soon 🚧")


# -------------------------------
# MAIN
# -------------------------------

def main():
    _ensure_session_state()

    if not st.session_state.authenticated:
        st.title("🥗 Welcome to NutriFit")
        st.info("Please login or register to continue.")
        return

    with st.sidebar:
        st.markdown(f"### 👋 Welcome {st.session_state.user.get('full_name','User')}")
        if st.button("Logout"):
            AuthService.sign_out()
            st.session_state.clear()
            st.rerun()

        page = st.radio(
            "Navigate",
            ["Dashboard", "Nutrition Plan", "Fitness Tracker", "AI Chat"],
        )

    if page == "Dashboard":
        dashboard_page()
    elif page == "Nutrition Plan":
        nutrition_plan_page()
    elif page == "Fitness Tracker":
        fitness_tracker_page()
    elif page == "AI Chat":
        ai_chat_page()


if __name__ == "__main__":
    main()
