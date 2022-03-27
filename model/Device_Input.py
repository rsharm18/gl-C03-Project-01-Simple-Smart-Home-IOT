from model.BaseModel import BaseModel


class Device_Input(BaseModel):
    def __init__(self, input_type, status, message, data=None):
        if data is None:
            data = {}
        self.input_type = input_type
        self.status = status
        self.message = message
        self.data = data
