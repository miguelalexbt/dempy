from typing import List, Dict, ByteString

from dempy._protofiles import EntityMessage


class Entity:
    def __init__(self, type: str, id: str, tags: List[str], metadata: Dict[str, str]):
        self.type = type
        self.id = id
        self.tags = tags
        self.metadata = metadata

    @staticmethod
    def to_protobuf(obj: "Entity") -> EntityMessage:
        entity_message = EntityMessage()
        entity_message.type = obj.type
        entity_message.id = obj.id
        entity_message.tags.extend(obj.tags)
        entity_message.metadata.update(obj.metadata)

        return entity_message

    @staticmethod
    def from_protobuf(obj: ByteString) -> "Entity":
        pass

    def __eq__(self, other):
        return self.type == other.type and self.id == other.id

    def __repr__(self):
        return f"<{self.type} id=\"{self.id}\">"

