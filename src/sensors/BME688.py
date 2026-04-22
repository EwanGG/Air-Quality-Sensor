import board
import busio
import sqlite3
import adafruit_bme680

class BME688Sensor:
    def __init__(self):
        self.sensor = None

        try:
            # I2C setup
            self.i2c = busio.I2C(board.SCL, board.SDA)

            # BME680 sensor
            self.sensor = adafruit_bme680.Adafruit_BME680_I2C(self.i2c, address=0x76)

            # Database connection
            self.conn = sqlite3.connect('./air_quality.db',check_same_thread=False)
            self.cursor = self.conn.cursor()

            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS bsec_bme688 (
                reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
                time_stamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                temp REAL,
                humidity REAL,
                pressure REAL,
                gas_level REAL,
                )
            """)
            self.conn.commit()

            # Starting BSEC2 process
            line = self.process.stdout.readline()
            print(line)

            print("Sensor and BSEC2 successfully")

        except Exception as e:
            print("Error initializing BME688 and BSEC2:", e)
            self.sensor = None

    def read_data(self):
        if self.sensor is None:
            return None

        try:
            data = {
                "temperature": round(self.sensor.temperature, 2),
                "pressure": round(self.sensor.pressure, 2),
                "humidity": round(self.sensor.humidity, 2),
                "gas": round(
                    getattr(self.sensor, "gas resistance", self.sensor.gas),2),
            }
            return data

        except Exception as e:
            print("Error reading sensor:", e)
            return None