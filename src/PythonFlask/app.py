from flask import Flask, request, jsonify

try:
    import board
    import busio
    import adafruit_bme688

    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_bme688.Adafruit_BME680_I2C(i2c)

    REAL_SENSOR = True

except ImportError:
    print("Running in simulation mode (no sensor detected)")
    REAL_SENSOR = False

app = Flask(__name__)

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
    if REAL_SENSOR:
        data = {
            "gas": sensor.gas,
            "temperature": sensor.temperature,
            "humidity": sensor.humidity,
            "pressure": sensor.pressure,
        }
    else:
        # Fake data for testing
        data = {
            "pm25": 120,
            "temperature": 22.5,
            "humidity": 55,
            "pressure": 100,
        }
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)