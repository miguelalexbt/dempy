from typing import List, Dict, Any
from .. import _base


class Sensor(_base.Entity):
    def __init__(self, type: str = "Sensor", id: str = "", manufacturer: str = "", model_name: str = "",
                 serial_number: str = "", sync_offset: int = None, time_unit: str = "SECONDS",
                 sensor_type: str = "", metadata: Dict[str, Any] = {}, tags: List[str] = []):
        super().__init__(type, id)
        self.manufacturer = manufacturer
        self.model_name = model_name
        self.serial_number = serial_number
        self.sync_offset = sync_offset
        self.time_unit = time_unit
        self.sensor_type = sensor_type
        self.metadata = metadata
        self.tags = tags

        #[MICROSECONDS, MILISECONDS, SECONDS, NANOSECONDS]

    @staticmethod
    def to_json(obj):
        if not isinstance(obj, Sensor):
            raise TypeError()

        return {
            "type": obj.type,
            "id": obj.id,
            "manufacturer": obj.manufacturer,
            "modelName": obj.model_name,
            "serialNumber": obj.serial_number,
            "syncOffset": obj.sync_offset,
            "timeUnit": obj.time_unit,
            "sensorType": obj.sensor_type,
            "metadata": obj.metadata,
            "tags": obj.tags
        }

    @staticmethod
    def from_json(obj: Dict[str, Any]):
        if not isinstance(obj, Dict):
            raise TypeError()

        if "type" in obj and obj["type"] == "Sensor":
            return Sensor(
                obj["type"], obj["id"], obj["manufacturer"], obj["modelName"], obj["serialNumber"],
                obj["syncOffset"], obj["timeUnit"], obj["sensorType"], obj["metadata"], obj["tags"]
            )
        return obj
