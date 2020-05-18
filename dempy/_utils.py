class SampleList(list):
    def by_device(self, device_id: int):
        return [i for i in self if i.deviceId == device_id]

    def by_sensor(self, sensor_id: int):
        return [i for i in self if i.sensorId == sensor_id]

class AnnotationList(list):
    def by_sample(self, sample_id: int):
        return [i for i in self if i.annotatedSampleId == sample_id]
