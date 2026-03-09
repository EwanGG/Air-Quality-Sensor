from flask import Flask, request, jsonify

app = Flask(__name__)

'''This is the server for the application.
This server allows us to be able to add the functions for each
of the html pages and test them to make sure that they work
using the flask web framework'''

@app.route('/login', methods=['POST'])
def login():

    data = request.json
    username = data['username']
    password = data['password']

    if username == "raspberry" and password == "team17":
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "fail"})

app.run(host="0.0.0.0", port=5000)

@app.route('airdata')
def airdata():
    data = {
        "pm25": 12,
        "temperature": 23,
        "humidity": 40,
        "fan_speed": "medium"
    }
    return jsonify(data)