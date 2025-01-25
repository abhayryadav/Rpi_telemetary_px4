# import serial
# import time

# # Replace with the correct serial port found earlier
# serial_port = '/dev/ttyS0'  # Change this if necessary
# baud_rate = 115200

# try:
#     ser = serial.Serial(serial_port, baud_rate, timeout=1)
#     print(f"Connected to {serial_port} at {baud_rate} baud rate.")
    
#     # Allow some time for the connection to establish
#     time.sleep(2)  # Give some time for the connection to settle

#     print("Listening for data from ESP8266...")
#     while True:
#         if ser.in_waiting > 0:
#             try:
#                 line = ser.readline().decode('utf-8').strip()  # Read a line from the serial port
#                 if line:  # Check if the line is not empty
#                     print(f"Received data: {line}")
#             except UnicodeDecodeError as e:
#                 print(f"Failed to decode line: {e}")  # Handle decoding issues
# except serial.SerialException as e:
#     print(f"Serial error: {e}")
# except Exception as e:
#     print(f"Error: {e}")









# import requests
# import RPi.GPIO as GPIO
# import time

# SERVER_URL = "http://192.168.29.221:4000/api/dronesensing"

# # GPIO Configuration
# GPIO_PIN = 4  # Use GPIO pin 4
# GPIO.setmode(GPIO.BCM)  # Set the GPIO mode to BCM
# GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set the pin as input with pull-down resistor

# # State token
# token = False

# def get_data_from_server():
#     try:
#         response = requests.get(SERVER_URL)
#         if response.status_code == 200:
#             return response.json()  # Return the JSON response
#         elif response.status_code == 404:
#             print("No earthquake data available.")
#         else:
#             print(f"Error on HTTP request: {response.status_code}")
#     except requests.RequestException as e:
#         print(f"Request error: {e}")
#     return None

# try:
#     print("Waiting for a HIGH signal on GPIO pin 4...")

#     while True:
#         gpio_state = GPIO.input(GPIO_PIN)

#         # Check for a stable HIGH signal
#         if gpio_state == GPIO.HIGH:
#             if not token:  # Only proceed if token is False (i.e., no request has been sent)
#                 print("Detected HIGH signal, waiting for stability...")
#                 time.sleep(0.1)  # Small delay to allow for stabilization
#                 if GPIO.input(GPIO_PIN) == GPIO.HIGH:  # Check if the signal is still HIGH
#                     print("Signal stable, sending request to server...")
#                     data = get_data_from_server()
                    
#                     if data is not None:
#                         print(f"Server Response: {data}")

#                         # Process the server response
#                         print("Earthquake detected and marked as false.")
#                         token = True  # Set the token to true to prevent further requests
#                         print(f"Signal sent to Raspberry Pi: {data}")

#         else:
#             token = False  # Reset the token when the signal goes LOW

#         time.sleep(0.1)  # Avoid too fast loop checks

# except KeyboardInterrupt:
#     print("Script terminated by user.")

# finally:
#     GPIO.cleanup()  # Clean up the GPIO pins





import requests
import RPi.GPIO as GPIO
import time
import socket

# Server URL
SERVER_URL = "http://192.168.29.221:4000/api/dronesensing"

# GPIO Configuration
GPIO_PIN = 4  # Use GPIO pin 5 (D1 equivalent)
GPIO.setmode(GPIO.BCM)  # Set the GPIO mode to BCM
GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set the pin as input with pull-down

# State token
token = False

# Debounce variables
DEBOUNCE_TIME = 0.2  # Time in seconds to consider the signal stable
last_state = GPIO.LOW  # Last known state of the GPIO pin
last_time = time.time()  # Last time the state was checked

# Function to get data from the server
def get_data_from_server():
    try:
        response = requests.get(SERVER_URL)
        if response.status_code == 200:
            return response.json()  # Return the JSON response
        elif response.status_code == 404:
            print("No earthquake data available.")
        else:
            print(f"Error on HTTP request: {response.status_code}")
    except requests.RequestException as e:
        print(f"Request error: {e}")
    return None

# Function to send data to the drone control script
def send_data_to_drone(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 65432))  # Change the host and port as necessary
        s.sendall(str(data).encode())  # Send the data as bytes

try:
    while True:
        current_time = time.time()
        gpio_state = GPIO.input(GPIO_PIN)

        # Check if the GPIO state has changed
        if gpio_state != last_state:
            last_time = current_time  # Reset the timer

        # If the state has been stable for DEBOUNCE_TIME seconds
        if (current_time - last_time) >= DEBOUNCE_TIME:
            if gpio_state == GPIO.HIGH and not token:
                # Signal is stable and high, proceed with the request
                data = get_data_from_server()
                if data is not None:
                    print(f"Server Response: {data}")
                    print("Earthquake detected and marked as false.")
                    token = True  # Set the token to true to prevent further requests
                    send_data_to_drone(data)  # Send data to the drone control script

            # Reset the token when the signal goes LOW again
            if gpio_state == GPIO.LOW:
                token = False

        last_state = gpio_state  # Update the last known state
        time.sleep(0.01)  # Small delay to avoid busy-waiting

except KeyboardInterrupt:
    print("Script terminated by user.")
finally:
    GPIO.cleanup()  # Clean up the GPIO pins
