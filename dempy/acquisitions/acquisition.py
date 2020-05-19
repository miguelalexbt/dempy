from typing import Union, List, Dict, Any

from .. import _base, _api_calls, _cache
from .._utils import SampleList, AnnotationList
from .subject import Subject
from .device import Device
from .image_sample import ImageSample
from .video_sample import VideoSample
from .timeseries_sample import TimeSeriesSample
from .annotation import Annotation


class Acquisition(_base.Entity):
    def __init__(self, type: str = "Acquisition", id: str = "", creation_timestamp: int = 0, sync_offset: int = None,
                 time_unit: str = "SECONDS", owner_id: str = "", creator_id: str = "", dataset_id: str = "",
                 metadata: Dict[str, Any] = {}, tags: List[str] = [], has_timeseries_samples: bool = False,
                 has_image_samples: bool = False, has_video_samples: bool = False):
        super().__init__(type, id)
        self.creation_timestamp = creation_timestamp
        self.sync_offset = sync_offset
        self.time_unit = time_unit
        self.owner_id = owner_id
        self.creator_id = creator_id
        self.dataset_id = dataset_id
        self.metadata = metadata
        self.tags = tags
        self.has_timeseries_samples = has_timeseries_samples
        self.has_image_samples = has_image_samples
        self.has_video_samples = has_video_samples

    @property
    def subject(self):
        class Inner:
            _SUBJECT_ENDPOINT = _ENDPOINT + "{}/subjects/".format(self.id)

            @staticmethod
            def get() -> Subject:
                return _api_calls.get(Inner._SUBJECT_ENDPOINT).json(object_hook=Subject.from_json)

            @staticmethod
            def create(subject: Subject) -> Subject:
                return _api_calls.put(Inner._SUBJECT_ENDPOINT, json=Subject.to_json(subject))\
                    .json(object_hook=Subject.from_json)

            @staticmethod
            def delete(subject_id: str) -> None:
                if not isinstance(subject_id, str):
                    raise TypeError()

                _api_calls.delete(Inner._SUBJECT_ENDPOINT + subject_id)

        return Inner()

    @property
    def devices(self):
        class Inner:
            _DEVICES_ENDPOINT = _ENDPOINT + "{}/devices/".format(self.id)

            @staticmethod
            def get(device_id: str = None) -> Union[Device, List[Device]]:
                if device_id is not None and not isinstance(device_id, str):
                    raise TypeError()

                if device_id is None:
                    return _api_calls.get(Inner._DEVICES_ENDPOINT).json(object_hook=Device.from_json)
                else:
                    return _api_calls.get(Inner._DEVICES_ENDPOINT + device_id).json(object_hook=Device.from_json)

            @staticmethod
            def create(device: Device) -> Device:
                if not isinstance(device, Device):
                    raise TypeError()

                return _api_calls.post(Inner._DEVICES_ENDPOINT, json=Device.to_json(device))\
                    .json(object_hook=Device.from_json)

            # TODO
            # @staticmethod
            # def modify(device_id, new_device):
            #     return _api_calls.put(inner._DEVICES_ENDPOINT, json={**new_device})
            #     .json(object_hook=lambda o: Device(**o))

            @staticmethod
            def delete(device_id: str) -> None:
                if not isinstance(device_id, str):
                    raise TypeError()

                _api_calls.delete(Inner._DEVICES_ENDPOINT + device_id)

            @staticmethod
            def usage() -> Dict[str, List[str]]:
                """Get a map identifying which device(s) and sensor(s) were used to acquire time series samples

                Returns:
                    Mapping[str, List[str]] -- Map of (key, value) pairs, with key being id of device and the value
                    a list of sensor ids which were used to capture samples
                """
                return _api_calls.get(Inner._DEVICES_ENDPOINT + "usage").json()

            @staticmethod
            def count() -> int:
                return _api_calls.get(Inner._DEVICES_ENDPOINT + "count").json()

        return Inner()

    @property
    def image_samples(self):
        class Inner:
            _IMAGE_SAMPLE_ENDPOINT = _ENDPOINT + "{}/samples/images/".format(self.id)

            @staticmethod
            def get() -> List[ImageSample]:
                return _api_calls.get(Inner._IMAGE_SAMPLE_ENDPOINT).json(cls=CustomDecoder)

            @staticmethod
            def count() -> int:
                return _api_calls.get(Inner._IMAGE_SAMPLE_ENDPOINT + "count").json()
            
            # TODO get actual image raw
            # TODO count image samples for datasets (maybe useful?, maybe create node image samples in root?)

        return Inner()

    @property
    def video_samples(self):
        class Inner:
            _VIDEO_SAMPLE_ENDPOINT = _ENDPOINT + "{}/samples/videos/".format(self.id)

            # TODO get video sample id?
            @staticmethod
            def get() -> List[VideoSample]:
                return _api_calls.get(Inner._VIDEO_SAMPLE_ENDPOINT).json(cls=CustomDecoder)

            @staticmethod
            def count() -> int:
                return _api_calls.get(Inner._VIDEO_SAMPLE_ENDPOINT + "count").json()

            # TODO get actual video raw
            # TODO get actual video stream
            # TODO meta info of video (HEAD)
            # TODO count video samples for datasets (maybe useful?, maybe create node video samples in root?)

        return Inner()

    @property
    def timeseries_samples(self):
        class Inner:
            _TIMESERIES_SAMPLE_ENDPOINT = _ENDPOINT + "{}/samples/timeseries/".format(self.id)

            @staticmethod
            def get() -> List[TimeSeriesSample]:
                try:
                    samples = _cache.get_cached_data("samples/{}/timeseries/".format(self.id),
                                                     object_hook=TimeSeriesSample.from_json)
                except:
                    print("Not cached")
                    samples = _api_calls.get(Inner._TIMESERIES_SAMPLE_ENDPOINT)\
                        .json(object_hook=TimeSeriesSample.from_json)
                    for sample in samples:
                        _cache.cache_data("samples/{}/timeseries/".format(self.id), sample,
                                          default=TimeSeriesSample.to_json)
                return SampleList(samples)

            # TODO create
            # TODO delete

            @staticmethod
            def count() -> int:
                return _api_calls.get(Inner._TIMESERIES_SAMPLE_ENDPOINT + "count").json()

        return Inner()

    @property
    def annotations(self):
        class Inner:
            _ANNOTATIONS_ENDPOINT = _ENDPOINT + "{}/annotations/".format(self.id)

            @staticmethod
            def get() -> AnnotationList:
                annotations = _api_calls.get(Inner._ANNOTATIONS_ENDPOINT).json(object_hook=Annotation.from_json)
                return AnnotationList(annotations)

            @staticmethod
            def count() -> int:
                return _api_calls.get(Inner._ANNOTATIONS_ENDPOINT + "count").json()

        return Inner()

    @staticmethod
    def to_json(obj):
        if not isinstance(obj, Acquisition):
            raise TypeError()

        # TODO add subject later??

        return {
            "type": obj.type,
            "id": obj.id,
            "creationTimestamp": obj.creation_timestamp,
            "syncOffset": obj.sync_offset,
            "timeUnit": obj.time_unit,
            "ownerId": obj.owner_id,
            "creatorId": obj.creator_id,
            "datasetId": obj.dataset_id,
            "metadata": obj.metadata,
            "tags": obj.tags,
            "hasTimeSeriesSamples": obj.has_timeseries_samples,
            "hasImageSamples": obj.has_image_samples,
            "hasVideoSamples": obj.has_video_samples
        }

    @staticmethod
    def from_json(obj: Dict[str, Any]):
        if not isinstance(obj, Dict):
            raise TypeError()

        if "type" in obj and obj["type"] == "Acquisition":
            return Acquisition(
                obj["type"], obj["id"], obj["creationTimestamp"], obj["syncOffset"], obj["timeUnit"],
                obj["ownerId"], obj["creatorId"], obj["datasetId"], obj["metadata"], obj["tags"],
                obj["hasTimeSeriesSamples"], obj["hasImageSamples"], obj["hasVideoSamples"]
            )
        return obj


_ENDPOINT = "api/acquisitions/"


def get(acquisition_id: str = None, dataset_id: str = None, tags: List = []) -> Union[Acquisition, List[Acquisition]]:
    if (acquisition_id is not None and not isinstance(acquisition_id, str)) or \
            (dataset_id is not None and not isinstance(dataset_id, str)):
        raise TypeError()

    if acquisition_id is None:
        acquisitions = _api_calls.get(_ENDPOINT, params={"datasetId": dataset_id, "tags": tags})\
            .json(object_hook=Acquisition.from_json)
        for acquisition in acquisitions:
            _cache.cache_data("acquisitions", acquisition, default=Acquisition.to_json)
        return acquisitions
    else:
        try:
            acquisition = _cache.get_cached_data("acquisitions", acquisition_id, object_hook=Acquisition.from_json)
        except:
            acquisition = _api_calls.get(_ENDPOINT + acquisition_id)\
                .json(object_hook=Acquisition.from_json)
            _cache.cache_data("acquisitions", acquisition, default=Acquisition.to_json)
        return acquisition


# TODO
def create(acquisition: Acquisition) -> Acquisition:
    if not isinstance(acquisition, Acquisition):
        raise TypeError()

    # acquisition = _api_calls.post(_ENDPOINT, json={**acquisition}) #.json(cls=CustomDecoder)
    # _cache.cache_data("acquisitions", acquisition, cls=CustomEncoder)

    return acquisition


def delete(acquisition_id: str) -> None:
    if not isinstance(acquisition_id, str):
        raise TypeError()

    _api_calls.delete(_ENDPOINT + acquisition_id)
    _cache.del_cached_data("acquisitions", acquisition_id)


def count() -> int:
    return _api_calls.get(_ENDPOINT + "count").json()

# Custom encoder/decoder


# class CustomEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, (Acquisition, Subject, Device, Sensor)):
#             return {**obj}
#         else:
#             return super().default(obj)
#
#
# class CustomDecoder(json.JSONDecoder):
#     def __init__(self, list_type=list, *args, **kwargs):
#         super().__init__(object_hook=self.object_hook, *args,  **kwargs)
#         self.parse_array = self.JSONArray
#         self.scan_once = json.scanner.py_make_scanner(self)
#         self.list_type = list_type
#
#     def JSONArray(self, s_and_end, scan_once, **kwargs):
#         values, end = json.decoder.JSONArray(s_and_end, scan_once, **kwargs)
#         return self.list_type(values), end
#
#     def object_hook(self, obj):
#         if "type" not in obj:
#             return obj
#
#         type = obj["type"]
#
#         if type == "Acquisition":
#             return Acquisition(**obj)
#         elif type.endswith("Subject"):
#             return Subject(**obj)
#         elif type == "Device":
#             return Device(**obj)
#         elif type == "Sensor":
#             return Sensor(**obj)
#         elif type.endswith("axialSample"):
#             return TimeSeriesSample(**obj)
#         elif type == "ImageSample":
#             return ImageSample(**obj)
#         elif type == "VideoSample":
#             return VideoSample(**obj)
#         elif type.endswith("Annotation"):
#             return Annotation(**obj)
#         else:
#             return obj
