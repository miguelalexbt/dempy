from typing import List, Dict, Any, ByteString, Union

from dempy._base import Entity
from dempy._protofiles import ImageMessage


class ImageSample(Entity):
    def __init__(self, type: str, id: str, tags: List[str], metadata: Dict[str, str], timestamp: int, acquisition_id: str, device_id: str,
                 sensor_id: str, media_type: str, image_source: str, has_rotation_metadata: bool):
        super().__init__(type, id, tags, metadata)
        self.timestamp = timestamp
        self.acquisition_id = acquisition_id
        self.device_id = device_id
        self.sensor_id = sensor_id
        self.media_type = media_type
        self.image_source = image_source
        self.has_rotation_metadata = has_rotation_metadata

    @staticmethod
    def to_protobuf(obj: "ImageSample") -> ImageMessage:
        image_message = ImageMessage()
        image_message.entity.CopyFrom(Entity.to_protobuf(obj))

        image_message.timestamp = obj.timestamp
        image_message.acquisition_id = obj.acquisition_id

        if obj.device_id is not None:
            image_message.device_id = obj.device_id
        if obj.sensor_id is not None:
            image_message.sensor_id = obj.sensor_id

        image_message.media_type = obj.media_type
        image_message.image_source = obj.image_source
        image_message.has_rotation_metadata = obj.has_rotation_metadata

        return image_message

    @staticmethod
    def from_protobuf(obj: Union[ByteString, ImageMessage]) -> "ImageSample":
        image_message = obj if isinstance(obj, ImageMessage) else ImageMessage().ParseFromString(obj)

        return ImageSample(
            type=image_message.entity.type,
            id=image_message.entity.id,
            tags=image_message.entity.tags,
            metadata=image_message.entity.metadata,
            timestamp=image_message.timestamp,
            acquisition_id=image_message.acquisition_id,
            device_id=image_message.device_id if image_message.HasField("device_id") else None,
            sensor_id=image_message.sensor_id if image_message.HasField("sensor_id") else None,
            media_type=image_message.media_type,
            image_source=image_message.image_source,
            has_rotation_metadata=image_message.has_rotation_metadata
        )

    @staticmethod
    def from_json(obj: Dict[str, Any]) -> Any:
        if "type" in obj and obj["type"] == "ImageSample":
            return ImageSample(
                type=obj["type"],
                id=obj["id"],
                tags=obj["tags"],
                metadata=obj["metadata"],
                timestamp=obj["timestamp"],
                acquisition_id=obj["acquisitionId"],
                device_id=obj["deviceId"],
                sensor_id=obj["sensorId"],
                media_type=obj["mediaType"],
                image_source=obj["imageSource"],
                has_rotation_metadata=obj["hasRotationMetadata"]
            )

        return obj


__all__ = [
    "ImageSample"
]
