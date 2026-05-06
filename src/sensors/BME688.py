import board
import busio
import sqlite3
import adafruit_bme680

class BME688Sensor:
    def __init__(self):
        self.process = None

        try:
            # Initialize sensor
            self.i2c = busio.I2C(board.SCL, board.SDA)

            self.sensor = adafruit_bme680.Adafruit_BME680_I2C(self.i2c, address=0x76)

            self.conn = sqlite3.connect('./air_quality.db',check_same_thread=False)
            self.cursor = self.conn.cursor()

            print("Sensor successfully initialized")

        except Exception as e:
            print("Error : ",e)
            self.sensor = None

    def read_data(self):
        if self.sensor is None:
            return None

        try:
            data = {
                "temperature": round(self.sensor.temperature, 2),
                "pressure": round(self.sensor.pressure, 2),
                "humidity": round(self.sensor.humidity, 2),
                "gas": round(self.sensor.gas, 2),
                "timestamp": self.sensor.timestamp
            }
            return data

        except Exception as e:
            print("Error : ",e)
            return None

