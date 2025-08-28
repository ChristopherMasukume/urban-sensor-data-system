FROM python:3.9-slim-bullseye

WORKDIR /app

# Install system dependencies required for psycopg2 and update packages
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY data_ingestion.py .
COPY data/ ./data/

# Create a non-root user to run the application
RUN useradd --create-home --shell /bin/bash appuser
RUN chown -R appuser:appuser /app
USER appuser

# Default command (can be overridden)
CMD ["python", "data_ingestion.py"]