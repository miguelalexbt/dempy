import dempy
import time
import json


def main():

    dempy.config.use_default()

    start_time = time.time()

    acq = dempy.acquisitions.get(acquisition_id="9e4096d5-099d-443f-a0d1-65a2bd95213d")

    acq.timeseries_samples.visualize(device_id=acq.devices.get()[0].id)

    acq.timeseries_samples.visualize(device_id=acq.devices.get()[0].id, sensor_id=acq.devices.get()[0].sensors.get()[0].id)

    print("--- ", time.time() - start_time, " ---")


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


if __name__ == "__main__":
    main()
