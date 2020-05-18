from typing import Union, List
from . import _api_calls, _cache

class Organization:
    def __init__(self, type: str = "Organization", id: str = "", name: str = "", description: str = "", url: str = "", email: str = "", phone: str = "", usersIds: List = []):
        self.type = type
        self.id = id
        self.name = name
        self.description = description
        self.url = url
        self.email = email
        self.phone = phone
        self.usersIds = usersIds

    @property
    def users(self):
        class inner:
            _USERS_ENDPOINT = _ENDPOINT + "{}/users/".format(self.id)

            @staticmethod
            def get():
                return _api_calls.get(inner._USERS_ENDPOINT).json()
            
            @staticmethod
            def add(user_id):
                _api_calls.put(inner._USERS_ENDPOINT + user_id)
            
            @staticmethod
            def remove(user_id):
                _api_calls.delete(inner._USERS_ENDPOINT + user_id)

            @staticmethod
            def count():
                return _api_calls.get(inner._USERS_ENDPOINT + "count").json()

        return inner()

    def keys(self):
        return self.__dict__.keys()

    def __getitem__(self, key):
        return getattr(self, key)

    def __repr__(self):
        return f"<Organization id=\"{self.id}\">"

_ENDPOINT = "api/organizations/"

def get(organization_id: str = None) -> Union[Organization, List[Organization]]:
    if organization_id != None and not isinstance(organization_id, str):
        raise TypeError()

    if organization_id is None:
        return _api_calls.get(_ENDPOINT).json(object_hook=lambda o: Organization(**o))
    else:
        return _api_calls.get(_ENDPOINT + organization_id).json(object_hook=lambda o: Organization(**o))

def create(organization: Organization) -> Organization:
    if not isinstance(organization, Organization):
        raise TypeError()

    return _api_calls.post(_ENDPOINT, json = {**organization}).json(object_hook=lambda o: Organization(**o))

def delete(organization_id: str) -> None:
    if not isinstance(organization_id, str):
        raise TypeError()

    _api_calls.delete(_ENDPOINT + organization_id)

def count() -> int:
    return _api_calls.get(_ENDPOINT + "count").json()
