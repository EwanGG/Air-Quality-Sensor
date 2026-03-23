import time
from GPS.map import generate_map
from GPS.sensor import get_gps_data
from alert_system import send_email_alert, check_air_quality, trigger_alert

def start():

    print("Welcome to Air Quality Alert")
    print("Starting Air Quality Monitoring System")

    while True:
        # Get air quality reading
        gas_value = check_air_quality()

        # Get gps location
        latitude, longitude = get_gps_data()

        print(f"Gas value : {gas_value}")
        print(f"Location : {latitude}, {longitude}")

        if gas_value > 100000:

            trigger_alert(gas_value)
            send_email_alert(gas_value)

        generate_map() # generating the map

        time.sleep(10) # Wait before reading


if __name__ == "__main__":
    start()