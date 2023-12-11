import csv

import time
import logging
from datetime import datetime

import sys
sys.path.append("lib")

from arduino_iot_cloud import ArduinoCloudClient

DEVICE_ID = b"YOUR_DEVICE_KEY"
SECRET_KEY = b"YOUR_SECRET_KEY"

def logging_func():
    logging.basicConfig(
        datefmt="%H:%M:%S",
        format="%(asctime)s.%(msecs)03d %(message)s",
        level=logging.INFO,
    )

# This function reads the data.csv file, and returns an array of tuples
# The tuples contain the variable name and variable value

def read_csv_file(file_path):
    data_array = []  # Array to store (first_value, second_value) tuples
    
    try:
        with open(file_path, 'r') as file:
            # Create a CSV reader object
            reader = csv.reader(file)
            
            # Iterate through each row in the CSV file
            for row in reader:
                # Check if the row has at least two values
                if len(row) >= 2:
                    # Create a variable from the first value and assign it the value of the second value
                    first_value = row[0]
                    second_value = row[1]
                    
                    # Append a tuple (first_value, second_value) to the data_array
                    data_array.append((first_value, second_value))
                else:
                    print("Skipping row with insufficient values")
    
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return data_array

# Replace 'your_file.csv' with the actual path to your CSV file
result = read_csv_file('data.csv')

# Check number of rows in the data.csv file
length = len(result)

if __name__ == "__main__":

    logging_func()
    client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY)
    
    for i in range(length):
        # Access the tuples (variable name + value)
        var = result[i][0]
        val = result[i][1]
        
        client.register(var)
        client[var] = val

        print(f"{var} registered with value: {val}")

    client.start()