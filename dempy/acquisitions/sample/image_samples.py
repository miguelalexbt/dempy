class ImageSample:
    def __init__(self, type: str = "TriaxialSample", id: str = "", acquisitionId: str = "", metadata={}, timestamp=int,
                 deviceId: str = "", sensorId: str = "", tags=[], mediaType : str = "", imageSource : str = "", hasRotationMetadata : bool = False):
        self.id = id
        self.type = type
        self.acquisitionId = acquisitionId
        self.timestamp = timestamp
        self.deviceId = deviceId
        self.sensorId = sensorId
        self.metadata = metadata
        self.tags = tags
        self.mediaType = mediaType
        self.imageSource = imageSource
        self.hasRotationMetadata = hasRotationMetadata


    def keys(self):
        return self.__dict__.keys()

    def __getitem__(self, key):
        return getattr(self, key)

    def __repr__(self):
        return f"<ImageSample id=\"{self.id}\" deviceId=\"{self.deviceId}\">"
