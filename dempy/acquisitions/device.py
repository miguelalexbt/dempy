from typing import List, Union, Dict, Any
from .. import _base
from .sensor import Sensor


class Device(_base.Entity):
    def __init__(self, type: str, id: str, serial_number: str, manufacturer: str, model_name: str,
                 sync_offset: int, time_unit: str, metadata: Dict[str, Any], sensors: List[Sensor], tags: List[str]):
        super().__init__(type, id)
        self.serial_number = serial_number
        self.manufacturer = manufacturer
        self.model_name = model_name
        self.sync_offset = sync_offset
        self.time_unit = time_unit
        self.metadata = metadata
        self.tags = tags

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
    def to_json(obj):
        if not isinstance(obj, Device):
            raise TypeError()

        return {
            "type": obj.type,
            "id": obj.id,
            "serialNumber": obj.serial_number,
            "manufacturer": obj.manufacturer,
            "modelName": obj.model_name,
            "syncOffset": obj.sync_offset,
            "timeUnit": obj.time_unit,
            "metadata": obj.metadata,
            "sensors": [Sensor.to_json(sensor) for sensor in obj._sensors],
            "tags": obj.tags
        }

    @staticmethod
    def from_json(obj: Dict[str, Any]):
        if not isinstance(obj, Dict):
            raise TypeError()

        if "type" in obj:
            if obj["type"] == "Device":
                return Device(
                    type=obj["type"],
                    id=obj["id"],
                    serial_number=obj["serialNumber"],
                    manufacturer=obj["manufacturer"],
                    model_name=obj["modelName"],
                    sync_offset=obj["syncOffset"],
                    time_unit=obj["timeUnit"],
                    metadata=obj["metadata"],
                    sensors=obj["sensors"],
                    tags=obj["tags"]
                )
            elif obj["type"] == "Sensor":
                return Sensor.from_json(obj)
            else:
                raise TypeError()
        return obj
