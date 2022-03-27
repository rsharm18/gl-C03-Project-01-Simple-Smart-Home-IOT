import json
from typing import List

import paho.mqtt.client as mqtt

from model.ActiveConstants import ActiveTopics, ActiveDeviceActionTypes, ActiveMessageStatus, ActiveDeviceTypes, \
    ActiveRooms
from model.Device_Input import Device_Input
from model.Device_Update_Model import Device_Update_Model
from model.Registration_Request import Registration_Request

WAIT_TIME = 0.25


class Edge_Server:

    def __init__(self, instance_name, server_host='localhost', server_port=1883):
        self._instance_id = instance_name

        self._server_host = server_host
        self._server_port = server_port

        self.client = mqtt.Client(self._instance_id)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.connect(server_host, server_port, keepalive=60)
        self.client.loop_start()
        self._registered_list: List[Registration_Request] = []

    # Terminating the MQTT broker and stopping the execution
    def terminate(self):
        self.client.disconnect()
        self.client.loop_stop()

    # Connect method to subscribe to various topics.     
    def _on_connect(self, client, userdata, flags, result_code):
        # print("Edge Server is Connected with result code " + str(result_code))
        client.subscribe("devices/#")

    # method to process the recieved messages and publish them on relevant topics 
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg):
        # print(msg.topic, msg.payload.decode('utf-8'), "retain", msg.retain, "qos", msg.qos, str(userdata))
        self.handle_topic(msg.topic, str(msg.payload.decode('utf-8')))

    # Returning the current registered list
    def get_registered_device_list(self):
        return self._registered_list

    # Getting the status for the connected devices
    def get_status(self):
        for device in self.get_registered_device_list():
            self.get_device_values_by_device_id(device.device_id)

    def get_device_values_by_device_type(self, device_type: ActiveDeviceTypes):
        for device in self.get_registered_device_list():
            if device.device_type == device_type.name:
                self.get_device_values_by_device_id(device.device_id)

    def get_device_values_by_room(self, room: ActiveRooms):
        for device in self.get_registered_device_list():
            if device.room_type == room.value:
                self.get_device_values_by_device_id(device.device_id)

    def get_device_values_by_device_id(self, device_id):
        # device = tuple(filter(lambda dev: dev.device_id == device_id, self.get_registered_device_list()))
        for device in self.get_registered_device_list():
            if device.device_id == device_id:
                self._get_device_status(device.device_id)

    def set_device_values__by_device_id(self, device_id, update_values: Device_Update_Model):
        # device = tuple(filter(lambda dev: dev.device_id == device_id, self.get_registered_device_list()))
        for device in self.get_registered_device_list():
            if device.device_id == device_id:
                self._set_device_status(device_id, update_values)
                break

    def set_device_values__by_device_type(self, device_type: ActiveDeviceTypes,update_values: Device_Update_Model):
        for device in self.get_registered_device_list():
            if device.device_type == device_type.name:
                self.set_device_values__by_device_id(device.device_id,update_values)
                break;

    def set_device_values__by_room(self, room: ActiveRooms,update_values: Device_Update_Model):
        for device in self.get_registered_device_list():
            if device.room_type == room.value:
                self.set_device_values__by_device_id(device.device_id,update_values)
                break

    # Controlling and performing the operations on the devices
    # based on the request received
    def set_status(self,update_values: Device_Update_Model):
        for device in self.get_registered_device_list():
            self.set_device_values__by_device_id(device.device_id,update_values)

    def handle_topic(self, topic_name, payload):
        if topic_name == ActiveTopics.DEVICE_REGISTER_REQUEST_TOPIC_NAME.value:
            self._device_registration_handler(Registration_Request.from_json(payload))
        elif topic_name == ActiveTopics.DEVICE_STATUS_RESPONSE_TOPIC_NAME.value:
            self._process_device_status(payload)
        else:
            print(" {} topic is not supported! ".format(topic_name))

    def _device_registration_handler(self, payload: Registration_Request):
        # print("Registration request is acknowledged for device '{}' in {}".format(payload.device_id, payload.room_type))
        self._registered_list.append(payload)
        registration_confirmation: Device_Input = Device_Input(
            input_type=ActiveDeviceActionTypes.REGISTRATION_RESPONSE.value, message='Registration Successful',
            status=ActiveMessageStatus.SUCCESS.name)
        self.send_message_to_device(ActiveTopics.DEVICE_REGISTER_RESPONSE_TOPIC_NAME.value.format(payload.device_id),
                                    registration_confirmation.to_json())
        print("Request is processed for {}.".format(payload.device_id))

    def _get_device_status(self, device_id):
        data = {
            'device_id': device_id
        }
        self.send_message_to_device(ActiveTopics.DEVICE_STATUS_REQUEST_TOPIC_NAME.value.format(device_id),
                                    json.dumps(data), qos=0)

    def _set_device_status(self, device_id, update_values: Device_Update_Model):
        self.send_message_to_device(ActiveTopics.DEVICE_STATUS_UPDATE_REQUEST_TOPIC_NAME.value.format(device_id),
                                    update_values.to_json(), qos=0)

    def _process_device_status(self, data):
        data = json.loads(data)
        print("Here is the current device-status for {} : {}".format(data['device_id'], data))

    def send_message_to_device(self, topic_name, device_payload, qos=0):
        self.client.publish(topic_name, device_payload, qos)
