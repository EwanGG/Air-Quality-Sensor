import serial
import adafruit_gps

class GPSSensor:
    def __init__(self, port='/dev/ttyACM0'):
        try:
            self.ser = serial.Serial(port, 9600, timeout=1)
            self.gps = adafruit_gps.GPS(self.ser, debug=False)

            # Configure GPS output
            self.gps.send_command(
                b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0'
            )
            self.gps.send_command(b'PMTK2C,1000')

            print("GPS connected")

        except Exception as e:
            print("GPS error : ",e)
            self.gps = None

    def get_data(self):
        if self.gps is None:
            return None

        try:
            self.gps.update()

            if self.gps.has_fixes:
                return self.gps.latitude, self.gps.longitude

        except Exception as e:
            print("GPS error : ",e)

        return None