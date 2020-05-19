class SampleList(list):
    def by_device(self, device_id: str):
        if not isinstance(device_id, str):
            raise TypeError()

        return [i for i in self if i.deviceId == device_id]

    def by_sensor(self, sensor_id: str):
        if not isinstance(sensor_id, str):
            raise TypeError()

        return [i for i in self if i.sensorId == sensor_id]


class AnnotationList(list):
    def by_sample(self, sample_id: str):
        if not isinstance(sample_id, str):
            raise TypeError()

        return [i for i in self if i.annotated_sample_id == sample_id]