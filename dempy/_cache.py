import io
import json
import os

from . import config


def create_cache_dir(data_dir):
    cache_dir = os.path.join(config.cache_dir, data_dir)

    try:
        os.makedirs(cache_dir)
    except OSError:
        pass

    return cache_dir


def cache_data(data_dir, data_file, data, **kwargs):
    cache_dir = create_cache_dir(data_dir)
    cache_file = os.path.join(cache_dir, data_file)

    with io.open(cache_file, "w", encoding="utf-8") as fp:
        json.dump(data, fp, **kwargs)


def get_cached_data(data_dir, data_file=None, **kwargs):
    cache_dir = create_cache_dir(data_dir)

    if data_file is None:
        cache_files = os.listdir(cache_dir)

        if len(cache_files) == 0:
            raise Exception()
        
        return [get_cached_data(dir, cache_file, **kwargs) for cache_file in cache_files]
    else:
        cache_file = os.path.join(cache_dir, data_file)

        try:
            with io.open(cache_file, "r", encoding="utf-8") as fp:
                data = json.load(fp, **kwargs)
            return data
        except (IOError, OSError):
            raise Exception()


def del_cached_data(dir, data_id):
    cache_dir = create_cache_dir(dir)
    data_file = os.path.join(cache_dir, data_id)

    try:
        os.remove(data_file)
    except (IOError, OSError):
        raise Exception()



    

# # Cache

# def _cache_acquisition(acquisition):
#     cache_dir = cache._create_cache_dir("acquisitions")
#     acquisition_file = os.path.join(cache_dir, acquisition.id)

#     with io.open(acquisition_file, "w", encoding="utf8") as fd:
#         fd.write(json.dumps({**acquisition}, cls=CustomEncoder))

# def _list_cached_acquisitions():
#     cache_dir = cache._create_cache_dir("acquisitions")

#     acquisition_list = os.listdir(cache_dir)
#     acquisition_list.sort()

#     return acquisition_list

# def _get_cached_acquisitions(datasetId, tags):
#     acquisition_list = _list_cached_acquisitions()

#     if len(acquisition_list) != count():
#         raise Exception(f"Some acquisitions are not cached")

#     acquisitions = []

#     for acquisitionId in acquisition_list:
#         acquisition = _get_cached_acquisition(acquisitionId)

#         if datasetId != None and acquisition.datasetId != datasetId:
#             continue

#         # Check intersection
#         if len(tags) > 0 and set(acquisition.tags).isdisjoint(tags):
#             continue

#         acquisitions.append(acquisition)

#     return acquisitions

# def _get_cached_acquisition(acquisitionId):
#     cache_dir = cache._create_cache_dir("acquisitions")
#     acquisition_file = os.path.join(cache_dir, acquisitionId)

#     # TODO separate inner stuff

#     try:
#         with io.open(acquisition_file, encoding="utf8") as fd:
#             acquisition = fd.read()
#         return json.loads(acquisition, cls=CustomDecoder)
#     except (IOError, OSError):
#         raise Exception(f"Dataset {acquisitionId} not cached")

