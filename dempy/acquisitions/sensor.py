from typing import List, Dict, Any, ByteString, Union
from .._base import Entity
from ..protofiles import SensorMessage


class Sensor(Entity):
    def __init__(self, type: str, id: str, tags: List[str], metadata: Dict[str, Any],
                 sync_offset: int, time_unit: str,
                 serial_number: str, manufacturer: str, model_name: str, sensor_type: str):
        super().__init__(type, id, tags, metadata)

        self.sync_offset = sync_offset
        self.time_unit = time_unit

        self.serial_number = serial_number
        self.manufacturer = manufacturer
        self.model_name = model_name
        self.sensor_type = sensor_type

    @staticmethod
    def to_protobuf(obj: "Sensor") -> SensorMessage:
        if not isinstance(obj, Sensor):
            raise TypeError

        sensor_message = SensorMessage()
        sensor_message.entity.CopyFrom(Entity.to_protobuf(obj))

        if obj.sync_offset is not None:
            sensor_message.sync_offset = obj.sync_offset
        if obj.time_unit is not None:
            sensor_message.time_unit = obj.time_unit
        if obj.serial_number is not None:
            sensor_message.serial_number = obj.serial_number
        if obj.manufacturer is not None:
            sensor_message.manufacturer = obj.manufacturer
        if obj.model_name is not None:
            sensor_message.model_name = obj.model_name
        if obj.sensor_type is not None:
            sensor_message.sensor_type = obj.sensor_type

        return sensor_message

    @staticmethod
    def from_protobuf(obj: Union[ByteString, SensorMessage]) -> "Sensor":
        if isinstance(obj, ByteString):
            sensor_message = SensorMessage()
            sensor_message.ParseFromString(obj)
        elif isinstance(obj, SensorMessage):
            sensor_message = obj
        else:
            raise TypeError

        return Sensor(
            type=sensor_message.entity.type,
            id=sensor_message.entity.id,
            tags=sensor_message.entity.tags,
            metadata=sensor_message.entity.metadata,
            sync_offset=sensor_message.sync_offset if sensor_message.HasField("sync_offset") else None,
            time_unit=sensor_message.time_unit if sensor_message.HasField("time_unit") else None,
            serial_number=sensor_message.serial_number if sensor_message.HasField("serial_number") else None,
            manufacturer=sensor_message.manufacturer if sensor_message.HasField("manufacturer") else None,
            model_name=sensor_message.model_name if sensor_message.HasField("model_name") else None,
            sensor_type=sensor_message.sensor_type if sensor_message.HasField("sensor_type") else None,
        )

    @staticmethod
    def from_json(obj: Dict[str, Any]) -> Any:
        if not isinstance(obj, Dict):
            raise TypeError

        if "type" in obj and obj["type"] == "Sensor":
            return Sensor(
                type=obj["type"],
                id=obj["id"],
                tags=obj["tags"],
                metadata=obj["metadata"],
                sync_offset=obj["syncOffset"],
                time_unit=obj["timeUnit"],
                serial_number=obj["serialNumber"],
                manufacturer=obj["manufacturer"],
                model_name=obj["modelName"],
                sensor_type=obj["sensorType"],
            )
        return obj
