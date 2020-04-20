import io, os, json

from typing import Union, List

from .. import cache
from .. import _api_calls
from .acquisition import Acquisition
from .subjects.subject import Subject
from .devices.device import Device
from .devices.sensor import Sensor
# from .annotation.annotation import Annotation

_ENDPOINT = "api/acquisitions/"

def get(acquisitionId = None, datasetId = None, tags = []) -> Union[Acquisition, List[Acquisition]]:
    if acquisitionId is None:
        try:
            return _get_cached_acquisitions(datasetId, tags)
        except Exception as e:
            acquisitions = _api_calls.get(_ENDPOINT, params={"datasetId": datasetId, "tags": tags}).json(cls=CustomDecoder)
            for acquisition in acquisitions:
                _cache_acquisition(acquisition)
            return acquisitions
    else:
        try:
            return _get_cached_acquisition(acquisitionId)
        except Exception:
            acquisition = _api_calls.get(_ENDPOINT + acquisitionId).json(cls=CustomDecoder)
            _cache_acquisition(acquisition)
            return acquisition

# TODO Create

# TODO check if delete should be here for consistency or in the object

def count() -> int:
    return _api_calls.get(_ENDPOINT + "count").json()

# Cache

def _cache_acquisition(acquisition):
    cache_dir = cache._create_cache_dir("acquisitions")
    acquisition_file = os.path.join(cache_dir, acquisition.id)

    with io.open(acquisition_file, "w", encoding="utf8") as fd:
        fd.write(json.dumps({**acquisition}, cls=CustomEncoder))

def _list_cached_acquisitions():
    cache_dir = cache._create_cache_dir("acquisitions")

    acquisition_list = os.listdir(cache_dir)
    acquisition_list.sort()

    return acquisition_list

def _get_cached_acquisitions(datasetId, tags):
    acquisition_list = _list_cached_acquisitions()

    if len(acquisition_list) != count():
        raise Exception(f"Some acquisitions are not cached")

    acquisitions = []

    for acquisitionId in acquisition_list:
        acquisition = _get_cached_acquisition(acquisitionId)

        if datasetId != None and acquisition.datasetId != datasetId:
            continue

        # Check intersection
        if len(tags) > 0 and set(acquisition.tags).isdisjoint(tags):
            continue

        acquisitions.append(acquisition)

    return acquisitions

def _get_cached_acquisition(acquisitionId):
    cache_dir = cache._create_cache_dir("acquisitions")
    acquisition_file = os.path.join(cache_dir, acquisitionId)

    # TODO separate inner stuff

    try:
        with io.open(acquisition_file, encoding="utf8") as fd:
            acquisition = fd.read()
        return json.loads(acquisition, cls=CustomDecoder)
    except (IOError, OSError):
        raise Exception(f"Dataset {acquisitionId} not cached")


# TODO Refactor later
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (Acquisition, Subject, Device, Sensor)):
            return {**obj}
        else:
            return super().default(obj)

class CustomDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook = self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if "type" not in obj:
            return obj
        
        type = obj["type"]

        if type == "Acquisition":
            return Acquisition(**obj)
        elif type.endswith("Subject"):
            return Subject(**obj)
        elif type == "Device":
            return Device(**obj)
        elif type == "Sensor":
            return Sensor(**obj)
        else:
            return obj