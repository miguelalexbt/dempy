class Annotation:
    def __init__(self, type : str= "WholeImageAnnotation", id : str = "", acquisitionId : str = "", metadata = {}, annotationObject = {}, creatorId : str = "", color : str = "", notes : str = "", tags = [], annotatedSampleId : str = ""):
        self.type = type
        self.id = id
        self.type = type
        self.acquisitionId = acquisitionId
        self.annotationObject = annotationObject
        self.creatorId = creatorId
        self.color = color
        self.notes = notes
        self.metadata = metadata
        self.tags = tags
        self.annotatedSampleId = annotatedSampleId

    def keys(self):
        return self.__dict__.keys()

    def __getitem__(self, key):
        return getattr(self, key)

    def __repr__(self):
        return f"<Annotation id=\"{self.id}\" type=\"{self.type}\" sample=\"{self.annotatedSampleId}\">"
