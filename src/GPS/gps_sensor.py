import serial
import adafruit_gps
import glob
import time

class GPSSensor:
    def __init__(self, baudrate=9600):
        self.gps = None
        self.serial_port = None

        try:
            port = self.find_gps_port()
            if not port:
                raise Exception("No GPS device found")

            self.serial_port = serial.Serial(port, baudrate, timeout=1)
            self.gps = adafruit_gps.GPS(self.serial_port, debug=False)

            # Configure GPS output (RMC + GGA)
            self.gps.send_command(
                b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0'
            )

            # Set update rate to 1Hz
            self.gps.send_command(b'PMTK220,1000')

            print(f"GPS connected on {port}")

        except Exception as e:
            print("GPS init error:", e)
            self.gps = None

    def find_gps_port(self):
        """
        Try to automatically find GPS device
        """
        possible_ports = glob.glob('/dev/ttyACM*') + glob.glob('/dev/ttyUSB*')

        for port in possible_ports:
            try:
                ser = serial.Serial(port, 9600, timeout=1)
                time.sleep(1)

                if ser.in_waiting:
                    data = ser.readline().decode(errors='ignore')
                    if "$GP" in data or "$GN" in data:
                        ser.close()
                        return port

                ser.close()
            except:
                continue

        return None

    def get_data(self):
        if self.gps is None:
            return None

        try:
            # Call update multiple times to flush buffer
            for _ in range(5):
                self.gps.update()

            if not self.gps.has_fix:
                return None

            # Optional: require at least 3 satellites
            if self.gps.satellites is not None and self.gps.satellites < 3:
                return None

            lat = self.gps.latitude
            lon = self.gps.longitude

            if lat is None or lon is None:
                return None

            return {
                "latitude": round(lat, 6),
                "longitude": round(lon, 6)
            }

        except Exception as e:
            print("GPS read error:", e)
            return None