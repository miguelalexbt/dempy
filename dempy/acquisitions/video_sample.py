from typing import List, Dict, Any
from .. import _base


class VideoSample(_base.Entity):
    def __init__(self, type: str, id: str, acquisition_id: str, metadata: Dict[str, Any], timestamp: int,
                 device_id: str, sensor_id: str, tags: List[str], media_type: str, video_source: str):
        super().__init__(type, id)
        self.acquisition_id = acquisition_id
        self.timestamp = timestamp
        self.device_id = device_id
        self.sensor_id = sensor_id
        self.metadata = metadata
        self.tags = tags
        self.media_type = media_type
        self.video_source = video_source

    @staticmethod
    def to_json(obj):
        if not isinstance(obj, VideoSample):
            raise TypeError

        return {
            "type": obj.type,
            "id": obj.id,
            "acquisitionId": obj.acquisition_id,
            "metadata": obj.metadata,
            "timestamp": obj.timestamp,
            "deviceId": obj.device_id,
            "sensorId": obj.sensor_id,
            "tags": obj.tags,
            "mediaType": obj.media_type,
            "videoSource": obj.video_source
        }

    @staticmethod
    def from_json(obj: Dict[str, Any]):
        if "type" in obj and obj["type"] == "VideoSample":
            return VideoSample(
                type=obj["type"],
                id=obj["id"],
                acquisition_id=obj["acquisitionId"],
                metadata=obj["metadata"],
                timestamp=obj["timestamp"],
                device_id=obj["deviceId"],
                sensor_id=obj["sensorId"],
                tags=obj["tags"],
                media_type=obj["mediaType"],
                video_source=obj["videoSource"],
            )
        return obj
