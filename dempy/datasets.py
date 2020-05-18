from typing import Union, List
from . import _api_calls, _cache
from .acquisitions import Acquisition, get as _get_acquisition

class Dataset:
    def __init__(self, type: str = "Dataset", id: str = "", name: str = "", description: str = "", creatorId: str = None, ownerId: str = None, tags: List = []):
        self.type = type
        self.id = id
        self.name = name
        self.description = description
        self.creatorId = creatorId
        self.ownerId = ownerId
        self.tags = tags

    @property
    def acquisitions(self):
        class inner:
            _ACQUISITIONS_ENDPOINT = _ENDPOINT + "{}/acquisitions/".format(self.id)

            @staticmethod
            def get() -> Union[Acquisition, List[Acquisition]]:
                return _get_acquisition(dataset_id=self.id)

            @staticmethod
            def add(acquisition_id: str) -> None:
                _api_calls.put(inner._ACQUISITIONS_ENDPOINT + acquisition_id)

            @staticmethod
            def remove(acquisition_id: str) -> None:
                _api_calls.delete(inner._ACQUISITIONS_ENDPOINT + acquisition_id)

            @staticmethod
            def count() -> int:
                return _api_calls.get(inner._ACQUISITIONS_ENDPOINT + "count").json()

        return inner()

    def keys(self):
        return self.__dict__.keys()

    def __getitem__(self, key):
        return getattr(self, key)

    def __repr__(self):
        return f"<Dataset id=\"{self.id}\">"

# Interface

_ENDPOINT = "api/datasets/"

def get(dataset_id: str = None, tags: List = []) -> Union[Dataset, List[Dataset]]:
    if (dataset_id != None and not isinstance(dataset_id, str)) or not isinstance(tags, List):
        raise TypeError()

    if dataset_id != None:
        try:
            dataset = _cache.get_cached_data("datasets", dataset_id, object_hook=lambda o: Dataset(**o))
        except Exception:
            dataset = _api_calls.get(_ENDPOINT + dataset_id).json(object_hook=lambda o: Dataset(**o))
            _cache.cache_data("datasets", dataset)
        return dataset
    else:
        datasets = _api_calls.get(_ENDPOINT, params={"tags": tags}).json(object_hook=lambda o: Dataset(**o))
        for dataset in datasets:
            _cache.cache_data("datasets", dataset)
        return datasets

def create(dataset: Dataset) -> Dataset:
    if not isinstance(dataset, Dataset):
        raise TypeError()

    dataset = _api_calls.post(_ENDPOINT, json={**dataset}).json(object_hook=lambda o: Dataset(**o))
    _cache.cache_data("datasets", dataset)

    return dataset

def delete(dataset_id : str) -> None:
    if not isinstance(dataset_id, str):
        raise TypeError()

    _api_calls.delete(_ENDPOINT + dataset_id)
    _cache.del_cached_data("datasets", dataset_id)

def count() -> int:
    return _api_calls.get(_ENDPOINT + "count").json()

# TODO prob wont use
# def _export_dataset(datasetId : str, path : str) -> None:
#     response = _api_calls.get(
#         _DATASET_ENDPOINT.format(datasetId=datasetId) + "export",
#         headers = {"accept": "application/zip"}
#     ).content

#     with open(os.path.expanduser(path), "wb") as fd:
#         fd.write(response)