from typing import List
import os

class Dataset:
    def __init__(self, type = "Dataset", id = "", name = "", description = "", creatorId = None, ownerId = None, tags : List[str] = []):
        self.id = id
        self.name = name
        self.description = description
        self.creatorId = creatorId
        self.ownerId = ownerId
        self.tags = tags

    def keys(self):
        return self.__dict__.keys()

    def __getitem__(self, key):
        return getattr(self, key)

    def __repr__(self):
        return f"<Dataset id=\"{self.id}\" name=\"{self.name}\">"

class DatasetsService:
    _ENDPOINT = "api/datasets/"

    def __init__(self, api):
        self._api = api

    def __iter__(self):
        yield from self.get()

    def id(self, datasetId : str):
        return DatasetService(self._api, datasetId)

    def get(self, tags : List[str] = []) -> List[Dataset]:
        return self._api.get(self._ENDPOINT).json(object_hook = lambda o: Dataset(**o))

    def create(self, dataset : Dataset) -> Dataset:
        return self._api.post(self._ENDPOINT, json = {**dataset}).json(object_hook = lambda o: Dataset(**o))

    def count(self) -> int:
        return self._api.get(self._ENDPOINT + "count").json()

class DatasetService:
    _ENDPOINT = "api/datasets/{datasetId}/"

    def __init__(self, api, datasetId):
        self._api = api
        self._ENDPOINT = self._ENDPOINT.format(datasetId = datasetId)
        self.acquisitions = AcquisitionService(self._api, datasetId)

    def get(self) -> Dataset:
        return self._api.get(self._ENDPOINT).json(object_hook = lambda o: Dataset(**o))

    def delete(self) -> None:
        self._api.delete(self._ENDPOINT)

    def export(self, path : str) -> None:
        response = self._api.get(
            self._ENDPOINT + "export",
            headers = {"accept": "application/zip"}
        ).content

        with open(os.path.expanduser(path), "wb") as fd:
            fd.write(self._api.get(self._ENDPOINT + "export").content)

class AcquisitionService:
    _ENDPOINT = "api/datasets/{datasetId}/acquisitions/"

    def __init__(self, api, datasetId):
        self._api = api
        self._ENDPOINT = self._ENDPOINT.format(datasetId = datasetId)

    def __iter__(self):
        yield from self.get()

    def get(self) -> List[str]:
        return self._api.get(self._ENDPOINT).json()

    def add(self, acquisitionId) -> None:
        self._api.put(self._ENDPOINT + acquisitionId)

    def remove(self, acquisitionId) -> None:
        self._api.delete(self._ENDPOINT + acquisitionId)

    def count(self) -> int:
        return self._api.get(self._ENDPOINT + "count").json()