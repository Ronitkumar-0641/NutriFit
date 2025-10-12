# Nutrition Plan Implementation with User Profiles

## Overview
This implementation adds comprehensive user profile management with real-time BMI calculation and AI-powered personalized nutrition plans using Gemini AI.

## Features Implemented

### 1. **User Profile System**
- Added user profile database table in Supabase
- Stores: weight, height, age, gender, BMI, fitness goals
- Row-level security policies for data protection

### 2. **Enhanced Registration Page**
- **Personal Information Fields:**
  - Weight (kg)
  - Height (cm)
  - Age
  - Gender (male, female, other, prefer not to say)
  - Fitness Goal (weight loss, muscle gain, maintenance, etc.)

- **Real-time BMI Calculator:**
  - Automatically calculates BMI as user enters weight/height
  - Color-coded BMI categories (Underweight, Normal, Overweight, Obese)
  - Visual feedback with appropriate colors

- **AI-Powered Health Advice:**
  - "Get AI Advice" button for personalized health tips
  - Uses Gemini AI to provide context-aware advice based on BMI, age, and gender
  - Encouraging and actionable recommendations

### 3. **Personalized Nutrition Plans**
- **Profile-Based Recommendations:**
  - Fetches user profile data automatically
  - Displays user metrics (weight, height, BMI, age, goal)
  - Generates highly personalized nutrition plans using Gemini AI

- **AI-Generated Content:**
  - Calorie recommendations based on profile
  - Macronutrient breakdown (protein, carbs, fats)
  - Meal timing suggestions
  - Hydration recommendations
  - Supplement suggestions tailored to user needs

- **BMI-Specific Food Suggestions:**
  - Underweight: High-calorie, nutrient-dense foods
  - Overweight: Lower-calorie, filling foods
  - Normal weight: Balanced maintenance foods

### 4. **Backend Services**

#### Profile Service (`profile_service.py`)
- `create_profile()` - Create user profile with BMI calculation
- `get_profile()` - Retrieve user profile data
- `update_profile()` - Update profile with automatic BMI recalculation
- `calculate_bmi()` - BMI calculation utility

#### Updated Auth Service
- Enhanced `sign_up()` to accept profile data
- Automatic profile creation during registration
- Seamless integration with Supabase Auth

#### API Endpoints
- `POST /profile/get` - Get user profile
- `POST /recommend` - Generate personalized nutrition plan
  - Accepts optional `user_id` parameter
  - Returns AI-generated plan based on user profile

## Database Schema

```sql
-- User profiles table
create table if not exists public.user_profiles (
    id uuid primary key references auth.users(id) on delete cascade,
    full_name text,
    weight_kg float,
    height_cm float,
    age int,
    gender text check (gender in ('male', 'female', 'other', 'prefer_not_to_say')),
    bmi float,
    fitness_goal text,
    created_at timestamp with time zone default timezone('utc', now()),
    updated_at timestamp with time zone default timezone('utc', now())
);
```

## How It Works

### Registration Flow
1. User enters account information (name, email, password)
2. User enters personal information (weight, height, age, gender)
3. BMI is calculated in real-time as they type
4. User can click "Get AI Advice" for personalized health tips
5. User selects fitness goal
6. On submit:
   - User account is created in Supabase Auth
   - User profile is created in user_profiles table
   - BMI is calculated and stored
   - User is logged in (if email confirmation not required)

### Nutrition Plan Flow
1. User navigates to Nutrition Plan page
2. System displays user profile summary (weight, height, BMI, age, goal)
3. User clicks "Generate Personalized Plan"
4. Backend:
   - Fetches user profile from database
   - Determines BMI category
   - Creates personalized prompt for Gemini AI
   - Generates nutrition plan with:
     - Detailed nutrition strategy
     - Calorie recommendations
     - Macronutrient breakdown
     - Meal timing
     - Hydration tips
     - Supplement recommendations
     - BMI-specific food suggestions
5. Plan is displayed with beautiful formatting

## AI Integration

### Gemini AI Usage
1. **BMI Health Advice** (Registration page)
   - Provides brief, encouraging health tips
   - Context-aware based on BMI, age, gender
   - 2-3 sentences of actionable advice

2. **Nutrition Plan Generation** (Nutrition page)
   - Comprehensive personalized plan
   - Based on complete user profile
   - Includes all nutritional aspects
   - Tailored to fitness goals and BMI category

## Files Modified

### Backend
- `backend/database.sql` - Added user_profiles table
- `backend/profile_service.py` - NEW: Profile management service
- `backend/auth.py` - Enhanced sign_up with profile creation
- `backend/main.py` - Added profile endpoints and enhanced /recommend

### Frontend
- `frontend/pages/2_📝_Register.py` - Complete redesign with profile fields
- `frontend/app.py` - Enhanced nutrition plan page with profile integration

## Setup Instructions

### 1. Database Setup
Run the SQL commands in `backend/database.sql` in your Supabase SQL editor to create the user_profiles table and policies.

### 2. Environment Variables
Ensure these are set in your `.env` file:
```
SUPABASE_URL=your_supabase_url
SUPABASE_API_KEY=your_supabase_key
GEMINI_API_KEY=your_gemini_api_key
API_URL=http://localhost:8000
```

### 3. Install Dependencies
No new dependencies required - uses existing packages.

### 4. Run the Application
```bash
# Start backend
python -m uvicorn backend.main:app --reload

# Start frontend (in another terminal)
streamlit run frontend/app.py
```

## Testing the Features

### Test Registration with Profile
1. Go to Register page
2. Fill in account information
3. Enter weight: 70 kg, height: 175 cm
4. Watch BMI calculate automatically (22.86 - Normal Weight)
5. Click "Get AI Advice" to see personalized tips
6. Select a fitness goal
7. Create account

### Test Personalized Nutrition Plan
1. Login with your account
2. Navigate to "Nutrition Plan" page
3. See your profile summary displayed
4. Click "Generate Personalized Plan"
5. Wait for AI to generate plan
6. Review personalized recommendations

## Benefits

1. **Personalization**: Every user gets a unique plan based on their data
2. **Real-time Feedback**: BMI calculated instantly as user types
3. **AI-Powered**: Leverages Gemini AI for intelligent recommendations
4. **Data-Driven**: Uses actual user metrics for accurate advice
5. **User-Friendly**: Beautiful UI with clear visual feedback
6. **Scalable**: Profile system ready for future enhancements

## Future Enhancements

- Profile editing page
- Progress tracking over time
- Weight/BMI history charts
- Meal planning with recipes
- Integration with fitness tracker
- Photo-based meal logging
- Social features (share progress)
- Notifications for goals

## Troubleshooting

### Profile Not Loading
- Check if user is logged in
- Verify user_id is in session state
- Check Supabase connection
- Verify RLS policies are set correctly

### BMI Not Calculating
- Ensure weight and height are > 0
- Check number input values
- Verify calculate_bmi function

### AI Advice Not Working
- Check GEMINI_API_KEY is set
- Verify internet connection
- Check Gemini API quota
- Review error logs

### Nutrition Plan Generic
- Verify user profile exists in database
- Check user_id is being sent to API
- Ensure profile data is complete
- Check API logs for errors

## Security Considerations

- User profiles protected by Row Level Security (RLS)
- Users can only access their own profile
- Profile data encrypted in transit
- No sensitive health data exposed in logs
- API endpoints validate user authentication

## Conclusion

This implementation provides a complete, production-ready user profile and personalized nutrition plan system. It leverages modern AI technology (Gemini) to provide truly personalized health and nutrition advice based on real user data.