-- Enable the TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Drop the table if it already exists. Useful for development and testing.
DROP TABLE IF EXISTS sensor_readings;

-- Create the main table to store our sensor data.
-- We use a 'long' format: each row is a single sensor reading.
CREATE TABLE sensor_readings (
    time TIMESTAMPTZ NOT NULL,        -- Timestamp of the reading (with timezone)
    sensor_id TEXT NOT NULL,           -- Identifier for the sensor (e.g., 'weather_station')
    metric_name TEXT NOT NULL,         -- Name of the metric (e.g., 'temperature', 'humidity')
    metric_value DOUBLE PRECISION NOT NULL -- The value of the measurement
);

-- Convert the standard PostgreSQL table into a TimescaleDB hypertable.
-- This is what makes it optimized for time-series data. It automatically
-- partitions data by time behind the scenes for much faster queries.
SELECT create_hypertable('sensor_readings', 'time');

-- Create a composite index on 'sensor_id' and 'metric_name'.
-- This will dramatically speed up queries that filter by a specific
-- sensor and metric (e.g., 'get all temperature data from sensor T1').
CREATE INDEX idx_sensor_metric ON sensor_readings (sensor_id, metric_name);

-- Print a success message (visible in the Docker logs)
DO $$
BEGIN
    RAISE NOTICE 'Database schema successfully initialized!';
END $$;