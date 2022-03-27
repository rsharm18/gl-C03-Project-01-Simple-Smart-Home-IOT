import json

import paho.mqtt.client as mqtt

from model.ActiveConstants import ActiveTopics, ActiveMessageStatus, ActiveDeviceTypes
from model.Device_Input import Device_Input
from model.Registration_Request import Registration_Request

HOST = "localhost"
PORT = 1883


class AC_Device():
    _MIN_TEMP = 18
    _MAX_TEMP = 32

    _VALID_SWITCH_STATUS = ['ON', 'OFF']

    def __init__(self, device_id, room, server_host='localhost', server_port=1883):

        self._device_id = device_id
        self._room_type = room
        self._temperature = 22
        self._device_type = ActiveDeviceTypes.AC.name
        self._device_registration_flag = False

        self._server_host = server_host
        self._server_port = server_port

        self._publish_topic = '{}/#'.format(device_id)

        self.client = mqtt.Client(self._device_id)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect
        self.client.connect(HOST, PORT, keepalive=60)
        self.client.loop_start()
        self._register_device(self._device_id, self._room_type, self._device_type)
        self._switch_status = "OFF"

    def __str__(self):
        return 'Device Type: {}, Id: {}, assigned to room : {}'.format(self._device_type, self._device_id,
                                                                       self._room_type)

    # calling registration method to register the device
    def _register_device(self, device_id, room_type, device_type):
        registration = Registration_Request(device_id, room_type, device_type)
        # publish the register message to
        self.client.publish(ActiveTopics.DEVICE_REGISTER_REQUEST_TOPIC_NAME.value, registration.to_json())

    # Connect method to subscribe to various topics. 
    def _on_connect(self, client, userdata, flags, result_code):
        # print("AC is Connected with result code " + str(result_code))
        client.subscribe(self._publish_topic)

    def _on_disconnect(self, user_data, rc):
        print("Disconnected with result code " + str(rc))

    # method to process the recieved messages and publish them on relevant topics
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg):
        # print("Received ", msg.topic, msg.payload.decode('utf-8'), "retain", msg.retain, "qos", msg.qos, str(userdata))
        self._handle_topic(msg.topic, msg.payload.decode('utf-8'))

    # Getting the current switch status of devices 
    def _get_switch_status(self):
        return self._switch_status

    # Setting the the switch of devices
    def _set_switch_status(self, switch_state):
        if (self._VALID_SWITCH_STATUS.index(switch_state) > -1):
            self._switch_status = switch_state
            print("{} is set to {} state ".format(self._device_id, self._switch_status))
        else:
            print("{} is an invalid state ".format(switch_state))

    # Getting the temperature for the devices
    def _get_temperature(self):
        return self._temperature

    # Setting up the temperature of the devices
    def _set_temperature(self, temperature):
        if (temperature >= self._MIN_TEMP and temperature <= self._MAX_TEMP):
            self._temperature = temperature
            print("{} is set to {} temperature ".format(self._device_id, self._temperature))
        else:
            print("{} is an invalid temperatue ".format(temperature))

    def _handle_topic(self, topic_name, payload):
        if topic_name == ActiveTopics.DEVICE_REGISTER_RESPONSE_TOPIC_NAME.value.format(self._device_id):
            self._handle_device_registration_response(Device_Input.from_json(payload))
        elif topic_name == ActiveTopics.DEVICE_STATUS_REQUEST_TOPIC_NAME.value.format(self._device_id):
            self._send_local_device_status()
        else:
            print(" {} topic is not supported! ".format(topic_name))

    def _handle_device_registration_response(self, payload: Device_Input):
        if payload.status == ActiveMessageStatus.SUCCESS.name:
            print("AC-DEVICE Registered! - Registration status is available for '{}' : True".format(self._device_id))
        else:
            print("AC-DEVICE registration failed! Registration status is available for '{}' : False".format(
                self._device_id))

    def _send_local_device_status(self):
        data = {
            'device_id': self._device_id,
            'switch_state': self._switch_status,
            'intensity': self._temperature
        }
        # payload:Device_Input=Device_Input(input_type=ActiveDeviceActionTypes.STATUS)
        self.client.publish(ActiveTopics.DEVICE_STATUS_RESPONSE_TOPIC_NAME.value, json.dumps(data))
