from typing import List, Dict, Any, ByteString, Union
from .._base import Entity
from ..protofiles import TimeseriesMessage


class TimeseriesSample(Entity):
    def __init__(self, type: str, id: str, tags: List[str], metadata: Dict[str, Any],
                 timestamp: int, acquisition_id: str, device_id: str, sensor_id: str,
                 x: int = None, y: int = None, z: int = None, u: int = None, w: int = None):
        super().__init__(type, id, tags, metadata)

        self.timestamp = timestamp
        self.acquisition_id = acquisition_id
        self.device_id = device_id
        self.sensor_id = sensor_id

        self.x = x
        self.y = y
        self.z = z
        self.u = u
        self.w = w

    @staticmethod
    def to_protobuf(obj: "TimeseriesSample"):
        if not isinstance(obj, TimeseriesSample):
            raise TypeError

        timeseries_message = TimeseriesMessage()
        timeseries_message.entity.CopyFrom(Entity.to_protobuf(obj))

        timeseries_message.timestamp = obj.timestamp
        timeseries_message.acquisition_id = obj.acquisition_id

        if obj.device_id is not None:
            timeseries_message.device_id = obj.device_id
        if obj.sensor_id is not None:
            timeseries_message.sensor_id = obj.sensor_id

        if obj.type == "UniaxialSample":
            timeseries_message.x = obj.x
        elif obj.type == "BiaxialSample":
            timeseries_message.x = obj.x
            timeseries_message.y = obj.y
        elif obj.type == "TriaxialSample":
            timeseries_message.x = obj.x
            timeseries_message.y = obj.y
            timeseries_message.z = obj.z
        elif obj.type == "QuadriaxialSample":
            timeseries_message.x = obj.x
            timeseries_message.y = obj.y
            timeseries_message.z = obj.z
            timeseries_message.u = obj.u
        elif obj.type == "QuinqueaxialSample":
            timeseries_message.x = obj.x
            timeseries_message.y = obj.y
            timeseries_message.z = obj.z
            timeseries_message.u = obj.u
            timeseries_message.w = obj.w

        return timeseries_message

    @staticmethod
    def from_protobuf(obj: Union[ByteString, TimeseriesMessage]):
        if isinstance(obj, ByteString):
            timeseries_message = TimeseriesMessage()
            timeseries_message.ParseFromString(obj)
        elif isinstance(obj, TimeseriesMessage):
            timeseries_message = obj
        else:
            raise TypeError

        return TimeseriesSample(
            type=timeseries_message.entity.type,
            id=timeseries_message.entity.id,
            tags=timeseries_message.entity.tags,
            metadata=timeseries_message.entity.metadata,
            timestamp=timeseries_message.timestamp,
            acquisition_id=timeseries_message.acquisition_id,
            device_id=timeseries_message.device_id if timeseries_message.HasField("device_id") else None,
            sensor_id=timeseries_message.sensor_id if timeseries_message.HasField("sensor_id") else None,
            x=timeseries_message.x if timeseries_message.HasField("x") else None,
            y=timeseries_message.y if timeseries_message.HasField("y") else None,
            z=timeseries_message.z if timeseries_message.HasField("z") else None,
            u=timeseries_message.u if timeseries_message.HasField("u") else None,
            w=timeseries_message.w if timeseries_message.HasField("w") else None
        )

    @staticmethod
    def from_json(obj: Dict[str, Any]):
        if not isinstance(obj, Dict):
            raise TypeError()

        if "type" in obj and obj["type"].endswith("axialSample"):
            return TimeseriesSample(
                type=obj["type"],
                id=obj["id"],
                tags=obj["tags"],
                metadata=obj["metadata"],
                timestamp=obj["timestamp"],
                acquisition_id=obj["acquisitionId"],
                device_id=obj["deviceId"],
                sensor_id=obj["sensorId"],
                x=obj["x"] if "x" in obj else None,
                y=obj["y"] if "y" in obj else None,
                z=obj["z"] if "z" in obj else None,
                u=obj["u"] if "u" in obj else None,
                w=obj["w"] if "w" in obj else None
            )
        return obj
