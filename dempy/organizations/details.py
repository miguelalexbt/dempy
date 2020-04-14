from .. import _api_calls

_ORGANIZATION_ENDPOINT = "api/organizations/{organizationId}/"
_USERS_ENDPOINT = "api/organizations/{organizationId}/users/"

def _delete_organization(organizationId) -> None:
    _api_calls.delete(_ORGANIZATION_ENDPOINT.format(organizationId=organizationId))

def _get_users(organizationId):
    return _api_calls.get(_USERS_ENDPOINT.format(organizationId=organizationId)).json()

def _add_user(organizationId, userId) -> None:
    _api_calls.put(_USERS_ENDPOINT.format(organizationId=organizationId) + userId)

def _remove_user(organizationId, userId) -> None:
    _api_calls.delete(_USERS_ENDPOINT.format(organizationId=organizationId) + userId)

def _count_users(organizationId) -> int:
    return _api_calls.get(_USERS_ENDPOINT.format(organizationId=organizationId) + "count").json()        
