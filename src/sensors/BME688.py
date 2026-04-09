class BME688Sensor:
    def __init__(self):
        try:
            import board
            import busio
            import adafruit_bme680
            import subprocess

            self.i2c = busio.I2C(board.SCL, board.SDA)
            self.sensor = adafruit_bme680.Adafruit_BME680_I2C(self.i2c, address=0x76)
            self.sensor.sea_level_pressure = 1013.25

            print("BME688 sensor initialized successfully")

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
                "indoor air quality": round(self.sensor.indoor_air_quality, 2),
                "volatile organic compounds": round(self.sensor.volatile_organic_compounds, 2),
                "carbon dioxide": round(self.sensor.carbon_dioxide, 2)
            }
        except Exception as e:
            print("Error reading sensor:", e)
            return None