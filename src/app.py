import random
import threading
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO
from GPS.sensor import get_gps_data
from sensors.BME688 import BME688Sensor
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
socketio = SocketIO(app, cors_allowed_origins="*")
# Initialize sensor

@app.route('/index', methods=['POST'])
def index():

    data = request.json
    username = data['username']
    password = data['password']

    if username == "raspberry" and password == "team17":
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "fail"})

@app.route("/air_data")
def air_data():

    while True:

        data = {
            "temperature": round(random.uniform(20, 30), 2),
            "humidity": round(random.uniform(40, 70), 2),
            "pressure": round(random.uniform(1000, 1025), 2),
            "gas": round(random.uniform(200, 400), 2)
        }

        socketio.emit("air_data", data)
        time.sleep(1)

        if data is None:
            return jsonify({
                "temperature": 22.5,
                "humidity": 55,
                "pressure": 1000,
                "gas": 120
            })
        return jsonify({}) and render_template("airpurifier.html")

if __name__ == "__main__":
    thread = threading.Thread(target=get_gps_data()).start()
    thread.daemon = True
    thread.start()
    socketio.run(app, host="0.0.0.0", port=14473, debug=True)