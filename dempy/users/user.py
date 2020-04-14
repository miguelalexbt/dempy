from .details import (
    _delete_user
)

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

    def delete(self):
        _delete_user(self.id)

    def keys(self):
        return self.__dict__.keys()

    def __getitem__(self, key):
        return getattr(self, key)

    def __repr__(self):
        return f"<User name=\"{self.firstName} {self.lastName}\">"