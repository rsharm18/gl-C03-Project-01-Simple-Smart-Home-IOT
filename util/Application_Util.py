import random
import time
from typing import List

from contants.ActiveConstants import ActiveSwitchStatus, ActiveLightIntensity
from model.Device_Update_Model import Device_Update_Model


class Application_Util:
    active_light_intensity: List[ActiveLightIntensity] = [ActiveLightIntensity.LOW,
                                                          ActiveLightIntensity.MEDIUM, ActiveLightIntensity.HIGH]

    @staticmethod
    def get_random_device_update_model():
        return Device_Update_Model(
            switch_status=ActiveSwitchStatus.ON.value,
            temperature=random.randint(18, 32),
            light_intensity=random.choice(Application_Util.active_light_intensity).value
        )

    @staticmethod
    def get_device_values_by_device_id(edge_server_1, WAIT_TIME, device_id, command_count):
        print("******************* GETTING THE STATUS BY DEVICE_ID *******************")

        print("Status based on device_id:")

        command_count += 1
        print("Command ID {} request is initiated.".format(command_count))
        edge_server_1.get_device_values_by_device_id(device_id=device_id)
        time.sleep(WAIT_TIME)
        print("Command ID {} request is executed.\n".format(command_count))
        command_count += 1

        return command_count

    @staticmethod
    def get_device_values_by_device_id_for_all_devices(edge_server_1, WAIT_TIME, registered_device_list, command_count):
        print("******************* GETTING THE STATUS BY DEVICE_ID *******************")

        print("Status based on device_id:")
        for device in registered_device_list:
            command_count += 1
            print("Command ID {} request is initiated.".format(command_count))
            edge_server_1.get_device_values_by_device_id(device_id=device.device_id)
            time.sleep(WAIT_TIME)
            print("Command ID {} request is executed.\n".format(command_count))
        command_count += 1

        return command_count

    @staticmethod
    def get_device_values_by_device_type(edge_server_1, WAIT_TIME, active_device_types, command_count):
        print("******************* GETTING THE STATUS BY DEVICE_TYPE *******************")

        for device_type in active_device_types:
            print("\n Status based on: {} DEVICE TYPE".format(device_type.name))
            print("Command ID {} request is initiated.".format(command_count))
            edge_server_1.get_device_values_by_device_type(device_type)
            time.sleep(WAIT_TIME)
            print("Command ID {} request is executed.\n".format(command_count))
            command_count += 1

        return command_count

    @staticmethod
    def get_device_values_by_room_type(edge_server_1, WAIT_TIME, active_rooms, command_count):
        print("\n******************* GETTING THE STATUS BY ROOM_TYPE *******************\n")
        for room in active_rooms:
            print("\n Status based on: {} ROOM_TYPE".format(room.name))
            print("Command ID {} request is initiated.".format(command_count))
            edge_server_1.get_device_values_by_room(room)
            time.sleep(WAIT_TIME)
            print("Command ID {} request is executed.\n".format(command_count))
            command_count += 1

        return command_count

    @staticmethod
    def get_device_values_for_entire_home(edge_server_1, WAIT_TIME, command_count):
        print("\n******************* GETTING THE STATUS BY ENTIRE_HOME *******************\n")
        print("\n Status based on room:")
        print("Command ID {} request is initiated.".format(command_count))
        edge_server_1.get_status()
        time.sleep(WAIT_TIME)
        print("Command ID {} request is executed.\n".format(command_count))
        command_count += 1

        return command_count

    @staticmethod
    def set_device_values_by_device_id(edge_server_1, WAIT_TIME, registered_device_list, command_count):
        print("\n Controlling the devices based on ID:")

        for device in registered_device_list:
            command_count += 1
            updated_status: Device_Update_Model = Application_Util.get_random_device_update_model()
            print("Command ID {} request is initiated.".format(command_count))
            edge_server_1.set_device_values__by_device_id(device_id=device.device_id, update_values=updated_status)
            time.sleep(WAIT_TIME)
            print("Command ID {} request is executed.\n".format(command_count))
        command_count += 1

        return command_count

    @staticmethod
    def set_device_values_by_device_type(edge_server_1, WAIT_TIME, active_device_types, command_count):
        print("******************* SETTING THE STATUS BY DEVICE_TYPE *******************")

        for device_type in active_device_types:
            updated_status: Device_Update_Model = Application_Util.get_random_device_update_model()
            print("Command ID {} request is initiated.".format(command_count))
            edge_server_1.set_device_values__by_device_type(device_type, updated_status)
            time.sleep(WAIT_TIME)
            print("Command ID {} request is executed.\n".format(command_count))
            command_count += 1

        return command_count

    @staticmethod
    def set_device_values_by_room_type(edge_server_1, WAIT_TIME, active_rooms, command_count):
        print("\nControlling the devices based on room:\n")
        for room in active_rooms:
            updated_status: Device_Update_Model = Application_Util.get_random_device_update_model()
            print("Command ID {} request is initiated.".format(command_count))
            edge_server_1.set_device_values__by_room(room, updated_status)
            time.sleep(WAIT_TIME)
            print("Command ID {} request is executed.\n".format(command_count))
            command_count += 1

        return command_count

    @staticmethod
    def set_device_values_for_entire_home(edge_server_1, WAIT_TIME, command_count):
        print("\n Status based on room:")
        updated_status: Device_Update_Model = Application_Util.get_random_device_update_model()
        print("Command ID {} request is initiated.".format(command_count))
        edge_server_1.set_status(updated_status)
        time.sleep(WAIT_TIME)
        print("Command ID {} request is executed.\n".format(command_count))
        command_count += 1

        return command_count

    @staticmethod
    def set_device_values_by_device_type_invalid_request(edge_server_1, WAIT_TIME, active_device_types, command_count):
        print("SETTING THE STATUS BY DEVICE_TYPE ")

        for device_type in active_device_types:
            updated_status: Device_Update_Model = Application_Util.get_random_device_update_model()
            # this should throw error as the temparature range is out of 18-32C
            updated_status._temperature = 200
            updated_status._light_intensity = "DUMMY-INCORRECT-VALUE"

            print("Command ID {} request is initiated.".format(command_count))
            edge_server_1.set_device_values__by_device_type(device_type, updated_status)
            time.sleep(WAIT_TIME)
            print("Command ID {} request is executed.\n".format(command_count))
            command_count += 1

        return command_count

    @staticmethod
    def get_current_setup_status(edge_server_1, WAIT_TIME, registered_device_list, command_count):
        print("Status based on device_id:")
        command_count += 1
        print("Command ID {} request is initiated.".format(command_count))
        for device in registered_device_list:
            edge_server_1.get_device_values_by_device_id(device_id=device.device_id)
            time.sleep(WAIT_TIME)

        print("Command ID {} request is executed.\n".format(command_count))
