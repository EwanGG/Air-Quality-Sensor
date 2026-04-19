import sqlite3

conn = sqlite3.connect("air_quality.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE sensor_data (
    reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
    time_stamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    language TEXT,
    temp REAL,
    humidity REAL,
    pressure REAL,
    gas_level REAL,
    gps_location REAL
)
""")

conn.commit()
conn.close()

print("Database and table created successfully!")