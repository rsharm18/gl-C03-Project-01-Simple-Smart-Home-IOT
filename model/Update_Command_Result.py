from model.BaseModel import BaseModel


class Update_Command_Result(BaseModel):
    def __init__(self, device_id, status, payload):
        self.device_id = device_id
        self.status = status
        self.payload = payload

