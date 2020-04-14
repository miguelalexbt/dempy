from .details import (
    _delete_dataset, _export_dataset,
    _get_acquisitions, _add_acquisition, _remove_acquisition, _count_acquisitions
)

class Dataset:
    def __init__(self, type = "Dataset", id = "", name = "", description = "", creatorId = None, ownerId = None, tags = []):
        self.id = id
        self.name = name
        self.description = description
        self.creatorId = creatorId
        self.ownerId = ownerId
        self.tags = tags

    @property
    def acquisitions(self):
        class inner:
            @staticmethod
            def get():
                return _get_acquisitions(self.id)

            @staticmethod
            def add(acquisitionId):
                _add_acquisition(self.id, acquisitionId)

            @staticmethod
            def remove(acquisitionId):
                _remove_acquisition(self.id, acquisitionId)

            @staticmethod
            def count():
                return _count_acquisitions(self.id)

        return inner()

    def delete(self):
        _delete_dataset(self.id)

    def export(self, path):
        _export_dataset(self.id, path)

    def keys(self):
        return self.__dict__.keys()

    def __getitem__(self, key):
        return getattr(self, key)

    def __repr__(self):
        return f"<Dataset id=\"{self.id}\" name=\"{self.name}\">"