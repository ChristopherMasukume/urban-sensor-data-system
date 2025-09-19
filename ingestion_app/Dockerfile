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


# Create a non-root user to run the application
RUN useradd --create-home --shell /bin/bash appuser
RUN chown -R appuser:appuser /app
USER appuser

# Default command (can be overridden)
CMD ["python", "data_ingestion.py"]

# nacigate to cd ingestion_app
# build the docker image with: docker build -t data-ingestion-app .

# Start the specific container
# -docker start urban-sensor-db
# Wait a few seconds for PostgreSQL to start, then try connecting
# -docker exec -it urban-sensor-db psql -U admin_user -d sensor_data_db