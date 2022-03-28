import time
from functools import reduce
import random
from typing import List

from model.ActiveConstants import SwitchStatus, ActiveDeviceTypes, ActiveRooms, ActiveLightIntensity
from model.Device_Update_Model import Device_Update_Model
from util.Application_Util import Application_Util

active_device_types: List[ActiveDeviceTypes] = [ActiveDeviceTypes.LIGHT, ActiveDeviceTypes.AC]
active_rooms: List[ActiveRooms] = [ActiveRooms.KITCHEN, ActiveRooms.BR1, ActiveRooms.BR2, ActiveRooms.LIVING]
active_light_intensity: List[ActiveLightIntensity] = [ActiveLightIntensity.LOW,
                                                      ActiveLightIntensity.MEDIUM, ActiveLightIntensity.HIGH]


def get_random_device_update_model():
    return Device_Update_Model(
        switch_status=SwitchStatus.ON.value,
        temperature=random.randint(18, 32),
        light_intensity=random.choice(active_light_intensity).value
    )


class Automate_Execution:
    def __init__(self, edge_server_1, WAIT_TIME):
        self.edge_server_1 = edge_server_1
        self.WAIT_TIME = WAIT_TIME

    def execute(self):
        print("******************* REGISTERED DEVICES ON THE SERVER *******************")
        print("Fetching the list of registered devices from EdgeServer")

        registered_device_list = self.edge_server_1.get_registered_device_list()

        print("The Registered devices on Edge-Server:\n[ {} ]".format(
            reduce(lambda x, y: x + " , " + y,
                   map(lambda x: x.device_id,
                       registered_device_list))))

        time.sleep(self.WAIT_TIME)

        command_count = 0

        print("******************* GETTING THE STATUS AND CONTROLLING THE DEVICES *******************")
        command_count = Application_Util.get_device_values_by_device_id_for_all_devices(self.edge_server_1, self.WAIT_TIME,
                                                                                        registered_device_list, command_count)
        command_count = Application_Util.get_device_values_by_device_type(self.edge_server_1, self.WAIT_TIME,
                                                                          active_device_types, command_count)
        command_count = Application_Util.get_device_values_by_room_type(self.edge_server_1, self.WAIT_TIME,
                                                                        active_rooms, command_count)
        command_count = Application_Util.get_device_values_for_entire_home(self.edge_server_1, self.WAIT_TIME,
                                                                           command_count)

        print("\n******************* SETTING UP THE STATUS AND CONTROLLING THE DEVICE_ID *******************\n")
        command_count = Application_Util.set_device_values_by_device_id(self.edge_server_1, self.WAIT_TIME,
                                                                        registered_device_list, command_count)

        command_count = Application_Util.set_device_values_by_device_type(self.edge_server_1, self.WAIT_TIME,
                                                                          active_device_types, command_count)

        print("\n******************* SETTING UP THE STATUS AND CONTROLLING BY ROOM *******************\n")
        command_count = Application_Util.set_device_values_by_room_type(self.edge_server_1, self.WAIT_TIME,
                                                                        active_rooms, command_count)
        print("\n******************* SETTING THE STATUS BY ENTIRE_HOME *******************\n")
        command_count = Application_Util.get_device_values_for_entire_home(self.edge_server_1, self.WAIT_TIME,
                                                                           command_count)

        print("\n******************* SETTING UP THE STATUS AND CONTROLLING FOR INVALID REQUESTS *******************\n")
        command_count = Application_Util.set_device_values_by_device_type_invalid_request(self.edge_server_1,
                                                                                          self.WAIT_TIME,
                                                                                          active_device_types,
                                                                                          command_count)

        print("\n******************* CURRENT STATUS BEFORE CLOSING THE PROGRAM *******************\n")
        command_count = Application_Util.get_current_setup_status(self.edge_server_1, self.WAIT_TIME,
                                                                  registered_device_list, command_count)
