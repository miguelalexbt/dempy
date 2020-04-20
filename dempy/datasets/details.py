import os

from .. import _api_calls
from ..acquisitions import interface as acquisitions_interface

_DATASET_ENDPOINT = "api/datasets/{datasetId}/"
_ACQUISITIONS_ENDPOINT = "api/datasets/{datasetId}/acquisitions/"

def _delete_dataset(datasetId : str) -> None:
    _api_calls.delete(_DATASET_ENDPOINT.format(datasetId=datasetId))

def _export_dataset(datasetId : str, path : str) -> None:
    response = _api_calls.get(
        _DATASET_ENDPOINT.format(datasetId=datasetId) + "export",
        headers = {"accept": "application/zip"}
    ).content

    with open(os.path.expanduser(path), "wb") as fd:
        fd.write(response)

def _get_acquisitions(datasetId):
    return acquisitions_interface.get(datasetId=datasetId)

def _add_acquisition(datasetId, acquisitionId) -> None:
    _api_calls.put(_ACQUISITIONS_ENDPOINT.format(datasetId=datasetId) + acquisitionId)

def _remove_acquisition(datasetId, acquisitionId) -> None:
    _api_calls.delete(_ACQUISITIONS_ENDPOINT.format(datasetId=datasetId) + acquisitionId)

def _count_acquisitions(datasetId) -> int:
    return _api_calls.get(_ACQUISITIONS_ENDPOINT.format(datasetId=datasetId) + "count").json()