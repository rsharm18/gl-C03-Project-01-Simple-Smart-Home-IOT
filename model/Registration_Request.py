import datetime

from model.BaseModel import BaseModel


class Registration_Request(BaseModel):
    def __init__(self, device_id, room_type, device_type):
        self.device_id = device_id
        self.room_type = room_type
        self.device_type = device_type
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

    def __str__(self):
        return '[ Device Type: {}, Device Id: {}, assigned to room : {} Registered on {} ]'.format(self.device_type,
                                                                                                   self.device_id,
                                                                                                   self.room_type,
                                                                                                   self.timestamp)
