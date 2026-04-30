import subprocess
import threading

class BME688Sensor:
    def __init__(self, binary_path="./bsec2_app"):
        self.process = None
        self.lock = threading.Lock()

        self.latest_data = {
            "temperature": None,
            "humidity": None,
            "pressure": None,
            "iaq": None,
            "co2": None,
            "voc": None
        }

        try:
            self.process = subprocess.Popen(
                [binary_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )

            print("BSEC2 process started")

        except Exception as e:
            print("BSEC2 error:", e)

    def read_data(self):
        if not self.process:
            return None

        try:
            line = self.process.stdout.readline()

            if not line:
                return None

            data = self._parse(line)

            if data:
                with self.lock:
                    self.latest_data = data

                return data

        except Exception as e:
            print("Read error:", e)

        return None

    def _parse(self, line):
        try:
            parts = line.strip().split(",")
            d = {}

            for p in parts:
                k, v = p.split(":")
                d[k] = float(v)

            return {
                "temperature": round(d["temp"], 2),
                "humidity": round(d["hum"], 2),
                "pressure": round(d["press"], 2),
                "iaq": round(d["iaq"], 2),
                "co2": round(d["co2"], 2),
                "voc": round(d["voc"], 2),
            }

        except:
            return None