from typing import Union, List, Dict, Any
from . import _base, _api_calls, _cache
from .acquisitions import Acquisition, get as _get_acquisition


class Dataset(_base.Entity):
    def __init__(self, type: str = "Dataset", id: str = "", name: str = "", description: str = "",
                 creator_id: str = None, owner_id: str = None, tags: List = []):
        super().__init__(type, id)
        self.name = name
        self.description = description
        self.creator_id = creator_id
        self.owner_id = owner_id
        self.tags = tags

    @property
    def acquisitions(self):
        class Inner:
            _ACQUISITIONS_ENDPOINT = _ENDPOINT + "{}/acquisitions/".format(self.id)

            @staticmethod
            def get() -> Union[Acquisition, List[Acquisition]]:
                return _get_acquisition(dataset_id=self.id)

            @staticmethod
            def add(acquisition_id: str) -> None:
                if not isinstance(acquisition_id, str):
                    raise TypeError()

                _api_calls.put(Inner._ACQUISITIONS_ENDPOINT + acquisition_id)

            @staticmethod
            def remove(acquisition_id: str) -> None:
                if not isinstance(acquisition_id, str):
                    raise TypeError()

                _api_calls.delete(Inner._ACQUISITIONS_ENDPOINT + acquisition_id)

            @staticmethod
            def count() -> int:
                return _api_calls.get(Inner._ACQUISITIONS_ENDPOINT + "count").json()

        return Inner()

    @staticmethod
    def to_json(obj):
        if not isinstance(obj, Dataset):
            raise TypeError()

        return {
            "type": obj.type,
            "id": obj.id,
            "name": obj.name,
            "description": obj.description,
            "creatorId": obj.creator_id,
            "ownerId": obj.owner_id,
            "tags": obj.tags
        }

    @staticmethod
    def from_json(obj: Dict[str, Any]):
        if not isinstance(obj, Dict):
            raise TypeError()

        if "type" in obj and obj["type"] == "Dataset":
            return Dataset(
                obj["type"], obj["id"], obj["name"], obj["description"],
                obj["creatorId"], obj["ownerId"], obj["tags"]
            )
        return obj


_ENDPOINT = "api/datasets/"


def get(dataset_id: str = None, tags: List[str] = []) -> Union[Dataset, List[Dataset]]:
    if (dataset_id is not None and not isinstance(dataset_id, str)) or not isinstance(tags, List):
        raise TypeError()

    if dataset_id is None:
        datasets = _api_calls.get(_ENDPOINT, params={"tags": tags}).json(object_hook=Dataset.from_json)
        for dataset in datasets:
            _cache.cache_data("datasets", dataset, default=Dataset.to_json)
        return datasets
    else:
        try:
            dataset = _cache.get_cached_data("datasets", dataset_id, object_hook=Dataset.from_json)
        except:
            dataset = _api_calls.get(_ENDPOINT + dataset_id).json(object_hook=Dataset.from_json)
            _cache.cache_data("datasets", dataset, default=Dataset.to_json)
        return dataset


def create(dataset: Dataset) -> Dataset:
    if not isinstance(dataset, Dataset):
        raise TypeError()

    dataset = _api_calls.post(_ENDPOINT, json=Dataset.to_json(dataset)).json(object_hook=Dataset.from_json)
    _cache.cache_data("datasets", dataset)

    return dataset


def delete(dataset_id: str) -> None:
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
