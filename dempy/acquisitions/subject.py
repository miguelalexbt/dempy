from typing import List, Union, Dict, Any, ByteString
from .._base import Entity
from .._protofiles import SubjectMessage


class Subject(Entity):
    def __init__(self, type: str, id: str, description: str, metadata: Dict[str, Any], tags: List[str],
                 first_name: str, last_name: str, birthdate_timestamp: int):
        super().__init__(type, id, tags, metadata)

        self.birthdate_timestamp = birthdate_timestamp
        self.description = description
        self.first_name = first_name
        self.last_name = last_name

    @staticmethod
    def to_protobuf(obj: "Subject") -> SubjectMessage:
        if not isinstance(obj, Subject):
            raise TypeError

        subject_message = SubjectMessage()
        subject_message.entity.CopyFrom(Entity.to_protobuf(obj))

        subject_message.birthdate_timestamp = obj.birthdate_timestamp

        if obj.description is not None:
            subject_message.description = obj.description
        if obj.first_name is not None:
            subject_message.first_name = obj.first_name
        if obj.last_name is not None:
            subject_message.last_name = obj.last_name

        return subject_message

    @staticmethod
    def from_protobuf(obj: Union[ByteString, SubjectMessage]) -> "Subject":
        if isinstance(obj, ByteString):
            subject_message = SubjectMessage()
            subject_message.ParseFromString(obj)
        elif isinstance(obj, SubjectMessage):
            subject_message = obj
        else:
            raise TypeError

        return Subject(
            type=subject_message.entity.type,
            id=subject_message.entity.id,
            tags=subject_message.entity.tags,
            metadata=subject_message.entity.metadata,
            birthdate_timestamp=subject_message.birthdate_timestamp if subject_message.HasField("birthdate_timestamp") else None,
            description=subject_message.description if subject_message.HasField("description") else None,
            first_name=subject_message.first_name if subject_message.HasField("first_name") else None,
            last_name=subject_message.last_name if subject_message.HasField("last_name") else None,
        )

    @staticmethod
    def from_json(obj: Dict[str, Any]) -> Any:
        if not isinstance(obj, Dict):
            raise TypeError

        if "type" in obj and obj["type"].endswith("Subject"):
            return Subject(
                type=obj["type"],
                id=obj["id"],
                metadata=obj["metadata"],
                tags=obj["tags"],
                birthdate_timestamp=obj["birthdateTimestamp"],
                description=obj["description"],
                first_name=obj["firstName"],
                last_name=obj["lastName"]
            )
        return obj
