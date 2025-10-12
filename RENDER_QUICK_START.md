# 🚀 Render Deployment - Quick Start

## ⚡ 5-Minute Deployment Guide

### 📝 Prerequisites (Have These Ready!)
```
✅ Supabase URL: _______________________
✅ Supabase API Key: ___________________
✅ Gemini API Key: _____________________
```

---

## 🎯 Deployment Steps

### 1️⃣ Go to Render
👉 **https://render.com** → Sign up with GitHub

### 2️⃣ Create Blueprint
- Click **"New +"** button
- Select **"Blueprint"**
- Connect repository: **Ronitkumar-0641/NutriFit**
- Click **"Apply"**

### 3️⃣ Add Environment Variables

#### Backend Service (nutrifit-backend):
```
GEMINI_API_KEY = [your key]
SUPABASE_URL = [your url]
SUPABASE_API_KEY = [your key]
```

#### Frontend Service (nutrifit-frontend):
```
API_URL = https://nutrifit-backend.onrender.com
SUPABASE_URL = [your url]
SUPABASE_API_KEY = [your key]
GEMINI_API_KEY = [your key]
```

### 4️⃣ Wait for Build
⏱️ Takes 5-10 minutes per service

### 5️⃣ Update Frontend API_URL
- Go to frontend service → Environment
- Update `API_URL` with your actual backend URL
- Save (will auto-redeploy)

### 6️⃣ Test Your App! 🎉
Visit: `https://nutrifit-frontend.onrender.com`

---

## 📋 Deployment Checklist

```
□ Render account created
□ GitHub repository connected
□ Backend service deployed
□ Frontend service deployed
□ Environment variables added
□ Frontend API_URL updated
□ App is accessible
□ Registration works
□ Login works
□ Features work
```

---

## 🆘 Quick Troubleshooting

**Build Failed?**
→ Check logs in Render dashboard

**Frontend can't connect to backend?**
→ Verify API_URL is correct

**Slow to load?**
→ Normal on free tier (30-60 sec first load)

**Authentication issues?**
→ Check Supabase credentials

---

## 📚 Full Guide
See **RENDER_DEPLOYMENT_STEPS.md** for detailed instructions

---

**Your URLs after deployment:**
- Frontend: `https://nutrifit-frontend.onrender.com`
- Backend: `https://nutrifit-backend.onrender.com`
- GitHub: `https://github.com/Ronitkumar-0641/NutriFit` ✅