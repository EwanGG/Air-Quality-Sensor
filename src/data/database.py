import sqlite3
import time
from datetime import datetime
from src.sensors.BME688 import BME688Sensor

# 1. Database Configuration
DB_NAME = "sensor_data.db"


def init_db():
    """Creates the database and table structure if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS environmental_readings
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       timestamp
                       DATETIME
                       DEFAULT
                       CURRENT_TIMESTAMP,
                       temperature
                       REAL,
                       humidity
                       REAL,
                       gas
                       REAL,
                       pressure 
                       REAL,
                       latitude
                       REAL,
                       longitude
                       REAL
                   )
                   ''')
    conn.commit()
    conn.close()


def log_data(temp, hum, gas, pre, lat, lon):
    """Inserts a single row of data into the database."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
                       INSERT INTO environmental_readings (temperature, humidity, gas, pressure, latitude, longitude)
                       VALUES (?, ?, ?, ?, ?, ?)
                       ''', (temp, hum, gas, pre, lat, lon))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Database error: {e}")


# 2. Main Loop
if __name__ == "__main__":
    init_db()
    print("Collector started. Press Ctrl+C to stop.")

    while True:
        # --- REPLACE THESE WITH YOUR ACTUAL SENSOR READS ---
        # Example: temp = bme280.get_temperature()
        temp = BME688Sensor.read_data()
        hum = BME688Sensor.read_data()
        gas = BME688Sensor.read_data()
        pre = BME688Sensor.read_data()
        lat = BME688Sensor.read_data()
        lon = BME688Sensor.read_data()
        # --------------------------------------------------

        log_data(temp, hum, gas, pre, lat, lon)
        print(f"[{datetime.now()}] Data logged successfully.")

        # Wait for 5 seconds before the next reading
        time.sleep(5)