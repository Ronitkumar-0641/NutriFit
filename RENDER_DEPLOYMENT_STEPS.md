# 🚀 Deploy NutriFit to Render - Step by Step Guide

**Your GitHub Repository:** https://github.com/Ronitkumar-0641/NutriFit ✅

---

## 📋 Before You Start - Gather Your Credentials

You'll need these environment variables. Have them ready:

```
✅ SUPABASE_URL = your_supabase_project_url
✅ SUPABASE_API_KEY = your_supabase_anon_key
✅ GEMINI_API_KEY = your_gemini_api_key
```

**Where to find them:**
- **Supabase:** Dashboard → Settings → API
- **Gemini API:** https://makersuite.google.com/app/apikey

---

## 🎯 Deployment Method: Choose One

### ⭐ Method 1: Blueprint Deployment (RECOMMENDED - Easiest)
Deploys both backend and frontend automatically using `render.yaml`

### Method 2: Manual Deployment
Deploy backend and frontend separately (more control)

---

## ⭐ METHOD 1: Blueprint Deployment (Recommended)

### Step 1: Create Render Account
1. Go to **https://render.com**
2. Click **"Get Started"** or **"Sign Up"**
3. Choose **"Sign up with GitHub"** (easiest option)
4. Authorize Render to access your GitHub account
5. Verify your email if prompted

### Step 2: Create New Blueprint
1. In Render Dashboard, click the **"New +"** button (top right)
2. Select **"Blueprint"**
3. You'll see "Connect a repository"

### Step 3: Connect Your GitHub Repository
1. Click **"Connect GitHub"** (if not already connected)
2. In the popup, find and select **"Ronitkumar-0641/NutriFit"**
3. Click **"Connect"**
4. Render will scan your repository and find `render.yaml`

### Step 4: Review Blueprint Configuration
Render will show you:
- ✅ **nutrifit-backend** (Backend API)
- ✅ **nutrifit-frontend** (Frontend Streamlit app)

Click **"Apply"** or **"Create Blueprint"**

### Step 5: Add Environment Variables

#### 🔧 For Backend Service (nutrifit-backend):
1. Click on **"nutrifit-backend"** service
2. Go to **"Environment"** tab (left sidebar)
3. Click **"Add Environment Variable"**
4. Add these one by one:

```
Key: GEMINI_API_KEY
Value: [paste your actual Gemini API key]

Key: SUPABASE_URL
Value: [paste your actual Supabase URL]

Key: SUPABASE_API_KEY
Value: [paste your actual Supabase anon key]
```

5. Click **"Save Changes"**

#### 🔧 For Frontend Service (nutrifit-frontend):
1. Click on **"nutrifit-frontend"** service
2. Go to **"Environment"** tab (left sidebar)
3. Click **"Add Environment Variable"**
4. Add these one by one:

```
Key: API_URL
Value: https://nutrifit-backend.onrender.com
(Note: This will be your backend URL - you can update it after backend deploys)

Key: SUPABASE_URL
Value: [paste your actual Supabase URL]

Key: SUPABASE_API_KEY
Value: [paste your actual Supabase anon key]

Key: GEMINI_API_KEY
Value: [paste your actual Gemini API key]
```

5. Click **"Save Changes"**

### Step 6: Wait for Deployment
- Both services will start building automatically
- **Backend:** Takes 5-8 minutes
- **Frontend:** Takes 5-8 minutes
- Watch the logs in real-time (click on each service to see logs)

### Step 7: Get Your URLs
After deployment completes, you'll have:
- **Backend URL:** `https://nutrifit-backend.onrender.com`
- **Frontend URL:** `https://nutrifit-frontend.onrender.com`

### Step 8: Update Frontend API_URL (Important!)
1. Go to **nutrifit-frontend** service
2. Click **"Environment"** tab
3. Find the **API_URL** variable
4. Update it to your actual backend URL (from Step 7)
5. Click **"Save Changes"**
6. Service will automatically redeploy

### Step 9: Test Your App! 🎉
1. Visit your frontend URL: `https://nutrifit-frontend.onrender.com`
2. Try registering a new account
3. Test login
4. Generate a nutrition plan
5. Verify all features work

---

## 🔧 METHOD 2: Manual Deployment (Alternative)

If Blueprint doesn't work, deploy manually:

### Deploy Backend First:

1. In Render Dashboard, click **"New +"** → **"Web Service"**
2. Click **"Connect GitHub"**
3. Select **"Ronitkumar-0641/NutriFit"**
4. Configure:
   - **Name:** `nutrifit-backend`
   - **Region:** Oregon (US West)
   - **Branch:** `main`
   - **Root Directory:** (leave empty)
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** Free
5. Click **"Advanced"** and add environment variables:
   ```
   GEMINI_API_KEY = your_key
   SUPABASE_URL = your_url
   SUPABASE_API_KEY = your_key
   ```
6. Click **"Create Web Service"**
7. Wait for deployment (5-8 minutes)
8. Copy the backend URL (e.g., `https://nutrifit-backend.onrender.com`)

### Deploy Frontend Second:

1. In Render Dashboard, click **"New +"** → **"Web Service"**
2. Select **"Ronitkumar-0641/NutriFit"** again
3. Configure:
   - **Name:** `nutrifit-frontend`
   - **Region:** Oregon (US West)
   - **Branch:** `main`
   - **Root Directory:** (leave empty)
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run frontend/app.py --server.port=$PORT --server.address=0.0.0.0`
   - **Instance Type:** Free
4. Click **"Advanced"** and add environment variables:
   ```
   API_URL = [your backend URL from step 8 above]
   SUPABASE_URL = your_url
   SUPABASE_API_KEY = your_key
   GEMINI_API_KEY = your_key
   ```
5. Click **"Create Web Service"**
6. Wait for deployment (5-8 minutes)

---

## ⚠️ Important Post-Deployment Steps

### 1. Update Supabase CORS Settings (If needed)
1. Go to Supabase Dashboard
2. Navigate to **Settings** → **API**
3. Scroll to **CORS Settings**
4. Add your Render URLs:
   ```
   https://nutrifit-frontend.onrender.com
   https://nutrifit-backend.onrender.com
   ```

### 2. Verify Database Tables
Make sure you have the `user_profiles` table in Supabase:
- Check `SETUP_DATABASE.md` for SQL schema
- Run the SQL in Supabase SQL Editor if not done yet

---

## 🐛 Troubleshooting

### Build Failed?
**Check the logs:**
1. Click on the service in Render dashboard
2. Go to **"Logs"** tab
3. Look for error messages

**Common issues:**
- ❌ Missing dependencies → Check `requirements.txt`
- ❌ Python version mismatch → Render uses Python 3.11
- ❌ Import errors → Check file paths

### Frontend Can't Connect to Backend?
1. Verify `API_URL` is set correctly in frontend environment variables
2. Check backend service is running (green status)
3. Test backend directly: `https://nutrifit-backend.onrender.com/health`

### Authentication Not Working?
1. Verify Supabase credentials are correct
2. Check Supabase logs for errors
3. Ensure database tables exist

### Slow First Load?
⚠️ **This is normal on free tier!**
- Free services "sleep" after 15 minutes of inactivity
- First request takes 30-60 seconds to wake up
- Subsequent requests are fast
- **Solution:** Upgrade to paid tier ($7/month) for always-on

---

## 📊 Monitor Your Deployment

### View Logs:
1. Go to Render Dashboard
2. Click on service name
3. Click **"Logs"** tab
4. See real-time logs

### Check Service Health:
- Green dot = Running ✅
- Yellow dot = Building 🔨
- Red dot = Failed ❌

### Enable Auto-Deploy:
1. Go to service settings
2. Find **"Auto-Deploy"** option
3. Enable it
4. Now every push to GitHub will auto-deploy!

---

## 🔄 Update Your Deployed App

When you make code changes:

```powershell
# 1. Make your changes locally
# 2. Commit and push to GitHub
git add .
git commit -m "Your update description"
git push origin main

# 3. Render will automatically redeploy (if auto-deploy is enabled)
```

---

## ✅ Deployment Checklist

Before you start:
- ✅ GitHub repository is ready (https://github.com/Ronitkumar-0641/NutriFit)
- ✅ Have Supabase URL and API key
- ✅ Have Gemini API key
- ✅ Render account created

During deployment:
- ✅ Backend service created
- ✅ Frontend service created
- ✅ Environment variables added to both services
- ✅ Both services deployed successfully (green status)
- ✅ Frontend API_URL updated with actual backend URL

After deployment:
- ✅ Frontend URL accessible
- ✅ Backend health check works: `/health` endpoint
- ✅ Registration works
- ✅ Login works
- ✅ Nutrition plan generation works
- ✅ All features functional

---

## 🎉 Your Deployment URLs

After deployment, your app will be live at:

- **Frontend (Main App):** `https://nutrifit-frontend.onrender.com`
- **Backend (API):** `https://nutrifit-backend.onrender.com`
- **GitHub Repository:** `https://github.com/Ronitkumar-0641/NutriFit`

---

## 💡 Pro Tips

1. **Free Tier Limitations:**
   - Services sleep after 15 minutes of inactivity
   - 750 hours/month of runtime per service
   - Slower performance than paid tier

2. **Upgrade to Paid ($7/month per service):**
   - Always-on (no cold starts)
   - Better performance
   - More resources

3. **Monitor Usage:**
   - Check Render dashboard regularly
   - Watch for build failures
   - Monitor logs for errors

4. **Keep Credentials Safe:**
   - Never commit `.env` to GitHub
   - Use Render's environment variables
   - Keep a secure backup of your keys

---

## 📞 Need Help?

**Render Support:**
- Documentation: https://render.com/docs
- Community: https://community.render.com

**NutriFit Documentation:**
- See `DEPLOYMENT_GUIDE.md` for more details
- Check `TROUBLESHOOTING.md` for common issues

---

**Ready to deploy? Follow the steps above and your app will be live in ~15 minutes! 🚀**