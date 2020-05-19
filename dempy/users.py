from typing import Union, List, Dict, Any
from . import _base, _api_calls


class User(_base.Entity):
    def __init__(self, type: str = "User", id: str = "", first_name: str = "", last_name: str = "",
                 email: str = "", username: str = "", password: str = "",
                 external_reference: str = None, active: bool = True):
        super().__init__(type, id)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password = password
        self.external_reference = external_reference
        self.active = active

    @staticmethod
    def to_json(obj):
        if not isinstance(obj, User):
            raise TypeError()

        return {
            "type": obj.type,
            "id": obj.id,
            "firstName": obj.first_name,
            "lastName": obj.last_name,
            "email": obj.email,
            "username": obj.username,
            "password": obj.password,
            "externalReference": obj.external_reference,
            "active": obj.active
        }

    @staticmethod
    def from_json(obj: Dict[str, Any]):
        if not isinstance(obj, Dict):
            raise TypeError()

        if "type" in obj and obj["type"] == "User":
            return User(
                obj["type"], obj["id"], obj["firstName"], obj["lastName"],
                obj["email"], obj["username"], obj["password"],
                obj["externalReference"], obj["active"]
            )
        return obj

    def __repr__(self):
        return f"<User id=\"{self.id}\">"


_ENDPOINT = "api/users/"


def get(user_id: str = None) -> Union[User, List[User]]:
    if user_id is not None and not isinstance(user_id, str):
        raise TypeError

    if user_id is None:
        return _api_calls.get(_ENDPOINT).json(object_hook=User.from_json)
    else:
        return _api_calls.get(_ENDPOINT + user_id).json(object_hook=User.from_json)


def create(user: User) -> User:
    if not isinstance(user, User):
        raise TypeError

    return _api_calls.post(_ENDPOINT, json=User.to_json(user)).json(object_hook=User.from_json)


def delete(user_id: str):
    if not isinstance(user_id, str):
        raise TypeError

    _api_calls.delete(_ENDPOINT + user_id)


def count() -> int:
    return _api_calls.get(_ENDPOINT + "count").json()
