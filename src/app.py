import threading
import time

from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO
from flask_cors import CORS

from GPS.gps_sensor import GPSSensor
from sensors.BME688 import BME688Sensor

# Flask setup
app = Flask(__name__)
CORS(app) # CORS support in case the flask server is not accessible from the browser
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# Sensor init
sensor = BME688Sensor()

gps_data = {"latitude": None, "longitude": None}
air_data = {"temperature": None, "humidity": None, "pressure": None, "gas": None}

# Background loops
def gps_loop():
    global gps_data

    while True:
        result = GPSSensor.get_data()

        if result:
            lat, lon = result
            gps_data = {"latitude": lat, "longitude": lon}

            socketio.emit("gps_data", gps_data)

        time.sleep(1)

def air_loop():

    global air_data

    while True:
        data = sensor.read_data()

        if data:
            air_data = data
            socketio.emit("air_data", air_data)

            print(data)

        time.sleep(1)

@app.route('/index', methods=['POST'])
def index():

    data = request.json
    username = data['username']
    password = data['password']

    if username == "raspberry" and password == "team17":
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "fail"})

@app.route('/')
def home():
    return render_template("airpurifier.html")

@app.route('/all_data')
def all_data():
    return jsonify({**air_data, **gps_data})

# Run app
if __name__ == "__main__":
    gps_thread = threading.Thread(target=gps_loop, daemon=True)
    air_thread = threading.Thread(target=air_loop, daemon=True)

    gps_thread.start()
    air_thread.start()

    socketio.run(app, host="0.0.0.0", port=14473, debug=True)