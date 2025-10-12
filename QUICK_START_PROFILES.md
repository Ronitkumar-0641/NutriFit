# Quick Start Guide - User Profiles & Personalized Nutrition

## 🎯 What's New?

Your NutriFit app now has:
- ✅ User profiles with weight, height, age, gender
- ✅ Real-time BMI calculation during registration
- ✅ AI-powered health advice using Gemini
- ✅ Personalized nutrition plans based on your profile
- ✅ BMI-specific food recommendations

## 🚀 Setup (5 minutes)

### Step 1: Database Setup

1. Open your **Supabase Dashboard**
2. Go to **SQL Editor**
3. Click **New Query**
4. Copy the SQL from `backend/database.sql` (lines 20-48)
5. Click **Run**

**Or run this command:**
```bash
python setup_profiles.py
```
This will show you the SQL to run in Supabase.

### Step 2: Verify Environment Variables

Make sure your `.env` file has:
```env
SUPABASE_URL=your_supabase_url
SUPABASE_API_KEY=your_supabase_key
GEMINI_API_KEY=your_gemini_api_key
API_URL=http://localhost:8000
```

### Step 3: Start the Application

**Terminal 1 - Backend:**
```bash
python -m uvicorn backend.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
streamlit run frontend/app.py
```

## 🎮 How to Use

### Register with Profile

1. Go to **Register** page
2. Fill in your account details
3. Enter your personal information:
   - Weight (kg)
   - Height (cm)
   - Age
   - Gender
   - Fitness Goal

4. **Watch the magic:**
   - BMI calculates automatically! 🧮
   - See your BMI category with color coding
   - Click "Get AI Advice" for personalized tips 🤖

5. Click **Create Account**

### Get Your Personalized Nutrition Plan

1. **Login** to your account
2. Navigate to **Nutrition Plan** page
3. See your profile summary at the top
4. Click **"Generate Personalized Plan"**
5. Wait for AI to create your custom plan
6. Review your:
   - Personalized nutrition strategy
   - Calorie recommendations
   - Macronutrient breakdown
   - Meal timing suggestions
   - Supplement recommendations
   - BMI-specific food suggestions

## 🎨 Features Showcase

### Real-time BMI Calculator
```
Weight: 70 kg
Height: 175 cm
→ BMI: 22.86 (Normal Weight) ✅
```

### AI Health Advice
Click "Get AI Advice" and receive personalized tips like:
> "Your BMI indicates a healthy weight range. Focus on maintaining this through balanced nutrition with lean proteins, whole grains, and plenty of vegetables. Stay active with regular exercise to support your overall wellness."

### Personalized Nutrition Plans
Based on your profile, you'll get:
- **Calorie targets** specific to your goals
- **Macros breakdown** (protein/carbs/fats)
- **Meal timing** optimized for you
- **Food suggestions** based on your BMI
- **Supplements** tailored to your needs

## 📊 BMI Categories

| BMI Range | Category | Color |
|-----------|----------|-------|
| < 18.5 | Underweight | Blue |
| 18.5 - 24.9 | Normal Weight | Green |
| 25.0 - 29.9 | Overweight | Orange |
| ≥ 30.0 | Obese | Red |

## 🔧 Troubleshooting

### "Profile not found" error
- Make sure you registered with the new form
- Check if database table was created
- Verify you're logged in

### BMI not calculating
- Enter valid weight (30-300 kg)
- Enter valid height (100-250 cm)
- Refresh the page

### AI advice not working
- Check GEMINI_API_KEY in .env
- Verify internet connection
- Check Gemini API quota

### Nutrition plan is generic
- Make sure you registered with profile data
- Check if profile was saved (look at profile summary)
- Try logging out and back in

## 🎯 Example User Journey

**Sarah's Story:**
1. Sarah registers: 65kg, 168cm, 28 years, female, goal: weight_loss
2. BMI calculated: 23.03 (Normal Weight)
3. Gets AI advice: "Focus on slight calorie deficit with strength training"
4. Generates nutrition plan
5. Receives personalized plan with:
   - 1,800 calorie target
   - 40% carbs, 30% protein, 30% fats
   - Meal timing for weight loss
   - Food suggestions for healthy weight management
   - Supplements: Multivitamin, Omega-3, Vitamin D

## 📝 What Data is Stored?

Your profile includes:
- Full name
- Weight (kg)
- Height (cm)
- Age
- Gender
- BMI (calculated)
- Fitness goal
- Created/updated timestamps

**Privacy:** All data is protected by Row Level Security (RLS). Only you can see your profile.

## 🚀 Next Steps

Try these features:
1. Register a new account with your real data
2. Get AI advice on your BMI
3. Generate your personalized nutrition plan
4. Explore the AI chatbot for nutrition questions
5. Track your progress on the dashboard

## 💡 Tips for Best Results

1. **Be accurate** with your measurements
2. **Update your profile** as you progress
3. **Regenerate plans** monthly for adjustments
4. **Follow the AI advice** - it's personalized for you!
5. **Combine with fitness tracking** for best results

## 🎉 Enjoy Your Personalized NutriFit Experience!

You now have a fully AI-powered, personalized nutrition and fitness companion. Every recommendation is tailored specifically to YOUR body, YOUR goals, and YOUR needs.

**Questions?** Check the full documentation in `NUTRITION_PLAN_IMPLEMENTATION.md`