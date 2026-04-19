class BME688Sensor:
    def __init__(self):
        try:
            import board
            import busio
            import sqlite3
            import adafruit_bme680
            import subprocess

            self.i2c = busio.I2C(board.SCL, board.SDA)
            self.sensor = adafruit_bme680.Adafruit_BME680_I2C(self.i2c, address=0x76)

            conn = sqlite3.connect('./air_quality.db')
            cursor = conn.cursor()

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS bsec_bme688 (
                reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
                time_stamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                temp REAL,
                humidity REAL,
                pressure REAL,
                gas_level REAL,
                gps_location REAL
            """)

            print("Sensor initialized successfully")

            self.process = subprocess.Popen(
                ["./bsec_bme688_example"],
                stdout=subprocess.PIPE,
                text=True
            )

            print("BSEC2 process started successfully")

        except Exception as e:
            print("Error initializing BME688 and BSEC2:", e)
            self.sensor = None

    def read_data(self):
        if self.sensor is None:
            return None

        try:
            return {
                "temperature": round(self.sensor.temperature, 2),
                "pressure": round(self.sensor.pressure, 2),
                "humidity": round(self.sensor.humidity, 2),
                "gas": round(self.sensor.gas, 2),
                "gps_location": self.sensor.gps_location
            }
        except Exception as e:
            print("Error reading sensor:", e)
            return None