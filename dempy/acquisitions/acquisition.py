from .details import (
    _delete_subject, _create_subject, _get_device, _create_device, _get_device_usage, _delete_device, _modify_device
)

class Acquisition:
    def __init__(self, type = "Acquisition", id = "", creationTimestamp = 0, syncOffset = None, timeUnit = "", ownerId = "", creatorId = "", datasetId = "", subject = object(), devices = [], metadata = object(), tags = [], hasTimeSeriesSamples = False, hasImageSamples = False, hasVideoSamples = False):
        self.id = id
        self.creationTimestamp = creationTimestamp
        self.syncOffset = syncOffset
        self.timeUnit = timeUnit
        self.ownerId = ownerId
        self.creatorId = creatorId
        self.datasetId = datasetId
        self._subjectData = subject
        self._devicesData = devices
        self.metadata = metadata
        self.tags = tags
        self.hasTimeSeriesSamples = hasTimeSeriesSamples
        self.hasImageSamples = hasImageSamples
        self.hasVideoSamples = hasVideoSamples

    @property
    def devices(self):
        class inner:
            @staticmethod
            def get(deviceId=None):
                if deviceId is None:
                    return self._devicesData
                else:
                    return _get_device(self.id, deviceId) #TODO: verificar isto

            @staticmethod
            def count():
                return len(self._devicesData)

            @staticmethod
            def create(device):
                device_created = _create_device(self.id, device)
                self._devicesData.append(device_created)
                return device_created

            """@staticmethod
            def modify(deviceId, new_device):
                return _modify_device(self.id, deviceId, new_device)
                pass"""

            @staticmethod
            def delete(deviceId):
                #self._devicesData = [device for device in self._devicesData if device.id != deviceId]
                for index in range(len(self._devicesData)):
                    if self._devicesData[index].id == deviceId:
                        del self._devicesData[index]
                _delete_device(self.id, deviceId)


            @staticmethod
            def usage():
                return _get_device_usage(self.id)


        return inner()

    @property
    def subject(self):
        class inner:
            @staticmethod
            def get():
                return self._subjectData
            
            @staticmethod
            def delete():
                _delete_subject(self.id, self._subjectData.id)
                self._subjectData = None

            @staticmethod
            def create(subject):
                self._subjectData = _create_subject(self.id, subject)
                return self._subjectData

        return inner() 

    def keys(self):
        return self.__dict__.keys()

    def __getitem__(self, key):
        return getattr(self, key)

    def __repr__(self):
        return f"<Acquisition id=\"{self.id}\">"

