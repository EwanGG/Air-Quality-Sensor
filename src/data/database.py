import sqlite3
import threading

lock = threading.Lock()

conn = sqlite3.connect("air_quality.db", check_same_thread=False)
cursor = conn.cursor()

# Sensor table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS sensor_data
    (
        reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
        time_stamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        temperature REAL,
        humidity REAL,
        pressure REAL,
        gas REAL,
        latitude REAL,
        longitude REAL
    );
""")

# User table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    );
""")

conn.commit()

def insert_data(data):
    with lock:
        try:
            cursor.execute("""
                INSERT INTO sensor_data
                (temperature, humidity, pressure, gas, latitude, longitude)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                data.get('temperature'),
                data.get('humidity'),
                data.get('pressure'),
                data.get('gas'),
                data.get('latitude'),
                data.get('longitude')
            ))
            conn.commit()
        except Exception as e:
            print("DB Error: ", e)