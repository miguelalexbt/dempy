import os
import platform
import subprocess
from itertools import chain
from typing import Union, List, Dict, Any, Callable, ByteString

import matplotlib as mpt
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from dempy import cache, _api_calls
from dempy._base import Entity
from dempy._protofiles import AcquisitionMessage
from dempy.acquisitions._utils import SampleList, AnnotationList
from dempy.acquisitions.annotation import Annotation
from dempy.acquisitions.device import Device
from dempy.acquisitions.image_sample import ImageSample
from dempy.acquisitions.sensor import Sensor
from dempy.acquisitions.subject import Subject
from dempy.acquisitions.timeseries_sample import TimeseriesSample
from dempy.acquisitions.video_sample import VideoSample

mpt.use("TkAgg")


class Acquisition(Entity):
    """Acquisition class"""
    def __init__(self, type: str, id: str, tags: List[str], metadata: Dict[str, str], creation_timestamp: int, sync_offset: int,
                 time_unit: str, owner_id: str, creator_id: str, dataset_id: str, subject: Subject, devices: List[Device],
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
        """Subject's API"""
        class Inner:
            _SUBJECT_ENDPOINT = _ENDPOINT + "{}/subjects/".format(self.id)

            @staticmethod
            def get() -> Subject:
                """Get subject from acquisition

                Returns:
                    Subject -- subject of the acquisition
                """
                return self._subject

        return Inner()

    @property
    def devices(self):
        """Devices' API"""
        class Inner:
            _DEVICES_ENDPOINT = _ENDPOINT + "{}/devices/".format(self.id)

            @staticmethod
            def get(device_id: str = None, tags: List[str] = [], metadata: Dict[str, str] = {}) -> Union[Device, List[Device]]:
                """Get a device identified by `device_id` or list of devices on this acquisition

                Keyword Arguments:
                    device_id {str} -- id of the device (default: {None})
                    tags {List[str]} -- tags of the devices (default: {[]})
                    metadata {Dict[str, str]} -- metadata of the devices (default: {{}})

                Raises:
                    IndexError: device identified by `device_id` does not exist in this acquisition

                Returns:
                    Union[Device, List[Device]] -- device or list of devices
                """
                if device_id is None:
                    if len(tags) > 0 or len(metadata) > 0:
                        return [d for d in self._devices if
                                len([k for k in d.metadata if k in metadata and d.metadata[k] == metadata[k]]) > 0]

                    return self._devices
                else:
                    try:
                        device = next((device for device in self._devices if device.id == device_id))
                    except StopIteration:
                        raise IndexError(f"device id {device_id} does not exist in acquisition id {self.id}")
                    return device

            @staticmethod
            def usage() -> Dict[str, List[str]]:
                """Get a map identifying which device(s) and sensor(s) were used to acquire time series samples

                Returns:
                    Mapping[str, List[str]] -- map of (key, value) pairs, with key being id of device and the value
                    a list of sensor ids which were used to capture samples
                """
                return _api_calls.get(Inner._DEVICES_ENDPOINT + "usage").json()

            @staticmethod
            def count() -> int:
                """Get the number of devices on this acquisition

                Returns:
                    int -- number of devices
                """
                return len(self._devices)

        return Inner()

    @property
    def timeseries_samples(self):
        """Timeseries samples' API"""
        class Inner:
            _TIMESERIES_SAMPLE_ENDPOINT = _ENDPOINT + "{}/samples/timeseries/".format(self.id)

            @staticmethod
            def get(tags: List[str] = [], metadata: Dict[str, str] = {}) -> SampleList:
                """Get all the timeseries samples that belong to this acquisition

                Keyword Arguments:
                    tags {List[str]} -- tags of the timeseries samples (default: {[]})
                    metadata {Dict[str, str]} -- metadata of the timeseries samples (default: {{}})

                Returns:
                    SampleList -- list of timeseries samples
                """
                if len(tags) > 0 or len(metadata) > 0:
                    processed_metadata = {f"metadata.{k}": metadata[k] for k in metadata}
                    samples = _api_calls.get(Inner._TIMESERIES_SAMPLE_ENDPOINT, params={"tags": tags, **processed_metadata}) \
                        .json(object_hook=TimeseriesSample.from_json)
                    samples.sort(key=lambda sample: sample.timestamp)
                    return SampleList(samples)

                try:
                    samples = cache._get_cached_data("samples/{}/".format(self.id), "timeseries", SampleList.from_protobuf)
                except FileNotFoundError:
                    samples = _api_calls.get(Inner._TIMESERIES_SAMPLE_ENDPOINT) \
                        .json(object_hook=TimeseriesSample.from_json)
                    samples.sort(key=lambda sample: sample.timestamp)
                    samples = SampleList(samples)
                    cache._cache_data("samples/{}/".format(self.id), "timeseries", samples, SampleList.to_protobuf)
                return samples

            @staticmethod
            def count() -> int:
                """Get the number of timeseries samples on this acquisition

                Returns:
                    int -- number of timeseries samples
                """
                return _api_calls.get(Inner._TIMESERIES_SAMPLE_ENDPOINT + "count").json()

            @staticmethod
            def visualize(device_id: str, sensor_id: str = None) -> None:
                """Graphically visualize the timeseries samples of a device identified by `device_id` 
                or of a given sensor identified by `sensor_id` of said device

                Arguments:
                    device_id {str} -- id of the device

                Keyword Arguments:
                    sensor_id {str} -- id of the sensor (default: {None})
                """
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
                    axis.set_ylim([min(chain(samples_x, samples_y, samples_z, samples_u, samples_w)),
                                   max(chain(samples_x, samples_y, samples_z, samples_u, samples_w))])

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
        """Image samples' API"""
        class Inner:
            _IMAGE_SAMPLE_ENDPOINT = _ENDPOINT + "{}/samples/images/".format(self.id)

            @staticmethod
            def get(sample_id: str = None, tags: List[str] = [], metadata: Dict[str, str] = {}) -> Union[ImageSample, SampleList]:
                """Get all the image samples that belong to this acquisition

                Keyword Arguments:
                    sample_id {str} -- id of the sample (default: {None})
                    tags {List[str]} -- tags of image samples (default: {[]})
                    metadata {Dict[str, str]} -- metadata of the image samples (default: {{}})

                Returns:
                    Union[ImageSample, SampleList] -- image sample or list of image samples
                """
                if sample_id is None:
                    if len(tags) > 0 or len(metadata) > 0:
                        processed_metadata = {f"metadata.{k}": metadata[k] for k in metadata}
                        samples = _api_calls.get(Inner._IMAGE_SAMPLE_ENDPOINT, params={"tags": tags, **processed_metadata}) \
                            .json(object_hook=ImageSample.from_json)
                        return SampleList(samples)

                    samples = _api_calls.get(Inner._IMAGE_SAMPLE_ENDPOINT).json(object_hook=ImageSample.from_json)
                    for sample in samples:
                        cache._cache_data("samples/{}/images/".format(self.id), sample.id, sample, ImageSample.to_protobuf)
                    return SampleList(samples)
                else:
                    try:
                        sample = cache._get_cached_data("samples/{}/images/".format(self.id), sample_id, ImageSample.from_protobuf)
                    except FileNotFoundError:
                        sample = _api_calls.get(Inner._IMAGE_SAMPLE_ENDPOINT + sample_id).json(object_hook=ImageSample.from_json)
                        cache._cache_data("samples/{}/images/".format(self.id), sample_id, sample, ImageSample.to_protobuf)
                    return sample

            @staticmethod
            def raw(sample_id: str) -> ByteString:
                """Get actual image from image sample identified by `sample_id` on this acquisition

                Arguments:
                    sample_id {str} -- id of the sample

                Returns:
                    ByteString -- bytes of the image
                """
                try:
                    image = cache._get_cached_data("samples/{}/images/raw/".format(self.id), sample_id)
                except FileNotFoundError:
                    image = _api_calls.get(Inner._IMAGE_SAMPLE_ENDPOINT + sample_id + "/raw")
                    file_ext = "." + image.headers["Content-Type"].split("/")[-1]
                    cache._cache_data("samples/{}/images/raw/".format(self.id), sample_id + file_ext, image.content)

                return image

            @staticmethod
            def count() -> int:
                """Get the number of image samples on this acquisition

                Returns:
                    int -- number of image samples
                """
                return _api_calls.get(Inner._IMAGE_SAMPLE_ENDPOINT + "count").json()

            @staticmethod
            def visualize(sample_id: str, backend: Callable[[str], None] = None) -> None:
                """Visualize the image of a sample identified by `sample_id`.
                By default opens the predefined system image application.
                A different callback can be given to open the image.

                Arguments:
                    sample_id {str} -- id of the sample

                Keyword Arguments:
                    backend {Callable[[str], None]} -- backend to open the image with (default: {None})
                """
                self.image_samples.raw(sample_id)
                image_path = cache._build_cache_path("samples/{}/images/raw/".format(self.id), sample_id)
                image_path = cache._add_file_extension(image_path)

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
        """Video samples' API"""
        class Inner:
            _VIDEO_SAMPLE_ENDPOINT = _ENDPOINT + "{}/samples/videos/".format(self.id)

            @staticmethod
            def get(sample_id: str = None, tags: List[str] = [], metadata: Dict[str, str] = {}) -> Union[VideoSample, SampleList]:
                """Get all the video samples that belong to this acquisition

                Keyword Arguments:
                    sample_id {str} -- id of the sample (default: {None})
                    tags {List[str]} -- tags of image samples (default: {[]})
                    metadata {Dict[str, str]} -- metadata of the image samples (default: {{}})

                Returns:
                    Union[VideoSample, SampleList] -- video sample or list of video samples
                """
                if sample_id is None:
                    if len(tags) > 0 or len(metadata) > 0:
                        processed_metadata = {f"metadata.{k}": metadata[k] for k in metadata}
                        samples = _api_calls.get(Inner._VIDEO_SAMPLE_ENDPOINT, params={"tags": tags, **processed_metadata}) \
                            .json(object_hook=VideoSample.from_json)
                        return SampleList(samples)

                    samples = _api_calls.get(Inner._VIDEO_SAMPLE_ENDPOINT).json(object_hook=VideoSample.from_json)
                    for sample in samples:
                        cache._cache_data("samples/{}/videos/".format(self.id), sample.id, sample, VideoSample.to_protobuf)
                    return SampleList(samples)
                else:
                    try:
                        sample = cache._get_cached_data("samples/{}/videos/".format(self.id), sample_id, VideoSample.from_protobuf)
                    except FileNotFoundError:
                        sample = _api_calls.get(Inner._VIDEO_SAMPLE_ENDPOINT + sample_id).json(object_hook=VideoSample.from_json)
                        cache._cache_data("samples/{}/videos/".format(self.id), sample_id, sample, VideoSample.to_protobuf)
                    return sample

            @staticmethod
            def raw(sample_id: str) -> ByteString:
                """Get actual video from video sample identified by `sample_id` on this acquisition 

                Arguments:
                    sample_id {str} -- id of the sample

                Returns:
                    ByteString -- bytes of the video
                """
                try:
                    video = cache._get_cached_data("samples/{}/videos/raw/".format(self.id), sample_id)
                except FileNotFoundError:
                    video = _api_calls.get(Inner._VIDEO_SAMPLE_ENDPOINT + sample_id + "/raw")
                    file_ext = "." + video.headers["Content-Type"].split("/")[-1]
                    cache._cache_data("samples/{}/videos/raw/".format(self.id), sample_id + file_ext, video.content)

                return video

            @staticmethod
            def count() -> int:
                """Get the number of video samples on this acquisition

                Returns:
                    int -- number of video samples
                """
                return _api_calls.get(Inner._VIDEO_SAMPLE_ENDPOINT + "count").json()

            @staticmethod
            def visualize(sample_id: str, backend: Callable[[str], None] = None) -> None:
                """Visualize the video of a sample identified by `sample_id`.
                By default opens the predefined system video application.
                A different callback can be given to open the video.

                Arguments:
                    sample_id {str} -- id of the sample

                Keyword Arguments:
                    backend {Callable[[str], None]} -- backend to open the video with (default: {None})
                """
                self.video_samples.raw(sample_id)
                video_path = cache._build_cache_path("samples/{}/videos/raw/".format(self.id), sample_id)
                video_path = cache._add_file_extension(video_path)

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
        """Annotations' API"""
        class Inner:
            _ANNOTATIONS_ENDPOINT = _ENDPOINT + "{}/annotations/".format(self.id)

            @staticmethod
            def get(annotation_id: str = None, tags: List[str] = [], metadata: Dict[str, str] = {}) -> AnnotationList:
                """Get all the annotations that belong to this acquisition

                Keyword Arguments:
                    annotation_id {str} -- id of the annotation (default: {None})
                    tags {List[str]} -- tags of the annotation (default: {[]})
                    metadata {Dict[str, str]} -- metadata of the annotation (default: {{}})

                Returns:
                    AnnotationList -- annotation or annotation of video samples
                """
                if annotation_id is None:
                    if len(tags) > 0 or len(metadata) > 0:
                        processed_metadata = {f"metadata.{k}": metadata[k] for k in metadata}
                        annotations = _api_calls.get(Inner._ANNOTATIONS_ENDPOINT, params={"tags": tags, **processed_metadata}) \
                            .json(object_hook=Annotation.from_json)
                        return AnnotationList(annotations)

                    annotations = _api_calls.get(Inner._ANNOTATIONS_ENDPOINT).json(object_hook=Annotation.from_json)
                    for annotation in annotations:
                        cache._cache_data("annotations", annotation.id, annotation, Annotation.to_protobuf)
                    return AnnotationList(annotations)
                else:
                    try:
                        annotation = cache._get_cached_data("annotations", annotation_id, Annotation.from_protobuf)
                    except FileNotFoundError:
                        annotation = _api_calls.get(Inner._ANNOTATIONS_ENDPOINT + annotation_id).json(object_hook=Annotation.from_json)
                        cache._cache_data("annotations", annotation_id, annotation, Annotation.to_protobuf)
                    return annotation

            @staticmethod
            def count() -> int:
                """Get the number of annotations on this acquisition

                Returns:
                    int -- number of annotations
                """
                return _api_calls.get(Inner._ANNOTATIONS_ENDPOINT + "count").json()

        return Inner()

    @staticmethod
    def to_protobuf(obj: "Acquisition") -> AcquisitionMessage:
        """Encode an acquisition to a Protobuf message

        Arguments:
            obj {Acquisition} -- acquisition to be encoded

        Returns:
            AcquisitionMessage -- encoded acquisition
        """
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
    def from_protobuf(obj: ByteString) -> "Acquisition":
        """Decode a Protobuf message to {Acquisition}

        Arguments:
            obj {ByteString} -- message to be decoded

        Returns:
            Acquisition -- decoded acquisition
        """
        acquisition_message = AcquisitionMessage()
        acquisition_message.ParseFromString(obj)

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
    def from_json(obj: Dict[str, str]) -> Any:
        """Parse a JSON dictionary to {Acquisition}

        Arguments:
            obj {Dict[str, str]} -- JSON object

        Raises:
            ValueError: unexpected object or sub-object

        Returns:
            Any -- parsed object and sub-objects
        """
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


def get(acquisition_id: str = None, dataset_id: str = None, tags: List[str] = [], metadata: Dict[str, str] = {}) \
    -> Union[Acquisition, List[Acquisition]]:
    """Get an acquisition identified by `acquisition_id` or a list of all the acquisitions

    Keyword Arguments:
        acquisition_id {str} -- id of the acquisition (default: {None})
        dataset_id {str} -- id of the dataset to which the acquisitions belong to (default: {None})
        tags {List[str]} -- tags of the acquisitions (default: {[]})
        metadata {Dict[str, str]} -- metadata of the acquisitions (default: {{}})

    Returns:
        Union[Acquisition, List[Acquisition]] -- acquisition or list of acquisitions
    """
    if acquisition_id is None:
        processed_metadata = {f"metadata.{k}": metadata[k] for k in metadata}
        acquisitions = _api_calls.get(_ENDPOINT, params={"datasetId": dataset_id, "tags": tags, **processed_metadata}) \
            .json(object_hook=Acquisition.from_json)
        for acquisition in acquisitions:
            cache._cache_data("acquisitions", acquisition.id, acquisition, Acquisition.to_protobuf)
        return acquisitions
    else:
        try:
            acquisition = cache._get_cached_data("acquisitions", acquisition_id, Acquisition.from_protobuf)
        except FileNotFoundError:
            acquisition = _api_calls.get(_ENDPOINT + acquisition_id).json(object_hook=Acquisition.from_json)
            cache._cache_data("acquisitions", acquisition_id, acquisition, Acquisition.to_protobuf)
        return acquisition


def count() -> int:
    """Get number of acquisitions

    Returns:
        int -- number of acquisitions
    """
    return _api_calls.get(_ENDPOINT + "count").json()


__all__ = [
    "Acquisition",
    "get", "count"
]
