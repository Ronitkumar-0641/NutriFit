# 🚀 NutriFit Deployment Guide - GitHub & Render

This guide will walk you through deploying NutriFit to GitHub and then to Render.

## 📋 Prerequisites

- Git installed on your computer
- GitHub account
- Render account (free tier available at https://render.com)
- Your environment variables ready:
  - `SUPABASE_URL`
  - `SUPABASE_API_KEY`
  - `GEMINI_API_KEY`

---

## Part 1: Push to GitHub

### Step 1: Initialize Git Repository (if not already done)

Open PowerShell in your project directory and run:

```powershell
cd C:\Users\nrk06\Desktop\NutriFit
git init
```

### Step 2: Verify .gitignore

The `.gitignore` file is already configured to exclude:
- ✅ `node_modules/`
- ✅ `venv/`
- ✅ `.env` (environment variables)
- ✅ `__pycache__/`
- ✅ `.qodo/` and `.zencoder/`

### Step 3: Add All Files

```powershell
git add .
```

### Step 4: Create Initial Commit

```powershell
git commit -m "Initial commit: NutriFit wellness app with AI-powered nutrition plans"
```

### Step 5: Create GitHub Repository

1. Go to https://github.com
2. Click the **"+"** icon in the top right
3. Select **"New repository"**
4. Repository settings:
   - **Name:** `NutriFit` (or your preferred name)
   - **Description:** `AI-powered wellness app with personalized nutrition plans and fitness tracking`
   - **Visibility:** Public or Private (your choice)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click **"Create repository"**

### Step 6: Connect Local Repository to GitHub

GitHub will show you commands. Use these (replace with your actual repository URL):

```powershell
git remote add origin https://github.com/YOUR_USERNAME/NutriFit.git
git branch -M main
git push -u origin main
```

**Example:**
```powershell
git remote add origin https://github.com/johndoe/NutriFit.git
git branch -M main
git push -u origin main
```

### Step 7: Verify Upload

- Go to your GitHub repository URL
- You should see all your files (except those in .gitignore)
- ✅ Verify `node_modules/` is NOT there
- ✅ Verify `venv/` is NOT there
- ✅ Verify `.env` is NOT there

---

## Part 2: Deploy to Render

### Step 1: Create Render Account

1. Go to https://render.com
2. Sign up (you can use your GitHub account)
3. Verify your email

### Step 2: Connect GitHub Repository

1. In Render dashboard, click **"New +"** button
2. Select **"Blueprint"**
3. Click **"Connect GitHub"**
4. Authorize Render to access your GitHub
5. Select your **NutriFit** repository

### Step 3: Configure Environment Variables

Render will detect the `render.yaml` file. Before deploying, you need to add environment variables:

#### For Backend Service:
1. Go to **nutrifit-backend** service settings
2. Click **"Environment"** tab
3. Add these variables:

```
GEMINI_API_KEY = your_actual_gemini_api_key
SUPABASE_URL = your_actual_supabase_url
SUPABASE_API_KEY = your_actual_supabase_anon_key
```

#### For Frontend Service:
1. Go to **nutrifit-frontend** service settings
2. Click **"Environment"** tab
3. Add these variables:

```
API_URL = https://nutrifit-backend.onrender.com
SUPABASE_URL = your_actual_supabase_url
SUPABASE_API_KEY = your_actual_supabase_anon_key
GEMINI_API_KEY = your_actual_gemini_api_key
```

**Note:** The `API_URL` should be the URL of your deployed backend service.

### Step 4: Deploy

1. Click **"Apply"** or **"Create Blueprint"**
2. Render will start building both services
3. Wait 5-10 minutes for the build to complete

### Step 5: Get Your URLs

After deployment, you'll have two URLs:
- **Backend:** `https://nutrifit-backend.onrender.com`
- **Frontend:** `https://nutrifit-frontend.onrender.com`

### Step 6: Update Frontend API_URL

1. Go to **nutrifit-frontend** service settings
2. Update the `API_URL` environment variable to your actual backend URL
3. Save and redeploy

---

## Alternative: Manual Deployment (Without render.yaml)

If you prefer to deploy services manually:

### Deploy Backend:

1. In Render dashboard, click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:
   - **Name:** `nutrifit-backend`
   - **Region:** Oregon (US West)
   - **Branch:** `main`
   - **Root Directory:** (leave empty)
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free
4. Add environment variables (see Step 3 above)
5. Click **"Create Web Service"**

### Deploy Frontend:

1. In Render dashboard, click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:
   - **Name:** `nutrifit-frontend`
   - **Region:** Oregon (US West)
   - **Branch:** `main`
   - **Root Directory:** (leave empty)
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run frontend/app.py --server.port=$PORT --server.address=0.0.0.0`
   - **Plan:** Free
4. Add environment variables (see Step 3 above)
5. Click **"Create Web Service"**

---

## 🔧 Post-Deployment Configuration

### 1. Update Supabase CORS Settings

Your Render URLs need to be allowed in Supabase:

1. Go to Supabase Dashboard
2. Navigate to **Settings** → **API**
3. Add your Render URLs to allowed origins:
   ```
   https://nutrifit-frontend.onrender.com
   https://nutrifit-backend.onrender.com
   ```

### 2. Test Your Deployment

1. Visit your frontend URL: `https://nutrifit-frontend.onrender.com`
2. Try to register a new account
3. Test the nutrition plan generation
4. Verify all features work

---

## 📝 Important Notes

### Free Tier Limitations:
- ⚠️ **Cold Starts:** Free tier services spin down after 15 minutes of inactivity
- ⚠️ **First Load:** May take 30-60 seconds to wake up
- ⚠️ **Build Time:** Limited to 500 build minutes per month
- ✅ **Solution:** Upgrade to paid tier ($7/month per service) for always-on services

### Database Setup:
- ✅ Make sure you've created the `user_profiles` table in Supabase
- ✅ Run the SQL from `SETUP_DATABASE.md` if you haven't already

### Environment Variables:
- ⚠️ **NEVER** commit `.env` file to GitHub
- ✅ Always use Render's environment variable settings
- ✅ Keep a backup of your environment variables securely

---

## 🐛 Troubleshooting

### Build Fails:
- Check the build logs in Render dashboard
- Verify `requirements.txt` is correct
- Ensure Python version is compatible (3.11 recommended)

### Frontend Can't Connect to Backend:
- Verify `API_URL` environment variable is set correctly
- Check backend service is running (green status in Render)
- Verify CORS settings in backend

### Authentication Issues:
- Verify Supabase environment variables are correct
- Check Supabase dashboard for error logs
- Ensure RLS policies are set up correctly

### Nutrition Plan Not Generating:
- Verify `GEMINI_API_KEY` is set correctly
- Check backend logs for Gemini API errors
- Ensure you have Gemini API quota available

---

## 🔄 Updating Your Deployment

When you make changes to your code:

```powershell
# 1. Commit your changes
git add .
git commit -m "Description of your changes"

# 2. Push to GitHub
git push origin main

# 3. Render will automatically redeploy (if auto-deploy is enabled)
```

To enable auto-deploy:
1. Go to service settings in Render
2. Enable **"Auto-Deploy"** option
3. Now every push to `main` branch will trigger a deployment

---

## 📊 Monitoring Your Deployment

### Render Dashboard:
- View logs in real-time
- Monitor service health
- Check resource usage
- View deployment history

### Useful Commands:
```powershell
# View backend logs
# (Available in Render dashboard under "Logs" tab)

# Check service status
# (Available in Render dashboard)
```

---

## 🎉 Success Checklist

- ✅ Code pushed to GitHub (without node_modules, venv, .env)
- ✅ Backend deployed on Render
- ✅ Frontend deployed on Render
- ✅ Environment variables configured
- ✅ Supabase database table created
- ✅ CORS settings updated
- ✅ App accessible via Render URL
- ✅ Registration works
- ✅ Login works
- ✅ Nutrition plan generation works
- ✅ All features functional

---

## 📞 Need Help?

### Common Issues:
1. **"Module not found" error:** Check `requirements.txt` includes all dependencies
2. **"Port already in use":** Render handles ports automatically with `$PORT`
3. **"Database connection failed":** Verify Supabase credentials
4. **"API key invalid":** Check Gemini API key is correct

### Resources:
- Render Documentation: https://render.com/docs
- Supabase Documentation: https://supabase.com/docs
- Streamlit Deployment: https://docs.streamlit.io/streamlit-community-cloud/get-started

---

## 🚀 Your Deployment URLs

After deployment, update this section with your actual URLs:

- **Frontend:** `https://nutrifit-frontend.onrender.com`
- **Backend:** `https://nutrifit-backend.onrender.com`
- **GitHub:** `https://github.com/YOUR_USERNAME/NutriFit`

---

**Congratulations! Your NutriFit app is now live! 🎉**