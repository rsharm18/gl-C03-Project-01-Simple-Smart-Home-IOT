import json
from collections import namedtuple


class BaseModel:

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def customRegistrationDecoder(registration_dict):
        return namedtuple('X', registration_dict.keys())(*registration_dict.values())

    @staticmethod
    def from_json(json_str):
        return json.loads(json_str, object_hook=BaseModel.customRegistrationDecoder)
