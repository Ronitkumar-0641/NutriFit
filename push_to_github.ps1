# NutriFit - GitHub Push Script
# This script helps you push your code to GitHub

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   NutriFit - GitHub Push Helper" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
try {
    git --version | Out-Null
    Write-Host "✅ Git is installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Git is not installed. Please install Git first." -ForegroundColor Red
    Write-Host "Download from: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit
}

Write-Host ""

# Check if already initialized
if (Test-Path ".git") {
    Write-Host "✅ Git repository already initialized" -ForegroundColor Green
} else {
    Write-Host "📦 Initializing Git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
}

Write-Host ""
Write-Host "📋 Checking files to be committed..." -ForegroundColor Yellow
Write-Host ""

# Show status
git status

Write-Host ""
Write-Host "⚠️  IMPORTANT: Verify that these are NOT listed above:" -ForegroundColor Yellow
Write-Host "   ❌ node_modules/" -ForegroundColor Red
Write-Host "   ❌ venv/" -ForegroundColor Red
Write-Host "   ❌ .env" -ForegroundColor Red
Write-Host ""

$continue = Read-Host "Do you want to continue? (y/n)"
if ($continue -ne "y") {
    Write-Host "❌ Aborted by user" -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "📦 Adding files to Git..." -ForegroundColor Yellow
git add .

Write-Host ""
Write-Host "💾 Creating commit..." -ForegroundColor Yellow
$commitMessage = Read-Host "Enter commit message (or press Enter for default)"
if ([string]::IsNullOrWhiteSpace($commitMessage)) {
    $commitMessage = "Initial commit: NutriFit AI-powered wellness app"
}
git commit -m "$commitMessage"

Write-Host ""
Write-Host "✅ Commit created successfully!" -ForegroundColor Green
Write-Host ""

# Check if remote exists
$remoteExists = git remote | Select-String "origin"
if ($remoteExists) {
    Write-Host "✅ Remote 'origin' already exists" -ForegroundColor Green
    Write-Host ""
    Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Yellow
    git push origin main
} else {
    Write-Host "📝 Now you need to create a GitHub repository:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "1. Go to: https://github.com/new" -ForegroundColor Cyan
    Write-Host "2. Repository name: NutriFit" -ForegroundColor Cyan
    Write-Host "3. Description: AI-powered wellness app with personalized nutrition plans" -ForegroundColor Cyan
    Write-Host "4. Choose Public or Private" -ForegroundColor Cyan
    Write-Host "5. DO NOT check any boxes (no README, no .gitignore, no license)" -ForegroundColor Cyan
    Write-Host "6. Click Create repository" -ForegroundColor Cyan
    Write-Host ""
    
    $repoUrl = Read-Host "Enter your GitHub repository URL (e.g., https://github.com/username/NutriFit.git)"
    
    if ([string]::IsNullOrWhiteSpace($repoUrl)) {
        Write-Host "❌ No URL provided. Exiting..." -ForegroundColor Red
        exit
    }
    
    Write-Host ""
    Write-Host "🔗 Adding remote repository..." -ForegroundColor Yellow
    git remote add origin $repoUrl
    
    Write-Host ""
    Write-Host "🌿 Setting main branch..." -ForegroundColor Yellow
    git branch -M main
    
    Write-Host ""
    Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Yellow
    git push -u origin main
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   ✅ SUCCESS!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your code is now on GitHub! 🎉" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. ✅ Code is on GitHub" -ForegroundColor Green
Write-Host "2. 📖 Read DEPLOYMENT_GUIDE.md for Render deployment" -ForegroundColor Cyan
Write-Host "3. 🚀 Deploy to Render" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")