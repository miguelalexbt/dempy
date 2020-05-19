
class Entity:
    def __init__(self, type: str, id: str):
        self.type = type
        self.id = id

    @staticmethod
    def to_json(obj):
        pass

    @staticmethod
    def from_json(obj):
        pass

    def __eq__(self, other):
        return self.type == other.type and self.id == other.id

    def __repr__(self):
        return f"<{self.type} id=\"{self.id}\">"
