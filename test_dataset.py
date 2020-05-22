import dempy

def main():

    dempy.config.use_default()

    print("Testing - Acquisitions")
    dempy.acquisitions.get()
    acq = dempy.acquisitions.get("9e4096d5-099d-443f-a0d1-65a2bd95213d")
    print("Subject:", acq.subject.get())
    print(f"Devices [{acq.devices.count()}]:", f"cached {len(acq.devices.get())}")
    print(f"Timeseries samples [{acq.timeseries_samples.count()}]:", f"cached {len(acq.timeseries_samples.get())}")
    print(f"Image samples [{acq.image_samples.count()}]:", f"cached {len(acq.image_samples.get())}")
    print(f"Video samples [{acq.video_samples.count()}]:", f"cached {len(acq.video_samples.get())}")

    acq.timeseries_samples.visualize("89715d20-faf3-49a6-ae71-c557cddb5315")
    acq.image_samples.visualize("a62478fe-5874-4ba2-b389-e37110d6d711")
    acq.video_samples.visualize("df74d79f-3cb6-49d4-8753-7621be3eee8a")


if __name__ == "__main__":
    main()
