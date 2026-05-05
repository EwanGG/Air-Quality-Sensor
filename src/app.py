import time

from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO
from flask_cors import CORS

from GPS.gps_sensor import GPSSensor
from GPS.save_data import log_data
from sensors.BME688 import BME688Sensor
from data.database import insert_data

# ----------Flask setup----------
app = Flask(__name__)
CORS(app) # CORS support in case the flask server is not accessible from the browser

socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# ----------Sensors----------
air_sensor = BME688Sensor()
gps_sensor = GPSSensor()

gps_data = {"latitude": None,
            "longitude": None}
air_data = {"temperature": None,
            "humidity": None,
            "pressure": None,
            "gas": None,
            "iaq": None,
            "co2": None,
            "voc": None}

# ----------Air Quality loop----------
def air_loop():

    global air_data, gps_data

    while True:
        air = air_sensor.read_data()
        gps = gps_sensor.get_data()

        if air is not None:
            air_data = air

        if gps is not None:
            gps_data = gps

        combined = {
            **air_data,
            **gps_data
        }

        print("COMBINED", combined)

        # Save to CSV
        log_data(combined)

        # Save to db
        insert_data(combined)

        socketio.emit("air_data", combined)

        time.sleep(5)


# ----------Routes----------
@app.route('/index', methods=['POST'])
def index():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    if username == "raspberry" and password == "team17":
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "fail"})

@app.route('/airpurifier')
def airpurifier():
    return render_template("airpurifier.html")

@app.route('/all_data')
def all_data():
    return jsonify({
        **air_data,
        **gps_data
    })

@app.route('/history')
def history():
    import sqlite3
    conn = sqlite3.connect('./air_quality.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM air_data ORDER BY timestamp DESC LIMIT 50")
    rows = cursor.fetchall()

    conn.close()

    return jsonify(rows)

# ----------Run app----------
if __name__ == "__main__":

    socketio.start_background_task(air_loop)

    socketio.run(app, host="0.0.0.0", port=14473, debug=False, use_reloader=False)