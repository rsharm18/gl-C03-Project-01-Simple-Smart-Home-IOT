from model.BaseModel import BaseModel


class Device_Update_Model(BaseModel):
    def __init__(self, switch_status=None, light_intensity=None, temperature=None):
        self._light_intensity = light_intensity
        self._switch_status = switch_status
        self._temperature = temperature

    @property
    def switch_status(self):
        return self._switch_status
