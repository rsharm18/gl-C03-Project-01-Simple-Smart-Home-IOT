import json
import string

import paho.mqtt.client as mqtt

from model.ActiveConstants import ActiveTopics, ActiveMessageStatus, ActiveDeviceTypes, SwitchStatus
from model.Device_Input import Device_Input
from model.Device_Update_Model import Device_Update_Model
from model.Registration_Request import Registration_Request
from model.Update_Command_Result import Update_Command_Result

HOST = "localhost"
PORT = 1883


class AC_Device:
    _MIN_TEMP = 18
    _MAX_TEMP = 32

    def __init__(self, device_id, room, server_host='localhost', server_port=1883):

        self._device_id = device_id
        self._room_type = room
        self._temperature = 22
        self._device_type = ActiveDeviceTypes.AC.name
        self._device_registration_flag = False
        self._switch_status = SwitchStatus.OFF.value

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
        self._switch_status = switch_state
        self._send_local_device_status()

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
        if topic_name == ActiveTopics.SET_DEVICE_REGISTRATION_STATUS_TOPIC_NAME.value.format(self._device_id):
            self._handle_device_registration_response(Device_Input.from_json(payload))
        elif topic_name == ActiveTopics.GET_DEVICE_STATUS_TOPIC_NAME.value.format(self._device_id):
            self._send_local_device_status()
        elif topic_name == ActiveTopics.DEVICE_UPDATE_REQUEST_TOPIC_NAME.value.format(self._device_id):
            self._handle_device_status_update_request(Device_Update_Model.from_json(payload))
        else:
            print(" {} topic is not supported! ".format(topic_name))

    def _handle_device_registration_response(self, payload: Device_Input):
        if payload.status == ActiveMessageStatus.SUCCESS.name:
            self._device_registration_flag = True
            print("AC-DEVICE Registered! - Registration status is available for '{}' : True".format(self._device_id))
        else:
            self._device_registration_flag = False
            print("AC-DEVICE registration failed! Registration status is available for '{}' : False".format(
                self._device_id))

    def _send_local_device_status(self):
        data = {
            'device_id': self._device_id,
            'switch_state': self._switch_status,
            'temperature': self._temperature
        }
        # payload:Device_Input=Device_Input(input_type=ActiveDeviceActionTypes.STATUS)
        self.client.publish(ActiveTopics.SEND_DEVICE_STATUS_TO_EDGE_TOPIC_NAME.value, json.dumps(data))

    def _handle_device_status_update_request(self, update_values: Device_Update_Model):
        variables = vars(self)
        updated_variables = vars(update_values)
        update_dataset = {}
        for var, value in updated_variables.items():
            if (var in variables and value is not None):
                update_dataset[var] = value
                # self.__setattr__(var, value)


        error_list = self._validate_update_dataset(update_dataset)
        if (len(error_list) > 0):
            self._send_device_update_status(isError=True,payload=error_list)
        else:
            for key, value in update_dataset.items():
                self.__setattr__(key, value)
            self._send_device_update_status(isError=False)
        # print(self)
        # self._set_switch_status(data['switch_status'])
        self._send_local_device_status()

    def _send_device_update_status(self, isError=False, payload=None):
        if payload is None:
            payload = []
        data = Update_Command_Result(
            device_id=self._device_id,
            status=ActiveMessageStatus.FAILED.value if isError else ActiveMessageStatus.SUCCESS.value,
            payload=payload
        )
        self.client.publish(ActiveTopics.DEVICE_UPDATE_COMMAND_RESULT_TOPIC_NAME.value, data.to_json())

    def _validate_update_dataset(self, dataset=None):
        if dataset is None:
            dataset = {}
        error = []
        for key,value in dataset.items():
            error_string = self.__validate__(key,value)
            if(len(error_string)>0):
                error.append(error_string)
        return error

    def __validate__(self,variable,value)-> string:
        if variable == '_temperature' and  not (self._MIN_TEMP <= value <= self._MAX_TEMP):
            return " {} change Failed. Invalid {} value ({}) received.".format(variable[1:len(variable)],variable,value)
        return ""