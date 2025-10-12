#!/bin/bash
# Unified startup script for NutriFit
# Runs both FastAPI backend and Streamlit frontend together

echo "🚀 Starting NutriFit Unified Service..."

# Start FastAPI backend in background
echo "📡 Starting FastAPI backend on port 8000..."
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend to be ready
echo "⏳ Waiting for backend to be ready..."
sleep 5

# Set API_URL for frontend to use local backend
export API_URL="http://localhost:8000"

# Start Streamlit frontend on the PORT provided by Render
echo "🎨 Starting Streamlit frontend on port $PORT..."
streamlit run frontend/app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true

# If Streamlit exits, kill the backend too
kill $BACKEND_PID