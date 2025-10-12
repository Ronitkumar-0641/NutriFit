# 🗄️ Database Setup Guide

## ⚠️ Important: Create the User Profiles Table

Your NutriFit app needs a `user_profiles` table in Supabase to store user health data.

## 📋 Quick Setup (2 minutes)

### Step 1: Open Supabase Dashboard

1. Go to [https://supabase.com](https://supabase.com)
2. Login to your account
3. Select your NutriFit project

### Step 2: Run the SQL

1. Click on **"SQL Editor"** in the left sidebar
2. Click **"New Query"**
3. Copy and paste the SQL below
4. Click **"Run"** (or press Ctrl+Enter)

```sql
-- User profiles table to store additional user information
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

-- Enable Row Level Security
alter table public.user_profiles enable row level security;

-- Create policies for user_profiles
create policy "Users can view their own profile"
    on public.user_profiles for select
    using (auth.uid() = id);

create policy "Users can insert their own profile"
    on public.user_profiles for insert
    with check (auth.uid() = id);

create policy "Users can update their own profile"
    on public.user_profiles for update
    using (auth.uid() = id);
```

### Step 3: Verify

After running the SQL, you should see:

```
Success. No rows returned
```

This means the table was created successfully!

## 🔍 Verify Table Creation

1. In Supabase, go to **"Table Editor"**
2. You should see `user_profiles` in the list of tables
3. Click on it to see the columns

## ✅ What This Does

- **Creates the table**: Stores user weight, height, age, gender, BMI, and fitness goals
- **Links to auth**: Each profile is linked to a user account (UUID)
- **Security**: Row Level Security (RLS) ensures users can only see their own data
- **Auto-delete**: If a user account is deleted, their profile is automatically deleted too

## 🎯 Table Structure

| Column | Type | Description |
|--------|------|-------------|
| id | uuid | User ID (from auth.users) |
| full_name | text | User's full name |
| weight_kg | float | Weight in kilograms |
| height_cm | float | Height in centimeters |
| age | int | User's age |
| gender | text | Gender (male/female/other/prefer_not_to_say) |
| bmi | float | Body Mass Index (calculated automatically) |
| fitness_goal | text | User's fitness goal |
| created_at | timestamp | When profile was created |
| updated_at | timestamp | When profile was last updated |

## 🔒 Security Policies

The table has Row Level Security (RLS) enabled with these policies:

1. **View**: Users can only view their own profile
2. **Insert**: Users can only create their own profile
3. **Update**: Users can only update their own profile

This ensures complete data privacy!

## 🚨 Troubleshooting

### "Table already exists" error
- This is fine! It means the table was already created
- You can skip this step

### "Permission denied" error
- Make sure you're logged in as the project owner
- Check that you're in the correct project

### "Relation does not exist" error in app
- The table wasn't created yet
- Run the SQL above in Supabase SQL Editor

## 🎉 Next Steps

Once the table is created:

1. ✅ Start the backend server
2. ✅ Start the frontend
3. ✅ Register a new account with your profile data
4. ✅ Generate your personalized nutrition plan!

---

**Need help?** Check the full documentation in `QUICK_START_PROFILES.md`