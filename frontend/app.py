import os
import sys

ROOT_DIR = os.path.abspath(".")
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import random
from datetime import datetime
from typing import List, Tuple

from backend.auth import login_user
from backend.profile_service import ProfileService
from backend.gemini_service import generate_diet_plan


import plotly.express as px
import requests
import streamlit as st

# Add parent directory to path to import auth module
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from backend.auth import AuthService

st.set_page_config(
    page_title="NutriFit Wellness Hub",
    page_icon="🥗",
    layout="wide",
)

API_URL = os.getenv("API_URL", "http://localhost:8000")


def inject_global_styles() -> None:
    """Apply custom styling so the UI feels on-brand for NutriFit."""
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

            :root {
                color-scheme: dark;
            }

            html, body {
                overflow-x: hidden;
            }

            .stApp {
                position: relative;
                min-height: 100vh;
                background: linear-gradient(130deg, #0f172a, #1e293b, #111827, #0b1120);
                background-size: 400% 400%;
                animation: gradientFlow 24s ease infinite;
                font-family: 'Poppins', sans-serif;
                color: #e2e8f0;
            }

            .stApp::before {
                content: "";
                position: fixed;
                inset: 0;
                pointer-events: none;
                background: radial-gradient(600px circle at 15% 20%, rgba(14, 165, 233, 0.22), transparent 60%),
                            radial-gradient(400px circle at 85% 15%, rgba(59, 130, 246, 0.2), transparent 55%),
                            radial-gradient(500px circle at 30% 80%, rgba(34, 211, 238, 0.18), transparent 60%);
                animation: pulseGlow 14s ease-in-out infinite alternate;
                z-index: 0;
            }

            @keyframes pulseGlow {
                0% {
                    opacity: 0.55;
                    transform: scale(1);
                }
                50% {
                    opacity: 0.75;
                    transform: scale(1.05);
                }
                100% {
                    opacity: 0.6;
                    transform: scale(1.02);
                }
            }

            @keyframes gradientFlow {
                0% {
                    background-position: 0% 50%;
                }
                50% {
                    background-position: 100% 50%;
                }
                100% {
                    background-position: 0% 50%;
                }
            }

            [data-testid="stSidebar"] {
                background: linear-gradient(200deg, rgba(8, 47, 73, 0.95), rgba(30, 64, 175, 0.85));
                backdrop-filter: blur(14px);
                color: #e2e8f0;
                border-right: 1px solid rgba(148, 163, 184, 0.2);
            }
            [data-testid="stSidebar"] h1,
            [data-testid="stSidebar"] h2,
            [data-testid="stSidebar"] h3,
            [data-testid="stSidebar"] p,
            [data-testid="stSidebar"] li,
            [data-testid="stSidebar"] span,
            [data-testid="stSidebar"] .stCaption,
            [data-testid="stSidebar"] .stMarkdown {
                color: rgba(241, 245, 249, 0.95) !important;
            }
            [data-testid="stSidebar"] [data-testid="stRadio"] label,
            [data-testid="stSidebar"] [data-testid="stRadio"] span {
                color: #f8fafc !important;
            }
            [data-testid="stSidebar"] [data-testid="stRadio"] label div[role="radio"] {
                display: inline-flex;
                align-items: center;
                gap: 0.45rem;
                color: inherit !important;
            }
            [data-testid="stSidebar"] [data-testid="stRadio"] label {
                background: rgba(0, 0, 0, 0.85);
                border-radius: 999px;
                padding: 0.4rem 0.9rem;
                margin-bottom: 0.35rem;
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                box-shadow: 0 12px 26px rgba(15, 23, 42, 0.5);
                border: 1px solid rgba(148, 163, 184, 0.35);
                transition: transform 0.2s ease, background 0.2s ease;
                position: relative;
                overflow: hidden;
            }
            [data-testid="stSidebar"] [data-testid="stRadio"] label::after {
                content: "";
                position: absolute;
                inset: 0;
                background: radial-gradient(circle at top left, rgba(59, 130, 246, 0.4), rgba(14, 116, 144, 0.2));
                opacity: 0;
                transition: opacity 0.2s ease;
            }
            [data-testid="stSidebar"] [data-testid="stRadio"] label:hover::after {
                opacity: 1;
            }
            [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
                background: rgba(15, 23, 42, 0.92);
                transform: translateY(-1px);
            }

            .hero-card {
                background: linear-gradient(135deg, rgba(15, 23, 42, 0.7), rgba(30, 41, 59, 0.85));
                border-radius: 18px;
                padding: 24px 28px;
                box-shadow: 0 14px 34px rgba(2, 6, 23, 0.45);
                margin-bottom: 28px;
                border: 1px solid rgba(148, 163, 184, 0.18);
                backdrop-filter: blur(18px);
            }

            .hero-card h1 {
                font-weight: 700;
                margin-bottom: 0.4rem;
                color: #f8fafc;
            }

            .hero-card p {
                margin: 0;
                font-size: 1.05rem;
                color: rgba(226, 232, 240, 0.85);
            }

            .stat-card {
                background: rgba(15, 23, 42, 0.75);
                border-radius: 16px;
                padding: 18px 22px;
                box-shadow: 0 24px 36px rgba(2, 6, 23, 0.35);
                border: 1px solid rgba(94, 234, 212, 0.12);
                color: #f8fafc;
                backdrop-filter: blur(12px);
            }

            .task-board {
                background: rgba(15, 23, 42, 0.8);
                border-radius: 16px;
                padding: 18px 22px;
                border: 1px solid rgba(148, 163, 184, 0.2);
                box-shadow: 0 20px 32px rgba(2, 6, 23, 0.35);
                backdrop-filter: blur(12px);
                color: #e2e8f0;
            }

            .tag-pill {
                display: inline-block;
                padding: 6px 14px;
                border-radius: 999px;
                background: rgba(56, 189, 248, 0.15);
                color: #60a5fa;
                font-weight: 600;
                margin: 4px 6px 4px 0;
                border: 1px solid rgba(56, 189, 248, 0.4);
            }

            .stButton > button {
                background: linear-gradient(120deg, #22d3ee, #3b82f6);
                color: #0f172a;
                border: none;
                border-radius: 999px;
                padding: 0.6rem 1.3rem;
                font-weight: 600;
                box-shadow: 0 18px 36px rgba(34, 211, 238, 0.35);
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }
            .stButton > button:hover {
                transform: translateY(-1px);
                box-shadow: 0 20px 42px rgba(59, 130, 246, 0.38);
            }

            .stTabs [data-baseweb="tab"] {
                font-size: 1rem;
                padding: 10px 18px;
                color: #e2e8f0;
            }

            .stMarkdown h2 {
                font-weight: 700;
                color: #f8fafc;
            }

            [data-testid="stMetric"] {
                background: rgba(15, 23, 42, 0.7);
                border-radius: 16px;
                padding: 1.2rem;
                border: 1px solid rgba(94, 234, 212, 0.12);
                box-shadow: inset 0 1px 0 rgba(148, 163, 184, 0.12);
            }
            [data-testid="stMetricValue"] {
                color: #38bdf8 !important;
            }
            [data-testid="stMetricDelta"] {
                color: #facc15 !important;
            }

            /* AI Chat Styles */
            .ai-chat-header {
                display: flex;
                align-items: center;
                gap: 1rem;
                background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(34, 211, 238, 0.1));
                border-radius: 16px;
                padding: 1.2rem 1.5rem;
                margin-bottom: 1.5rem;
                border: 1px solid rgba(59, 130, 246, 0.3);
                box-shadow: 0 8px 24px rgba(59, 130, 246, 0.15);
            }

            .ai-avatar {
                font-size: 2.5rem;
                line-height: 1;
            }

            .ai-label {
                font-size: 1.3rem;
                font-weight: 700;
                color: #f8fafc;
                margin: 0;
            }

            .ai-subtext {
                font-size: 0.9rem;
                color: rgba(226, 232, 240, 0.75);
                margin: 0.2rem 0 0 0;
            }

            .ai-badge {
                margin-left: auto;
                background: linear-gradient(120deg, #22d3ee, #3b82f6);
                color: #0f172a;
                padding: 0.4rem 0.9rem;
                border-radius: 999px;
                font-weight: 700;
                font-size: 0.85rem;
                box-shadow: 0 4px 12px rgba(34, 211, 238, 0.3);
            }

            /* Sidebar Logo Styling */
            [data-testid="stSidebar"] [data-testid="stImage"] {
                margin-bottom: 1.5rem;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
            }
            
            [data-testid="stSidebar"] [data-testid="stImage"] img {
                border-radius: 12px;
                background: white;
                padding: 1rem;
            }

            /* Daily Quote Styling */
            [data-testid="stSidebar"] .element-container:has(.stAlert) {
                margin-top: 0.5rem;
                margin-bottom: 0.5rem;
            }
            
            [data-testid="stSidebar"] .stAlert {
                background: linear-gradient(135deg, rgba(34, 211, 238, 0.12), rgba(59, 130, 246, 0.08)) !important;
                border-left: 3px solid #22d3ee !important;
                border-radius: 12px !important;
                padding: 1rem !important;
                font-style: italic;
                font-size: 0.9rem;
                line-height: 1.5;
                box-shadow: 0 4px 12px rgba(34, 211, 238, 0.15);
            }
            
            [data-testid="stSidebar"] .stAlert p {
                color: #f1f5f9 !important;
                margin: 0 !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _get_random_quote() -> str:
    """Return a random fitness/nutrition quote."""
    quotes = [
        "💪 'The only bad workout is the one that didn't happen.' - Unknown",
        "🥗 'Let food be thy medicine and medicine be thy food.' - Hippocrates",
        "🏃 'Take care of your body. It's the only place you have to live.' - Jim Rohn",
        "🌟 'Fitness is not about being better than someone else. It's about being better than you used to be.' - Khloe Kardashian",
        "🍎 'You are what you eat, so don't be fast, cheap, easy, or fake.' - Unknown",
        "💯 'The groundwork for all happiness is good health.' - Leigh Hunt",
        "🔥 'Your body can stand almost anything. It's your mind you have to convince.' - Unknown",
        "🥑 'Eat clean, stay fit, and have a burger to stay sane.' - Gigi Hadid",
        "⚡ 'Strength doesn't come from what you can do. It comes from overcoming the things you once thought you couldn't.' - Rikki Rogers",
        "🌱 'Health is not just about what you're eating. It's also about what you're thinking and saying.' - Unknown",
        "🏋️ 'The only way to keep your health is to eat what you don't want, drink what you don't like, and do what you'd rather not.' - Mark Twain",
        "🎯 'Success starts with self-discipline.' - Unknown",
        "🥤 'Water is the driving force of all nature.' - Leonardo da Vinci",
        "💚 'A healthy outside starts from the inside.' - Robert Urich",
        "🌈 'Don't count calories, make calories count.' - Unknown",
        "🚀 'The body achieves what the mind believes.' - Unknown",
        "🍓 'Eat well, live well, be well.' - Unknown",
        "⭐ 'Your health is an investment, not an expense.' - Unknown",
        "🧘 'Physical fitness is the first requisite of happiness.' - Joseph Pilates",
        "🌞 'Every day is a new opportunity to improve yourself. Take it and make the most of it.' - Unknown"
    ]
    return random.choice(quotes)


def _ensure_session_state() -> None:
    if "weights" not in st.session_state:
        st.session_state.weights = [70.0, 69.5, 69.0, 68.8]
    if "calories" not in st.session_state:
        st.session_state.calories = [2200, 2100, 2000, 2300]
    if "hydration" not in st.session_state:
        st.session_state.hydration = [1.6, 1.8, 2.0, 2.1]
    if "chat_history" not in st.session_state:
        st.session_state.chat_history: List[Tuple[str, str]] = []
    if "daily_goals" not in st.session_state:
        st.session_state.daily_goals = {
            "2L Water": False,
            "30 min Cardio": False,
            "Log Meals": False,
        }
    if "last_recommendation" not in st.session_state:
        st.session_state.last_recommendation = None
    # Generate a new quote only once per session (on login)
    if "daily_quote" not in st.session_state:
        st.session_state.daily_quote = _get_random_quote()
    # Authentication state
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "access_token" not in st.session_state:
        st.session_state.access_token = None


def _render_page_header(title: str, subtitle: str, icon: str) -> None:
    st.markdown(
        f"""
        <div class="hero-card">
            <h1>{icon} {title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def dashboard_page() -> None:
    _render_page_header(
        title="Daily Wellness Snapshot",
        subtitle="Stay on top of your weight, hydration, and energy trends with a quick glance.",
        icon="📊",
    )

    st.caption(f"Last synced {datetime.now():%b %d, %Y %I:%M %p}")
    latest_weight = st.session_state.weights[-1]
    height_cm = st.session_state.get("height_cm", 175)
    height_m = height_cm / 100.0
    bmi = round(latest_weight / (height_m * height_m), 2)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Weight", f"{latest_weight:.1f} kg", f"{latest_weight - st.session_state.weights[0]:+.1f} kg")
    with col2:
        st.metric("BMI", f"{bmi}")
    with col3:
        hydration = st.session_state.hydration[-1]
        st.metric("Hydration", f"{hydration:.1f} L", "Goal: 2.5 L")

    weight_col, cal_col = st.columns((7, 5))
    with weight_col:
        st.markdown("## Weight Trend")
        fig = px.line(
            y=st.session_state.weights,
            x=list(range(len(st.session_state.weights))),
            labels={"x": "Day", "y": "Weight (kg)"},
            markers=True,
        )
        fig.update_layout(
            template="plotly_dark",
            height=320,
            paper_bgcolor="rgba(17, 24, 39, 0.6)",
            plot_bgcolor="rgba(15, 23, 42, 0.42)",
            font=dict(color="#e2e8f0"),
            hoverlabel=dict(bgcolor="#1e293b"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with cal_col:
        st.markdown("## Calorie Balance")
        fig2 = px.bar(
            y=st.session_state.calories,
            x=list(range(len(st.session_state.calories))),
            labels={"x": "Day", "y": "Calories"},
            color=st.session_state.calories,
            color_continuous_scale=["#22d3ee", "#2563eb"],
        )
        fig2.update_layout(
            coloraxis_showscale=False,
            height=320,
            template="plotly_dark",
            paper_bgcolor="rgba(17, 24, 39, 0.6)",
            plot_bgcolor="rgba(15, 23, 42, 0.42)",
            font=dict(color="#e2e8f0"),
            hoverlabel=dict(bgcolor="#1e293b"),
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("## Daily Focus")
    with st.container():
        st.markdown("### Goals Checklist")
        goal_cols = st.columns(len(st.session_state.daily_goals))
        for idx, (goal, status) in enumerate(st.session_state.daily_goals.items()):
            with goal_cols[idx]:
                st.session_state.daily_goals[goal] = st.checkbox(goal, value=status, key=f"goal_{goal}")

    st.markdown("### Quick Tips")
    st.info(
        "Stay hydrated before workouts and balance your meals with lean proteins, complex carbs, and colorful vegetables."
    )


def nutrition_plan_page() -> None:
    _render_page_header(
        title="Personalized Nutrition Plan",
        subtitle="Generate AI-powered nutrition guidance tailored to your wellness goals.",
        icon="🥗",
    )

    # Get user ID from session
    user_id = None
    if st.session_state.get("user"):
        user_id = st.session_state.user.get("id")
    
    # Display user profile info if available
    if user_id:
        try:
            profile_resp = requests.post(
                f"{API_URL}/profile/get",
                json={"user_id": user_id},
                timeout=10
            )
            if profile_resp.status_code == 200:
                profile_data = profile_resp.json()
                if profile_data.get("success"):
                    profile = profile_data.get("profile", {})
                    
                    # Display profile summary
                    st.markdown("### 👤 Your Profile")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Weight", f"{profile.get('weight_kg', 0):.1f} kg")
                    with col2:
                        st.metric("Height", f"{profile.get('height_cm', 0):.0f} cm")
                    with col3:
                        st.metric("BMI", f"{profile.get('bmi', 0):.1f}")
                    with col4:
                        st.metric("Age", f"{profile.get('age', 0)}")
                    
                    st.caption(f"Goal: {profile.get('fitness_goal', 'general_health').replace('_', ' ').title()}")
                    st.markdown("---")
        except Exception as e:
            st.warning("Could not load profile data. Generating general plan.")

    if st.button("🎯 Generate Personalized Plan", use_container_width=True):
        with st.spinner("🤖 AI is designing your personalized nutrition blueprint..."):
            try:
                # Send user_id if available for personalized plan
                payload = {"user_id": user_id} if user_id else {}
                resp = requests.post(
                    f"{API_URL}/recommend",
                    json=payload,
                    timeout=60
                )
                resp.raise_for_status()
                data = resp.json()
                st.session_state.last_recommendation = data
                st.success("✅ Your personalized plan is ready!")
                st.balloons()
            except requests.exceptions.RequestException as exc:
                st.error(f"❌ Could not retrieve recommendations: {exc}")

    recommendation = st.session_state.last_recommendation
    if recommendation:
        nutrition_text = recommendation.get("nutrition", "")
        supplements = recommendation.get("supplements", [])

        st.markdown("### 🥦 Your Personalized Nutrition Strategy")
        st.markdown(
            f"""
            <div style="background: rgba(15, 23, 42, 0.8); 
                        border-radius: 16px; 
                        padding: 20px; 
                        border-left: 4px solid #22d3ee;
                        margin: 20px 0;">
                {nutrition_text}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("### 💊 Recommended Supplements")
        if supplements:
            supplement_tags = "".join(f"<span class='tag-pill'>{item}</span>" for item in supplements)
            st.markdown(supplement_tags, unsafe_allow_html=True)
        else:
            st.info("No additional supplements recommended at this time.")
    else:
        st.info("👆 Click the button above to generate your personalized nutrition plan!")


def fitness_tracker_page() -> None:
    _render_page_header(
        title="Dynamic Fitness Tracker",
        subtitle="Log your sessions and visualize the calorie impact over time.",
        icon="🏃‍♂️",
    )

    col1, col2 = st.columns((4, 5))
    with col1:
        activity = st.text_input("Activity", placeholder="e.g., Morning Run")
        duration = st.number_input("Duration (minutes)", min_value=1, value=30)
        intensity = st.select_slider("Intensity", options=["Low", "Moderate", "High"], value="Moderate")
        if st.button("Log Activity"):
            cal_burn = int(duration * (6 if intensity == "Low" else 8 if intensity == "Moderate" else 11))
            st.success(f"Logged {activity or 'Activity'}, ~{cal_burn} kcal burned!")

    with col2:
        st.markdown("### Weekly Hydration")
        hydration_fig = px.area(
            y=st.session_state.hydration,
            x=list(range(len(st.session_state.hydration))),
            labels={"x": "Day", "y": "Liters"},
            color_discrete_sequence=["#38bdf8"],
        )
        hydration_fig.update_layout(
            template="plotly_dark",
            height=320,
            paper_bgcolor="rgba(17, 24, 39, 0.6)",
            plot_bgcolor="rgba(15, 23, 42, 0.42)",
            font=dict(color="#e2e8f0"),
            hoverlabel=dict(bgcolor="#1e293b"),
        )
        st.plotly_chart(hydration_fig, use_container_width=True)

    st.markdown("### Motivation")
    st.success("Remember: consistency beats intensity. Plan small, regular workouts to build lasting momentum!")


def ai_chat_page() -> None:
    _render_page_header(
        title="AI Wellness Coach",
        subtitle="Chat with your supportive assistant for nutrition and fitness guidance.",
        icon="🤖💬",
    )

    st.caption("Ask anything about meal planning, workouts, or healthy habits.")

    if st.session_state.chat_history:
        last_topic = st.session_state.chat_history[-1][0]
    else:
        last_topic = None

    st.markdown(
        """
        <div class="ai-chat-header">
            <div class="ai-avatar">🤖</div>
            <div>
                <p class="ai-label">NutriFit AI Coach</p>
                <p class="ai-subtext">Focused on nutrition and fitness guidance</p>
            </div>
            <span class="ai-badge">AI</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Suggested prompts as clickable buttons
    suggested_prompts = [
        "🤖 What should I eat before a morning workout?",
        "🤖 Can you help me plan a high-protein dinner?",
        "🤖 How many rest days should I take each week?",
    ]
    
    st.write("**Need inspiration? Try one:**")
    cols = st.columns(len(suggested_prompts))
    
    # Create a variable to store the selected prompt
    selected_prompt = None
    
    for idx, prompt in enumerate(suggested_prompts):
        with cols[idx]:
            if st.button(prompt, key=f"prompt_{idx}", use_container_width=True):
                selected_prompt = prompt.replace("🤖 ", "")  # Remove emoji for cleaner message

    # Display chat history
    for role, text in st.session_state.chat_history:
        avatar = "🤖" if role == "assistant" else "🧑"
        with st.chat_message(role, avatar=avatar):
            st.markdown(text)

    # Handle user input from chat input or button click
    prompt = st.chat_input("Start a conversation with your AI coach")
    
    # Use selected prompt if a button was clicked
    if selected_prompt:
        prompt = selected_prompt
    
    if prompt:
        st.session_state.chat_history.append(("user", prompt))
        with st.chat_message("user", avatar="🧑"):
            st.markdown(prompt)

        messages = [message for _, message in st.session_state.chat_history]
        try:
            resp = requests.post(f"{API_URL}/ai_chat", json={"messages": messages}, timeout=60)
            resp.raise_for_status()
            reply = resp.json().get(
                "reply",
                "I'm here to help whenever you're ready to chat!",
            )
        except requests.exceptions.RequestException as error:
            reply = f"Sorry, I couldn't reach the AI service right now. {error}"

        st.session_state.chat_history.append(("assistant", reply))
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(reply)
        
        # Rerun to show the new messages
        st.rerun()


def medical_report_page() -> None:
    _render_page_header(
        title="Medical Report Insights",
        subtitle="Upload lab reports or scans and let NutriFit extract actionable highlights.",
        icon="🩺",
    )

    uploaded = st.file_uploader("Upload medical report (PNG, JPG, PDF)", type=["png", "jpg", "jpeg", "pdf"])
    if uploaded is not None:
        with st.spinner("Analyzing your document with OCR..."):
            try:
                files = {"file": (uploaded.name, uploaded.getvalue(), uploaded.type)}
                resp = requests.post(f"{API_URL}/ocr", files=files, timeout=120)
                resp.raise_for_status()
                data = resp.json()
                st.subheader("Analysis Summary")
                st.json(data)
            except requests.exceptions.RequestException as exc:
                st.error(f"OCR service unavailable: {exc}")


def main() -> None:
    inject_global_styles()
    _ensure_session_state()

    # Check if user is authenticated
    if not st.session_state.authenticated:
        st.markdown(
            """
            <div style="text-align: center; padding: 4rem 2rem;">
                <h1 style="font-size: 3rem; margin-bottom: 1rem;">🥗 Welcome to NutriFit</h1>
                <p style="font-size: 1.3rem; color: rgba(226, 232, 240, 0.8); margin-bottom: 2rem;">
                    Your personal wellness companion for nutrition and fitness
                </p>
                <p style="font-size: 1.1rem; color: rgba(226, 232, 240, 0.7);">
                    Please login or register to continue
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.info("👈 Use the sidebar to navigate to Login or Register pages")
        
        return

    with st.sidebar:
        # Use absolute path for logo
        logo_path = os.path.join(os.path.dirname(__file__), "nutrifit_logo.jpg")
        if os.path.exists(logo_path):
            st.image(
                logo_path,
                use_container_width=True,
            )
        
        # Display user info
        user_name = st.session_state.user.get("full_name", "User")
        if user_name:
            st.markdown(f"### Welcome back, {user_name}! 👋")
        else:
            st.markdown("### Welcome back, Trailblazer! 👋")
        
        # Display user email
        user_email = st.session_state.user.get("email", "")
        if user_email:
            st.caption(f"📧 {user_email}")
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            AuthService.sign_out()
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.access_token = None
            st.success("Logged out successfully!")
            st.rerun()
        
        # Display the daily quote
        st.markdown("---")
        st.markdown("#### 💭 Daily Inspiration")
        st.info(st.session_state.daily_quote)
        st.markdown("---")

    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Navigate",
        ["Dashboard", "Nutrition Plan", "Fitness Tracker", "AI Chat", "Medical Report"],
        label_visibility="collapsed"
    )

    if page == "Dashboard":
        dashboard_page()
    elif page == "Nutrition Plan":
        nutrition_plan_page()
    elif page == "Fitness Tracker":
        fitness_tracker_page()
    elif page == "AI Chat":
        ai_chat_page()
    elif page == "Medical Report":
        medical_report_page()


if __name__ == "__main__":
    main()
