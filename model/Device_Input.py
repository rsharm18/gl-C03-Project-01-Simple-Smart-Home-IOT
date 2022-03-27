from model.BaseModel import BaseModel


class Device_Input(BaseModel):
    def __init__(self, input_type, status, message, data=None):
        if data is None:
            data = {}
        self._input_type = input_type
        self._status = status
        self._message = message
        self._data = data

    @property
    def status(self):
        return self._status
