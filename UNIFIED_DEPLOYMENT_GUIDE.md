# 🚀 NutriFit Unified Deployment Guide

## ✅ What Changed?

Your NutriFit app is now configured for **single unified deployment** instead of separate backend/frontend services!

### Benefits:
- ✅ **Simpler setup** - Only ONE service to deploy
- ✅ **No CORS issues** - Everything on same domain
- ✅ **Easier configuration** - Set environment variables once
- ✅ **Faster cold starts** - Only one service wakes up
- ✅ **Lower complexity** - Perfect for getting started

---

## 📋 What Was Modified?

### 1. **render.yaml** - Simplified to single service
```yaml
services:
  - type: web
    name: nutrifit
    env: python
    region: oregon
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: bash start_unified.sh
```

### 2. **requirements.txt** - Added Streamlit
Now includes both backend AND frontend dependencies:
- FastAPI + Uvicorn (backend)
- Streamlit + Plotly (frontend)
- All other dependencies

### 3. **start_unified.sh** - New startup script
Runs both services together:
- Starts FastAPI backend on port 8000
- Starts Streamlit frontend on Render's $PORT
- Frontend automatically connects to backend

---

## 🚀 Deploy to Render (15 Minutes)

### Step 1: Push to GitHub

```powershell
git add .
git commit -m "Configure unified deployment"
git push origin main
```

### Step 2: Go to Render

1. Visit: https://render.com
2. Sign in with GitHub
3. Click **"New +"** → **"Blueprint"**

### Step 3: Connect Repository

1. Select repository: **Ronitkumar-0641/NutriFit**
2. Click **"Connect"**
3. Render will detect `render.yaml`
4. Click **"Apply"**

### Step 4: Add Environment Variables

Click on your **nutrifit** service, go to **Environment**, and add:

```
GEMINI_API_KEY = AIzaSyAmnBYVLItjiLvoCu6blbZ3453lmXxjE_E
SUPABASE_URL = https://tereffehsopjmyxuhnwk.supabase.co
SUPABASE_API_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRlcmVmZmVoc29wam15eHVobndrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTIwODAzNzcsImV4cCI6MjA2NzY1NjM3N30.-QdrHk5lIghA1Xmm5rGdM2RJDos-dEfA-lTETiMocJ4
JWT_SECRET = 07b6b7b2c8ed5409e9f7c6fd078a254e59997a30ec618862d0a6c580005ad7e1
```

**Important:** Click **"Save Changes"** after adding each variable!

### Step 5: Wait for Deployment

- Build time: ~5-7 minutes
- Watch the logs for progress
- Look for: "✅ Build successful"

### Step 6: Test Your App

Once deployed, your app will be at:
```
https://nutrifit.onrender.com
```

Click the URL and test:
- ✅ Homepage loads
- ✅ Login/Register works
- ✅ Chatbot responds
- ✅ All features work

---

## 🎯 Environment Variables Explained

| Variable | Purpose | Where to Get It |
|----------|---------|-----------------|
| **GEMINI_API_KEY** | AI chatbot responses | https://makersuite.google.com/app/apikey |
| **SUPABASE_URL** | Database connection | Supabase Dashboard → Settings → API |
| **SUPABASE_API_KEY** | Database authentication | Supabase Dashboard → Settings → API (anon/public key) |
| **JWT_SECRET** | Secure user sessions | Already in your .env file |

---

## 🔧 How It Works

### Architecture:
```
User Request → Render (Port $PORT)
                  ↓
            Streamlit Frontend
                  ↓
            FastAPI Backend (Port 8000)
                  ↓
            Supabase Database
```

### Startup Process:
1. Render runs `start_unified.sh`
2. Script starts FastAPI backend on port 8000
3. Script starts Streamlit frontend on Render's port
4. Frontend connects to backend via `http://localhost:8000`
5. Both services run together in one container

---

## 🐛 Troubleshooting

### Issue: "Build failed"
**Solution:** Check the build logs for missing dependencies
- Make sure `requirements.txt` includes all packages
- Verify Python version is 3.11.0

### Issue: "Application failed to respond"
**Solution:** Check the runtime logs
- Look for errors in FastAPI or Streamlit startup
- Verify environment variables are set correctly

### Issue: "Database connection failed"
**Solution:** Check Supabase credentials
- Verify SUPABASE_URL is correct
- Verify SUPABASE_API_KEY is the anon/public key
- Check if `user_profiles` table exists in Supabase

### Issue: "Chatbot not responding"
**Solution:** Check Gemini API key
- Verify GEMINI_API_KEY is correct
- Test at: https://makersuite.google.com/app/apikey
- Check API quota hasn't been exceeded

### Issue: "Service keeps sleeping"
**Solution:** This is normal on free tier
- Services sleep after 15 minutes of inactivity
- First request takes 30-60 seconds (cold start)
- Consider upgrading to paid tier for always-on service

---

## 📊 Free Tier Limitations

| Feature | Free Tier |
|---------|-----------|
| **Services** | 1 web service (perfect for unified!) |
| **Sleep** | After 15 minutes inactivity |
| **Cold Start** | 30-60 seconds |
| **Build Time** | ~5-7 minutes |
| **Monthly Hours** | 750 hours/month |
| **Bandwidth** | 100 GB/month |

---

## 🎨 Customization

### Change Service Name
Edit `render.yaml`:
```yaml
name: nutrifit  # Change this to your preferred name
```

### Change Region
Edit `render.yaml`:
```yaml
region: oregon  # Options: oregon, frankfurt, singapore
```

### Add Custom Domain
1. Go to Render Dashboard
2. Click your service
3. Go to "Settings" → "Custom Domain"
4. Follow instructions to add your domain

---

## 🔄 Enable Auto-Deploy

To automatically deploy when you push to GitHub:

1. Go to Render Dashboard
2. Click your **nutrifit** service
3. Go to **Settings**
4. Find **"Auto-Deploy"**
5. Toggle **ON**
6. Select branch: **main**

Now every `git push` will trigger a new deployment! 🎉

---

## 📈 Monitoring

### View Logs
1. Go to Render Dashboard
2. Click your service
3. Click **"Logs"** tab
4. See real-time logs from both FastAPI and Streamlit

### Check Health
Your backend has a health endpoint:
```
https://nutrifit.onrender.com/health
```

Should return:
```json
{"status": "healthy"}
```

---

## 🚀 Next Steps

### 1. Test Everything
- [ ] Homepage loads
- [ ] Login/Register works
- [ ] Profile creation works
- [ ] Chatbot responds
- [ ] Nutrition plans generate
- [ ] Health reports work

### 2. Share Your App
Your app is live at:
```
https://nutrifit.onrender.com
```

Share this URL with friends, family, or users!

### 3. Monitor Usage
- Check Render Dashboard for:
  - Request count
  - Response times
  - Error rates
  - Bandwidth usage

### 4. Consider Upgrading
If you need:
- ✅ No sleep (always-on)
- ✅ Faster cold starts
- ✅ More bandwidth
- ✅ Custom domains

Upgrade to Render's paid tier ($7/month per service)

---

## 💡 Tips

### Faster Development
1. Enable auto-deploy for instant updates
2. Use Render's logs for debugging
3. Test locally before pushing to GitHub

### Better Performance
1. Optimize database queries
2. Cache frequently used data
3. Minimize API calls to Gemini
4. Use Streamlit's caching features

### Security
1. Never commit `.env` file (already in .gitignore ✅)
2. Rotate API keys regularly
3. Use environment variables for all secrets
4. Enable Supabase Row Level Security (RLS)

---

## 📞 Need Help?

### Render Support
- Docs: https://render.com/docs
- Community: https://community.render.com
- Status: https://status.render.com

### NutriFit Issues
- Check logs in Render Dashboard
- Review this guide's troubleshooting section
- Test locally first: `streamlit run frontend/app.py`

---

## 🎉 Success Checklist

- [ ] Code pushed to GitHub
- [ ] Render Blueprint created
- [ ] Environment variables added
- [ ] Build completed successfully
- [ ] App is accessible at Render URL
- [ ] Login/Register works
- [ ] Chatbot responds
- [ ] All features tested
- [ ] Auto-deploy enabled (optional)
- [ ] Custom domain added (optional)

---

## 🔗 Important Links

- **Your GitHub:** https://github.com/Ronitkumar-0641/NutriFit
- **Render Dashboard:** https://dashboard.render.com
- **Supabase Dashboard:** https://supabase.com/dashboard
- **Gemini API:** https://makersuite.google.com/app/apikey

---

**Ready to deploy? Push to GitHub and follow the steps above!** 🚀

Your app will be live in ~15 minutes with just ONE service to manage!