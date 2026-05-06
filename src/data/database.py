import sqlite3
import time
from datetime import datetime


# 1. Database Configuration
DB_NAME = "air_quality.db"


def init_db():
    """Creates the database and table structure if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS sensor_readings
                   (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                       temperature REAL,
                       humidity REAL,
                       gas REAL,
                       pressure REAL,
                       latitude REAL,
                       longitude REAL,
                       reading_time DATETIME DEFAULT CURRENT_TIMESTAMP
                   )
                   ''')
    conn.commit()
    conn.close()


def insert_data(temp, hum, gas, pre, lat, lon):
    """Inserts a single row of data into the database."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
                       INSERT INTO sensor_readings (temperature, humidity, gas, pressure, latitude, longitude)
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

    sensor = BME688Sensor()

    while True:

        data = sensor.read_data()

        if data:
            temp = data["temperature"]
            hum = data["humidity"]
            gas = data["gas"]
            pre = data["pressure"]
            lat = data["latitude"]
            lon = data["longitude"]
        # --------------------------------------------------

        insert_data(temp, hum, gas, pre, lat, lon)
        print(f"[{datetime.now()}] Data logged successfully.")

        # Wait for 5 seconds before the next reading
        time.sleep(5)