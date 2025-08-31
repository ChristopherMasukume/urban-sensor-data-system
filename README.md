# Urban Sensor Data System

A Dockerized data engineering pipeline for ingesting and storing smart home sensor data with weather information into TimescaleDB.

## 🚀 Features

- **PostgreSQL with TimescaleDB** for time-series optimization
- **Automated data ingestion** from CSV to database
- **Docker containerization** for reproducibility
- **Batch processing** for large datasets (14M+ records)
- **Error handling** and automatic retries

Access sensor data csv from https://drive.google.com/file/d/1NRn3ws4bHYOUwufW-zi6Bz6KW_zuk61-/view?usp=sharing
  

## 📁 Project Structure

urban-sensor-data-system/
├── docker-compose.yml
├── README.md
├── .gitignore
├── sql_scripts/
│ └── init.sql
└── ingestion_app/
├── Dockerfile
├── data_ingestion.py
├── requirements.txt
├── .dockerignore
└── data/
└── Smart Home Dataset with Weather Information.csv
text


## 🛠️ Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/urban-sensor-data-system.git
   cd urban-sensor-data-system

    Start the database
    bash

docker-compose up -d postgres-db

Run data ingestion
bash

docker-compose run data-ingestion

Access the database
bash

    docker exec -it urban-sensor-db psql -U admin_user -d sensor_data_db

📊 Data Schema

The system uses a optimized time-series schema:

    time: Timestamp (UTC)

    sensor_id: Sensor identifier

    metric_name: Measurement type

    metric_value: Numeric value

🔧 Technologies Used

    Python 3.9 with pandas and psycopg2

    PostgreSQL 17 with TimescaleDB extension

    Docker and Docker Compose

    Batch processing for high-volume data

📈 Performance

    Processes 503,911 CSV rows → 14,109,480 time-series measurements

    Batch insertion (10,000 records/batch)

    TimescaleDB hypertables for optimized queries
