"""
Setup script to create user_profiles table in Supabase.
Run this script to set up the database schema for user profiles.
"""
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

if not SUPABASE_URL or not SUPABASE_API_KEY:
    print("❌ Error: SUPABASE_URL and SUPABASE_API_KEY must be set in .env file")
    exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

# SQL to create user_profiles table
CREATE_TABLE_SQL = """
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
"""

def main():
    print("🚀 Setting up user_profiles table in Supabase...")
    print("\n" + "="*60)
    print("IMPORTANT: This script requires SQL execution in Supabase")
    print("="*60)
    print("\nPlease follow these steps:")
    print("\n1. Go to your Supabase Dashboard")
    print("2. Navigate to: SQL Editor")
    print("3. Click 'New Query'")
    print("4. Copy and paste the SQL below:")
    print("\n" + "-"*60)
    print(CREATE_TABLE_SQL)
    print("-"*60)
    print("\n5. Click 'Run' to execute the SQL")
    print("\n✅ Once done, your database will be ready for user profiles!")
    print("\nAlternatively, you can find this SQL in: backend/database.sql")

if __name__ == "__main__":
    main()