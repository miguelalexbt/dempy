from typing import ByteString, Union
from .acquisitions.timeseries_sample import TimeseriesSample
from .acquisitions.image_sample import ImageSample
from .acquisitions.video_sample import VideoSample
from .acquisitions.annotation import Annotation
from ._protofiles import SampleListMessage, AnnotationListMessage


class SampleList(list):
    def by_device(self, device_id: str) -> "SampleList":
        if not isinstance(device_id, str):
            raise TypeError()

        return SampleList([i for i in self if i.device_id is not None and i.device_id == device_id])

    def by_sensor(self, sensor_id: str) -> "SampleList":
        if not isinstance(sensor_id, str):
            raise TypeError()

        return SampleList([i for i in self if i.sensor_id is not None and i.sensor_id == sensor_id])

    @staticmethod
    def to_protobuf(obj: "SampleList") -> SampleListMessage:
        if not isinstance(obj, SampleList):
            raise TypeError

        sample_list_message = SampleListMessage()

        for sample in obj:
            if isinstance(sample, TimeseriesSample):
                sample_list_message.timeseries.append(TimeseriesSample.to_protobuf(sample))
            elif isinstance(sample, ImageSample):
                sample_list_message.images.append(ImageSample.to_protobuf(sample))
            elif isinstance(sample, VideoSample):
                sample_list_message.videos.append(VideoSample.to_protobuf(sample))
            else:
                raise TypeError

        return sample_list_message

    @staticmethod
    def from_protobuf(obj: Union[ByteString, SampleListMessage]) -> "SampleList":
        if isinstance(obj, ByteString):
            sample_list_message = SampleListMessage()
            sample_list_message.ParseFromString(obj)
        elif isinstance(obj, SampleListMessage):
            sample_list_message = obj
        else:
            raise TypeError

        samples = list()
        samples.extend([TimeseriesSample.from_protobuf(s) for s in sample_list_message.timeseries])
        samples.extend([ImageSample.from_protobuf(s) for s in sample_list_message.images])
        samples.extend([VideoSample.from_protobuf(s) for s in sample_list_message.videos])

        return SampleList(samples)


class AnnotationList(list):
    def by_sample(self, sample_id: str) -> "AnnotationList":
        if not isinstance(sample_id, str):
            raise TypeError()

        return AnnotationList([i for i in self if i.annotated_sample_id == sample_id])

    @staticmethod
    def to_protobuf(obj: "AnnotationList") -> AnnotationListMessage:
        if not isinstance(obj, AnnotationList):
            raise TypeError

        annotation_list_message = AnnotationListMessage()
        annotation_list_message.annotations.extend([Annotation.to_protobuf(a) for a in obj])

        return annotation_list_message

    @staticmethod
    def from_protobuf(obj: Union[ByteString, AnnotationListMessage]) -> "AnnotationList":
        if isinstance(obj, ByteString):
            annotation_list_message = AnnotationListMessage()
            annotation_list_message.ParseFromString(obj)
        elif isinstance(obj, AnnotationListMessage):
            annotation_list_message = obj
        else:
            raise TypeError

        annotations = list()
        annotations.extend([Annotation.from_protobuf(a) for a in annotation_list_message.annotation])

        return AnnotationList(annotations)
