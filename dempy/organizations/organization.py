from .details import (
    _delete_organization,
    _get_users, _add_user, _remove_user, _count_users
)

class Organization:
    def __init__(self, type : str = "Organization", id : str = "", name : str = "", description : str = "", url : str = "", email : str = "", phone : str = "", usersIds = []):
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
            @staticmethod
            def get():
                return _get_users(self.id)
            
            @staticmethod
            def add(userId):
                _add_user(self.id, userId)
            
            @staticmethod
            def remove(userId):
                _remove_user(self.id, userId)

            @staticmethod
            def count():
                return _count_users(self.id)

        return inner()

    def delete(self):
        return _delete_organization(self.id)

    def keys(self):
        return self.__dict__.keys()

    def __getitem__(self, key):
        return getattr(self, key)

    def __repr__(self): #todo
        return f"<Organization id=\"{self.id}\" name=\"{self.name}\" description=\"{self.description}\" url=\"{self.url}\">"