import io, os, json

from typing import Union, List

from .. import cache
from .. import _api_calls
from .dataset import Dataset

_ENDPOINT = "api/datasets/"

def get(datasetId = None, tags = []) -> Union[Dataset, List[Dataset]]:
    if datasetId is None:
        try:
            return _get_cached_datasets(tags)
        except Exception:
            datasets = _api_calls.get(_ENDPOINT, params={"tags": tags}).json(object_hook=lambda o: Dataset(**o))
            for dataset in datasets:
                _cache_dataset(dataset)
            return datasets
    else:
        try:
            return _get_cached_dataset(datasetId)
        except Exception:
            dataset = _api_calls.get(_ENDPOINT + datasetId).json(object_hook=lambda o: Dataset(**o))
            _cache_dataset(dataset)
            return dataset

def create(dataset : Dataset) -> Dataset:
    dataset = _api_calls.post(_ENDPOINT, json={**dataset}).json(object_hook=lambda o: Dataset(**o))
    _cache_dataset(dataset)
    return dataset

def count() -> int:
    return _api_calls.get(_ENDPOINT + "count").json()

# Cache

def _cache_dataset(dataset):
    cache_dir = cache._create_cache_dir("datasets")
    dataset_file = os.path.join(cache_dir, dataset.id)

    with io.open(dataset_file, "w", encoding="utf8") as fd:
        fd.write(json.dumps({**dataset}))

# TODO
# def _remove_cache(dataset):
#    pass

def _list_cached_datasets():
    cache_dir = cache._create_cache_dir("datasets")

    dataset_list = os.listdir(cache_dir)
    dataset_list.sort()

    return dataset_list

def _get_cached_datasets(tags):
    dataset_list = _list_cached_datasets()

    if len(dataset_list) != count():
        raise Exception(f"Some datasets are not cached")

    datasets = []

    for datasetId in dataset_list:
        dataset = _get_cached_dataset(datasetId)

        # Check intersection
        if len(tags) > 0 and set(dataset.tags).isdisjoint(tags):
            continue

        datasets.append(dataset)

    return datasets

def _get_cached_dataset(datasetId) -> Dataset:
    cache_dir = cache._create_cache_dir("datasets")
    dataset_file = os.path.join(cache_dir, datasetId)

    try:
        with io.open(dataset_file, encoding="utf8") as fd:
            dataset = fd.read()
        return json.loads(dataset, object_hook=lambda o: Dataset(**o))
    except (IOError, OSError):
        print(f"Dataset {datasetId} not cached")
        raise Exception(f"Dataset {datasetId} not cached")

