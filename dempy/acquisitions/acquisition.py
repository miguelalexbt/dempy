import os
import subprocess
import platform

from itertools import chain
from typing import Union, List, Dict, Any, Callable, ByteString
from .. import _api_calls, _cache
from .._base import Entity
from .._utils import SampleList, AnnotationList
from .subject import Subject
from .device import Device
from .sensor import Sensor
from .image_sample import ImageSample
from .video_sample import VideoSample
from .timeseries_sample import TimeseriesSample
from .annotation import Annotation
from .._protofiles import AcquisitionMessage

import matplotlib as mpt
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
mpt.use("TkAgg")


class Acquisition(Entity):
    def __init__(self, type: str, id: str, tags: List[str], metadata: Dict[str, Any],
                 creation_timestamp: int, sync_offset: int, time_unit: str,
                 owner_id: str, creator_id: str, dataset_id: str,
                 subject: Subject, devices: List[Device],
                 has_timeseries_samples: bool, has_image_samples: bool, has_video_samples: bool):
        super().__init__(type, id, tags, metadata)

        self.creation_timestamp = creation_timestamp
        self.sync_offset = sync_offset
        self.time_unit = time_unit

        self.owner_id = owner_id
        self.creator_id = creator_id
        self.dataset_id = dataset_id

        self.has_timeseries_samples = has_timeseries_samples
        self.has_image_samples = has_image_samples
        self.has_video_samples = has_video_samples

        self._subject = subject
        self._devices = devices

    @property
    def subject(self):
        class Inner:
            # _SUBJECT_ENDPOINT = _ENDPOINT + "{}/subjects/".format(self.id)

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
                else:
                    try:
                        device = next((device for device in self._devices if device.id == device_id), None)
                    except StopIteration:
                        raise IndexError(f"device {device_id} does not exist in acquisition {self.id}")
                    return device

            @staticmethod
            def usage() -> Dict[str, List[str]]:
                """Get a map identifying which device(s) and sensor(s) were used to acquire time series samples.proto

                Returns:
                    Mapping[str, List[str]] -- Map of (key, value) pairs, with key being id of device and the value
                    a list of sensor ids which were used to capture samples.proto
                """
                return _api_calls.get(Inner._DEVICES_ENDPOINT + "usage").json()

            @staticmethod
            def count() -> int:
                return len(self._devices)

        return Inner()

    @property
    def timeseries_samples(self):
        class Inner:
            _TIMESERIES_SAMPLE_ENDPOINT = _ENDPOINT + "{}/samples/timeseries/".format(self.id)

            @staticmethod
            def get() -> SampleList:
                try:
                    samples = _cache.get_cached_data("samples/{}/".format(self.id), "timeseries", SampleList.from_protobuf)
                except FileNotFoundError:
                    samples = _api_calls.get(Inner._TIMESERIES_SAMPLE_ENDPOINT).json(object_hook=TimeseriesSample.from_json)
                    samples.sort(key=lambda sample: sample.timestamp)
                    samples = SampleList(samples)
                    _cache.cache_data("samples/{}/".format(self.id), "timeseries", samples, SampleList.to_protobuf)
                return samples

            @staticmethod
            def count() -> int:
                return _api_calls.get(Inner._TIMESERIES_SAMPLE_ENDPOINT + "count").json()

            @staticmethod
            def visualize(device_id: str, sensor_id: str = None) -> None:
                def visualize_sensor_samples(axis, sensor, sensor_samples):
                    timestamps = [s.timestamp for s in sensor_samples]

                    # Sample x, y, z, u, w
                    samples_x = [s.x for s in sensor_samples if hasattr(s, "x")]
                    samples_y = [s.y for s in sensor_samples if hasattr(s, "y")]
                    samples_z = [s.z for s in sensor_samples if hasattr(s, "z")]
                    samples_u = [s.u for s in sensor_samples if hasattr(s, "u")]
                    samples_w = [s.w for s in sensor_samples if hasattr(s, "w")]

                    # Title and x label
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

                    sensor_samples = self.timeseries_samples.get().by_sensor(sensor_id)

                    visualize_sensor_samples(ax, device.sensors.get(sensor_id=sensor_id), sensor_samples)

                plt.show()

        return Inner()

    @property
    def image_samples(self):
        class Inner:
            _IMAGE_SAMPLE_ENDPOINT = _ENDPOINT + "{}/samples/images/".format(self.id)

            @staticmethod
            def get(sample_id: str = None) -> Union[ImageSample, SampleList]:
                if sample_id is not None and not isinstance(sample_id, str):
                    raise TypeError

                if sample_id is None:
                    samples = _api_calls.get(Inner._IMAGE_SAMPLE_ENDPOINT).json(object_hook=ImageSample.from_json)
                    for sample in samples:
                        _cache.cache_data("samples/{}/images/".format(self.id), sample.id, sample, ImageSample.to_protobuf)
                    return SampleList(samples)
                else:
                    try:
                        sample = _cache.get_cached_data("samples/{}/images/".format(self.id), sample_id, ImageSample.from_protobuf)
                    except FileNotFoundError:
                        sample = _api_calls.get(Inner._IMAGE_SAMPLE_ENDPOINT + sample_id).json(object_hook=ImageSample.from_json)
                        _cache.cache_data("samples/{}/images/".format(self.id), sample_id, sample, ImageSample.to_protobuf)
                    return sample

            @staticmethod
            def raw(sample_id: str) -> ByteString:
                if not isinstance(sample_id, str):
                    raise TypeError

                try:
                    image = _cache.get_cached_data("samples/{}/images/raw/".format(self.id), sample_id)
                except FileNotFoundError:
                    image = _api_calls.get(Inner._IMAGE_SAMPLE_ENDPOINT + sample_id + "/raw")
                    file_ext = "." + image.headers["Content-Type"].split("/")[-1]
                    _cache.cache_data("samples/{}/images/raw/".format(self.id), sample_id + file_ext, image.content)

                return image

            @staticmethod
            def count() -> int:
                return _api_calls.get(Inner._IMAGE_SAMPLE_ENDPOINT + "count").json()

            @staticmethod
            def visualize(sample_id: str, backend: Callable[[str], None] = None) -> None:
                if not isinstance(sample_id, str):
                    raise TypeError

                self.image_samples.raw(sample_id)
                image_path = _cache.build_cache_path("samples/{}/images/raw/".format(self.id), sample_id)
                image_path = _cache.add_file_extension(image_path)

                if backend is None:
                    system = platform.system()

                    if system == "Darwin":
                        subprocess.call(("open", image_path))
                    elif system == "Windows":
                        os.startfile(image_path)
                    else:
                        subprocess.call(("xdg-open", image_path))
                else:
                    backend(image_path)

        return Inner()

    @property
    def video_samples(self):
        class Inner:
            _VIDEO_SAMPLE_ENDPOINT = _ENDPOINT + "{}/samples/videos/".format(self.id)

            @staticmethod
            def get(sample_id: str = None) -> Union[VideoSample, SampleList]:
                if sample_id is not None and not isinstance(sample_id, str):
                    raise TypeError

                if sample_id is None:
                    samples = _api_calls.get(Inner._VIDEO_SAMPLE_ENDPOINT).json(object_hook=VideoSample.from_json)
                    for sample in samples:
                        _cache.cache_data("samples/{}/videos/".format(self.id), sample.id, sample, VideoSample.to_protobuf)
                    return SampleList(samples)
                else:
                    try:
                        sample = _cache.get_cached_data("samples/{}/videos/".format(self.id), sample_id, VideoSample.from_protobuf)
                    except FileNotFoundError:
                        sample = _api_calls.get(Inner._VIDEO_SAMPLE_ENDPOINT + sample_id).json(object_hook=VideoSample.from_json)
                        _cache.cache_data("samples/{}/videos/".format(self.id), sample_id, sample, VideoSample.to_protobuf)
                    return sample

            @staticmethod
            def raw(sample_id: str) -> ByteString:
                if not isinstance(sample_id, str):
                    raise TypeError

                try:
                    video = _cache.get_cached_data("samples/{}/videos/raw/".format(self.id), sample_id)
                except FileNotFoundError:
                    video = _api_calls.get(Inner._VIDEO_SAMPLE_ENDPOINT + sample_id + "/raw")
                    file_ext = "." + video.headers["Content-Type"].split("/")[-1]
                    _cache.cache_data("samples/{}/videos/raw/".format(self.id), sample_id + file_ext, video.content)

                return video

            @staticmethod
            def count() -> int:
                return _api_calls.get(Inner._VIDEO_SAMPLE_ENDPOINT + "count").json()

            @staticmethod
            def visualize(sample_id: str, backend: Callable[[str], None] = None) -> None:
                if not isinstance(sample_id, str):
                    raise TypeError

                self.video_samples.raw(sample_id)
                video_path = _cache.build_cache_path("samples/{}/videos/raw/".format(self.id), sample_id)
                video_path = _cache.add_file_extension(video_path)

                if backend is None:
                    system = platform.system()

                    if system == "Darwin":
                        subprocess.call(("open", video_path))
                    elif system == "Windows":
                        os.startfile(video_path)
                    else:
                        subprocess.call(("xdg-open", video_path))
                else:
                    backend(video_path)

        return Inner()

    @property
    def annotations(self):
        class Inner:
            _ANNOTATIONS_ENDPOINT = _ENDPOINT + "{}/annotations/".format(self.id)

            @staticmethod
            def get(annotation_id: str = None) -> AnnotationList:
                if annotation_id is not None and not isinstance(annotation_id, str):
                    raise TypeError

                if annotation_id is None:
                    annotations = _api_calls.get(Inner._ANNOTATIONS_ENDPOINT).json(object_hook=Annotation.from_json)
                    for annotation in annotations:
                        _cache.cache_data("annotations", annotation.id, annotation, Annotation.to_protobuf)
                    return AnnotationList(annotations)
                else:
                    try:
                        annotation = _cache.get_cached_data("annotations", annotation_id, Annotation.from_protobuf)
                    except FileNotFoundError:
                        annotation = _api_calls.get(Inner._ANNOTATIONS_ENDPOINT + annotation_id).json(object_hook=Annotation.from_json)
                        _cache.cache_data("annotations", annotation_id, annotation, Annotation.to_protobuf)
                    return annotation

            @staticmethod
            def count() -> int:
                return _api_calls.get(Inner._ANNOTATIONS_ENDPOINT + "count").json()

        return Inner()

    @staticmethod
    def to_protobuf(obj: "Acquisition") -> AcquisitionMessage:
        if not isinstance(obj, Acquisition):
            raise TypeError

        acquisition_message = AcquisitionMessage()
        acquisition_message.entity.CopyFrom(Entity.to_protobuf(obj))
        acquisition_message.creation_timestamp = obj.creation_timestamp

        if obj.sync_offset is not None:
            acquisition_message.sync_offset = obj.sync_offset
        if obj.time_unit is not None:
            acquisition_message.time_unit = obj.time_unit
        if obj.owner_id is not None:
            acquisition_message.owner_id = obj.owner_id
        if obj.creator_id is not None:
            acquisition_message.creator_id = obj.creator_id
        if obj.dataset_id is not None:
            acquisition_message.dataset_id = obj.dataset_id

        acquisition_message.subject.CopyFrom(Subject.to_protobuf(obj._subject))
        acquisition_message.devices.extend([Device.to_protobuf(d) for d in obj._devices])
        acquisition_message.has_timeseries_samples = obj.has_timeseries_samples
        acquisition_message.has_image_samples = obj.has_image_samples
        acquisition_message.has_video_samples = obj.has_video_samples

        return acquisition_message

    @staticmethod
    def from_protobuf(obj: Union[ByteString, AcquisitionMessage]) -> "Acquisition":
        if isinstance(obj, ByteString):
            acquisition_message = AcquisitionMessage()
            acquisition_message.ParseFromString(obj)
        elif isinstance(obj, AcquisitionMessage):
            acquisition_message = obj
        else:
            raise TypeError

        return Acquisition(
            type=acquisition_message.entity.type,
            id=acquisition_message.entity.id,
            tags=acquisition_message.entity.tags,
            metadata=acquisition_message.entity.metadata,
            creation_timestamp=acquisition_message.creation_timestamp,
            sync_offset=acquisition_message.sync_offset if acquisition_message.HasField("sync_offset") else None,
            time_unit=acquisition_message.time_unit,
            owner_id=acquisition_message.owner_id if acquisition_message.HasField("owner_id") else None,
            creator_id=acquisition_message.creator_id if acquisition_message.HasField("creator_id") else None,
            dataset_id=acquisition_message.dataset_id if acquisition_message.HasField("dataset_id") else None,
            subject=Subject.from_protobuf(acquisition_message.subject),
            devices=[Device.from_protobuf(d) for d in acquisition_message.devices],
            has_timeseries_samples=acquisition_message.has_timeseries_samples,
            has_image_samples=acquisition_message.has_image_samples,
            has_video_samples=acquisition_message.has_video_samples
        )

    @staticmethod
    def from_json(obj: Dict[str, Any]) -> Any:
        if not isinstance(obj, Dict):
            raise TypeError

        if "type" in obj:
            if obj["type"] == "Acquisition":
                return Acquisition(
                    type=obj["type"],
                    id=obj["id"],
                    tags=obj["tags"],
                    metadata=obj["metadata"],
                    creation_timestamp=obj["creationTimestamp"],
                    sync_offset=obj["syncOffset"],
                    time_unit=obj["timeUnit"],
                    owner_id=obj["ownerId"],
                    creator_id=obj["creatorId"],
                    dataset_id=obj["datasetId"],
                    subject=obj["subject"],
                    devices=obj["devices"],
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
                raise ValueError
        return obj


_ENDPOINT = "api/acquisitions/"


def get(acquisition_id: str = None, dataset_id: str = None, tags: List[str] = []) -> Union[Acquisition, List[Acquisition]]:
    if (acquisition_id is not None and not isinstance(acquisition_id, str)) or (dataset_id is not None and not isinstance(dataset_id, str)):
        raise TypeError

    if acquisition_id is None:
        acquisitions = _api_calls.get(_ENDPOINT, params={"datasetId": dataset_id, "tags": tags}).json(object_hook=Acquisition.from_json)
        for acquisition in acquisitions:
            _cache.cache_data("acquisitions", acquisition.id, acquisition, Acquisition.to_protobuf)
        return acquisitions
    else:
        try:
            acquisition = _cache.get_cached_data("acquisitions", acquisition_id, Acquisition.from_protobuf)
        except FileNotFoundError:
            acquisition = _api_calls.get(_ENDPOINT + acquisition_id).json(object_hook=Acquisition.from_json)
            _cache.cache_data("acquisitions", acquisition_id, acquisition, Acquisition.to_protobuf)
        return acquisition


def count() -> int:
    return _api_calls.get(_ENDPOINT + "count").json()
