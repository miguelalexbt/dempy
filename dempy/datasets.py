from typing import Union, List, Dict, Any, ByteString

from dempy import cache, _api_calls
from dempy._base import Entity
from dempy._protofiles import DatasetMessage
from dempy.acquisitions import Acquisition, get as _get_acquisition


class Dataset(Entity):
    """Dataset class"""
    def __init__(self, type: str, id: str, tags: List[str], name: str, description: str, creator_id: str, owner_id: str):
        super().__init__(type, id, tags, dict())
        self.name = name
        self.description = description
        self.creator_id = creator_id
        self.owner_id = owner_id

    @property
    def acquisitions(self):
        """Acquisitions' API"""
        class Inner:
            _ACQUISITIONS_ENDPOINT = _ENDPOINT + "{}/acquisitions/".format(self.id)

            @staticmethod
            def get(tags: List[str] = [], metadata: Dict[str, str] = {}) -> List[Acquisition]:
                """Get acquisitions that belong to this dataset

                Keyword Arguments:
                    tags {List[str]} -- tags of the acquisitions (default: {[]})
                    metadata {Dict[str, str]} -- metadata of the acquisitions (default: {{}})

                Returns:
                    List[Acquisition] --list of acquisitions
                """
                return _get_acquisition(dataset_id=self.id, tags=tags, metadata=metadata)

            @staticmethod
            def count() -> int:
                """Get the number of acquisitions on this dataset

                Returns:
                    int -- number of acquisitions
                """
                return _api_calls.get(Inner._ACQUISITIONS_ENDPOINT + "count").json()

        return Inner()

    @staticmethod
    def to_protobuf(obj: "Dataset") -> DatasetMessage:
        """Encode an dataset to a Protobuf message

        Arguments:
            obj {Dataset} -- dataset to be encoded

        Returns:
            DatasetMessage -- encoded dataset
        """
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
    def from_protobuf(obj: ByteString) -> "Dataset":
        """Decode a Protobuf message to {Dataset}

        Arguments:
            obj {ByteString} -- message to be decoded

        Returns:
            Dataset -- decoded dataset
        """
        dataset_message = DatasetMessage()
        dataset_message.ParseFromString(obj)

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
    def from_json(obj: Dict[str, str]) -> Any:
        """Parse a JSON dictionary to {Dataset}

        Arguments:
            obj {Dict[str, str]} -- JSON object

        Returns:
            Any -- parsed object and sub-objects
        """
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
    """Get a dataset identified by `dataset_id` or a list of all the datasets

    Keyword Arguments:
        dataset_id {str} -- id of the dataset (default: {None})
        tags {List[str]} -- tags of the datasets (default: {[]})

    Returns:
        Union[Dataset, List[Dataset]] -- dataset or list of datasets
    """
    if dataset_id is None:
        datasets = _api_calls.get(_ENDPOINT, params={"tags": tags}).json(object_hook=Dataset.from_json)
        for dataset in datasets:
            cache._cache_data("datasets", dataset.id, dataset, Dataset.to_protobuf)
        return datasets
    else:
        try:
            dataset = cache._get_cached_data("datasets", dataset_id, Dataset.from_protobuf)
        except FileNotFoundError:
            dataset = _api_calls.get(_ENDPOINT + dataset_id).json(object_hook=Dataset.from_json)
            cache._cache_data("datasets", dataset_id, dataset, Dataset.to_protobuf)
        return dataset


def count() -> int:
    """Get the number of datasets

    Returns:
        int -- number of datasets
    """
    return _api_calls.get(_ENDPOINT + "count").json()


__all__ = [
    "Dataset",
    "get", "count"
]
