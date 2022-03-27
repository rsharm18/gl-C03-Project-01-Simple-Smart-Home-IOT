import datetime

import paho.mqtt.client as mqtt

HOST = "localhost"
PORT = 1883


class AC_Device():
    # Register topic name
    REGISTER_DEVICE_TOPIC_NAME = "devices/register"

    _MIN_TEMP = 18
    _MAX_TEMP = 32

    _VALID_SWITCH_STATUS = ['ON', 'OFF']


    def __init__(self, device_id, room, publish_topic, server_host='localhost', server_port=1883):

        self._device_id = device_id
        self._room_type = room
        self._temperature = 22
        self._device_type = "AC"
        self._device_registration_flag = False

        self._server_host = server_host
        self._server_port = server_port

        self._publish_topic = publish_topic

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
        payload = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "device_id": device_id,
            "device_type": device_type,
            "room_type": room_type
        }
        self.client.publish(self.REGISTER_DEVICE_TOPIC_NAME, payload)

    # Connect method to subscribe to various topics. 
    def _on_connect(self, client, userdata, flags, result_code):
        pass

    def _on_disconnect(self):
        pass

    # method to process the recieved messages and publish them on relevant topics
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg):
        pass

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
