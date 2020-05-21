from typing import List, Dict, Any
from .. import _base


class TimeSeriesSample(_base.Entity):
    def __init__(self, type: str, id: str, acquisition_id: str, metadata: Dict[str, Any], timestamp: int,
                 device_id: str, sensor_id: str, tags: List[str],
                 x: int = None, y: int = None, z: int = None, u: int = None, w: int = None):
        super().__init__(type, id)
        self.acquisition_id = acquisition_id
        self.timestamp = timestamp
        self.device_id = device_id
        self.sensor_id = sensor_id
        self.metadata = metadata
        self.tags = tags
        self.x = x
        self.y = y
        self.z = z
        self.u = u
        self.w = w

    @staticmethod
    def to_json(obj):
        if not isinstance(obj, TimeSeriesSample):
            raise TypeError()

        obj_dict = {
            "type": obj.type,
            "id": obj.id,
            "acquisitionId": obj.acquisition_id,
            "metadata": obj.metadata,
            "timestamp": obj.timestamp,
            "deviceId": obj.device_id,
            "sensorId": obj.sensor_id,
            "tags": obj.tags
        }

        if obj.type == "UniaxialSample":
            obj_dict["x"] = obj.x
        elif obj.type == "BiaxialSample":
            obj_dict["x"] = obj.x
            obj_dict["y"] = obj.y
        elif obj.type == "TriaxialSample":
            obj_dict["x"] = obj.x
            obj_dict["y"] = obj.y
            obj_dict["z"] = obj.z
        elif obj.type == "QuadriaxialSample":
            obj_dict["x"] = obj.x
            obj_dict["y"] = obj.y
            obj_dict["z"] = obj.z
            obj_dict["u"] = obj.u
        elif obj.type == "QuinqueaxialSample":
            obj_dict["x"] = obj.x
            obj_dict["y"] = obj.y
            obj_dict["z"] = obj.z
            obj_dict["u"] = obj.u
            obj_dict["w"] = obj.w

        return obj_dict

    @staticmethod
    def from_json(obj: Dict[str, Any]):
        if not isinstance(obj, Dict):
            raise TypeError()

        if "type" in obj and obj["type"].endswith("axialSample"):
            return TimeSeriesSample(
                type=obj["type"],
                id=obj["id"],
                acquisition_id=obj["acquisitionId"],
                metadata=obj["metadata"],
                timestamp=obj["timestamp"],
                device_id=obj["deviceId"],
                sensor_id=obj["sensorId"],
                tags=obj["tags"],
                x=obj["x"] if "x" in obj else None,
                y=obj["y"] if "y" in obj else None,
                z=obj["z"] if "z" in obj else None,
                u=obj["u"] if "u" in obj else None,
                w=obj["w"] if "w" in obj else None
            )
        return obj
