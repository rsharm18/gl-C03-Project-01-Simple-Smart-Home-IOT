import json
import random
import time
from functools import reduce
from typing import List

from ACDevice import AC_Device
from Automate_Execution import Automate_Execution
from EdgeServer import Edge_Server
from LightDevice import Light_Device
from contants.ActiveConstants import ActiveDeviceTypes, ActiveRooms, ActiveSwitchStatus, ActiveLightIntensity
from model.Device_Update_Model import Device_Update_Model
from util.Application_Util import Application_Util

WAIT_TIME = 0.25

print("\nSmart Home Simulation started.")
# Creating the edge-server for the communication with the user

# read from config.json. IT has the list of ac and device devices
f = open("config.json")
config = json.loads(f.read())
f.close()

SERVER_HOST = config['broker_host']
SERVER_PORT = config['broker_port']

edge_server_1 = Edge_Server('edge_server_1', SERVER_HOST, SERVER_PORT)
time.sleep(WAIT_TIME)

# Creating the light and ac devices
print("Initiate the device creation and registration process.")


# create and register the devices
light_device_list = []
ac_device_list = []

print("******************* REGISTRATION OF THE DEVICES THROUGH SERVER : START *******************")
for device in config['devices']:
    if device['device_type'] == 'LIGHT':
        light_device_list.append(
            Light_Device(device['device_id'], device['room_type'], SERVER_HOST, SERVER_PORT))
    elif device['device_type'] == 'AC':
        ac_device_list.append(
            AC_Device(device['device_id'], device['room_type'], SERVER_HOST, SERVER_PORT))
    else:
        print(" {} is not supported ".format(device))
    print()

time.sleep(WAIT_TIME)

print("******************* REGISTRATION OF THE DEVICES THROUGH SERVER : END *******************")
# get registered devices
registered_device_list = edge_server_1.get_registered_device_list()

print("\n\n\n")
exec_mode = 'A' #input("Select Mode! \n Enter \n A for automatic execution \n I for interactive (READ only) ")
while True:

    if exec_mode == 'A':
        automate_exec = Automate_Execution(edge_server_1, WAIT_TIME)
        automate_exec.execute()
        break
    elif exec_mode == 'I':
        break
    exec_mode = input("Select Mode! \n Enter \n A for automatic execution \n I for interactive ")

if exec_mode == 'I':
    mode = ''
    while mode != "Q":

        mode = input(
            "Enter \n 1 to get Status by Device Id \n 2 to get Status Device Type \n 3 to get Status by Room \n 4 to get Status for Entire Home \n Q to Quit \n ")

        if mode == "1":
            device_id = input("Enter Device Id. Valid ids are [{}] ".format(
                reduce(lambda x, y: x + " , " + y,
                       map(lambda x: x.device_id,
                           registered_device_list))))
            Application_Util.get_device_values_by_device_id(edge_server_1, WAIT_TIME, device_id, 0)
        if mode == "2":
            device_type = input("Enter 1 for Light and 2 for AC ")
            if device_type == "1":
                Application_Util.get_device_values_by_device_type(edge_server_1, WAIT_TIME,
                                                                  [ActiveDeviceTypes.LIGHT], 0)
            elif device_type == "2":
                Application_Util.get_device_values_by_device_type(edge_server_1, WAIT_TIME,
                                                                  [ActiveDeviceTypes.AC], 0)
            else:
                print("Invalid Selection")
        if mode == "3":
            device_type = input("Enter 1 for Kitchen , 2 for BR1, 3 for BR2, adn 4 for Living ")
            if device_type == "1":
                Application_Util.get_device_values_by_room_type(edge_server_1, WAIT_TIME,
                                                                [ActiveRooms.KITCHEN], 0)
            elif device_type == "2":
                Application_Util.get_device_values_by_room_type(edge_server_1, WAIT_TIME,
                                                                [ActiveRooms.BR1], 0)
            elif device_type == "3":
                Application_Util.get_device_values_by_room_type(edge_server_1, WAIT_TIME,
                                                                [ActiveRooms.BR2], 0)
            elif device_type == "4":
                Application_Util.get_device_values_by_room_type(edge_server_1, WAIT_TIME,
                                                                [ActiveRooms.LIVING], 0)
            else:
                print("Invalid Selection")
        if mode == "4":
            Application_Util.get_device_values_for_entire_home(edge_server_1, WAIT_TIME, 0)

print("\nSmart Home Simulation stopped.")

edge_server_1.terminate()
