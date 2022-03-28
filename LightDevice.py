import json
import string

import paho.mqtt.client as mqtt

from contants.ActiveConstants import ActiveTopics, ActiveMessageStatus, ActiveDeviceTypes, ActiveSwitchStatus, \
    ActiveLightIntensity
from model.Device_Input import Device_Input
from model.Device_Update_Model import Device_Update_Model
from model.Registration_Request import Registration_Request
from model.Update_Command_Result import Update_Command_Result

HOST = "localhost"
PORT = 1883


class Light_Device:
    def __init__(self, device_id, room, server_host='localhost', server_port=1883):
        # Assigning device level information for each of the devices. 
        self._device_id = device_id
        self._room_type = room
        self._light_intensity = ActiveLightIntensity.LOW.value
        self._device_type = ActiveDeviceTypes.LIGHT.name
        self._device_registration_flag = False
        self._switch_status = ActiveSwitchStatus.OFF.value
        self._server_host = server_host
        self._server_port = server_port

        # topic name format <device_id>/*
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
        # publish the register request message
        self.client.publish(ActiveTopics.DEVICE_REGISTER_REQUEST_TOPIC_NAME.value, registration.to_json())

    # Connect method to subscribe to various topics. 
    def _on_connect(self, client, userdata, flags, result_code):
        # print("light is Connected with result code " + str(result_code))
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

    # Getting the device intensity for the devices
    def _get_light_intensity(self):
        return self._light_intensity

    # Setting the device intensity for devices
    def _set_light_intensity(self, light_intensity):
        self._light_intensity = light_intensity

    # handle the device_specific messages
    def _handle_topic(self, topic_name, payload):
        if topic_name == ActiveTopics.SET_DEVICE_REGISTRATION_STATUS_TOPIC_NAME.value.format(self._device_id):
            self._handle_device_registration_response(Device_Input.from_json(payload))
        elif topic_name == ActiveTopics.GET_DEVICE_STATUS_TOPIC_NAME.value.format(self._device_id):
            self._send_local_device_status()
        elif topic_name == ActiveTopics.DEVICE_UPDATE_REQUEST_TOPIC_NAME.value.format(self._device_id):
            self._handle_device_status_update_request(Device_Input.from_json(payload))
        else:
            print(" {} topic is not supported! ".format(topic_name))

    # process the registration ack from edge
    def _handle_device_registration_response(self, payload: Device_Input):
        if payload.status == ActiveMessageStatus.SUCCESS.name:
            self._device_registration_flag = True
        else:
            self._device_registration_flag = False

        print("LIGHT-DEVICE Registered! - Registration status is available for '{}' : {}".format(self._device_id,self._device_registration_flag))

    # publish local device status to edge server
    def _send_local_device_status(self):
        data = {
            'device_id': self._device_id,
            'switch_state': self._switch_status,
            'intensity': self._light_intensity
        }
        self.client.publish(ActiveTopics.SEND_DEVICE_STATUS_TO_EDGE_TOPIC_NAME.value, json.dumps(data))

    # Handle device state update command from edge server
    def _handle_device_status_update_request(self, update_values: Device_Update_Model):

        # get the list of properties of the device
        variables = vars(self)

        # get the list of properties from the update model
        updated_variables = vars(update_values)

        update_dataset = {}
        # extract the fields that are relevant for the device and prepare the data set
        for var, value in updated_variables.items():
            if var in variables and value is not None:
                update_dataset[var] = value

        # validate the new data set
        error_list = self._validate_update_dataset(update_dataset)

        # if there is any validation error then send the update status as error and skip updating the object
        if len(error_list) > 0:
            self._send_device_update_status(isError=True, payload=error_list)
        else:
            # if there is no validation error then update the local device state and send the update status as success
            for key, value in update_dataset.items():
                self.__setattr__(key, value)

            # if the device status is OFF then set the light intensity as LOW as well
            if self._get_switch_status() == ActiveSwitchStatus.OFF.value and self._get_light_intensity() != ActiveLightIntensity.LOW.value:
                self._light_intensity(ActiveLightIntensity.LOW.value)

            # not sure if its needed - leaving it to showcase we can drive the device light intensity based on switch state
            # elif (self._get_switch_status() == ActiveSwitchStatus.ON.value and self._get_light_intensity() == ActiveSwitchStatus.OFF.value):
            #     self._light_intensity(ActiveLightIntensity.LOW.value)

            # send success device update command status
            self._send_device_update_status(isError=False)

        # send the device status to edge server
        self._send_local_device_status()

    # send the  device update command result to edge
    def _send_device_update_status(self, isError=False, payload=None):
        if payload is None:
            payload = []
        data = Update_Command_Result(
            device_id=self._device_id,
            status=ActiveMessageStatus.FAILED.value if isError else ActiveMessageStatus.SUCCESS.value,
            payload=payload
        )
        self.client.publish(ActiveTopics.DEVICE_UPDATE_COMMAND_RESULT_TOPIC_NAME.value, data.to_json())

    # validate the update dataset
    def _validate_update_dataset(self, dataset=None):
        if dataset is None:
            dataset = {}
        error = []
        for key, value in dataset.items():
            error_string = self.__validate__(key, value)
            if len(error_string) > 0:
                error.append(error_string)
        return error

    # validation local to the device
    def __validate__(self, variable, value) -> string:
        if (variable == '_light_intensity' and value not in ActiveLightIntensity.__members__):
            return " {} change Failed. Invalid {} value ({}) received.".format(variable[1:len(variable)], variable,
                                                                               value)
        return ""
