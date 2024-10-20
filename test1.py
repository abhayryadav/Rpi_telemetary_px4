#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
© Copyright 2015-2016, 3D Robotics.
vehicle_state.py:

Demonstrates how to get and set vehicle state and parameter information,
and how to observe vehicle attribute (state) changes.

Full documentation is provided at http://python.dronekit.io/examples/vehicle_state.html
"""
from collections.abc import MutableMapping

from dronekit import connect, VehicleMode, LocationGlobalRelative, APIException
import time
from collections.abc import MutableMapping
import socket
import exceptions  # This line seems unnecessary. Python's built-in exceptions are available without import.
import math
import argparse  # Corrected import statement.

def connectMyCopter():
    parser = argparse.ArgumentParser(description='commands')  # Corrected assignment operator.
    parser.add_argument('--connect')
    args = parser.parse_args()  # Corrected assignment operator.
    connection_string = args.connect  # Corrected assignment operator.
    baud_rate = 57600  # You didn't define baud_rate, so I'm adding it here.
    vehicle = connect(connection_string, baud=baud_rate, wait_ready=True)  # Corrected arguments and assignment.
    return vehicle

def arm(vehicle):
    while not vehicle.is_armable:  # Changed 'is armable' to 'is_armable'.
        print("Waiting for vehicle to become armable...")
        time.sleep(1)
    print("Vehicle is now armable.")

    print("")

    vehicle.armed = True  # Changed 'armed' to 'vehicle.armed'.

    while not vehicle.armed:  # Changed 'armed' to 'vehicle.armed'.
        print("Waiting for drone to become armed...")
        time.sleep(1)
    print("Vehicle is now armed.")
    print("Propellers are spinning. LOOK OUT!!!")

    return None

vehicle = connectMyCopter()
arm()



# Get all vehicle attributes (state)
print("\nGet all vehicle attribute values:")
print(" Autopilot Firmware version: %s" % vehicle.version)
print("   Major version number: %s" % vehicle.version.major)
print("   Minor version number: %s" % vehicle.version.minor)
print("   Patch version number: %s" % vehicle.version.patch)
print("   Release type: %s" % vehicle.version.release_type())
print("   Release version: %s" % vehicle.version.release_version())
print("   Stable release?: %s" % vehicle.version.is_stable())
print(" Autopilot capabilities")
print("   Supports MISSION_FLOAT message type: %s" % vehicle.capabilities.mission_float)
print("   Supports PARAM_FLOAT message type: %s" % vehicle.capabilities.param_float)
print("   Supports MISSION_INT message type: %s" % vehicle.capabilities.mission_int)
print("   Supports COMMAND_INT message type: %s" % vehicle.capabilities.command_int)
print("   Supports PARAM_UNION message type: %s" % vehicle.capabilities.param_union)
print("   Supports ftp for file transfers: %s" % vehicle.capabilities.ftp)
print("   Supports commanding attitude offboard: %s" % vehicle.capabilities.set_attitude_target)
print("   Supports commanding position and velocity targets in local NED frame: %s" % vehicle.capabilities.set_attitude_target_local_ned)
print("   Supports set position + velocity targets in global scaled integers: %s" % vehicle.capabilities.set_altitude_target_global_int)
print("   Supports terrain protocol / data handling: %s" % vehicle.capabilities.terrain)
print("   Supports direct actuator control: %s" % vehicle.capabilities.set_actuator_target)
print("   Supports the flight termination command: %s" % vehicle.capabilities.flight_termination)
print("   Supports mission_float message type: %s" % vehicle.capabilities.mission_float)
print("   Supports onboard compass calibration: %s" % vehicle.capabilities.compass_calibration)
print(" Global Location: %s" % vehicle.location.global_frame)
print(" Global Location (relative altitude): %s" % vehicle.location.global_relative_frame)
print(" Local Location: %s" % vehicle.location.local_frame)
print(" Attitude: %s" % vehicle.attitude)
print(" Velocity: %s" % vehicle.velocity)
print(" GPS: %s" % vehicle.gps_0)
print(" Gimbal status: %s" % vehicle.gimbal)
print(" Battery: %s" % vehicle.battery)
print(" EKF OK?: %s" % vehicle.ekf_ok)
print(" Last Heartbeat: %s" % vehicle.last_heartbeat)
print(" Rangefinder: %s" % vehicle.rangefinder)
print(" Rangefinder distance: %s" % vehicle.rangefinder.distance)
print(" Rangefinder voltage: %s" % vehicle.rangefinder.voltage)
print(" Heading: %s" % vehicle.heading)
print(" Is Armable?: %s" % vehicle.is_armable)
print(" System status: %s" % vehicle.system_status.state)
print(" Groundspeed: %s" % vehicle.groundspeed)    # settable
print(" Airspeed: %s" % vehicle.airspeed)    # settable
print(" Mode: %s" % vehicle.mode.name)    # settable
print(" Armed: %s" % vehicle.armed)    # settable

print("Completed")
exit()
