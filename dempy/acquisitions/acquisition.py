class Acquisition:
    def __init__(self, type = "Acquisition", id = "", creationTimestamp = 0, syncOffset = None, timeUnit = "", ownerId = "", creatorId = "", datasetId = "", subject = object(), devices = [], metadata = object(), tags = [], hasTimeSeriesSamples = False, hasImageSamples = False, hasVideoSamples = False):
        self.id = id
        self.creationTimestamp = creationTimestamp
        self.syncOffset = syncOffset
        self.timeUnit = timeUnit
        self.ownerId = ownerId
        self.creatorId = creatorId
        self.datasetId = datasetId
        self.subject = subject
        self.devices = devices
        self.metadata = metadata
        self.tags = tags
        self.hasTimeSeriesSamples = hasTimeSeriesSamples
        self.hasImageSamples = hasImageSamples
        self.hasVideoSamples = hasVideoSamples

    def keys(self):
        return self.__dict__.keys()

    def __getitem__(self, key):
        return getattr(self, key)

    def __repr__(self):
        return f"<Acquisition id=\"{self.id}\">"

