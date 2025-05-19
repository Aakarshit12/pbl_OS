# Importing necessary modules
import csv  # For reading and writing CSV files
from datetime import datetime  # For getting the current timestamp

# Function to log performance or any kind of data into a CSV file
def log_data(data, file_path="performance_log.csv"):
    # Extract the keys from the data dictionary to use as CSV field names
    fieldnames = data.keys()

    # Add a timestamp entry to the data with the current date and time
    data["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Open the CSV file in append mode (creates the file if it doesn't exist)
    with open(file_path, "a", newline="") as csvfile:
        # Create a DictWriter object using the fieldnames from the data
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # If the file is empty, write the header first
        if csvfile.tell() == 0:
            writer.writeheader()
        
        # Write the data dictionary as a row in the CSV file
        writer.writerow(data)
