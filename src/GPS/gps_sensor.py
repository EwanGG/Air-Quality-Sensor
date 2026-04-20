def get_gps_data():

    try:
        import time
        import serial
        import pynmea2
        import adafruit_gps

        port = '/dev/ttyUSB0'

        ser = serial.Serial(port, baudrate=9600, timeout=30)

        gps = adafruit_gps.GPS(ser, debug=False)

        gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        gps.send_command(b'PMTK220,1000')

        start_time = time.monotonic()

        while time.monotonic() - start_time < 5:  # wait max 5 seconds
           gps.update()

           if gps.has_fix:
               return gps.latitude, gps.longitude

        return None

    except Exception as e:
        print("GPS Error:", e)
        return None, None