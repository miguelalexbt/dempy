class Subject:
    def __init__(self, type = "HumanSubject", id = "", description = "", metadata = object(), tags = [], firstName = "", lastName = "", birthdateTimestamp = 0):
        self.id = id
        self.description = description
        self.metadata = metadata
        self.tags = tags
        self.firstName = firstName
        self.lastName = lastName
        self.birthdateTimestamp = birthdateTimestamp
    
    def keys(self):
        return self.__dict__.keys()

    def __getitem__(self, key):
        return getattr(self, key)

    def __repr__(self):
        return f"<Subject id=\"{self.id}\">"
