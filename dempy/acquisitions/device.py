from typing import Union, List, Dict, Any

from dempy._base import Entity
from dempy._protofiles import DeviceMessage
from dempy.acquisitions.sensor import Sensor


class Device(Entity):
    """Device class"""
    def __init__(self, type: str, id: str, tags: List[str], metadata: Dict[str, str], sync_offset: int, time_unit: str, serial_number: str,
                 manufacturer: str, model_name: str, sensors: List[Sensor]):
        super().__init__(type, id, tags, metadata)
        self.sync_offset = sync_offset
        self.time_unit = time_unit
        self.serial_number = serial_number
        self.manufacturer = manufacturer
        self.model_name = model_name
        self._sensors = sensors

    @property
    def sensors(self):
        """Sensors' API"""
        class Inner:
            @staticmethod
            def get(sensor_id: str = None, tags: List[str] = [], metadata: Dict[str, str] = {}) -> Union[Sensor, List[Sensor]]:
                """Get all the sensors that belong to this device

                Keyword Arguments:
                    sensor_id {str} -- id of the sensor (default: {None})
                    tags {List[str]} -- tags of the sensor (default: {[]})
                    metadata {Dict[str, str]} -- metadata of the sensor (default: {{}})

                Raises:
                    IndexError: sensor identified by `sensor_id` does not exist in this device

                Returns:
                    Union[Sensor, List[Sensor]] -- sensor or list of sensors
                """                
                if sensor_id is None:
                    if len(tags) > 0 or len(metadata) > 0:
                        return [s for s in self._sensors if
                                len([k for k in s.metadata if k in metadata and s.metadata[k] == metadata[k]]) > 0]

                    return self._sensors
                else:
                    try:
                        sensor = next((sensor for sensor in self._sensors if sensor.id == sensor_id))
                    except StopIteration:
                        raise IndexError(f"sensor id {sensor_id} does not exist in acquisition id {self.id}")
                    return sensor

            @staticmethod
            def count() -> int:
                """Get the number of sensors on this device

                Returns:
                    int -- number of sensors
                """
                return len(self._sensors)

        return Inner()

    @staticmethod
    def to_protobuf(obj: "Device") -> DeviceMessage:
        """Encode an device to a Protobuf message

        Arguments:
            obj {Device} -- device to be encoded

        Returns:
            DeviceMessage -- encoded device
        """
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
    def from_protobuf(device_message: DeviceMessage) -> "Device":
        """Decode a Protobuf message to {Device}

        Arguments:
            obj {DeviceMessage} -- message to be decoded

        Returns:
            Device -- decoded device
        """
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
    def from_json(obj: Dict[str, str]) -> Any:
        """Parse a JSON dictionary to {Device}

        Arguments:
            obj {Dict[str, str]} -- JSON object

        Raises:
            ValueError: unexpected object or sub-object

        Returns:
            Any -- parsed object and sub-objects
        """
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
                raise ValueError

        return obj


__all__ = [
    "Device"
]
