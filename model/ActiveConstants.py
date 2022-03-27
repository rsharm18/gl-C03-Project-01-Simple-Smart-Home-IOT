import enum


class ActiveTopics(enum.Enum):
    DEVICE_REGISTER_REQUEST_TOPIC_NAME = "devices/register-request"
    DEVICE_REGISTER_RESPONSE_TOPIC_NAME = "{}/register-response"



class ActiveMessageStatus(enum.Enum):
    SUCCESS = "SUCCESS",
    FAILED = "FAILED"


class ActiveDeviceActionTypes(enum.Enum):
    REGISTRATION_RESPONSE = "REGISTRATION_RESPONSE",
    ACTION = "ACTION"
