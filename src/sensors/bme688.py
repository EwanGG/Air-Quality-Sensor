class BME688Sensor:
    def __init__(self):
        try:
            import time
            import board
            import busio
            import adafruit_bme680
            # Initialize I2C bus
            self.i2c = busio.I2C(board.SCL, board.SDA)

            # Initialize sensor
            self.sensor = adafruit_bme680.Adafruit_BME680_I2C(self.i2c, address=0x76)

            # Optional settings
            self.sensor.sea_level_pressure = 1013.25

            print("BME688 sensor initialized successfully")

            while True:
                print("Temperature : ", self.sensor.temperature)
                print("Pressure : ", self.sensor.pressure)
                print("Humidity : ", self.sensor.humidity)
                print("Gas : ", self.sensor.gas)
                print("------------------------------")

                time.sleep(2)

        except Exception as e:
            print("Error initializing BME688:", e)
            self.sensor = None

    def read_data(self):

        if self.sensor is None:
            return None

        try:
            data = {
                "temperature": self.sensor.temperature,
                "pressure": self.sensor.pressure,
                "humidity": self.sensor.humidity,
                "gas": self.sensor.gas,
            }
            return data

        except Exception as e:
            print("Error reading sensor:", e)
            return None

    def get_gas_resistance(self):

        data = self.read_data()

        if data is None:
            return data["gas_resistance"]

        return None
