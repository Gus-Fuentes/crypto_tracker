FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8000
ENV DJANGO_SETTINGS_MODULE cryptotracker.settings
ENV DEBUG 0
ENV REDIS_URL redis://redis:6379/1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose default port
EXPOSE ${PORT}

# Create a non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Run the application
CMD ["sh", "-c", "echo 'Running migrations...' && python manage.py migrate && echo 'Starting Gunicorn...' && gunicorn cryptotracker.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --access-logfile - --error-logfile - --log-level info"]
