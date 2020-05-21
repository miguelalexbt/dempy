from typing import List, Dict, Any
from .. import _base


class Subject(_base.Entity):
    def __init__(self, type: str, id: str, description: str, metadata: Dict[str, Any], tags: List[str],
                 first_name: str, last_name: str, birthdate_timestamp: int):
        super().__init__(type, id)
        self.description = description
        self.metadata = metadata
        self.tags = tags
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate_timestamp = birthdate_timestamp

    @staticmethod
    def to_json(obj):
        if not isinstance(obj, Subject):
            raise TypeError()

        return {
            "type": obj.type,
            "id": obj.id,
            "description": obj.description,
            "metadata": obj.metadata,
            "tags": obj.tags,
            "firstName": obj.first_name,
            "lastName": obj.last_name,
            "birthdateTimestamp": obj.birthdate_timestamp
        }

    @staticmethod
    def from_json(obj: Dict[str, Any]):
        if "type" in obj and obj["type"].endswith("Subject"):
            return Subject(
                type=obj["type"],
                id=obj["id"],
                description=obj["description"],
                metadata=obj["metadata"],
                tags=obj["tags"],
                first_name=obj["firstName"],
                last_name=obj["lastName"],
                birthdate_timestamp=obj["birthdateTimestamp"]
            )
        return obj
