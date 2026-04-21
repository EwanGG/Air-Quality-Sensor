import sqlite3

conn = sqlite3.connect("air_quality.db", check_same_thread=False)
cursor = conn.cursor()

def insert_data(data):
    cursor.execute("""
        CREATE TABLE sensor_data (
            reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
            time_stamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            username TEXT NOT NULL,
            password  TEXT NOT NULL,
            description TEXT,
            language TEXT,
            temp REAL,
            humidity REAL,
            pressure REAL,
            gas_level REAL,
            gps_location REAL)
        
        INSERT INTO sensor_data (temp,humidity,pressure,language,gps_location)
        VALUES (?,?,?,?,?,?,?,?,?)
        """, (
        data['reading_id'],
        data['time_stamp'],
        data['username'],
        data['password'],
        data['description'],
        data['language'],
        data['temp'],
        data['humidity'],
        data['pressure'],
        data['gas_level'],
        data['gps_location']
    ))

    conn.commit()
    conn.close()

    print("Database and table created successfully!")