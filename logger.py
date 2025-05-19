import csv
from datetime import datetime

def log_data(data, file_path="performance_log.csv"):
    fieldnames = data.keys()
    data["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(file_path, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow(data)
