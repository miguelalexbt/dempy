import matplotlib as mpt
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from itertools import chain
from typing import Union, List, Dict, Any
from .. import _base, _api_calls, _cache
from .._utils import SampleList, AnnotationList
from .subject import Subject
from .device import Device
from .sensor import Sensor
from .image_sample import ImageSample
from .video_sample import VideoSample
from .timeseries_sample import TimeSeriesSample
from .annotation import Annotation
mpt.use("TkAgg")


class Acquisition(_base.Entity):
    def __init__(self, type: str, id: str, creation_timestamp: int, sync_offset: int, time_unit: str,
                 owner_id: str, creator_id: str, dataset_id: str, subject: Subject, devices: List[Device],
                 metadata: Dict[str, Any], tags: List[str],
                 has_timeseries_samples: bool, has_image_samples: bool, has_video_samples: bool):
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

        self._subject = subject
        self._devices = devices

    @property
    def subject(self):
        class Inner:
            _SUBJECT_ENDPOINT = _ENDPOINT + "{}/subjects/".format(self.id)

            @staticmethod
            def get() -> Subject:
                return self._subject
                # return _api_calls.get(Inner._SUBJECT_ENDPOINT).json(object_hook=Subject.from_json)

            # @staticmethod
            # def create(subject: Subject) -> Subject:
            #     return _api_calls.put(Inner._SUBJECT_ENDPOINT, json=Subject.to_json(subject)).json(object_hook=Subject.from_json)

            # @staticmethod
            # def delete(subject_id: str) -> None:
            #     if not isinstance(subject_id, str):
            #         raise TypeError()
            #     _api_calls.delete(Inner._SUBJECT_ENDPOINT + subject_id)

        return Inner()

    @property
    def devices(self):
        class Inner:
            _DEVICES_ENDPOINT = _ENDPOINT + "{}/devices/".format(self.id)

            @staticmethod
            def get(device_id: str = None) -> Union[Device, List[Device]]:
                if device_id is not None and not isinstance(device_id, str):
                    raise TypeError

                if device_id is None:
                    return self._devices
                    # return _api_calls.get(Inner._DEVICES_ENDPOINT).json(object_hook=Device.from_json)
                else:
                    return next((device for device in self._devices if device.id == device_id), None)
                    # return _api_calls.get(Inner._DEVICES_ENDPOINT + device_id).json(object_hook=Device.from_json)

            # @staticmethod
            # def create(device: Device) -> Device:
            #     if not isinstance(device, Device):
            #         raise TypeError()
            #
            #     return _api_calls.post(Inner._DEVICES_ENDPOINT, json=Device.to_json(device))\
            #         .json(object_hook=Device.from_json)

            # TODO
            # @staticmethod
            # def modify(device_id, new_device):
            #     return _api_calls.put(inner._DEVICES_ENDPOINT, json={**new_device})
            #     .json(object_hook=lambda o: Device(**o))

            # @staticmethod
            # def delete(device_id: str) -> None:
            #     if not isinstance(device_id, str):
            #         raise TypeError()
            #     _api_calls.delete(Inner._DEVICES_ENDPOINT + device_id)

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
                return len(self._devices)
                # return _api_calls.get(Inner._DEVICES_ENDPOINT + "count").json()

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
            def get() -> SampleList:
                try:
                    samples = _cache.get_cached_data("samples/{}/".format(self.id), "timeseries", object_hook=TimeSeriesSample.from_json)
                except:
                    samples = _api_calls.get(Inner._TIMESERIES_SAMPLE_ENDPOINT).json(object_hook=TimeSeriesSample.from_json)
                    samples.sort(key=lambda sample: sample.timestamp)
                    _cache.cache_data("samples/{}/".format(self.id), "timeseries", samples, default=TimeSeriesSample.to_json)
                return SampleList(samples)

            @staticmethod
            def count() -> int:
                return _api_calls.get(Inner._TIMESERIES_SAMPLE_ENDPOINT + "count").json()

            @staticmethod
            def visualize(device_id: str, sensor_id: str = None) -> None:
                def visualize_sensor_samples(axis, sensor, sensor_samples):
                    timestamps = [s.timestamp for s in sensor_samples]

                    # Sample x, y, z, u, w
                    samples_x = [s.x for s in sensor_samples if s.x is not None]
                    samples_y = [s.y for s in sensor_samples if s.y is not None]
                    samples_z = [s.z for s in sensor_samples if s.z is not None]
                    samples_u = [s.u for s in sensor_samples if s.u is not None]
                    samples_w = [s.w for s in sensor_samples if s.w is not None]

                    axis.set_title(f"{sensor.sensor_type}\n{sensor.id}", loc="left")
                    axis.set_xlabel(sensor.time_unit if sensor.time_unit is not None else device_time_unit)

                    # Axis limit
                    axis.set_xlim([0, timestamps[-1]])
                    axis.set_ylim([min(chain(samples_x, samples_y, samples_z, samples_u, samples_w)), max(chain(samples_x, samples_y, samples_z, samples_u, samples_w))])

                    # Axis formatter
                    axis.xaxis.set_major_formatter(ticker.FormatStrFormatter("%.0f"))
                    axis.yaxis.set_major_formatter(ticker.FormatStrFormatter("%.0f"))

                    # Axis plot
                    labels = []

                    if len(samples_x) > 0:
                        axis.plot(timestamps, samples_x, color="cornflowerblue")
                        labels.append("x")
                    if len(samples_y) > 0:
                        axis.plot(timestamps, samples_y, color="mediumseagreen")
                        labels.append("y")
                    if len(samples_z) > 0:
                        axis.plot(timestamps, samples_z, color="indianred")
                        labels.append("z")
                    if len(samples_u) > 0:
                        axis.plot(timestamps, samples_u, color="mediumorchid")
                        labels.append("u")
                    if len(samples_w) > 0:
                        axis.plot(timestamps, samples_w, color="slategray")
                        labels.append("w")

                    axis.legend(labels=labels, loc="upper right")

                if not isinstance(device_id, str) or (sensor_id is not None and not isinstance(sensor_id, str)):
                    raise TypeError

                device = self.devices.get(device_id=device_id)
                device_time_unit = device.time_unit if device.time_unit is not None else self.time_unit

                if sensor_id is None:
                    fig, axs = plt.subplots(nrows=device.sensors.count(), figsize=(15, 10), dpi=80, constrained_layout=True)
                    fig.suptitle(f"{device.model_name} ({device.manufacturer})\n{device.id}", wrap=True)

                    device_samples = self.timeseries_samples.get().by_device(device_id=device.id)

                    for i, sensor in enumerate(device.sensors.get()):
                        visualize_sensor_samples(axs[i], sensor, device_samples.by_sensor(sensor.id))
                else:
                    fig, ax = plt.subplots(nrows=1, figsize=(10, 4), dpi=80, constrained_layout=True)
                    fig.suptitle(f"{device.model_name} ({device.manufacturer})\n{device.id}", wrap=True)

                    visualize_sensor_samples(ax, device.sensors.get(sensor_id=sensor_id), self.timeseries_samples.get().by_sensor(sensor_id))

                plt.show()

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
            raise TypeError

        return {
            "type": obj.type,
            "id": obj.id,
            "creationTimestamp": obj.creation_timestamp,
            "syncOffset": obj.sync_offset,
            "timeUnit": obj.time_unit,
            "ownerId": obj.owner_id,
            "creatorId": obj.creator_id,
            "datasetId": obj.dataset_id,
            "subject": Subject.to_json(obj._subject),
            "devices": [Device.to_json(device) for device in obj._devices],
            "metadata": obj.metadata,
            "tags": obj.tags,
            "hasTimeSeriesSamples": obj.has_timeseries_samples,
            "hasImageSamples": obj.has_image_samples,
            "hasVideoSamples": obj.has_video_samples
        }

    @staticmethod
    def from_json(obj: Dict[str, Any]):
        if not isinstance(obj, Dict):
            raise TypeError

        if "type" in obj:
            if obj["type"] == "Acquisition":
                return Acquisition(
                    type=obj["type"],
                    id=obj["id"],
                    creation_timestamp=obj["creationTimestamp"],
                    sync_offset=obj["syncOffset"],
                    time_unit=obj["timeUnit"],
                    owner_id=obj["ownerId"],
                    creator_id=obj["creatorId"],
                    dataset_id=obj["datasetId"],
                    subject=obj["subject"],
                    devices=obj["devices"],
                    metadata=obj["metadata"],
                    tags=obj["tags"],
                    has_timeseries_samples=obj["hasTimeSeriesSamples"],
                    has_image_samples=obj["hasImageSamples"],
                    has_video_samples=obj["hasVideoSamples"]
                )
            elif obj["type"].endswith("Subject"):
                return Subject.from_json(obj)
            elif obj["type"] == "Device":
                return Device.from_json(obj)
            elif obj["type"] == "Sensor":
                return Sensor.from_json(obj)
            else:
                raise TypeError
        return obj


_ENDPOINT = "api/acquisitions/"


def get(acquisition_id: str = None, dataset_id: str = None, tags: List[str] = []) -> Union[
    Acquisition, List[Acquisition]]:
    if (acquisition_id is not None and not isinstance(acquisition_id, str)) or (
            dataset_id is not None and not isinstance(dataset_id, str)):
        raise TypeError

    if acquisition_id is None:
        acquisitions = _api_calls.get(_ENDPOINT, params={"datasetId": dataset_id, "tags": tags}).json(
            object_hook=Acquisition.from_json)
        for acquisition in acquisitions:
            _cache.cache_data("acquisitions", acquisition.id, acquisition, default=Acquisition.to_json)
        return acquisitions
    else:
        try:
            acquisition = _cache.get_cached_data("acquisitions", acquisition_id, object_hook=Acquisition.from_json)
        except:
            acquisition = _api_calls.get(_ENDPOINT + acquisition_id).json(object_hook=Acquisition.from_json)
            _cache.cache_data("acquisitions", acquisition.id, acquisition, default=Acquisition.to_json)
        return acquisition


# TODO
# def create(acquisition: Acquisition) -> Acquisition:
#     if not isinstance(acquisition, Acquisition):
#         raise TypeError()
#
#     # acquisition = _api_calls.post(_ENDPOINT, json={**acquisition}) #.json(cls=CustomDecoder)
#     # _cache.cache_data("acquisitions", acquisition, cls=CustomEncoder)
#
#     return acquisition


# def delete(acquisition_id: str) -> None:
#     if not isinstance(acquisition_id, str):
#         raise TypeError()
#
#     _api_calls.delete(_ENDPOINT + acquisition_id)
#     _cache.del_cached_data("acquisitions", acquisition_id)


def count() -> int:
    return _api_calls.get(_ENDPOINT + "count").json()
