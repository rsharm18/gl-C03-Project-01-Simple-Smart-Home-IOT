import enum


class ActiveRooms(enum.Enum):
    KITCHEN = "Kitchen"
    BR1 = "BR1"
    BR2 = "BR2"
    LIVING = "Living"


class ActiveDeviceTypes(enum.Enum):
    AC = "AC"
    LIGHT = "LIGHT"


class ActiveTopics(enum.Enum):
    DEVICE_REGISTER_REQUEST_TOPIC_NAME = "devices/register-request"
    DEVICE_REGISTER_RESPONSE_TOPIC_NAME = "{}/register-response"
    DEVICE_STATUS_REQUEST_TOPIC_NAME = "{}/status-request"
    DEVICE_STATUS_RESPONSE_TOPIC_NAME = "devices/status-response"


class ActiveMessageStatus(enum.Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class ActiveDeviceActionTypes(enum.Enum):
    REGISTRATION_RESPONSE = "REGISTRATION_RESPONSE"
    ACTION = "ACTION"
