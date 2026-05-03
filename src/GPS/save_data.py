import csv
import os
from datetime import datetime

FILE_NAME = "log_data.csv"

def log_data(data):
    file_exists = os.path.isfile(FILE_NAME)

    with open(FILE_NAME, 'a', newline='') as file:
        writer = csv.writer(file)

        # Write the header once
        if not file_exists:
            writer.writerow([
                "timestamp",
                "temperature",
                "humidity",
                "pressure",
                "iaq",
                "co2",
                "voc",
                "latitude",
                "longitude"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data.get("temperature"),
            data.get("humidity"),
            data.get("pressure"),
            data.get("iaq"),
            data.get("co2"),
            data.get("voc"),
            data.get("latitude"),
            data.get("longitude")
        ])