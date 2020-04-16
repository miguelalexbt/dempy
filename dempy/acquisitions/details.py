from typing import List

from .devices.sensor import Sensor
from .. import _api_calls
from .subject.subject import Subject
from .devices.device import Device
from .sample.image_samples import ImageSample
from .sample.video_samples import VideoSample
from .annotation.annotation import Annotation
from .sample.timeseries_samples import TimeSeriesSample
import json

_ACQUISITION_ENDPOINT = "api/acquisitions/{acquisitionId}/"
_SUBJECT_ENDPOINT = "api/acquisitions/{acquisitionId}/subjects/"
_DEVICE_ENDPOINT = "api/acquisitions/{acquisitionId}/devices/"
_TIMESERIES_SAMPLE_ENDPOINT = "api/acquisitions/{acquisitionId}/samples/timeseries/"
_VIDEO_SAMPLE_ENDPOINT = "api/acquisitions/{acquisitionId}/samples/videos/"
_IMAGE_SAMPLE_ENDPOINT = "api/acquisitions/{acquisitionId}/samples/images/"
_ANNOTATIONS_ENDPOINT = "api/acquisitions/{acquisitionId}/annotations/"

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
    return _api_calls.get(
        _DEVICE_ENDPOINT.format(acquisitionId=acquisitionId) + "usage").json()  # TODO: o que devolve isto?


def _get_timeseries_samples(acquisitionId) -> List[TimeSeriesSample]:
    return _api_calls.get(_TIMESERIES_SAMPLE_ENDPOINT.format(acquisitionId=acquisitionId)).json(cls=CustomDecoder)

def _get_timeseries_samples_count(acquisitionId) -> int:
    return _api_calls.get(_TIMESERIES_SAMPLE_ENDPOINT.format(acquisitionId=acquisitionId) + "count").json()


def _get_video_samples(acquisitionId) -> List[VideoSample]:
    return _api_calls.get(_VIDEO_SAMPLE_ENDPOINT.format(acquisitionId=acquisitionId)).json(cls=CustomDecoder)

def _get_video_samples_count(acquisitionId) -> int:
    return _api_calls.get(_VIDEO_SAMPLE_ENDPOINT.format(acquisitionId=acquisitionId) + "count").json()


def _get_image_samples(acquisitionId) -> List[ImageSample]:
    return _api_calls.get(_IMAGE_SAMPLE_ENDPOINT.format(acquisitionId=acquisitionId)).json(cls=CustomDecoder)

def _get_image_samples_count(acquisitionId) -> int:
    return _api_calls.get(_IMAGE_SAMPLE_ENDPOINT.format(acquisitionId=acquisitionId) + "count").json()


def _get_annotations(acquisitionId) -> List[Annotation]:
    return _api_calls.get(_ANNOTATIONS_ENDPOINT.format(acquisitionId=acquisitionId)).json(cls=CustomDecoder)

def _get_annotations_count(acquisitionId) -> int:
    return _api_calls.get(_ANNOTATIONS_ENDPOINT.format(acquisitionId=acquisitionId) + "count").json()


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
        elif type.endswith("axialSample"):
            return TimeSeriesSample(**obj)
        elif type == "ImageSample":
            return ImageSample(**obj)
        elif type == "VideoSample":
            return VideoSample(**obj)
        elif type.endswith("Annotation"):
            return Annotation(**obj)
        else:
            return obj
