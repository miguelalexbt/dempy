class TimeSeriesSample:
    def __init__(self, type : str= "TriaxialSample", id : str = "", acquisitionId : str = "", metadata = {}, timestamp = int, deviceId : str = "", sensorId : str = "", tags = [], x : int = 0, y : int = None, z : int = None, u : int = None, w : int = None):
        self.id = id
        self.type = type
        self.acquisitionId = acquisitionId
        self.timestamp = timestamp
        self.deviceId = deviceId
        self.sensorId = sensorId
        self.metadata = metadata
        self.tags = tags
        self.x = x
        self.y = y
        self.z = z
        self.u = u
        self.w = w

    def __init__(self,**o):
        for k,v in o.items():
            setattr(self, k, v)

    def keys(self):
        return self.__dict__.keys()

    def __getitem__(self, key):
        return getattr(self, key)

    def __repr__(self):
        #TODO: rever isto meter logo no init dentro de uma list?
        point = [self.x]
        if hasattr(self, 'y'):
            point.append(self.y)
        if hasattr(self, 'z'):
            point.append(self.z)
        if hasattr(self, 'u'):
            point.append(self.u)
        if hasattr(self, 'w'):
            point.append(self.w)
        return f"<TimeSeriesSample id=\"{self.id}\" deviceId=\"{self.deviceId}\">"
