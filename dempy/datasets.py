from typing import Union, List, Dict, Any, ByteString
from . import _api_calls, _cache
from ._base import Entity
from .acquisitions import Acquisition, get as _get_acquisition
from .protofiles import DatasetMessage


class Dataset(Entity):
    def __init__(self, type: str, id: str, tags: List[str],
                 name: str, description: str,
                 creator_id: str, owner_id: str):
        super().__init__(type, id, tags, dict())

        self.name = name
        self.description = description

        self.creator_id = creator_id
        self.owner_id = owner_id

    @property
    def acquisitions(self):
        class Inner:
            _ACQUISITIONS_ENDPOINT = _ENDPOINT + "{}/acquisitions/".format(self.id)

            @staticmethod
            def get() -> Union[Acquisition, List[Acquisition]]:
                return _get_acquisition(dataset_id=self.id)

            # @staticmethod
            # def add(acquisition_id: str) -> None:
            #     if not isinstance(acquisition_id, str):
            #         raise TypeError
            #
            #     _api_calls.put(Inner._ACQUISITIONS_ENDPOINT + acquisition_id)

            # @staticmethod
            # def remove(acquisition_id: str) -> None:
            #     if not isinstance(acquisition_id, str):
            #         raise TypeError
            #
            #     _api_calls.delete(Inner._ACQUISITIONS_ENDPOINT + acquisition_id)

            @staticmethod
            def count() -> int:
                return _api_calls.get(Inner._ACQUISITIONS_ENDPOINT + "count").json()

        return Inner()

    @staticmethod
    def to_protobuf(obj: "Dataset") -> DatasetMessage:
        if not isinstance(obj, Dataset):
            raise TypeError

        dataset_message = DatasetMessage()
        dataset_message.entity.CopyFrom(Entity.to_protobuf(obj))

        dataset_message.name = obj.name

        if obj.description is not None:
            dataset_message.description = obj.description
        if obj.creator_id is not None:
            dataset_message.creator_id = obj.creator_id
        if obj.owner_id is not None:
            dataset_message.owner_id = obj.owner_id

        return dataset_message

    @staticmethod
    def from_protobuf(obj: Union[ByteString, DatasetMessage]) -> "Dataset":
        if isinstance(obj, ByteString):
            dataset_message = DatasetMessage()
            dataset_message.ParseFromString(obj)
        elif isinstance(obj, DatasetMessage):
            dataset_message = obj
        else:
            raise TypeError

        return Dataset(
            type=dataset_message.entity.type,
            id=dataset_message.entity.id,
            tags=dataset_message.entity.tags,
            name=dataset_message.name,
            description=dataset_message.description if dataset_message.HasField("description") else None,
            creator_id=dataset_message.creator_id if dataset_message.HasField("creator_id") else None,
            owner_id=dataset_message.owner_id if dataset_message.HasField("owner_id") else None,
        )

    @staticmethod
    def from_json(obj: Dict[str, Any]) -> Any:
        if not isinstance(obj, Dict):
            raise TypeError

        if "type" in obj and obj["type"] == "Dataset":
            return Dataset(
                type=obj["type"],
                id=obj["id"],
                tags=obj["tags"],
                name=obj["name"],
                description=obj["description"],
                creator_id=obj["creatorId"],
                owner_id=obj["ownerId"],
            )
        return obj


_ENDPOINT = "api/datasets/"


def get(dataset_id: str = None, tags: List[str] = []) -> Union[Dataset, List[Dataset]]:
    if (dataset_id is not None and not isinstance(dataset_id, str)) or not isinstance(tags, List):
        raise TypeError

    if dataset_id is None:
        datasets = _api_calls.get(_ENDPOINT, params={"tags": tags}).json(object_hook=Dataset.from_json)
        for dataset in datasets:
            _cache.cache_data("datasets", dataset.id, dataset, Dataset.to_protobuf)
        return datasets
    else:
        try:
            dataset = _cache.get_cached_data("datasets", dataset_id, Dataset.from_protobuf)
        except FileNotFoundError:
            dataset = _api_calls.get(_ENDPOINT + dataset_id).json(object_hook=Dataset.from_json)
            _cache.cache_data("datasets", dataset_id, dataset, Dataset.to_protobuf)
        return dataset


def count() -> int:
    return _api_calls.get(_ENDPOINT + "count").json()
