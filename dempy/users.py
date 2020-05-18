from typing import Union, List
from . import _api_calls, _cache

class User:
    def __init__(self, type: str = "User", id: str = "", firstName: str = "", lastName: str = "", email: str = "", username: str = "", password: str = "", externalReference: str = None, active: bool = True):
        self.type = type
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.username = username
        self.password = password
        self.externalReference = externalReference
        self.active = active

    def keys(self):
        return self.__dict__.keys()

    def __eq__(self, other):
        return type(self) == type(other) and self.id == other.id

    def __getitem__(self, key):
        return getattr(self, key)

    def __repr__(self):
        return f"<User id=\"{self.id}\">"

_ENDPOINT = "api/users/"

def get(user_id: str = None) -> Union[User, List[User]]:
    if user_id != None and not isinstance(user_id, str):
        raise TypeError

    if user_id is None:
        return _api_calls.get(_ENDPOINT).json(object_hook=lambda o: User(**o))
    else:
        return _api_calls.get(_ENDPOINT + user_id).json(object_hook=lambda o: User(**o))

def create(user: User) -> User:
    if not isinstance(user, User):
        raise TypeError

    return _api_calls.post(_ENDPOINT, json={**user}).json(object_hook=lambda o: User(**o))

def delete(user_id: str):
    if not isinstance(user_id, str):
        raise TypeError

    _api_calls.delete(_ENDPOINT + user_id)

def count() -> int:
    return _api_calls.get(_ENDPOINT + "count").json()