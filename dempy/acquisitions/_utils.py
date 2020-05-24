from typing import ByteString, Union

from dempy._protofiles import SampleListMessage
from dempy.acquisitions.image_sample import ImageSample
from dempy.acquisitions.timeseries_sample import TimeseriesSample
from dempy.acquisitions.video_sample import VideoSample


class SampleList(list):
    def by_device(self, device_id: str) -> "SampleList":
        return SampleList([i for i in self if i.device_id is not None and i.device_id == device_id])

    def by_sensor(self, sensor_id: str) -> "SampleList":
        return SampleList([i for i in self if i.sensor_id is not None and i.sensor_id == sensor_id])

    @staticmethod
    def to_protobuf(obj: "SampleList") -> SampleListMessage:
        sample_list_message = SampleListMessage()

        if len(obj) > 0:
            if isinstance(obj[0], TimeseriesSample):
                sample_list_message.timeseries.extend([TimeseriesSample.to_protobuf(s) for s in obj])
            elif isinstance(obj[0], ImageSample):
                sample_list_message.images.extend([ImageSample.to_protobuf(s) for s in obj])
            elif isinstance(obj[0], VideoSample):
                sample_list_message.videos.extend([VideoSample.to_protobuf(s) for s in obj])
            else:
                raise TypeError

        return sample_list_message

    @staticmethod
    def from_protobuf(obj: Union[ByteString, SampleListMessage]) -> "SampleList":
        sample_list_message = SampleListMessage()
        sample_list_message.ParseFromString(obj)

        sample_list = SampleList()
        sample_list.extend([TimeseriesSample.from_protobuf(s) for s in sample_list_message.timeseries])
        sample_list.extend([ImageSample.from_protobuf(s) for s in sample_list_message.images])
        sample_list.extend([VideoSample.from_protobuf(s) for s in sample_list_message.videos])

        return sample_list


class AnnotationList(list):
    def by_sample(self, sample_id: str) -> "AnnotationList":
        return AnnotationList([i for i in self if i.annotated_sample_id == sample_id])
