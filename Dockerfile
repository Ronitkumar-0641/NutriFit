FROM python:3.11-slim

# Set working directory for backend app
WORKDIR /app

# Copy shared requirements into the image
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend/ ./backend/

# Expose backend port
EXPOSE 8000

# Default command to launch FastAPI via Uvicorn
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]