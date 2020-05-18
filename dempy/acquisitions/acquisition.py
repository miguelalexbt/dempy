import json
from typing import Union, List, Mapping

from .. import _api_calls, _cache, _utils
from .subject import Subject
from .device import Device
from .sensor import Sensor
from .image_sample import ImageSample
from .video_sample import VideoSample
from .timeseries_sample import TimeSeriesSample
from .annotation import Annotation

class Acquisition:
    def __init__(self, type="Acquisition", id="", creationTimestamp=0, syncOffset=None, timeUnit="", ownerId="",
                 creatorId="", datasetId="", subject=object(), devices=[], metadata={}, tags=[],
                 hasTimeSeriesSamples=False, hasImageSamples=False, hasVideoSamples=False):
        self.type = type
        self.id = id
        self.creationTimestamp = creationTimestamp
        self.syncOffset = syncOffset
        self.timeUnit = timeUnit
        self.ownerId = ownerId
        self.creatorId = creatorId
        self.datasetId = datasetId
        self._subjectData = subject
        self._devicesData = devices
        self.metadata = metadata
        self.tags = tags
        self.hasTimeSeriesSamples = hasTimeSeriesSamples
        self.hasImageSamples = hasImageSamples
        self.hasVideoSamples = hasVideoSamples
        self._timeSeriesSamplesData = []

    @property
    def subject(self):
        # TODO rever

        class inner:
            _SUBJECT_ENDPOINT= _ENDPOINT + "{}/subjects/".format(self.id)

            @staticmethod
            def get() -> Subject:
                # _api_calls.get(inner._SUBJECT_ENDPOINT).json(object_hook=lambda o: Subject(**o))
                return self._subjectData

            @staticmethod
            def create(subject: Subject) -> Subject:
                self._subjectData = _api_calls.put(inner._SUBJECT_ENDPOINT, json={**subject}).json(object_hook=lambda o: Subject(**o))
                return self._subjectData

            @staticmethod
            def delete() -> None:
                _api_calls.delete(inner._SUBJECT_ENDPOINT + self._subjectData.id)
                self._subjectData = None

        return inner()

    @property
    def devices(self):
        class inner:
            _DEVICES_ENDPOINT = _ENDPOINT + "{}/devices/".format(self.id)

            @staticmethod
            def get(device_id: str = None) -> Union[Device, List[Device]]:
                if device_id != None and not isinstance(device_id, str):
                    raise TypeError()

                if device_id is None:
                    return self._devicesData
                else:
                    return _api_calls.get(inner._DEVICES_ENDPOINT + device_id).json(cls=CustomDecoder)

            @staticmethod
            def create(device: Device) -> Device:
                if not isinstance(device, Device):
                    raise TypeError()

                device_created = _api_calls.post(inner._DEVICES_ENDPOINT, json={**device}).json(object_hook=lambda o: Device(**o))
                self._devicesData.append(device_created)
                return device_created

            # TODO
            # @staticmethod
            # def modify(device_id, new_device):
            #     return _api_calls.put(inner._DEVICES_ENDPOINT, json={**new_device}).json(object_hook=lambda o: Device(**o))

            @staticmethod
            def delete(device_id: str) -> None:
                if not isinstance(device_id, str):
                    raise TypeError()

                # self._devicesData = [device for device in self._devicesData if device.id != deviceId]
                for index in range(len(self._devicesData)):
                    if self._devicesData[index].id == device_id:
                        del self._devicesData[index]
                _api_calls.delete(inner._DEVICES_ENDPOINT + device_id)

            @staticmethod
            def usage() -> Mapping[str, List[str]]:
                """Get a map identifying which device(s) and sensor(s) were used to acquire time series samples

                Returns:
                    Mapping[str, List[str]] -- Map of (key, value) pairs, with key being id of device and the value
                    a list of sensor ids which were used to capture samples
                """
                return _api_calls.get(inner._DEVICES_ENDPOINT + "usage").json()

            @staticmethod
            def count() -> int:
                return len(self._devicesData)

        return inner()

    @property
    def imageSamples(self):
        class inner:
            _IMAGE_SAMPLE_ENDPOINT = _ENDPOINT + "{}/samples/images/".format(self.id)

            @staticmethod
            def get() -> List[ImageSample]:
                return _api_calls.get(inner._IMAGE_SAMPLE_ENDPOINT).json(cls=CustomDecoder)

            @staticmethod
            def count() -> int:
                return _api_calls.get(inner._IMAGE_SAMPLE_ENDPOINT + "count").json()
            
            # TODO get actual image raw
            # TODO count image samples for datasets (maybe useful?, maybe create node image samples in root?)

        return inner()

    @property
    def videoSamples(self):
        class inner:
            _VIDEO_SAMPLE_ENDPOINT = _ENDPOINT + "{}/samples/videos/".format(self.id)

            # TODO get video sample id?
            @staticmethod
            def get() -> List[VideoSample]:
                return _api_calls.get(inner._VIDEO_SAMPLE_ENDPOINT).json(cls=CustomDecoder)

            @staticmethod
            def count() -> int:
                return _api_calls.get(inner._VIDEO_SAMPLE_ENDPOINT + "count").json()

            # TODO get actual video raw
            # TODO get actual video stream
            # TODO meta info of video (HEAD)
            # TODO count video samples for datasets (maybe useful?, maybe create node video samples in root?)

        return inner()

    @property
    def timeSeriesSamples(self):
        class inner:
            _TIMESERIES_SAMPLE_ENDPOINT = _ENDPOINT + "{}/samples/timeseries/".format(self.id)

            @staticmethod
            def get() -> List[TimeSeriesSample]:
                try:
                    samples = _cache.get_cached_data("samples/{}/timeseries/".format(self.id), object_hook=lambda o: TimeSeriesSample(**o))
                except Exception:
                    print("Not cached")
                    samples = _api_calls.get(inner._TIMESERIES_SAMPLE_ENDPOINT).json(cls=CustomDecoder, list_type=_utils.SampleList)
                    for sample in samples:
                        _cache.cache_data("samples/{}/timeseries/".format(self.id), sample)
                return samples

            # TODO create
            # TODO delete

            @staticmethod
            def count() -> int:
                return _api_calls.get(inner._TIMESERIES_SAMPLE_ENDPOINT + "count").json()

        return inner()

    @property
    def annotations(self):
        class inner:
            _ANNOTATIONS_ENDPOINT = _ENDPOINT + "{}/annotations/".format(self.id)

            @staticmethod
            def get() -> List[Annotation]:
                return _api_calls.get(inner._ANNOTATIONS_ENDPOINT).json(cls=CustomDecoder, list_type=_utils.AnnotationList)

            @staticmethod
            def count() -> int:
                return _api_calls.get(inner._ANNOTATIONS_ENDPOINT + "count").json()

        return inner()

    def keys(self):
        return self.__dict__.keys()

    def __getitem__(self, key):
        return getattr(self, key)

    def __repr__(self):
        return f"<Acquisition id=\"{self.id}\">"

# Interface

_ENDPOINT = "api/acquisitions/"

def get(acquisition_id: str = None, dataset_id: str = None, tags: List = []) -> Union[Acquisition, List[Acquisition]]:
    if (acquisition_id != None and not isinstance(acquisition_id, str)) or (dataset_id != None and not isinstance(dataset_id, str)):
        raise TypeError()

    if acquisition_id != None:
        try:
            acquisition = _cache.get_cached_data("acquisitions", acquisition_id, cls=CustomDecoder)
        except Exception:
            acquisition = _api_calls.get(_ENDPOINT + acquisition_id).json(cls=CustomDecoder)
            _cache.cache_data("acquisitions", acquisition, cls=CustomEncoder)
        return acquisition
    else:
        acquisitions = _api_calls.get(_ENDPOINT, params={"datasetId": dataset_id, "tags": tags}).json(cls=CustomDecoder)
        for acquisition in acquisitions:
            _cache.cache_data("acquisitions", acquisition, cls=CustomEncoder)
        return acquisitions

# TODO
def create(acquisition: Acquisition) -> Acquisition:
    if not isinstance(acquisition, Acquisition):
        raise TypeError()

    return
    
    acquisition = _api_calls.post(_ENDPOINT, json={**acquisition}) #.json(cls=CustomDecoder)
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

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (Acquisition, Subject, Device, Sensor)):
            return {**obj}
        else:
            return super().default(obj)

class CustomDecoder(json.JSONDecoder):
    def __init__(self, list_type=list, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args,  **kwargs)
        self.parse_array = self.JSONArray
        self.scan_once = json.scanner.py_make_scanner(self)
        self.list_type = list_type

    def JSONArray(self, s_and_end, scan_once, **kwargs):
        values, end = json.decoder.JSONArray(s_and_end, scan_once, **kwargs)
        return self.list_type(values), end

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
