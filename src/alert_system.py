import smtplib
from email.mime.text import MIMEText
import time
try:
    import board
    import busio
    import adafruit_bme688

    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_bme688.Adafruit_BME680_I2C(i2c)

    SAFE_THRESHOLD = 100000  # Adjust after calibration
except ImportError:
    print("Running in simulation mode (no sensor detected)")

# Sending an email alert to the user

def send_email_alert(value):
    msg = MIMEText(f"Warning, Poor air quality detector.\nGas Value : {value}")
    msg['Subject'] = "Alert"
    msg['From'] = "email@gmail.com"
    msg['To'] = "recipient@gmail.com"

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(msg['From'], msg['To'])
        server.send_message(msg)

# Initializing the sensor

def check_air_quality():
    gas = sensor.gas
    print(f"Gas : {gas}")

    if gas > SAFE_THRESHOLD:
        print("Poor air quality detected")
        send_email_alert(gas)

def trigger_alert(value):
    print(f"⚠️ Warning : poor air quality detected.\nGas Value : {value}")
    print(f"Gas : {value}")
    send_email_alert(value)

while True:
    check_air_quality()
    time.sleep(10)