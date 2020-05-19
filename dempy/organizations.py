from typing import Union, List
from . import _base, _api_calls


class Organization(_base.Entity):
    def __init__(self, type: str = "Organization", id: str = "", name: str = "", description: str = "",
                 url: str = "", email: str = "", phone: str = ""):
        super().__init__(type, id)
        self.name = name
        self.description = description
        self.url = url
        self.email = email
        self.phone = phone

    @property
    def users(self):
        class Inner:
            _USERS_ENDPOINT = _ENDPOINT + "{}/users/".format(self.id)

            @staticmethod
            def get():
                return _api_calls.get(Inner._USERS_ENDPOINT).json()
            
            @staticmethod
            def add(user_id: str) -> None:
                if not isinstance(user_id, str):
                    raise TypeError()

                _api_calls.put(Inner._USERS_ENDPOINT + user_id)
            
            @staticmethod
            def remove(user_id: str) -> None:
                if not isinstance(user_id, str):
                    raise TypeError()

                _api_calls.delete(Inner._USERS_ENDPOINT + user_id)

            @staticmethod
            def count() -> int:
                return _api_calls.get(Inner._USERS_ENDPOINT + "count").json()

        return Inner()

    @staticmethod
    def to_json(obj):
        return {
            "type": obj.type,
            "id": obj.id,
            "name": obj.name,
            "description": obj.description,
            "url": obj.url,
            "email": obj.email,
            "phone": obj.phone,
        }

    @staticmethod
    def from_json(obj):
        if "type" in obj and obj["type"] == "Organization":
            return Organization(
                obj["type"], obj["id"], obj["name"], obj["description"],
                obj["url"], obj["email"], obj["phone"]
            )
        return obj

    def __repr__(self):
        return f"<Organization id=\"{self.id}\">"


_ENDPOINT = "api/organizations/"


def get(organization_id: str = None) -> Union[Organization, List[Organization]]:
    if organization_id is not None and not isinstance(organization_id, str):
        raise TypeError()

    if organization_id is None:
        return _api_calls.get(_ENDPOINT).json(object_hook=Organization.from_json)
    else:
        return _api_calls.get(_ENDPOINT + organization_id).json(object_hook=Organization.from_json)


def create(organization: Organization) -> Organization:
    if not isinstance(organization, Organization):
        raise TypeError()

    return _api_calls.post(_ENDPOINT, json=Organization.to_json(organization)).json(object_hook=Organization.from_json)


def delete(organization_id: str) -> None:
    if not isinstance(organization_id, str):
        raise TypeError()

    _api_calls.delete(_ENDPOINT + organization_id)


def count() -> int:
    return _api_calls.get(_ENDPOINT + "count").json()
