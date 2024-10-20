# from dronekit import connect, VehicleMode,APIException
# import time

# connection_string = 'COM6'


# baud_rate = 57600
# timeout_sec = 500
# heartbeat_timeout_sec = 60
# print(f"Connecting to vehicle on: {connection_string} with timeout: {timeout_sec} seconds and heartbeat timeout: {heartbeat_timeout_sec} seconds")
# try:
#     vehicle = connect(connection_string, wait_ready=True, baud=baud_rate, timeout=timeout_sec, heartbeat_timeout=heartbeat_timeout_sec)
# except APIException as e:
#     print(f"Failed to connect: {e}")
#     exit()

# # Function to print the current GPS location
# def print_gps_location():
#     gps = vehicle.location.global_frame
#     print(f"GPS Location: Lat: {gps.lat}, Lon: {gps.lon}, Alt: {gps.alt}")

# # Function to print all vehicle statuses
# def print_vehicle_status():
#     print(f"Mode: {vehicle.mode.name}")
#     print(f"Armed: {vehicle.armed}")
#     print(f"Battery: {vehicle.battery}")
#     print(f"Altitude: {vehicle.location.global_relative_frame.alt}")
#     print_gps_location()
#     print("")

# # Callback function to handle mode changes
# def mode_callback(self, attr_name, value):
#     print(f"Mode changed to: {value.name}")

# # Add a listener to mode attribute
# vehicle.add_attribute_listener('mode', mode_callback)

# # Spin motors at 5% throttle for 15 seconds
# def spin_motors():
#     print("Spinning motors at 5% throttle for 15 seconds...")
#     vehicle.armed = True
#     while not vehicle.armed:
#         vehicle.arm()
#         print(" Waiting for arming...")
#         time.sleep(1)
    
#     vehicle.mode = VehicleMode("GUIDED")
#     time.sleep(1)
    
#     vehicle.channels.overrides = {'3': 1000 + (1000 * 0.05)}  # 5% throttle
#     time.sleep(15)
#     vehicle.channels.overrides = {'3': 0}  # Stop motors
#     print("Stopped motors.")
    
#     vehicle.armed = False
#     while vehicle.armed:
#         print(" Waiting for disarming...")
#         time.sleep(1)

# # Main loop
# try:
#     while True:
#         print_vehicle_status()
#         time.sleep(5)  # Print status every 5 seconds

#         # For demonstration, spin motors once
#         spin_motors()
#         time.sleep(5)  # Wait for a while before next status print

# except KeyboardInterrupt:
#     print("Exiting...")

# finally:
#     vehicle.remove_attribute_listener('mode', mode_callback)
#     vehicle.close()
#     print("Disconnected from vehicle.")















from dronekit import connect, VehicleMode, APIException
import time


connection_string = 'COM6'
baud_rate = 57600
timeout_sec = 500
heartbeat_timeout_sec = 60
print(f"Connecting to vehicle on: {connection_string} with timeout: {timeout_sec} seconds and heartbeat timeout: {heartbeat_timeout_sec} seconds")
try:
    vehicle = connect(connection_string, wait_ready=True, baud=baud_rate, timeout=timeout_sec, heartbeat_timeout=heartbeat_timeout_sec)
except APIException as e:
    print(f"Failed to connect: {e}")
    exit()

def print_gps_location():
    gps = vehicle.location.global_frame
    print(f"GPS Location: Lat: {gps.lat}, Lon: {gps.lon}, Alt: {gps.alt}")


def print_vehicle_status():
    print(f"Mode: {vehicle.mode.name}")
    print(f"Armed: {vehicle.armed}")
    print(f"Battery: {vehicle.battery}")
    print(f"Altitude: {vehicle.location.global_relative_frame.alt}")
    print_gps_location()
    print("")

def mode_callback(self, attr_name, value):
    print(f"Mode changed to: {value.name}")

vehicle.add_attribute_listener('mode', mode_callback)

def spin_motors():
    print("Spinning motors at 40% throttle for 15 seconds...")
    vehicle.armed = True
    while not vehicle.armed:
        vehicle.arm()
        print(" Waiting for arming...")
        time.sleep(1)
    
    vehicle.mode = VehicleMode("GUIDED")
    time.sleep(1)
    
    vehicle.channels.overrides = {'3': int(1000 + (1000 * 4))} 
    time.sleep(15)
    vehicle.channels.overrides = {'3': 0}  
    print("Stopped motors.")
    
    vehicle.armed = False
    while vehicle.armed:
        print(" Waiting for disarming...")
        time.sleep(1)

try:
    while True:
        print_vehicle_status()
        time.sleep(2)  

        spin_motors()
        time.sleep(2) 

except KeyboardInterrupt:
    print("Exiting...")

finally:
    vehicle.remove_attribute_listener('mode', mode_callback)
    vehicle.close()
    print("Disconnected from vehicle.")
