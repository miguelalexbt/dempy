from typing import Union, List, Dict, Any, ByteString
from . import cache, _api_calls
from ._base import Entity
from ._protofiles import UserMessage


class User(Entity):
    def __init__(self, type: str = "User", id: str = "", first_name: str = "", last_name: str = "",
                 email: str = "", username: str = "", password: str = "", external_reference: str = None, active: bool = True):
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
        if not isinstance(obj, User):
            raise TypeError

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
    def from_protobuf(obj: Union[ByteString, UserMessage]) -> "User":
        if isinstance(obj, ByteString):
            user_message = UserMessage()
            user_message.ParseFromString(obj)
        elif isinstance(obj, UserMessage):
            user_message = obj
        else:
            raise TypeError

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
    def from_json(obj: Dict[str, Any]) -> Any:
        if not isinstance(obj, Dict):
            raise TypeError

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
    if user_id is not None and not isinstance(user_id, str):
        raise TypeError

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


# def create(user: User) -> User:
#     if not isinstance(user, User):
#         raise TypeError
#
#     return _api_calls.post(_ENDPOINT, json=User.to_json(user)).json(object_hook=User.from_json)
#
#
# def delete(user_id: str):
#     if not isinstance(user_id, str):
#         raise TypeError
#
#     _api_calls.delete(_ENDPOINT + user_id)


def count() -> int:
    return _api_calls.get(_ENDPOINT + "count").json()
