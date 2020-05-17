import dempy

def main():

    dempy.config.use_default()

    """ Acquisitions """

    acquisition = dempy.acquisitions.get("9485e3e0-7ee1-4b84-8d27-34cc2b9cf82f")
    # timeSeriesSamples = acquisition.timeSeriesSamples.get()
    # for tss in timeSeriesSamples:
    #     print(tss)
    # print("\n")
    # print(timeSeriesSamples[0])
    # print("\n")
    # print(timeSeriesSamples.by_device("18f30887-9d81-48d7-af70-8363ed74b7a3"))
    print(acquisition.annotations.get().by_device())

def testImageSamples(acquisition):
    """ Samples """
    timeseriessamples = acquisition.timeSeriesSamples.get()
    timeseriessamples_count = acquisition.timeSeriesSamples.count()
    print(timeseriessamples[-1])
    print(timeseriessamples_count)

    videoSamples = acquisition.videoSamples.get()
    videoSamples_count = acquisition.videoSamples.count()
    print(videoSamples)
    print(videoSamples_count)

    imageSamples = acquisition.imageSamples.get()
    imageSamples_count = acquisition.imageSamples.count()
    print(imageSamples)
    print(imageSamples_count)

    annotations = acquisition.annotations.get()
    annotations_count = acquisition.annotations.count()
    print(annotations)
    print(annotations_count)

    """ End """


def testDevices(acquisition):
    """ Devices """

    ## Get Devices

    devices = acquisition.devices.get()
    print(devices)

    ## Get a Device

    first_device = acquisition.devices.get()[0]
    print(first_device)

    device_id = acquisition.devices.get("046d22c9-db2f-4e4e-96df-16fd455c6f1a") #last
    print(device_id)

    ## Devices Count

    devices_count = acquisition.devices.count()
    print("1:", devices_count)

    ## Create Device

    device = acquisition.devices.create(dempy.Device(manufacturer="MIGUEL"))

    ## Devices delete
    devices_count = acquisition.devices.count()
    print("2:", devices_count)
    acquisition.devices.delete(device.id)

    devices_count = acquisition.devices.count()
    print("3:", devices_count)

    #talvez dar ao device/subject/... o id do acquisition a que pertence
    #pergunta sobre como fazer isto vvvv
    # for device in acquisition.devices.get():
    #     device.delete()

    ## Get devices usage

    print(acquisition.devices.usage())





    """ End Devices """


def testSubject(acquisition):
    """ Subject """

    ## Get subject

    subject = acquisition.subject.get()
    print(subject)

    ## Delete subject
    acquisition.subject.delete()

    subject = acquisition.subject.get()
    print(subject)

    ## Create subject
    new_subject = acquisition.subject.create(dempy.Subject(description="1", firstName="Miguel", lastName="TEix"))

    print(new_subject)

    """ End Subject """

if __name__	== "__main__":
	main()
