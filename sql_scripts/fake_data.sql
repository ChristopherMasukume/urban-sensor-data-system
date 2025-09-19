-- Insert fake sensor data for testing alerts in Grafana
-- Temperature (T1–T3)
INSERT INTO sensor_readings (time, sensor_id, metric_name, metric_value) VALUES
  (NOW() - INTERVAL '10 minutes', 'T1', 'temperature', 22.5),
  (NOW() - INTERVAL '8 minutes', 'T2', 'temperature', 23.1),
  (NOW() - INTERVAL '5 minutes', 'T3', 'temperature', 24.7),
  (NOW() - INTERVAL '2 minutes', 'T1', 'temperature', 25.3),
  (NOW(), 'T2', 'temperature', 26.1);

-- CO₂ values (will trigger alert > 1000 ppm)
INSERT INTO sensor_readings (time, sensor_id, metric_name, metric_value) VALUES
  (NOW() - INTERVAL '10 minutes', 'S1', 'co2', 800),
  (NOW() - INTERVAL '5 minutes', 'S1', 'co2', 950),
  (NOW(), 'S1', 'co2', 1200);

-- Humidity values (will trigger alert < 30%)
INSERT INTO sensor_readings (time, sensor_id, metric_name, metric_value) VALUES
  (NOW() - INTERVAL '15 minutes', 'H1', 'humidity', 45),
  (NOW() - INTERVAL '10 minutes', 'H1', 'humidity', 35),
  (NOW(), 'H1', 'humidity', 25);

-- Windspeed values (gauge panel)
INSERT INTO sensor_readings (time, sensor_id, metric_name, metric_value) VALUES
  (NOW() - INTERVAL '20 minutes', 'W1', 'windspeed', 10),
  (NOW() - INTERVAL '10 minutes', 'W1', 'windspeed', 35),
  (NOW(), 'W1', 'windspeed', 65);
