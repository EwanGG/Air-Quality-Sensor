import board
import busio
import sqlite3
import adafruit_bme680

class BME688Sensor:
    def __init__(self):
        self.process = None

        try:
            self.i2c = busio.I2C(board.SCL, board.SDA)

            self.sensor = adafruit_bme680.Adafruit_BME680_I2C(self.i2c, address=0x76)

            self.conn = sqlite3.connect('./air_quality.db',check_same_thread=False)
            self.cursor = self.conn.cursor()

            self.cursor.execute("""
                                CREATE TABLE IF NOT EXISTS sensor_data (
                                    reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    time_stamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                                    temperature REAL,
                                    humidity REAL,
                                    pressure REAL,
                                    gas REAL, 
                                )
            """)
            self.conn.commit()

        print("Sensor successfully initialized")

        except Exception as e:
            print("Error : ",e)
            self.sensor = None

    def read_sensor_data(self):
        if self.sensor is None:
            return None

        try:
            data = {
                "reading_id": self.sensor.temperature,
                "time_stamp": self.sensor.time_stamp,
                "temperature": round(self.sensor.temperature, 2),
                "pressure": round(self.sensor.pressure, 2),
                "humidity": round(self.sensor.humidity, 2),
                "gas": round(
                    getattr(self.sensor, "gas", self.sensor.gas), 2),
            }
            return data

        except Exception as e:
            print("Error : ",e)
            return None

