import json
import time

from ACDevice import AC_Device
from EdgeServer import Edge_Server
from LightDevice import Light_Device

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

light_device_list = []
ac_device_list = []
for device in config['devices']:
    if device['device_type'] == 'LIGHT':
        light_device_list.append(
            Light_Device(device['device_id'], device['room_type'],  SERVER_HOST, SERVER_PORT))
    elif device['device_type'] == 'AC':
        ac_device_list.append(
            AC_Device(device['device_id'], device['room_type'],  SERVER_HOST, SERVER_PORT))
    else:
        print(" {} is not supported ".format(device))

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

print("\nSmart Home Simulation stopped.")

edge_server_1.terminate()
