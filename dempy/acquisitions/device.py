from typing import List, Dict, Any
from .. import _base
from .sensor import Sensor


class Device(_base.Entity):
    def __init__(self, type: str = "Device", id: str = "", serial_number: str = "",
                 manufacturer: str = "", model_name: str = "", sync_offset: int = None, time_unit: str = "SECONDS",
                 metadata: Dict[str, Any] = {}, sensors: List[Sensor] = [], tags: List[str] = []):
        super().__init__(type, id)
        self.serial_number = serial_number
        self.manufacturer = manufacturer
        self.model_name = model_name
        self.sync_offset = sync_offset
        self.time_unit = time_unit
        self.metadata = metadata
        self.sensors = sensors
        self.tags = tags

        # [MICROSECONDS, MILISECONDS, SECONDS, NANOSECONDS]

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
            "sensors": obj.sensors,
            "tags": obj.tags
        }

    @staticmethod
    def from_json(obj: Dict[str, Any]):
        if not isinstance(obj, Dict):
            raise TypeError()

        if "type" in obj:
            if obj["type"] == "Device":
                return Device(
                    obj["type"], obj["id"], obj["serialNumber"], obj["manufacturer"], obj["modelName"],
                    obj["syncOffset"], obj["timeUnit"], obj["metadata"], obj["sensors"], obj["tags"]
                )
            elif obj["type"] == "Sensor":
                return Sensor.from_json(obj)
            else:
                raise TypeError()
        return obj
    
    def __repr__(self):
        return f"<Device id=\"{self.id}\">"
