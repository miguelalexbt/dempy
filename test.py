import dempy
import time

# Acquisitions
# acquisitions = dempy.acquisitions.get()
# acquisition = dempy.acquisitions.create(dempy.Acquisition())
# acquisition = dempy.acquisitions.get(acquisition_id=acquisition.id)
# dempy.acquisitions.delete(acquisition.id)
# dempy.acquisitions.count()

# acquisition = dempy.acquisitions.get(acquisition_id="9e4096d5-099d-443f-a0d1-65a2bd95213d")
# x = acquisition.timeSeriesSamples.get()
# print(len(x))


















# Datasets
datasets = dempy.datasets.get()
dataset = dempy.datasets.create(dempy.Dataset())
dataset = dempy.datasets.get(dataset_id=dataset.id)
dempy.datasets.delete(dataset.id)
dempy.datasets.count()

# dataset = dempy.datasets.get(dataset_id="0ef20ae6-b0d6-4452-8f52-f5dff8c7cdfd")
# dataset.acquisitions.get()
# dataset.acquisitions.count()

# Organizations
organizations = dempy.organizations.get()
organization = dempy.organizations.create(dempy.Organization())
organization = dempy.organizations.get(organization.id)
dempy.organizations.delete(organization.id)
dempy.organizations.count()

# Users
users = dempy.users.get()
user = dempy.users.create(dempy.User())
user = dempy.users.get(user.id)
dempy.users.delete(user.id)
dempy.users.count()
