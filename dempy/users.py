from typing import Union, List, Dict, Any, ByteString

from dempy import cache, _api_calls
from dempy._base import Entity
from dempy._protofiles import UserMessage


class User(Entity):
    """User class"""
    def __init__(self, type: str, id: str, first_name: str, last_name: str, email: str, username: str, password: str,
                 external_reference: str, active: bool):
        super().__init__(type, id, list(), dict())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password = password
        self.external_reference = external_reference
        self.active = active

    @staticmethod
    def to_protobuf(obj: "User") -> UserMessage:
        """Encode an user to a Protobuf message

        Arguments:
            obj {User} -- user to be encoded

        Returns:
            UserMessage -- encoded user
        """
        user_message = UserMessage()
        user_message.entity.CopyFrom(Entity.to_protobuf(obj))

        if obj.first_name is not None:
            user_message.first_name = obj.first_name
        if obj.last_name is not None:
            user_message.last_name = obj.last_name
        if obj.email is not None:
            user_message.email = obj.email

        user_message.username = obj.username
        user_message.password = obj.password

        if obj.external_reference is not None:
            user_message.external_reference = obj.external_reference

        user_message.active = obj.active

        return user_message

    @staticmethod
    def from_protobuf(obj: ByteString) -> "User":
        """Decode a Protobuf message to {User}

        Arguments:
            obj {ByteString} -- message to be decoded

        Returns:
            User -- decoded user
        """
        user_message = UserMessage()
        user_message.ParseFromString(obj)

        return User(
            type=user_message.entity.type,
            id=user_message.entity.id,
            first_name=user_message.first_name if user_message.HasField("first_name") else None,
            last_name=user_message.last_name if user_message.HasField("last_name") else None,
            email=user_message.email if user_message.HasField("email") else None,
            username=user_message.username,
            password=user_message.password,
            external_reference=user_message.external_reference if user_message.HasField("external_reference") else None,
            active=user_message.active
        )

    @staticmethod
    def from_json(obj: Dict[str, str]) -> Any:
        """Parse a JSON dictionary to {User}

        Arguments:
            obj {Dict[str, str]} -- JSON object

        Returns:
            Any -- parsed object and sub-objects
        """
        if "type" in obj and obj["type"] == "User":
            return User(
                type=obj["type"],
                id=obj["id"],
                first_name=obj["firstName"],
                last_name=obj["lastName"],
                email=obj["email"],
                username=obj["username"],
                password=obj["password"],
                external_reference=obj["externalReference"],
                active=obj["active"]
            )

        return obj


_ENDPOINT = "api/users/"


def get(user_id: str = None) -> Union[User, List[User]]:
    """Get an user identified by `user_id` or a list of all users

    Keyword Arguments:
        user_id {str} -- id of the user (default: {None})

    Returns:
        Union[User, List[User]] -- user or list of users
    """
    if user_id is None:
        users = _api_calls.get(_ENDPOINT).json(object_hook=User.from_json)
        for user in users:
            cache._cache_data("users", user.id, user, User.to_protobuf)
        return users
    else:
        try:
            user = cache._get_cached_data("users", user_id, User.from_protobuf)
        except FileNotFoundError:
            user = _api_calls.get(_ENDPOINT + user_id).json(object_hook=User.from_json)
            cache._cache_data("users", user_id, user, User.to_protobuf)
        return user


def count() -> int:
    """Get the number of users

    Returns:
        int -- number of users
    """
    return _api_calls.get(_ENDPOINT + "count").json()


__all__ = [
    "User",
    "get", "count"
]
