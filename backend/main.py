from typing import Any, Dict, Optional
import json
from fastapi import (
    FastAPI,
    File,
    UploadFile,
    HTTPException,
    Body,
)
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .health_report import process_health_document_sync
from .schemas import ChatRequest, RecommendResponse
from .gemini_service import get_gemini_response, extract_json_from_response
from .auth import AuthService
from .profile_service import ProfileService

app = FastAPI(title="NutriFit API", version="0.1.0")

# Allow the local Streamlit frontend to communicate with this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://127.0.0.1",
        "http://localhost:8501",
        "http://127.0.0.1:8501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root() -> Dict[str, str]:
    return {"message": "NutriFit API is running"}


@app.get("/health")
def health_check() -> Dict[str, str]:
    return {"status": "ok"}


# Authentication Models
class SignUpRequest(BaseModel):
    email: str
    password: str
    full_name: str = ""
    weight_kg: float = None
    height_cm: float = None
    age: int = None
    gender: str = None
    fitness_goal: str = None


class SignInRequest(BaseModel):
    email: str
    password: str


class PasswordResetRequest(BaseModel):
    email: str


# Profile Models
class ProfileRequest(BaseModel):
    user_id: str


class RecommendRequest(BaseModel):
    user_id: Optional[str] = None


# Authentication Endpoints
@app.post("/auth/signup")
def signup(request: SignUpRequest) -> Dict[str, Any]:
    """Register a new user."""
    result = AuthService.sign_up(
        email=request.email,
        password=request.password,
        full_name=request.full_name,
        weight_kg=request.weight_kg,
        height_cm=request.height_cm,
        age=request.age,
        gender=request.gender,
        fitness_goal=request.fitness_goal
    )
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.post("/auth/signin")
def signin(request: SignInRequest) -> Dict[str, Any]:
    """Sign in an existing user."""
    result = AuthService.sign_in(request.email, request.password)
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["error"])
    return result


@app.post("/auth/signout")
def signout() -> Dict[str, Any]:
    """Sign out the current user."""
    result = AuthService.sign_out()
    return result


@app.post("/auth/reset-password")
def reset_password(request: PasswordResetRequest) -> Dict[str, Any]:
    """Send password reset email."""
    result = AuthService.reset_password(request.email)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.post("/profile/get")
def get_profile(request: ProfileRequest) -> Dict[str, Any]:
    """Get user profile."""
    profile = ProfileService.get_profile(request.user_id)
    if profile:
        return {"success": True, "profile": profile}
    else:
        raise HTTPException(status_code=404, detail="Profile not found")


@app.post("/recommend", response_model=RecommendResponse)
def recommend_plan(request: Optional[RecommendRequest] = Body(None)) -> RecommendResponse:
    """Generate personalized nutrition plan based on user profile."""
    
    # Get user profile if user_id provided
    user_profile = None
    if request and request.user_id:
        user_profile = ProfileService.get_profile(request.user_id)
    
    # Build personalized prompt
    if user_profile:
        bmi = user_profile.get("bmi", 0)
        age = user_profile.get("age", 0)
        gender = user_profile.get("gender", "")
        weight = user_profile.get("weight_kg", 0)
        height = user_profile.get("height_cm", 0)
        fitness_goal = user_profile.get("fitness_goal", "general_health")
        
        # Determine BMI category
        if bmi < 18.5:
            bmi_category = "underweight"
        elif 18.5 <= bmi < 25:
            bmi_category = "normal weight"
        elif 25 <= bmi < 30:
            bmi_category = "overweight"
        else:
            bmi_category = "obese"
        
        prompt = f"""
        As a nutrition expert, create a highly personalized nutrition plan for a user with the following profile:
        
        - Age: {age} years
        - Gender: {gender}
        - Weight: {weight} kg
        - Height: {height} cm
        - BMI: {bmi} ({bmi_category})
        - Fitness Goal: {fitness_goal}
        
        Based on this profile, provide:
        1. A detailed, personalized nutrition strategy that addresses their BMI category and fitness goal
        2. Specific calorie recommendations
        3. Macronutrient breakdown (protein, carbs, fats)
        4. Meal timing suggestions
        5. Hydration recommendations
        
        IMPORTANT: You MUST respond with ONLY a valid JSON object. Do not include any markdown formatting, code blocks, or additional text.
        
        Return ONLY this JSON structure:
        {{
            "nutrition": "Based on your profile as a {age}-year-old {gender} with a BMI of {bmi} ({bmi_category}) and a goal of {fitness_goal}, here is your personalized nutrition plan: [Include detailed calorie recommendations, macronutrient breakdown (protein/carbs/fats percentages), meal timing, and hydration advice. Make it comprehensive and specific to their profile.]",
            "supplements": ["Supplement 1", "Supplement 2", "Supplement 3"]
        }}
        
        Make the nutrition text detailed (at least 200 words) and highly personalized to their specific BMI category and fitness goal.
        """
    else:
        # Generic plan if no profile
        prompt = """
        As a nutrition expert, create a general nutrition plan for maintaining good health.
        
        IMPORTANT: You MUST respond with ONLY a valid JSON object. Do not include any markdown formatting, code blocks, or additional text.
        
        Return ONLY this JSON structure:
        {
            "nutrition": "Here is a comprehensive general nutrition plan for maintaining good health: [Include calorie recommendations, macronutrient breakdown, meal timing, hydration advice. Make it detailed and actionable.]",
            "supplements": ["Vitamin D", "Omega-3", "Multivitamin"]
        }
        
        Make the nutrition text detailed (at least 150 words) with specific, actionable advice.
        """
    
    response_text = get_gemini_response(prompt)
    
    # Extract JSON from response (handles markdown code blocks)
    json_text = extract_json_from_response(response_text)
    
    try:
        response_json = json.loads(json_text)
        
        # Validate that we have the required keys
        if "nutrition" not in response_json:
            response_json["nutrition"] = "Unable to generate nutrition plan."
        if "supplements" not in response_json:
            response_json["supplements"] = []
        
        # Add personalized food suggestions if profile exists
        if user_profile:
            bmi = user_profile.get("bmi", 0)
            if bmi < 18.5:
                food_suggestions = "\n\n**Recommended Foods (for healthy weight gain):**\n- Breakfast: Whole grain toast with peanut butter, banana, and full-fat milk\n- Lunch: Chicken breast with brown rice and avocado\n- Dinner: Salmon with sweet potato and olive oil dressing\n- Snacks: Trail mix, protein smoothies, cheese and crackers"
            elif bmi >= 25:
                food_suggestions = "\n\n**Recommended Foods (for healthy weight management):**\n- Breakfast: Oatmeal with berries and chia seeds\n- Lunch: Grilled chicken salad with mixed greens and light dressing\n- Dinner: Baked fish with steamed vegetables and quinoa\n- Snacks: Greek yogurt, raw vegetables with hummus, apple slices"
            else:
                food_suggestions = "\n\n**Recommended Foods (for maintenance):**\n- Breakfast: Eggs with whole grain toast and fruit\n- Lunch: Turkey wrap with vegetables\n- Dinner: Lean protein with brown rice and roasted vegetables\n- Snacks: Nuts, fruit, Greek yogurt"
        else:
            food_suggestions = "\n\n**General Food Suggestions:**\n- Breakfast: Oatmeal with berries and nuts\n- Lunch: Grilled chicken salad with mixed greens\n- Dinner: Baked salmon with quinoa and roasted vegetables\n- Snacks: Greek yogurt, almonds, apple slices"
        
        response_json["nutrition"] += food_suggestions
        return RecommendResponse(**response_json)
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error parsing Gemini response: {e}")
        print(f"Raw response: {response_text}")
        print(f"Extracted JSON: {json_text}")
        
        # Return a fallback response with basic nutrition advice
        return RecommendResponse(
            nutrition="Sorry, I couldn't generate a nutrition plan. Please try again.",
            supplements=[]
        )


@app.post("/ai_chat")
def ai_chat(
    request: ChatRequest,
) -> Dict[str, str]:
    
    nutrition_keywords = [
        "nutrition", "diet", "meal", "calorie", "protein", "carb", "fat", "vitamin", 
        "supplement", "eat", "food", "breakfast", "lunch", "dinner", "snack", "recipe",
        "nutrient", "fiber", "sugar", "sodium", "healthy eating", "portion", "serving"
    ]
    fitness_keywords = [
        "workout", "exercise", "training", "cardio", "strength", "yoga", "run", 
        "fitness", "gym", "rest", "recovery", "muscle", "weight lifting", "hiit",
        "stretching", "flexibility", "endurance", "athletic", "sport", "activity",
        "physical", "movement", "body", "health", "wellness"
    ]

    def _is_relevant(message: str) -> bool:
        lowered = message.lower()
        return any(keyword in lowered for keyword in nutrition_keywords + fitness_keywords)

    last_user_message = next((msg for msg in reversed(request.messages)), "")

    if not _is_relevant(last_user_message):
        reply = (
            "I'm here as your NutriFit AI coach, so I focus on nutrition and fitness. "
            "Ask me anything about meal planning, workouts, hydration, or healthy habits!"
        )
        return {"reply": reply}

    prompt = (
        "You are a friendly, evidence-based AI assistant specializing exclusively in nutrition and fitness. "
        "Always keep responses on-topic and avoid medical diagnoses. "
        "Provide clear, actionable advice that's easy to understand and implement. "
        "Here is the conversation history:\n"
    )

    for msg in request.messages:
        prompt += f"- {msg}\n"
    prompt += (
        "\nProvide a motivating, practical answer with actionable tips. "
        "Keep your response concise but informative (2-4 paragraphs). "
        "If the conversation drifts away from nutrition or fitness, gently steer it back."
    )

    reply = get_gemini_response(prompt)
    return {"reply": reply}



@app.post("/ocr")
async def ocr_analysis(file: UploadFile = File(...)) -> Dict[str, Any]:
    contents = await file.read()
    report = await process_health_document_sync(contents, file.filename)
    return {
        "raw_text": report.raw_text,
        "metrics": [metric.__dict__ for metric in report.metrics],
        "summary": report.summary,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)