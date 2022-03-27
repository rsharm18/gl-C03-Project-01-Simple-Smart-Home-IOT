import json
import time
from functools import reduce
from typing import List

from ACDevice import AC_Device
from EdgeServer import Edge_Server
from LightDevice import Light_Device
from model.ActiveConstants import ActiveDeviceTypes, ActiveRooms

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
print("Intitate the device creation and registration process.")

active_device_types: List[ActiveDeviceTypes] = [ActiveDeviceTypes.LIGHT, ActiveDeviceTypes.AC]
active_rooms: List[ActiveRooms] = [ActiveRooms.KITCHEN, ActiveRooms.BR1, ActiveRooms.BR2, ActiveRooms.LIVING]

light_device_list = []
ac_device_list = []
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

# print(" ##### list of lights :  {} ".format(len(light_device_list)))
# for light in light_device_list:
#     print(light)

# print("\n ##### list of acs :  {} ".format(len(ac_device_list)))
# for ac in ac_device_list:
#     print(ac)

# time.sleep(20000)

# print("Registered Devices :")
# for registered_device in edge_server_1.get_registered_device_list():
#     print(registered_device)

print("******************* REGISTERED DEVICES ON THE SERVER *******************")
print("Fetching the list of registered devices from EdgeServer")

registered_device_list = edge_server_1.get_registered_device_list()

print("The Registered devices on Edge-Server:\n[ {} ]".format(
    reduce(lambda x, y: x + " , " + y,
           map(lambda x: x.device_id,
               registered_device_list))))

time.sleep(WAIT_TIME)

print("******************* GETTING THE STATUS AND CONTROLLING THE DEVICES *******************")
print("******************* GETTING THE STATUS BY DEVICE_ID *******************")

print("Status based on device_id:")
command_count = 0
for device in registered_device_list:
    command_count += 1
    print("Command ID {} request is intiated.".format(command_count))
    edge_server_1.get_status_by_device_id(device_id=device.device_id)
    time.sleep(WAIT_TIME)
    print("Command ID {} request is executed.\n".format(command_count))
command_count += 1
print("******************* GETTING THE STATUS BY DEVICE_TYPE *******************")

for device_type in active_device_types:
    print("\n Status based on: {} DEVICE TYPE".format(device_type.name))
    print("Command ID {} request is intiated.".format(command_count))
    edge_server_1.get_status_by_device_type(device_type)
    time.sleep(WAIT_TIME)
    print("Command ID {} request is executed.\n".format(command_count))
    command_count += 1
print("\n******************* GETTING THE STATUS BY ROOM_TYPE *******************\n")
for room in active_rooms:
    print("\n Status based on: {} ROOM_TYPE".format(room.name))
    print("Command ID {} request is intiated.".format(command_count))
    edge_server_1.get_status_by_room(room)
    time.sleep(WAIT_TIME)
    print("Command ID {} request is executed.\n".format(command_count))
    command_count += 1

print("\n******************* GETTING THE STATUS BY ENTIRE_HOME *******************\n")
print("\n Status based on room:")
print("Command ID {} request is intiated.".format(command_count))
edge_server_1.get_status()
time.sleep(WAIT_TIME)
print("Command ID {} request is executed.\n".format(command_count))
command_count += 1
# print("\n Status based on: AC DEVICE TYPE")
# print("Command ID {} request is intiated.".format(command_count))
# edge_server_1.get_status_by_device_type(ActiveDeviceTypes.AC)
# time.sleep(WAIT_TIME)
# print("Command ID {} request is executed.\n".format(command_count))
# mode = input(
#     "Enter \n 1 to get Status by Device Id \n 2 to get Status Device Type \n 3 to get Status by Room \n 4 to get Status for Entire Home \n Q to Quit \n "
# )
# while mode != "Q":
#     mode="Q"

print("\nSmart Home Simulation stopped.")

edge_server_1.terminate()
