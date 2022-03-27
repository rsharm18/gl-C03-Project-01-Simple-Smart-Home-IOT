import paho.mqtt.client as mqtt

from model.ActiveConstants import ActiveTopics, ActiveDeviceActionTypes, ActiveMessageStatus
from model.Device_Input import Device_Input
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
        self._registered_list = []

    # Terminating the MQTT broker and stopping the execution
    def terminate(self):
        self.client.disconnect()
        self.client.loop_stop()

    # Connect method to subscribe to various topics.     
    def _on_connect(self, client, userdata, flags, result_code):
        print("Edge Server is Connected with result code " + str(result_code))
        client.subscribe("devices/#")

    # method to process the recieved messages and publish them on relevant topics 
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg):
        print(msg.topic, msg.payload.decode('utf-8'), "retain", msg.retain, "qos", msg.qos, str(userdata))
        self.handle_topic(msg.topic, msg.payload.decode('utf-8'))

    # Returning the current registered list
    def get_registered_device_list(self):
        return self._registered_list

    # Getting the status for the connected devices
    def get_status(self):
        pass

    # Controlling and performing the operations on the devices
    # based on the request received
    def set(self):
        pass

    def handle_topic(self, topic_name, payload):
        if topic_name == ActiveTopics.DEVICE_REGISTER_REQUEST_TOPIC_NAME.value:
            self.device_registration_handler(Registration_Request.from_json(payload))
        else:
            print(" {} topic is not supported! ".format(topic_name))

    def device_registration_handler(self, payload: Registration_Request):
        self._registered_list.append(payload)
        registration_confirmation: Device_Input = Device_Input(
            input_type=ActiveDeviceActionTypes.REGISTRATION_RESPONSE.value, message='Registration Successful',
            status=ActiveMessageStatus.SUCCESS.value)
        self.send_message_to_device(ActiveTopics.DEVICE_REGISTER_RESPONSE_TOPIC_NAME.value.format(payload.device_id), registration_confirmation)

    def send_message_to_device(self, topic_name, device_payload: Device_Input):
        self.client.publish(topic_name, device_payload.to_json())
