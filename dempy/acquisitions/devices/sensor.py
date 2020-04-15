class Sensor:
    def __init__(self, type = "Sensor", id = "", manufacturer = "", modelName = "", serialNumber = "", syncOffset = None, timeUnit = "SECONDS", sensorType = "", metadata ={}, tags = []):
        self.id = id
        self.manufacturer = manufacturer
        self.modelName = modelName
        self.serialNumber = serialNumber
        self.syncOffset = syncOffset
        self.timeUnit = timeUnit
        self.sensorType = sensorType
        self.metadata = metadata
        self.tags = tags

        #[MICROSECONDS, MILISECONDS, SECONDS, NANOSECONDS]



    def keys(self):
        return self.__dict__.keys()

    def __getitem__(self, key):
        return getattr(self, key)

    def __repr__(self):
        return f"<Sensor id=\"{self.id}\">"