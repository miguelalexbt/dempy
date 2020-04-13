from typing import List
from .user import User

class Organization:
    def __init__(self, type : str = "Organization", id : str = "", name : str = "", description : str = "", url : str = "", email : str = "", phone : str = "", usersIds : List[User] = []):
        self.id = id
        self.name = name
        self.description = description
        self.url = url
        self.email = email
        self.phone = phone
        self.usersIds = usersIds

    def keys(self):
        return self.__dict__.keys()

    def __getitem__(self, key):
        return getattr(self, key)

    def __repr__(self): #todo
        return f"<Organization id=\"{self.id}\" name=\"{self.name}\" description=\"{self.description}\" url=\"{self.url}\">"

class OrganizationsService:
    _ENDPOINT = "api/organizations/"

    def __init__(self, api):
        self._api = api

    def __iter__(self):
        yield from self.get()

    """ def __call__(self, organization: Organization):
        return OrganizationService(self._api, organization.id) """
    
    def id(self, organizationId : str):
        return OrganizationService(self._api, organizationId)

    def get(self) -> List[Organization]:
        return self._api.get(self._ENDPOINT).json(object_hook = lambda o: Organization(**o))

    def create(self, organization : Organization) -> Organization:
        return self._api.post(self._ENDPOINT, json = {**organization}).json(object_hook = lambda o: Organization(**o))

    def count(self) -> int:
        return self._api.get(self._ENDPOINT + "count").json()

class OrganizationService:
    _ENDPOINT = "api/organizations/{organizationId}"

    def __init__(self, api, organizationId):
        self._api = api
        self.users = UsersService(api, organizationId)
        self._ENDPOINT = self._ENDPOINT.format(organizationId = organizationId)

    def get(self) -> Organization:
        return self._api.get(self._ENDPOINT).json(object_hook = lambda o: Organization(**o))

    def delete(self) -> None:
        self._api.delete(self._ENDPOINT)


class UsersService:
    _ENDPOINT = "api/organizations/{organizationId}/users/"

    def __init__(self, api, organizationId):
        self._api = api
        self._ENDPOINT = self._ENDPOINT.format(organizationId = organizationId)

    def __iter__(self):
        yield from self.get()

    def get(self) -> List[str]:
        return self._api.get(self._ENDPOINT).json()

    def add(self, userId) -> None:
        self._api.put(self._ENDPOINT + userId)

    def remove(self, userId) -> None:
        self._api.delete(self._ENDPOINT + userId)

    def count(self) -> int:
        return self._api.get(self._ENDPOINT + "count").json()        
