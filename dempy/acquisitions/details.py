from .devices.sensor import Sensor
from .. import _api_calls
from .subject.subject import Subject
from .devices.device import Device
import json

_ACQUISITION_ENDPOINT = "api/acquisitions/{acquisitionId}/"
_SUBJECT_ENDPOINT = "api/acquisitions/{acquisitionId}/subjects/"
_DEVICE_ENDPOINT = "api/acquisitions/{acquisitionId}/devices/"

""" def _get_subject(acquisitionId):
    return _api_calls.get(_SUBJECT_ENDPOINT.format(acquisitionId=acquisitionId)).json() """


def _delete_subject(acquisitionId, subejctId) -> None:
    _api_calls.delete(_SUBJECT_ENDPOINT.format(acquisitionId=acquisitionId) + subejctId)


def _create_subject(acquisitionId: str, subject: Subject) -> Subject:
    return _api_calls.put(_SUBJECT_ENDPOINT.format(acquisitionId=acquisitionId), json={**subject}).json(
        object_hook=lambda o: Subject(**o))


def _get_device(acquisitionId, deviceId) -> Device:  # object_hook=lambda o: Device(**o)
    return _api_calls.get(_DEVICE_ENDPOINT.format(acquisitionId=acquisitionId) + deviceId).json(cls=CustomDecoder)


def _create_device(acquisitionId: str, device: Device) -> Device:
    return _api_calls.post(_DEVICE_ENDPOINT.format(acquisitionId=acquisitionId), json={**device}).json(
        object_hook=lambda o: Device(**o))


"""def _modify_device(acquisitionId: str, deviceId : str, device: Device) -> Device:
    return _api_calls.put(_DEVICE_ENDPOINT.format(acquisitionId=acquisitionId), json={**device}).json(
        object_hook=lambda o: Device(**o))"""


def _delete_device(acquisitionId, deviceId) -> None:
    _api_calls.delete(_DEVICE_ENDPOINT.format(acquisitionId=acquisitionId) + deviceId)


def _get_device_usage(acquisitionId: str) -> Device:
    return _api_calls.get(_DEVICE_ENDPOINT.format(acquisitionId=acquisitionId) + "usage").json() #TODO: o que devolve isto?


class CustomDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if "type" not in obj:
            return obj

        type = obj["type"]

        if type == "Device":
            return Device(**obj)
        elif type == "Sensor":
            return Sensor(**obj)
        else:
            return obj