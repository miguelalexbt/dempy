from typing import List, Dict, Any, Union, ByteString

from dempy._base import Entity
from dempy._protofiles import VideoMessage


class VideoSample(Entity):
    """VideoSample class"""
    def __init__(self, type: str, id: str, tags: List[str], metadata: Dict[str, str], timestamp: int, acquisition_id: str, device_id: str,
                 sensor_id: str, media_type: str, video_source: str):
        super().__init__(type, id, tags, metadata)
        self.timestamp = timestamp
        self.acquisition_id = acquisition_id
        self.device_id = device_id
        self.sensor_id = sensor_id
        self.media_type = media_type
        self.video_source = video_source

    @staticmethod
    def to_protobuf(obj: "VideoSample") -> VideoMessage:
        """Encode a video sample to a Protobuf message

        Arguments:
            obj {VideoSample} -- video sample to be encoded

        Returns:
            VideoMessage -- encoded video sample
        """
        video_message = VideoMessage()
        video_message.entity.CopyFrom(Entity.to_protobuf(obj))

        video_message.timestamp = obj.timestamp
        video_message.acquisition_id = obj.acquisition_id

        if obj.device_id is not None:
            video_message.device_id = obj.device_id
        if obj.sensor_id is not None:
            video_message.sensor_id = obj.sensor_id

        video_message.media_type = obj.media_type
        video_message.video_source = obj.video_source

        return video_message

    @staticmethod
    def from_protobuf(obj: Union[ByteString, VideoMessage]) -> "VideoSample":
        """Decode a Protobuf message to {VideoSample}

        Arguments:
            obj {Union[ByteString, VideoMessage]} -- message to be decoded

        Returns:
            VideoSample -- decoded video sample
        """
        video_message = obj if isinstance(obj, VideoMessage) else VideoMessage().ParseFromString(obj)

        return VideoSample(
            type=video_message.entity.type,
            id=video_message.entity.id,
            tags=video_message.entity.tags,
            metadata=video_message.entity.metadata,
            timestamp=video_message.timestamp,
            acquisition_id=video_message.acquisition_id,
            device_id=video_message.device_id if video_message.HasField("device_id") else None,
            sensor_id=video_message.sensor_id if video_message.HasField("sensor_id") else None,
            media_type=video_message.media_type,
            video_source=video_message.video_source
        )

    @staticmethod
    def from_json(obj: Dict[str, str]) -> Any:
        """Parse a JSON dictionary to {VideoSample}

        Arguments:
            obj {Dict[str, str]} -- JSON object

        Returns:
            Any -- parsed object and sub-objects
        """
        if "type" in obj and obj["type"] == "VideoSample":
            return VideoSample(
                type=obj["type"],
                id=obj["id"],
                tags=obj["tags"],
                metadata=obj["metadata"],
                timestamp=obj["timestamp"],
                acquisition_id=obj["acquisitionId"],
                device_id=obj["deviceId"],
                sensor_id=obj["sensorId"],
                media_type=obj["mediaType"],
                video_source=obj["videoSource"],
            )

        return obj


__all__ = [
    "VideoSample"
]
