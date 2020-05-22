from typing import List, Union, Dict, Any, ByteString
from .._base import Entity
from .sensor import Sensor
from ..protofiles import DeviceMessage


class Device(Entity):
    def __init__(self, type: str, id: str, tags: List[str], metadata: Dict[str, Any],
                 sync_offset: int, time_unit: str,
                 serial_number: str, manufacturer: str, model_name: str,
                 sensors: List[Sensor]):
        super().__init__(type, id, tags, metadata)

        self.sync_offset = sync_offset
        self.time_unit = time_unit

        self.serial_number = serial_number
        self.manufacturer = manufacturer
        self.model_name = model_name

        self._sensors = sensors

    @property
    def sensors(self):
        class Inner:
            @staticmethod
            def get(sensor_id: str = None) -> Union[Sensor, List[Sensor]]:
                if sensor_id is not None and not isinstance(sensor_id, str):
                    raise TypeError

                if sensor_id is None:
                    return self._sensors
                else:
                    return next((sensor for sensor in self._sensors if sensor.id == sensor_id), None)

            @staticmethod
            def count() -> int:
                return len(self._sensors)

        return Inner()

    @staticmethod
    def to_protobuf(obj: "Device"):
        if not isinstance(obj, Device):
            raise TypeError

        device_message = DeviceMessage()
        device_message.entity.CopyFrom(Entity.to_protobuf(obj))

        if obj.sync_offset is not None:
            device_message.sync_offset = obj.sync_offset
        if obj.time_unit is not None:
            device_message.time_unit = obj.time_unit
        if obj.serial_number is not None:
            device_message.serial_number = obj.serial_number
        if obj.manufacturer is not None:
            device_message.manufacturer = obj.manufacturer
        if obj.model_name is not None:
            device_message.model_name = obj.model_name

        device_message.sensors.extend([Sensor.to_protobuf(s) for s in obj._sensors])

        return device_message

    @staticmethod
    def from_protobuf(obj: Union[ByteString, DeviceMessage]):
        if isinstance(obj, ByteString):
            device_message = DeviceMessage()
            device_message.ParseFromString(obj)
        elif isinstance(obj, DeviceMessage):
            device_message = obj
        else:
            raise TypeError

        return Device(
            type=device_message.entity.type,
            id=device_message.entity.id,
            tags=device_message.entity.tags,
            metadata=device_message.entity.metadata,
            sync_offset=device_message.sync_offset if device_message.HasField("sync_offset") else None,
            time_unit=device_message.time_unit if device_message.HasField("time_unit") else None,
            serial_number=device_message.serial_number if device_message.HasField("serial_number") else None,
            manufacturer=device_message.manufacturer if device_message.HasField("manufacturer") else None,
            model_name=device_message.model_name if device_message.HasField("model_name") else None,
            sensors=[Sensor.from_protobuf(s) for s in device_message.sensors]
        )

    @staticmethod
    def from_json(obj: Dict[str, Any]):
        if not isinstance(obj, Dict):
            raise TypeError()

        if "type" in obj:
            if obj["type"] == "Device":
                return Device(
                    type=obj["type"],
                    id=obj["id"],
                    tags=obj["tags"],
                    metadata=obj["metadata"],
                    sync_offset=obj["syncOffset"],
                    time_unit=obj["timeUnit"],
                    serial_number=obj["serialNumber"],
                    manufacturer=obj["manufacturer"],
                    model_name=obj["modelName"],
                    sensors=obj["sensors"],
                )
            elif obj["type"] == "Sensor":
                return Sensor.from_json(obj)
            else:
                raise TypeError()
        return obj
