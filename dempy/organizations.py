from typing import Union, List, Dict, Any, ByteString
from . import _api_calls, _cache
from ._base import Entity
from .users import User, get as _get_user
from ._protofiles import OrganizationMessage


class Organization(Entity):
    def __init__(self, type: str, id: str, name: str, description: str, url: str, email: str, phone: str, users_ids: List[str]):
        super().__init__(type, id, list(), dict())

        self.name = name
        self.description = description
        self.url = url
        self.email = email
        self.phone = phone

        self._users_ids = users_ids

    @property
    def users(self):
        class Inner:
            _USERS_ENDPOINT = _ENDPOINT + "{}/users/".format(self.id)

            @staticmethod
            def get() -> List[User]:
                return [_get_user(u) for u in self._users_ids]
                # return _api_calls.get(Inner._USERS_ENDPOINT).json()
            
            # @staticmethod
            # def add(user_id: str) -> None:
            #     if not isinstance(user_id, str):
            #         raise TypeError
            #
            #     _api_calls.put(Inner._USERS_ENDPOINT + user_id)
            #
            # @staticmethod
            # def remove(user_id: str) -> None:
            #     if not isinstance(user_id, str):
            #         raise TypeError
            #
            #     _api_calls.delete(Inner._USERS_ENDPOINT + user_id)

            @staticmethod
            def count() -> int:
                return len(self._users_ids)
                # return _api_calls.get(Inner._USERS_ENDPOINT + "count").json()

        return Inner()

    @staticmethod
    def to_protobuf(obj: "Organization") -> OrganizationMessage:
        if not isinstance(obj, Organization):
            raise TypeError

        organization_message = OrganizationMessage()
        organization_message.entity.CopyFrom(Entity.to_protobuf(obj))

        organization_message.name = obj.name

        if obj.description is not None:
            organization_message.description = obj.description
        if obj.url is not None:
            organization_message.url = obj.url
        if obj.email is not None:
            organization_message.email = obj.email
        if obj.phone is not None:
            organization_message.phone = obj.phone

        organization_message.users_ids.extend(obj._users_ids)

        return organization_message

    @staticmethod
    def from_protobuf(obj: Union[ByteString, OrganizationMessage]) -> "Organization":
        if isinstance(obj, ByteString):
            organization_message = OrganizationMessage()
            organization_message.ParseFromString(obj)
        elif isinstance(obj, OrganizationMessage):
            organization_message = obj
        else:
            raise TypeError

        return Organization(
            type=organization_message.entity.type,
            id=organization_message.entity.id,
            name=organization_message.name,
            description=organization_message.description if organization_message.HasField("description") else None,
            url=organization_message.url if organization_message.HasField("url") else None,
            email=organization_message.email if organization_message.HasField("email") else None,
            phone=organization_message.phone if organization_message.HasField("phone") else None,
            users_ids=organization_message.users_ids
        )

    @staticmethod
    def from_json(obj: Dict[str, Any]) -> Any:
        if not isinstance(obj, Dict):
            raise TypeError

        if "type" in obj and obj["type"] == "Organization":
            return Organization(
                type=obj["type"],
                id=obj["id"],
                name=obj["name"],
                description=obj["description"],
                url=obj["url"],
                email=obj["email"],
                phone=obj["phone"],
                users_ids=obj["usersIds"]
            )
        return obj


_ENDPOINT = "api/organizations/"


def get(organization_id: str = None) -> Union[Organization, List[Organization]]:
    if organization_id is not None and not isinstance(organization_id, str):
        raise TypeError

    if organization_id is None:
        organizations = _api_calls.get(_ENDPOINT).json(object_hook=Organization.from_json)
        for organization in organizations:
            _cache.cache_data("organizations", organization.id, organization, Organization.to_protobuf)
        return organizations
    else:
        try:
            organization = _cache.get_cached_data("organizations", organization_id, Organization.from_protobuf)
        except FileNotFoundError:
            organization = _api_calls.get(_ENDPOINT + organization_id).json(object_hook=Organization.from_json)
            _cache.cache_data("organizations", organization_id, organization, Organization.to_protobuf)
        return organization


# def create(organization: Organization) -> Organization:
#     if not isinstance(organization, Organization):
#         raise TypeError
#
#     return _api_calls.post(_ENDPOINT, json=Organization.to_json(organization)).json(object_hook=Organization.from_json)
#
#
# def delete(organization_id: str) -> None:
#     if not isinstance(organization_id, str):
#         raise TypeError
#
#     _api_calls.delete(_ENDPOINT + organization_id)


def count() -> int:
    return _api_calls.get(_ENDPOINT + "count").json()
