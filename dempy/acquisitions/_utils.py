from typing import ByteString, Union

from dempy._protofiles import SampleListMessage
from dempy.acquisitions.image_sample import ImageSample
from dempy.acquisitions.timeseries_sample import TimeseriesSample
from dempy.acquisitions.video_sample import VideoSample


class SampleList(list):
    """Wrapper list class with custom methods for handling samples

    Arguments:
        list {List[Sample]} -- list of samples
    """
    def by_device(self, device_id: str) -> "SampleList":
        """Returns the samples of a device specified by `device_id`

        Arguments:
            device_id {str} -- id of the device

        Returns:
            SampleList -- List containing the samples
        """
        return SampleList([i for i in self if i.device_id is not None and i.device_id == device_id])

    
    def by_sensor(self, sensor_id: str) -> "SampleList":
        """Returns the samples that use the sensor specified by `sensor_id`

        Arguments:
            sensor_id {str} -- id of the device

        Returns:
            SampleList -- List containing the samples
        """
        return SampleList([i for i in self if i.sensor_id is not None and i.sensor_id == sensor_id])

    @staticmethod
    def to_protobuf(obj: "SampleList") -> SampleListMessage:
        """Encode a sample list to a Protobuf message

        Arguments:
            obj {SampleList} -- sample list to be encoded

        Returns:
            SampleListMessage -- encoded sample list
        """
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
    def from_protobuf(obj: ByteString) -> "SampleList":
        """Decode a Protobuf message to {SampleList}

        Arguments:
            obj {ByteString} -- message to be decoded

        Returns:
            SampleList -- decoded sample list
        """
        sample_list_message = SampleListMessage()
        sample_list_message.ParseFromString(obj)

        sample_list = SampleList()
        sample_list.extend([TimeseriesSample.from_protobuf(s) for s in sample_list_message.timeseries])
        sample_list.extend([ImageSample.from_protobuf(s) for s in sample_list_message.images])
        sample_list.extend([VideoSample.from_protobuf(s) for s in sample_list_message.videos])

        return sample_list


class AnnotationList(list):
    """Wrapper list class with custom methods for handling annotations

    Arguments:
        list {List[Annotation]} -- list of annotations
    """
    def by_sample(self, sample_id: str) -> "AnnotationList":
        """Returns the annotations containing a sample specified by `sample_id`

        Arguments:
            sample_id {str} -- id of the sample

        Returns:
            AnnotationList -- List containing the annotations
        """
        return AnnotationList([i for i in self if i.annotated_sample_id == sample_id])
