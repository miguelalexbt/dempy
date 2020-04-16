import json

from typing import Union, List
from .acquisition import Acquisition
from .. import _api_calls
from .devices.device import Device
from .devices.sensor import Sensor
from .annotation.annotation import Annotation
from .subject.subject import Subject

_ENDPOINT = "api/acquisitions/"

def get(acquisitionId = None, datasetId = None, tags = []) -> Union[Acquisition, List[Acquisition]]:
    if acquisitionId is None:
        return _api_calls.get(_ENDPOINT, params={"datasetId": datasetId}).json(cls=CustomDecoder)
    else:
        return _api_calls.get(_ENDPOINT + acquisitionId).json(cls=CustomDecoder)

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (Acquisition, Subject, Device, Sensor)):
            return {**obj}
        else:
            return super().default(obj)

class CustomDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook = self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if "type" not in obj:
            return obj
        
        type = obj["type"]

        if type == "Acquisition":
            return Acquisition(**obj)
        elif type.endswith("Subject"):
            return Subject(**obj)
        elif type == "Device":
            return Device(**obj)
        elif type == "Sensor":
            return Sensor(**obj)
        else:
            return obj