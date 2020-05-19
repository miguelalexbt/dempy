import dempy

def main():
    acq = dempy.acquisitions.get()[0]

    print(acq.devices.get()[0].sensors)


    # user = dempy.users.create(dempy.User())
    # dempy.organizations.create(dempy.Organization())
    # org = dempy.organizations.get()[0]
    # org.users.add(user.id)
    # org.users.remove(user.id)
    # dempy.users.delete(user.id)
    # dempy.organizations.delete(org.id)

    # Datasets
    # users = dempy.users.get()
    # user = dempy.users.create(dempy.User())
    # dempy.users.delete("8bb67598-f9cb-4f40-ac63-784df20d185b")

    # datasets = dempy.datasets.get()
    #
    # print(datasets)

    # dataset = dempy.datasets.create(dempy.Dataset())
    # dataset = dempy.datasets.get(dataset_id=dataset.id)
    # dempy.datasets.delete(dataset.id)
    # dempy.datasets.count()

    # dataset = dempy.datasets.get(dataset_id="0ef20ae6-b0d6-4452-8f52-f5dff8c7cdfd")
    # dataset.acquisitions.get()
    # dataset.acquisitions.count()

main()
