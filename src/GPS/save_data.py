import csv

def log_data(gas, temperature, pressure, humidity):
    with open('log_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([gas, temperature, pressure, humidity])