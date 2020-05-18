class VideoSample:
    def __init__(self, type: str = "TriaxialSample", id: str = "", acquisitionId: str = "", metadata={}, timestamp=int,
                 deviceId: str = "", sensorId: str = "", tags=[], mediaType : str = "", videoSource : str = ""):
        self.type = type
        self.id = id
        self.type = type
        self.acquisitionId = acquisitionId
        self.timestamp = timestamp
        self.deviceId = deviceId
        self.sensorId = sensorId
        self.metadata = metadata
        self.tags = tags
        self.mediaType = mediaType
        self.videoSource = videoSource

    def keys(self):
        return self.__dict__.keys()

    def __getitem__(self, key):
        return getattr(self, key)

    def __repr__(self):
        return f"<VideoSample id=\"{self.id}\" deviceId=\"{self.deviceId}\">"
