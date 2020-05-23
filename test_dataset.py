import dempy


def main():
    dempy.config.use_default()

    print("Testing - Users")
    print(f"Users [{dempy.users.count()}]:", f"cached {len(dempy.users.get())}")
    dempy.users.get("e695c872-edb4-4488-932b-2f49dd5c1b04")

    print("---")

    print("Testing - Organizations")
    print(f"Organizations [{dempy.organizations.count()}]:", f"cached {len(dempy.organizations.get())}")
    org = dempy.organizations.get("5729b044-800e-425a-8a58-a4b4c9aa86e4")
    print(f"Users [{org.users.count()}]:", f"cached {len(org.users.get())}")

    print("---")

    print("Testing - Datasets")
    print(f"Datasets [{dempy.datasets.count()}]:", f"cached {len(dempy.datasets.get())}")
    dts = dempy.datasets.get("0ef20ae6-b0d6-4452-8f52-f5dff8c7cdfd")
    print(f"Acquisitions [{dts.acquisitions.count()}]:", f"cached {len(dts.acquisitions.get())}")

    print("---")

    print("Testing - Acquisitions")
    dempy.acquisitions.get()
    acq = dempy.acquisitions.get("9e4096d5-099d-443f-a0d1-65a2bd95213d")
    print("Subject:", acq.subject.get())
    print(f"Devices [{acq.devices.count()}]:", f"cached {len(acq.devices.get())}")
    print(f"Timeseries samples [{acq.timeseries_samples.count()}]:", f"cached {len(acq.timeseries_samples.get())}")
    print(f"Image samples [{acq.image_samples.count()}]:", f"cached {len(acq.image_samples.get())}")
    print(f"Video samples [{acq.video_samples.count()}]:", f"cached {len(acq.video_samples.get())}")

    # acq.timeseries_samples.visualize("89715d20-faf3-49a6-ae71-c557cddb5315")
    # acq.image_samples.visualize("a62478fe-5874-4ba2-b389-e37110d6d711")
    # acq.video_samples.visualize("df74d79f-3cb6-49d4-8753-7621be3eee8a")


if __name__ == "__main__":
    main()
