from functools import partial

import requests

from dempy import config


def request(endpoint: str, method: str, **kwargs) -> requests.Response:
    uri = f"{config.base_url}{endpoint}"

    with requests.Session() as session:
        session.headers.setdefault("content-type", "application/json")
        session.headers.setdefault("accept", "application/json")

        # TODO Auth
        # if user is not None and password is not None:
        #     session.auth = (user, password)

        result = session.request(method, uri, **kwargs)
        result.raise_for_status()

        return result


get = partial(request, method="GET")
post = partial(request, method="POST")
patch = partial(request, method="PATCH")
put = partial(request, method="PUT")
delete = partial(request, method="DELETE")
option = partial(request, method="OPTION")
head = partial(request, method="HEAD")
