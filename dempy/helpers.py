from functools import partialmethod
import requests
import json

def createSession(user : str = None, password : str = None):
    session = requests.Session()
    session.headers.setdefault("content-type", "application/json")
    session.headers.setdefault("accept", "application/json")

    # TODO auth
    # if user is not None and password is not None:
    #     session.auth = (user, password)

    return session

class ApiConnector:
    def __init__(self, base_url, session):
        if not base_url.startswith("http://"):
            raise IOError("URL must start with 'http://'")
        
        self.base_url = base_url.strip("/") + "/"
        self.session = session

    def request(self, endpoint, method, **args):
        uri = f"{self.base_url}{endpoint}"

        result = self.session.request(method, uri, **args)
        result.raise_for_status()

        return result

    get = partialmethod(request, method="GET")
    post = partialmethod(request, method="POST")
    patch = partialmethod(request, method="PATCH")
    put = partialmethod(request, method="PUT")
    delete = partialmethod(request, method="DELETE")
    option = partialmethod(request, method="OPTION")
    head = partialmethod(request, method="HEAD")
