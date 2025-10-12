# 🚀 Quick GitHub Push Guide

## Step-by-Step Commands

Copy and paste these commands in PowerShell (in your project directory):

### 1. Initialize Git (if not already done)
```powershell
cd C:\Users\nrk06\Desktop\NutriFit
git init
```

### 2. Check what will be committed
```powershell
git status
```

**Verify that these are NOT listed:**
- ❌ `node_modules/`
- ❌ `venv/`
- ❌ `.env`

If they appear, they'll be ignored by `.gitignore` automatically.

### 3. Add all files
```powershell
git add .
```

### 4. Create initial commit
```powershell
git commit -m "Initial commit: NutriFit AI-powered wellness app"
```

### 5. Create GitHub Repository

1. Go to: https://github.com/new
2. Repository name: `NutriFit`
3. Description: `AI-powered wellness app with personalized nutrition plans`
4. Choose Public or Private
5. **DO NOT** check any boxes (no README, no .gitignore, no license)
6. Click **"Create repository"**

### 6. Connect to GitHub

**Replace `YOUR_USERNAME` with your actual GitHub username:**

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

### 7. Enter GitHub Credentials

When prompted:
- Enter your GitHub username
- Enter your GitHub password (or Personal Access Token)

**Note:** If using 2FA, you need a Personal Access Token:
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo` (full control)
4. Copy the token and use it as your password

### 8. Verify Upload

Go to your repository URL:
```
https://github.com/YOUR_USERNAME/NutriFit
```

**Check that:**
- ✅ All your code files are there
- ✅ `node_modules/` is NOT there
- ✅ `venv/` is NOT there
- ✅ `.env` is NOT there
- ✅ `.gitignore` is there

---

## 🎉 Success!

Your code is now on GitHub! 

**Next Steps:**
1. ✅ Code is on GitHub
2. 📖 Read `DEPLOYMENT_GUIDE.md` for Render deployment
3. 🚀 Deploy to Render

---

## 🔄 Future Updates

When you make changes:

```powershell
# 1. Check what changed
git status

# 2. Add changes
git add .

# 3. Commit with a message
git commit -m "Description of what you changed"

# 4. Push to GitHub
git push origin main
```

---

## ⚠️ Important Security Notes

**NEVER commit these files:**
- ❌ `.env` (contains API keys)
- ❌ `venv/` (virtual environment)
- ❌ `node_modules/` (dependencies)
- ❌ `__pycache__/` (Python cache)

These are already in `.gitignore` and will be automatically excluded.

**If you accidentally committed `.env`:**
```powershell
# Remove from Git but keep locally
git rm --cached .env
git commit -m "Remove .env from repository"
git push origin main

# Then regenerate your API keys for security!
```

---

## 📝 Repository Description

Use this for your GitHub repository description:

```
NutriFit - AI-Powered Wellness Hub

A comprehensive wellness application featuring:
- 🤖 AI-powered personalized nutrition plans (Gemini AI)
- 👤 User profiles with BMI calculation
- 🥗 Meal planning and recommendations
- 🏃 Fitness tracking
- 💬 AI wellness coach chatbot
- 🩺 Medical report analysis with OCR
- 🔐 Secure authentication (Supabase)

Tech Stack: Python, Streamlit, FastAPI, Supabase, Google Gemini AI
```

---

## 🏷️ Suggested Topics/Tags

Add these topics to your GitHub repository:
- `python`
- `streamlit`
- `fastapi`
- `ai`
- `gemini`
- `nutrition`
- `fitness`
- `wellness`
- `health`
- `supabase`
- `machine-learning`
- `chatbot`

---

**Ready to deploy? Check out `DEPLOYMENT_GUIDE.md`!**