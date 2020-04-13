from .dataset import DatasetsService
# from .acquisition import AcquisitionsService
# from .organization import OrganizationsService
from .user import UsersService
from .helpers import *

class DemAPI:

    def __init__(self, host : str):
        api = ApiConnector(host, createSession())

        self.datasets = DatasetsService(api)
        # self.acquisitions = AcquisitionsService(api)
        # self.organizations = OrganizationsService(api)
        self.users = UsersService(api)