import json
from types import SimpleNamespace as Namespace


class BaseModel:
    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(json_str):
        return json.loads(json_str, object_hook=lambda d: Namespace(**d))
