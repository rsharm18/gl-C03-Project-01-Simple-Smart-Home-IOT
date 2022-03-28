from model.BaseModel import BaseModel


class Device_Input(BaseModel):
    def __init__(self,  status, message, data=None):
        if data is None:
            data = {}
        self.status = status
        self.message = message
        self.data = data
