class Device:
    def __init__(self, type = "Device", id = "", serialNumber = "", manufacturer = "", modelName = "", syncOffset = None, timeUnit = "SECONDS", metadata = {}, sensors = [], tags = []):
        self.type = type
        self.id = id
        self.serialNumber = serialNumber
        self.manufacturer = manufacturer
        self.modelName = modelName
        self.syncOffset = syncOffset
        self.timeUnit = timeUnit
        self.metadata = metadata
        self.sensors = sensors
        self.tags = tags

        # [MICROSECONDS, MILISECONDS, SECONDS, NANOSECONDS]
    def keys(self):
        return self.__dict__.keys()

    def __getitem__(self, key):
        return getattr(self, key)
    
    def __repr__(self):
        return f"<Device id=\"{self.id}\" manufacturer=\"{self.manufacturer}\" modelName=\"{self.modelName}\">"