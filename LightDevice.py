import datetime

import paho.mqtt.client as mqtt

HOST = "localhost"
PORT = 1883


class Light_Device():
    # Register topic name
    REGISTER_DEVICE_TOPIC_NAME = "devices/register"

    # setting up the intensity choices for Smart Light Bulb
    _INTENSITY = ["LOW", "HIGH", "MEDIUM", "OFF"]

    def __init__(self, device_id, room, publish_topic, server_host='localhost', server_port=1883):
        # Assigning device level information for each of the devices. 
        self._device_id = device_id
        self._room_type = room
        self._light_intensity = self._INTENSITY[0]
        self._device_type = "LIGHT"
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
        pass

    # Setting the the switch of devices
    def _set_switch_status(self, switch_state):
        pass

    # Getting the device intensity for the devices
    def _get_light_intensity(self):
        pass

    # Setting the device intensity for devices
    def _set_light_intensity(self, light_intensity):
        pass
