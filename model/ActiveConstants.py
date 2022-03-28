import enum


class ActiveLightIntensity(enum.Enum):
    LOW = "LOW"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    OFF = "OFF"


class ActiveRooms(enum.Enum):
    KITCHEN = "Kitchen"
    BR1 = "BR1"
    BR2 = "BR2"
    LIVING = "Living"


class ActiveDeviceTypes(enum.Enum):
    AC = "AC"
    LIGHT = "LIGHT"


class ActiveTopics(enum.Enum):
    # topic to register a device in teh edge
    DEVICE_REGISTER_REQUEST_TOPIC_NAME = "devices/register-request"
    # topic to send device status to edge
    SEND_DEVICE_STATUS_TO_EDGE_TOPIC_NAME = "devices/device-status-response"
    # topic to send the device update command result
    DEVICE_UPDATE_COMMAND_RESULT_TOPIC_NAME = "devices/update-command-result"

    # topic to process edge response against the device's registration request
    SET_DEVICE_REGISTRATION_STATUS_TOPIC_NAME = "{}/register-response"
    # topic to request device status
    GET_DEVICE_STATUS_TOPIC_NAME = "{}/get-status"
    # topic to send update to a device
    DEVICE_UPDATE_REQUEST_TOPIC_NAME = "{}/update"


class ActiveMessageStatus(enum.Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class ActiveDeviceActionTypes(enum.Enum):
    REGISTRATION_RESPONSE = "REGISTRATION_RESPONSE"
    ACTION = "ACTION"


class SwitchStatus(enum.Enum):
    ON = 'ON'
    OFF = 'OFF'
