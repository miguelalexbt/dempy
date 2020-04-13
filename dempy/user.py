from typing import List

class User:
    def __init__(self, type : str = "User", id = "", firstName = "", lastName = "", email = "", username : str = "", password : str = "", externalReference = None, active : bool = True):
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

    def __getitem__(self, key):
        return getattr(self, key)

    def __repr__(self):
        return f"<User name=\"{self.firstName} {self.lastName}\">"

class UsersService:
    _ENDPOINT = "api/users/"

    def __init__(self, api):
        self._api = api

    def __iter__(self):
        yield from self.get()
    
    def id(self, userId : str):
        return UserService(self._api, userId)

    def get(self) -> List[User]:
        return self._api.get(self._ENDPOINT).json(object_hook = lambda o: User(**o))

    def create(self, user : User) -> User:
        return self._api.post(self._ENDPOINT, json = {**user}).json(object_hook = lambda o: User(**o))

    def count(self) -> int:
        return self._api.get(self._ENDPOINT + "count").json()

class UserService:
    _ENDPOINT = "api/users/{userId}"

    def __init__(self, api, userId):
        self._api = api
        self._ENDPOINT = self._ENDPOINT.format(userId = userId)

    def get(self) -> User:
        return self._api.get(self._ENDPOINT).json(object_hook = lambda o: User(**o))

    def delete(self) -> None:
        self._api.delete(self._ENDPOINT)
