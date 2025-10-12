# Quick GitHub Push Script
# Run this after creating your GitHub repository

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   NutriFit - Quick GitHub Push" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Show current status
Write-Host "Current Git Status:" -ForegroundColor Yellow
git status --short
Write-Host ""

# Verify important files are ignored
Write-Host "Verifying .gitignore is working..." -ForegroundColor Yellow
$ignored = git check-ignore node_modules/ venv/ .env 2>$null
if ($ignored) {
    Write-Host "✅ node_modules/, venv/, and .env are properly ignored" -ForegroundColor Green
} else {
    Write-Host "⚠️  Warning: Some files might not be ignored" -ForegroundColor Yellow
}
Write-Host ""

# Ask for repository URL
Write-Host "Enter your GitHub repository URL" -ForegroundColor Cyan
Write-Host "Example: https://github.com/yourusername/NutriFit.git" -ForegroundColor Gray
$repoUrl = Read-Host "Repository URL"

if ([string]::IsNullOrWhiteSpace($repoUrl)) {
    Write-Host "❌ No URL provided. Exiting..." -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "📝 Creating commit..." -ForegroundColor Yellow
$commitMsg = Read-Host "Commit message (press Enter for default)"
if ([string]::IsNullOrWhiteSpace($commitMsg)) {
    $commitMsg = "Initial commit: NutriFit AI-powered wellness app"
}

git commit -m "$commitMsg"

Write-Host ""
Write-Host "🔗 Adding remote repository..." -ForegroundColor Yellow
git remote add origin $repoUrl

Write-Host ""
Write-Host "🌿 Setting main branch..." -ForegroundColor Yellow
git branch -M main

Write-Host ""
Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Yellow
git push -u origin main

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   ✅ SUCCESS!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your code is now on GitHub! 🎉" -ForegroundColor Green
Write-Host ""
Write-Host "Repository URL: $repoUrl" -ForegroundColor Cyan
Write-Host ""