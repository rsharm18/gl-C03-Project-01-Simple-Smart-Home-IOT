import json
from typing import List

import paho.mqtt.client as mqtt

from contants.ActiveConstants import ActiveTopics, ActiveMessageStatus, ActiveDeviceTypes, \
    ActiveRooms
from model.Device_Input import Device_Input
from model.Device_Update_Model import Device_Update_Model
from model.Registration_Request import Registration_Request
from model.Update_Command_Result import Update_Command_Result

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
        # subscribe to all device/* topics
        client.subscribe("devices/#")

    # method to process the recieved messages and publish them on relevant topics 
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg):
        # print(msg.topic, msg.payload.decode('utf-8'), "retain", msg.retain, "qos", msg.qos, str(userdata))
        self.handle_topic(msg.topic, str(msg.payload.decode('utf-8')))

    # Returning the current registered list
    def get_registered_device_list(self):
        return self._registered_list

    ################ GET call(s) to get device status/values :: START ################

    # Getting the status for the connected devices
    def get_status(self):
        # get status for all registered devices
        for device in self.get_registered_device_list():
            self._get_device_status(device.device_id)

    def get_device_values_by_device_type(self, device_type: ActiveDeviceTypes):
        for device in self.get_registered_device_list():
            if device.device_type == device_type.name:
                self._get_device_status(device.device_id)

    def get_device_values_by_room(self, room: ActiveRooms):
        for device in self.get_registered_device_list():
            if device.room_type == room.value:
                self._get_device_status(device.device_id)

    def get_device_values_by_device_id(self, device_id):
        for device in self.get_registered_device_list():
            if device.device_id == device_id:
                self._get_device_status(device.device_id)
                break

    def _get_device_status(self, device_id):
        data = {
            'device_id': device_id
        }

        # request device status a message to device by publishing the data to a topic  with name starting with the device_id
        self.send_message_to_device(ActiveTopics.GET_DEVICE_STATUS_TOPIC_NAME.value.format(device_id),
                                    json.dumps(data), qos=0)

    ################ GET call(s) to get device status/values :: END ################

    ################ SET call(s) to set device status/values :: START ################
    def set_device_values__by_device_id(self, device_id, update_values: Device_Update_Model):
        # device = tuple(filter(lambda dev: dev.device_id == device_id, self.get_registered_device_list()))
        for device in self.get_registered_device_list():
            if device.device_id == device_id:
                self._set_device_status(device_id, update_values)
                break

    def set_device_values__by_device_type(self, device_type: ActiveDeviceTypes, update_values: Device_Update_Model):
        for device in self.get_registered_device_list():
            if device.device_type == device_type.name:
                self._set_device_status(device.device_id, update_values)

    def set_device_values__by_room(self, room: ActiveRooms, update_values: Device_Update_Model):
        for device in self.get_registered_device_list():
            if device.room_type == room.value:
                self._set_device_status(device.device_id, update_values)

    # Controlling and performing the operations on the devices
    # based on the request received
    def set_status(self, update_values: Device_Update_Model):
        for device in self.get_registered_device_list():
            self._set_device_status(device.device_id, update_values)


    def _set_device_status(self, device_id, update_values: Device_Update_Model):
        self.send_message_to_device(ActiveTopics.DEVICE_UPDATE_REQUEST_TOPIC_NAME.value.format(device_id),
                                    update_values.to_json(), qos=0)

    ################ SET call(s) to set device status/values :: START ################

    # handle different subscribed topics
    def handle_topic(self, topic_name, payload):
        if topic_name == ActiveTopics.DEVICE_REGISTER_REQUEST_TOPIC_NAME.value:
            self._device_registration_handler(Registration_Request.from_json(payload))
        elif topic_name == ActiveTopics.SEND_DEVICE_STATUS_TO_EDGE_TOPIC_NAME.value:
            self._process_device_status(payload)
        elif topic_name == ActiveTopics.DEVICE_UPDATE_COMMAND_RESULT_TOPIC_NAME.value:
            self._handle_device_update_ack(Update_Command_Result.from_json(payload))
        else:
            print(" {} topic is not supported! ".format(topic_name))

    # handle device registration request
    def _device_registration_handler(self, payload: Registration_Request):
        self._registered_list.append(payload)

        print("Registration request is acknowledged for device '{}' in {}".format(payload.device_id,payload.room_type))
        registration_confirmation: Device_Input = Device_Input(message='Registration Successful',
                                                               status=ActiveMessageStatus.SUCCESS.name)

        # send the registration confirmation to the registered device where topic name starts with the device_id
        self.send_message_to_device(
            ActiveTopics.SET_DEVICE_REGISTRATION_STATUS_TOPIC_NAME.value.format(payload.device_id),
            registration_confirmation.to_json())

        print("Request is processed for {}.".format(payload.device_id))

    # collects the device status
    def _process_device_status(self, data):
        data = json.loads(data)
        print("Here is the current device-status for {} : {}".format(data['device_id'], data))

    def send_message_to_device(self, topic_name, device_payload, qos=0):
        self.client.publish(topic_name, device_payload, qos)

    # track the device update status
    def _handle_device_update_ack(self, payload: Update_Command_Result):
        if payload.status == ActiveMessageStatus.FAILED.value:
            print(payload.payload)
