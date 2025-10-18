# Lightweight production-like image for FactReal
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/root/.cache/huggingface

WORKDIR /app

# System deps (optional; add git if models need it)
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps first for better cache
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend ./backend

# Expose port
EXPOSE 8000

# Default command
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
