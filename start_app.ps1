# NutriFit Application Startup Script
# This script starts both the backend API and frontend Streamlit app

Write-Host "🥗 Starting NutriFit Application..." -ForegroundColor Green
Write-Host ""

# Get the project root directory
$ProjectRoot = $PSScriptRoot
$VenvPython = Join-Path $ProjectRoot "venv\Scripts\python.exe"
$VenvStreamlit = Join-Path $ProjectRoot "venv\Scripts\streamlit.exe"
$BackendDir = Join-Path $ProjectRoot "backend"
$FrontendDir = Join-Path $ProjectRoot "frontend"

# Check if virtual environment exists
if (-not (Test-Path $VenvPython)) {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please create a virtual environment first:" -ForegroundColor Yellow
    Write-Host "  python -m venv venv" -ForegroundColor Yellow
    Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    Write-Host "  pip install -r requirements.txt" -ForegroundColor Yellow
    Write-Host "  pip install -r frontend\requirements.txt" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Cyan
& "$ProjectRoot\venv\Scripts\Activate.ps1"

# Start backend API in a new window
Write-Host "🚀 Starting Backend API..." -ForegroundColor Cyan
$BackendCommand = "Set-Location '$BackendDir'; & '$VenvPython' -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $BackendCommand

# Wait a bit for backend to start
Start-Sleep -Seconds 3

# Start frontend Streamlit app
Write-Host "🎨 Starting Frontend..." -ForegroundColor Cyan
Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Green
Write-Host ("=" * 60) -ForegroundColor Green
Write-Host "✅ NutriFit is starting!" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Backend API: http://localhost:8000" -ForegroundColor Yellow
Write-Host "📍 Frontend App: http://localhost:8501" -ForegroundColor Yellow
Write-Host ""
Write-Host "🔐 Login or Register to get started!" -ForegroundColor Cyan
Write-Host "=" -NoNewline -ForegroundColor Green
Write-Host ("=" * 60) -ForegroundColor Green
Write-Host ""

# Start frontend
Set-Location $FrontendDir
& $VenvStreamlit run app.py