# NutriFit Pages

This directory contains Streamlit pages for the NutriFit application.

## Pages

1. **🔐 Login** (`1_🔐_Login.py`) - User login page
2. **📝 Register** (`2_📝_Register.py`) - User registration page

## How it works

Streamlit automatically discovers pages in the `pages/` directory and adds them to the sidebar navigation. The numbering prefix (1_, 2_, etc.) determines the order in which they appear.

## Authentication Flow

1. Users start at the main app (app.py)
2. If not authenticated, they're prompted to login or register
3. After successful login/registration, they can access all features
4. Users can logout from the main app sidebar