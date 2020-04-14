from .. import _api_calls

_USER_ENDPOINT = "api/users/{userId}"

def _delete_user(userId) -> None:
    _api_calls.delete(_USER_ENDPOINT.format(userId=userId))
