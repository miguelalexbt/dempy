from typing import Union, List

from .. import _api_calls
from .organization import Organization

_ENDPOINT = "api/organizations/"

def get(organizationId = None) -> Union[Organization, List[Organization]]:
    if organizationId is None:
        return _api_calls.get(_ENDPOINT).json(object_hook = lambda o: Organization(**o))
    else:
        return _api_calls.get(_ENDPOINT + organizationId).json(object_hook = lambda o: Organization(**o))

def create(organization : Organization) -> Organization:
    return _api_calls.post(_ENDPOINT, json = {**organization}).json(object_hook = lambda o: Organization(**o))

def count() -> int:
    return _api_calls.get(_ENDPOINT + "count").json()