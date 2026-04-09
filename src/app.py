from flask import Flask, request, jsonify
from GPS.map import generate_map
from GPS.sensor import get_gps_data
from alert_system import send_email_alert, check_air_quality, trigger_alert
from sensors.bme688 import BME688Sensor
from flask_cors import CORS


sensor = BME688Sensor()

try:
    import time
    import board
    import busio
    import adafruit_bme680

    i2c = busio.I2C(board.SCL, board.SDA)

    sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c, address=0x76)

    REAL_SENSOR = True

except ImportError:
    print("Running in simulation mode (no sensor detected)")
    REAL_SENSOR = False

app = Flask(__name__)
CORS(app) # CORS support in case the flask server is not accessible from the browser
'''This is the server for the application.
This server allows us to be able to add the functions for each
of the html pages and test them to make sure that they work
using the flask web framework'''

# Initialize sensor

@app.route('/login', methods=['POST'])
def login():

    data = request.json
    username = data['username']
    password = data['password']

    if username == "raspberry" and password == "team17":
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "fail"})

@app.route("/air_data")
def air_data():
    data = sensor.read_data()

    if data is None:
        return jsonify({
            "temperature": 22.5,
            "humidity": 55,
            "pressure": 1000,
            "gas": 120
        })

    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=14473, debug=True)