from typing import List, Dict, Any
from .. import _base


class Annotation(_base.Entity):
    def __init__(self, type: str = "WholeImageAnnotation", id: str = "", acquisition_id: str = "",
                 metadata: Dict[str, Any] = {}, annotation_object: Dict[str, Any] = {}, creator_id: str = "",
                 color: str = "", notes: str = "", tags: List[str] = [], annotated_sample_id: str = ""):
        super().__init__(type, id)
        self.acquisition_id = acquisition_id
        self.annotation_object = annotation_object
        self.creator_id = creator_id
        self.color = color
        self.notes = notes
        self.metadata = metadata
        self.tags = tags
        self.annotated_sample_id = annotated_sample_id

    @staticmethod
    def to_json(obj):
        if not isinstance(obj, Annotation):
            raise TypeError()

        return {
                "type": obj.type,
                "id": obj.id,
                "acquisitionId": obj.acquisition_id,
                "metadata": obj.metadata,
                "annotationObject": obj.annotation_object,
                "creatorId": obj.creator_id,
                "color": obj.color,
                "notes": obj.notes,
                "tags": obj.tags,
                "annotatedSampleId": obj.annotated_sample_id
        }

    @staticmethod
    def from_json(obj: Dict[str, Any]):
        if not isinstance(obj, Dict):
            raise TypeError()

        if "type" in obj and obj["type"].endswith("Annotation"):
            return Annotation(
                type=obj["type"],
                id=obj["id"],
                acquisition_id=obj["acquisitionId"],
                metadata=obj["metadata"],
                annotation_object=obj["annotationObject"],
                creator_id=obj["creatorId"],
                color=obj["color"],
                notes=obj["notes"],
                tags=obj["tags"],
                annotated_sample_id=obj["annotatedSampleId"]
            )
        return obj
