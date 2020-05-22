from typing import Union, List, Dict, Any, ByteString
from . import _base, _api_calls, _cache
from .acquisitions import Acquisition, get as _get_acquisition
from .protofiles import dataset_pb2


class Dataset(_base.Entity):
    def __init__(self, type: str, id: str, name: str, description: str, creator_id: str, owner_id: str, tags: List[str]):
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
    def serialize(obj) -> dataset_pb2.Dataset:
        if not isinstance(obj, Dataset):
            raise TypeError

        dataset = dataset_pb2.Dataset()
        dataset.type = obj.type
        dataset.id = obj.id
        dataset.name = obj.name

        if obj.description is not None:
            dataset.description = obj.description
        if obj.creator_id is not None:
            dataset.creator_id = obj.creator_id
        if obj.owner_id is not None:
            dataset.owner_id = obj.owner_id

        dataset.tags.extend(obj.tags)

        return dataset.SerializeToString()

    @staticmethod
    def deserialize(obj: ByteString):
        if not isinstance(obj, ByteString):
            raise TypeError

        dataset = dataset_pb2.Dataset()
        dataset.ParseFromString(obj)

        return Dataset(
            type=dataset.type,
            id=dataset.id,
            name=dataset.name,
            description=dataset.description if dataset.HasField("description") else None,
            creator_id=dataset.creator_id if dataset.HasField("creator_id") else None,
            owner_id=dataset.owner_id if dataset.HasField("owner_id") else None,
            tags=dataset.tags
        )

    @staticmethod
    def to_json(obj):
        if not isinstance(obj, Dataset):
            raise TypeError

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
                type=obj["type"],
                id=obj["id"],
                name=obj["name"],
                description=obj["description"],
                creator_id=obj["creatorId"],
                owner_id=obj["ownerId"],
                tags=obj["tags"]
            )
        return obj


_ENDPOINT = "api/datasets/"


def get(dataset_id: str = None, tags: List[str] = []) -> Union[Dataset, List[Dataset]]:
    if (dataset_id is not None and not isinstance(dataset_id, str)) or not isinstance(tags, List):
        raise TypeError

    if dataset_id is None:
        datasets = _api_calls.get(_ENDPOINT, params={"tags": tags}).json(object_hook=Dataset.from_json)
        for dataset in datasets:
            _cache.cache_data_protobuf("datasets", dataset.id, dataset, Dataset.serialize)
            # _cache.cache_data("datasets", dataset.id, dataset, default=Dataset.to_json)
        return datasets
    else:
        try:
            dataset = _cache.get_cached_data_protobuf("datasets", dataset_id, Dataset.deserialize)
            # dataset = _cache.get_cached_data("datasets", dataset_id, object_hook=Dataset.from_json)
        except:
            dataset = _api_calls.get(_ENDPOINT + dataset_id).json(object_hook=Dataset.from_json)
            _cache.cache_data_protobuf("datasets", dataset_id, dataset, Dataset.serialize)
            # _cache.cache_data("datasets", dataset_id, dataset, default=Dataset.to_json)
        return dataset


# def create(dataset: Dataset) -> Dataset:
#     if not isinstance(dataset, Dataset):
#         raise TypeError
#
#     dataset = _api_calls.post(_ENDPOINT, json=Dataset.to_json(dataset)).json(object_hook=Dataset.from_json)
#     _cache.cache_data("datasets", dataset)
#
#     return dataset
#
#
# def delete(dataset_id: str) -> None:
#     if not isinstance(dataset_id, str):
#         raise TypeError
#
#     _api_calls.delete(_ENDPOINT + dataset_id)
#     _cache.del_cached_data("datasets", dataset_id)


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
