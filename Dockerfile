# Dockerfile for Django app (admin_AsteriscoSiete7)
FROM python:3.13-slim

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies (if any needed, e.g., libpq-dev for PostgreSQL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libcairo2-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Collect static files (optional, can be done at runtime)
RUN python admin_AsteriscoSiete-server/admin_AsteriscoSiete7/manage.py collectstatic --noinput

# Expose port used by Cloud Run (default 8080)
EXPOSE 8080

# Set environment variable for production settings
ENV DJANGO_SETTINGS_MODULE=admin_asterisco7.settings_production

# Entrypoint: runs migrations + setup + gunicorn
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]
