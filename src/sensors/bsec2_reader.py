def read_data(self):
    if self.process is None:
        return None

    try:
        line = self.process.stdout.readline().strip()

        if not line:
            return None

        parts = line.split(",")

        return {
            "iaq": float(parts[0].split(":")[1]),
            "co2": float(parts[1].split(":")[1]),
            "voc": float(parts[2].split(":")[1]),
        }
    except Exception as e:
        print("Error reading data/BSEC2:", e)
        return None