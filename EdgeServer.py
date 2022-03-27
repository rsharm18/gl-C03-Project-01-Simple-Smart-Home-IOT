import paho.mqtt.client as mqtt

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
        print("Connected with result code " + str(result_code))
        client.subscribe("test")

    # method to process the recieved messages and publish them on relevant topics 
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg):
        print(msg.topic,str(msg.payload), "retain", msg.retain, "qos", msg.qos, str(userdata) )

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
