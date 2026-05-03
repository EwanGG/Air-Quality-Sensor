import sqlite3
import threading

lock = threading.Lock()

conn = sqlite3.connect("air_quality.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS sensor_data (
        reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
        time_stamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        temperature REAL,
        humidity REAL,
        pressure REAL,
        gas REAL,
        latitude REAL,
        longitude REAL,
        iaq REAL,
        co2 REAL,
        voc REAL
    )
""")

conn.commit()

def insert_data(data):
    with lock:
        cursor.execute("""
                       INSERT INTO sensor_data
                       (temperature, humidity, pressure, gas, latitude, longitude, iaq, co2, voc)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                       """, (
                           data.get('temperature'),
                           data.get('humidity'),
                           data.get('pressure'),
                           data.get('gas'),
                           data.get('latitude'),
                           data.get('longitude'),
                           data.get('iaq'),
                           data.get('co2'),
                           data.get('voc')
                       ))

        conn.commit()