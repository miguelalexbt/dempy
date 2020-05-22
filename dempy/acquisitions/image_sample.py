from typing import List, Dict, Any
from .. import _base


class ImageSample(_base.Entity):
    def __init__(self, type: str, id: str, acquisition_id: str, metadata: Dict[str, Any], timestamp: int,
                 device_id: str, sensor_id: str, tags: List[str], media_type: str, image_source: str,
                 has_rotation_metadata: bool):
        super().__init__(type, id)
        self.acquisition_id = acquisition_id
        self.timestamp = timestamp
        self.device_id = device_id
        self.sensor_id = sensor_id
        self.metadata = metadata
        self.tags = tags
        self.media_type = media_type
        self.image_source = image_source
        self.has_rotation_metadata = has_rotation_metadata

    @staticmethod
    def to_json(obj):
        if not isinstance(obj, ImageSample):
            raise TypeError

        return {
            "type": obj.type,
            "id": obj.id,
            "type": obj.type,
            "acquisitionId": obj.acquisition_id,
            "timestamp": obj.timestamp,
            "deviceId": obj.device_id,
            "sensorId": obj.sensor_id,
            "metadata": obj.metadata,
            "tags": obj.tags,
            "mediaType": obj.media_type,
            "imageSource": obj.image_source,
            "hasRotationMetadata": obj.has_rotation_metadata
        }

    @staticmethod
    def from_json(obj: Dict[str, Any]):
        if not isinstance(obj, Dict):
            raise TypeError

        if "type" in obj and obj["type"] == "ImageSample":
            return ImageSample(
                type=obj["type"],
                id=obj["id"],
                acquisition_id=obj["acquisitionId"],
                timestamp=obj["timestamp"],
                device_id=obj["deviceId"],
                sensor_id=obj["sensorId"],
                metadata=obj["metadata"],
                tags=obj["tags"],
                media_type=obj["mediaType"],
                image_source=obj["imageSource"],
                has_rotation_metadata=obj["hasRotationMetadata"]
            )
        return obj
