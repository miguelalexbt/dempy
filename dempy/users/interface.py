from typing import Union, List

from .. import _api_calls
from .user import User

_ENDPOINT = "api/users/"

def get(userId = None) -> Union[User, List[User]]:
    if userId is None:
        return _api_calls.get(_ENDPOINT).json(object_hook = lambda o: User(**o))
    else:
        return _api_calls.get(_ENDPOINT + userId).json(object_hook = lambda o: User(**o))

def create(user : User) -> User:
    return _api_calls.post(_ENDPOINT, json = {**user}).json(object_hook = lambda o: User(**o))

def count() -> int:
    return _api_calls.get(_ENDPOINT + "count").json()
