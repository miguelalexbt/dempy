from functools import partial
from . import config
import requests

def request(endpoint, method, **args):
    uri = f"{config.base_url}{endpoint}"

    with requests.Session() as session:
        session.headers.setdefault("content-type", "application/json")
        session.headers.setdefault("accept", "application/json")

        # TODO auth
        # if user is not None and password is not None:
        #     session.auth = (user, password)

        result = session.request(method, uri, **args)
        #print(result._content)
        result.raise_for_status()

        return result

get = partial(request, method="GET")
post = partial(request, method="POST")
patch = partial(request, method="PATCH")
put = partial(request, method="PUT")
delete = partial(request, method="DELETE")
option = partial(request, method="OPTION")
head = partial(request, method="HEAD")
