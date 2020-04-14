from typing import Union, List
from .dataset import Dataset
from .. import _api_calls

_ENDPOINT = "api/datasets/"

def get(datasetId = None, tags = []) -> Union[Dataset, List[Dataset]]:
    if datasetId is None:
        return _api_calls.get(_ENDPOINT, params={"tags": tags}).json(object_hook=lambda o: Dataset(**o))
    else:
        return _api_calls.get(_ENDPOINT + datasetId).json(object_hook=lambda o: Dataset(**o))

def create(dataset : Dataset) -> Dataset:
    return _api_calls.post(_ENDPOINT, json={**dataset}).json(object_hook=lambda o: Dataset(**o))

def count() -> int:
    return _api_calls.get(_ENDPOINT + "count").json()
