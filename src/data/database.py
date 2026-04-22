import sqlite3

conn = sqlite3.connect("air_quality.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS sensor_data (
        reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
        time_stamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        temp REAL,
        humidity REAL,
        pressure REAL,
        gas_level REAL,
        latitude REAL,
        longitude REAL
    )
""")

conn.commit()

def insert_data(data):
    cursor.execute("""
        INSERT INTO sensor_data 
        (temp, humidity, pressure, gas_level, latitude, longitude)
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