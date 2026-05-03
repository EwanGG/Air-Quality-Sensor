import subprocess
import threading
import os

class BME688Sensor:
    def __init__(self):
        self.process = None
        self.lock = threading.Lock()

        self.latest_data = {
            "temperature": None,
            "humidity": None,
            "pressure": None,
            "gas": None,
            "iaq": None,
            "co2": None,
            "voc": None
        }

        # Build absolute path to binary (always correct)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        binary_path = os.path.join(base_dir, "bsec2_app")

        print("Looking for binary at:", binary_path)

        try:
            # Optional: check if file exists first
            if not os.path.isfile(binary_path):
                raise FileNotFoundError(f"Binary not found at {binary_path}")

            # Optional: ensure executable permission
            if not os.access(binary_path, os.X_OK):
                raise PermissionError(f"Binary is not executable: {binary_path}")

            self.process = subprocess.Popen(
                [binary_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )

            print("BSEC2 process started successfully")

            # Start stderr reader thread
            threading.Thread(target=self._read_stderr, daemon=True).start()

        except Exception as e:
            print("BSEC2 error:", e)

    def _read_stderr(self):
        """Continuously read errors from the C program"""
        if self.process and self.process.stderr:
            for line in self.process.stderr:
                print("BSEC ERROR:", line.strip())

    def read_data(self):
        if not self.process:
            return None

        try:
            line = self.process.stdout.readline()

            if not line:
                return None

            print("RAW:", line.strip())

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
                if ":" not in p:
                    continue

                k, v = p.split(":")
                d[k] = float(v)

            return {
                "temperature": round(d.get("temp", 0), 2),
                "humidity": round(d.get("hum", 0), 2),
                "pressure": round(d.get("press", 0), 2),
                "gas": round(d.get("gas", 0), 2),
                "iaq": round(d.get("iaq", 0), 2),
                "co2": round(d.get("co2", 0), 2),
                "voc": round(d.get("voc", 0), 2),
            }

        except Exception as e:
            print("Parse error:", e)
            return None