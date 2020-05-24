from functools import partial
from typing import List, Dict, Any, ByteString

from dempy._base import Entity
from dempy._protofiles import AnnotationObjectMessage, AnnotationPointMessage, AnnotationMessage


class AnnotationObject:
    def __init__(self, type: str, **kwargs):
        self.type = type

        if self.type == "AnnotationText":
            self.text: str = kwargs.get("text")
        elif self.type == "AnnotationImage":
            self.media_type: str = kwargs.get("media_type")
            self.image_source: str = kwargs.get("image_source")
        else:
            raise ValueError

    @staticmethod
    def to_protobuf(obj: "AnnotationObject") -> AnnotationObjectMessage:
        annotation_object_message = AnnotationObjectMessage()
        annotation_object_message.type = obj.type

        if obj.type == "AnnotationText":
            if obj.text is not None:
                annotation_object_message.text = obj.text
        elif obj.type == "AnnotationImage":
            if obj.media_type is not None:
                annotation_object_message.media_type = obj.media_type
            if obj.image_source is not None:
                annotation_object_message.image_source = obj.image_source
        else:
            raise ValueError

        return annotation_object_message

    @staticmethod
    def from_protobuf(annotation_object_message: AnnotationObjectMessage) -> "AnnotationObject":
        return AnnotationObject(
            type=annotation_object_message.type,
            text=annotation_object_message.text if annotation_object_message.HasField("text") else None,
            media_type=annotation_object_message.media_type if annotation_object_message.HasField("media_type") else None,
            image_source=annotation_object_message.image_source if annotation_object_message.HasField("image_source") else None,
        )

    @staticmethod
    def from_json(obj: Dict[str, Any]) -> Any:
        if "type" in obj:
            if obj["type"] == "AnnotationText":
                return AnnotationObject(
                    type=obj["type"],
                    text=obj["text"]
                )
            elif obj["type"] == "AnnotationImage":
                return AnnotationObject(
                    type=obj["type"],
                    media_type=obj["mediatype"],
                    image_source=obj["imageSource"]
                )
            else:
                raise ValueError

        return obj

    def __repr__(self):
        return f"<{self.type}>"


class AnnotationPoint:
    def __init__(self, x: float, y: float):
        self.type = "AnnotationPoint"
        self.x = x
        self.y = y

    @staticmethod
    def to_protobuf(obj: "AnnotationPoint") -> AnnotationPointMessage:
        annotation_point_message = AnnotationPointMessage()
        annotation_point_message.x = obj.x
        annotation_point_message.y = obj.y

        return annotation_point_message

    @staticmethod
    def from_protobuf(annotation_point_message: AnnotationPointMessage) -> "AnnotationPoint":
        return AnnotationPoint(
            x=annotation_point_message.x,
            y=annotation_point_message.y
        )

    @staticmethod
    def from_json(obj: Dict[str, Any]) -> Any:
        return AnnotationPoint(
            x=obj["x"],
            y=obj["y"]
        )

    def __repr__(self):
        return f"<{self.type} x=\"{self.x}\" y=\"{self.y}\">"


class Annotation(Entity):
    def __init__(self, type: str, id: str, tags: List[str], metadata: Dict[str, str], acquisition_id: str, creator_id: str,
                 annotation_object: AnnotationObject, color: str, notes: str, **kwargs):
        super().__init__(type, id, tags, metadata)
        self.acquisition_id = acquisition_id
        self.creator_id = creator_id
        self.annotation_object = annotation_object
        self.color = color
        self.notes = notes

        if self.type == "WholeImageAnnotation":
            self.annotated_sample_id: str = kwargs.get("annotated_sample_id")
        elif self.type == "PointAnnotation":
            self.annotated_sample_id: str = kwargs.get("annotated_sample_id")
            self.point: AnnotationPoint = kwargs.get("point")
        elif self.type == "CircleAnnotation":
            self.annotated_sample_id: str = kwargs.get("annotated_sample_id")
            self.center: AnnotationPoint = kwargs.get("center")
            self.radius: float = kwargs.get("radius")
        elif self.type == "DrawAnnotation":
            self.annotated_sample_id: str = kwargs.get("annotated_sample_id")
            self.points: List[AnnotationPoint] = kwargs.get("points")
        elif self.type == "RectangleAnnotation":
            self.annotated_sample_id: str = kwargs.get("annotated_sample_id")
            self.point: AnnotationPoint = kwargs.get("point")
            self.width: float = kwargs.get("width")
            self.height: float = kwargs.get("height")
        elif self.type == "PolygonAnnotation":
            self.annotated_sample_id: str = kwargs.get("annotated_sample_id")
            self.points: List[AnnotationPoint] = kwargs.get("points")
        elif self.type == "TimeSeriesInstantAnnotation":
            self.timestamp: int = kwargs.get("timestamp")
            self.device_id: str = kwargs.get("device_id")
            self.sensor_id: str = kwargs.get("sensor_id")
        elif self.type == "TimeSeriesIntervalAnnotation":
            self.timestamp_start: int = kwargs.get("timestamp_start")
            self.timestamp_end: int = kwargs.get("timestamp_end")
            self.device_id: str = kwargs.get("device_id")
            self.sensor_id: str = kwargs.get("sensor_id")
        else:
            raise ValueError

    @staticmethod
    def to_protobuf(obj: "Annotation") -> AnnotationMessage:
        annotation_message = AnnotationMessage()
        annotation_message.entity.CopyFrom(Entity.to_protobuf(obj))
        annotation_message.acquisition_id = obj.acquisition_id

        if obj.creator_id is not None:
            annotation_message.creator_id = obj.creator_id

        annotation_message.annotation_object.CopyFrom(AnnotationObject.to_protobuf(obj.annotation_object))

        if obj.color is not None:
            annotation_message.color = obj.color
        if obj.notes is not None:
            annotation_message.notes = obj.notes

        if obj.type == "WholeImageAnnotation":
            annotation_message.annotated_sample_id = obj.annotated_sample_id
        elif obj.type == "PointAnnotation":
            annotation_message.annotated_sample_id = obj.annotated_sample_id
            annotation_message.point.CopyFrom(AnnotationPoint.to_protobuf(obj.point))
        elif obj.type == "CircleAnnotation":
            annotation_message.annotated_sample_id = obj.annotated_sample_id
            annotation_message.center.CopyFrom(AnnotationPoint.to_protobuf(obj.center))
            annotation_message.radius = obj.radius
        elif obj.type == "DrawAnnotation":
            annotation_message.annotated_sample_id = obj.annotated_sample_id
            annotation_message.points.extend([AnnotationPoint.to_protobuf(p) for p in obj.points])
        elif obj.type == "RectangleAnnotation":
            annotation_message.annotated_sample_id = obj.annotated_sample_id
            annotation_message.point.CopyFrom(AnnotationPoint.to_protobuf(obj.point))
            annotation_message.width = obj.width
            annotation_message.height = obj.height
        elif obj.type == "PolygonAnnotation":
            annotation_message.annotated_sample_id = obj.annotated_sample_id
            annotation_message.points.extend([AnnotationPoint.to_protobuf(p) for p in obj.points])
        elif obj.type == "TimeSeriesInstantAnnotation":
            annotation_message.timestamp = obj.timestamp

            if obj.device_id is not None:
                annotation_message.device_id = obj.device_id
            if obj.sensor_id is not None:
                annotation_message.sensor_id = obj.sensor_id
        elif obj.type == "TimeSeriesIntervalAnnotation":
            annotation_message.timestamp_start = obj.timestamp_start
            annotation_message.timestamp_end = obj.timestamp_end

            if obj.device_id is not None:
                annotation_message.device_id = obj.device_id
            if obj.sensor_id is not None:
                annotation_message.sensor_id = obj.sensor_id
        else:
            raise ValueError

        return annotation_message

    @staticmethod
    def from_protobuf(obj: ByteString) -> "Annotation":
        annotation_message = AnnotationMessage()
        annotation_message.ParseFromString(obj)

        return Annotation(
            type=annotation_message.entity.type,
            id=annotation_message.entity.id,
            tags=annotation_message.entity.tags,
            metadata=annotation_message.entity.metadata,
            acquisition_id=annotation_message.acquisition_id,
            creator_id=annotation_message.creator_id,
            annotation_object=AnnotationObject.from_protobuf(annotation_message.annotation_object),
            color=annotation_message.color if annotation_message.HasField("color") else None,
            notes=annotation_message.notes if annotation_message.HasField("notes") else None,
            annotated_sample_id=annotation_message.annotated_sample_id if annotation_message.HasField("annotated_sample_id") else None,
            point=AnnotationPoint.from_protobuf(annotation_message.point) if annotation_message.HasField("point") else None,
            center=AnnotationPoint.from_protobuf(annotation_message.center) if annotation_message.HasField("center") else None,
            radius=annotation_message.radius if annotation_message.HasField("radius") else None,
            points=[AnnotationPoint.from_protobuf(p) for p in annotation_message.points],
            width=annotation_message.width if annotation_message.HasField("width") else None,
            height=annotation_message.height if annotation_message.HasField("height") else None,
            timestamp=annotation_message.timestamp if annotation_message.HasField("timestamp") else None,
            device_id=annotation_message.device_id if annotation_message.HasField("device_id") else None,
            sensor_id=annotation_message.sensor_id if annotation_message.HasField("sensor_id") else None,
            timestamp_start=annotation_message.timestamp_start if annotation_message.HasField("timestamp_start") else None,
            timestamp_end=annotation_message.timestamp_end if annotation_message.HasField("timestamp_end") else None,
        )

    @staticmethod
    def from_json(obj: Dict[str, Any]) -> Any:
        if "type" in obj:
            if obj["type"].endswith("Annotation"):
                annotation = partial(
                    Annotation,
                    type=obj["type"],
                    id=obj["id"],
                    tags=obj["tags"],
                    metadata=obj["metadata"],
                    acquisition_id=obj["acquisitionId"],
                    creator_id=obj["creatorId"],
                    annotation_object=obj["annotationObject"],
                    color=obj["color"],
                    notes=obj["notes"]
                )

                if obj["type"] == "WholeImageAnnotation":
                    return annotation(
                        annotated_sample_id=obj["annotatedSampleId"]
                    )
                elif obj["type"] == "PointAnnotation":
                    return annotation(
                        annotated_sample_id=obj["annotatedSampleId"],
                        point=AnnotationPoint.from_json(obj["point"])
                    )
                elif obj["type"] == "CircleAnnotation":
                    return annotation(
                        annotated_sample_id=obj["annotatedSampleId"],
                        center=AnnotationPoint.from_json(obj["center"]),
                        radius=obj["radius"]
                    )
                elif obj["type"] == "DrawAnnotation":
                    return annotation(
                        annotated_sample_id=obj["annotatedSampleId"],
                        points=[AnnotationPoint.from_json(p) for p in obj["points"]]
                    )
                elif obj["type"] == "RectangleAnnotation":
                    return annotation(
                        annotated_sample_id=obj["annotatedSampleId"],
                        point=AnnotationPoint.from_json(obj["point"]),
                        width=obj["width"],
                        height=obj["height"]
                    )
                elif obj["type"] == "PolygonAnnotation":
                    return annotation(
                        annotated_sample_id=obj["annotatedSampleId"],
                        points=[AnnotationPoint.from_json(p) for p in obj["points"]]
                    )
                elif obj["type"] == "TimeSeriesInstantAnnotation":
                    return annotation(
                        timestamp=obj["timestamp"],
                        device_id=obj["deviceId"],
                        sensor_id=obj["sensorId"]
                    )
                elif obj["type"] == "TimeSeriesIntervalAnnotation":
                    return annotation(
                        timestamp_start=obj["timestampStart"],
                        timestamp_end=obj["timestampEnd"],
                        device_id=obj["deviceId"],
                        sensor_id=obj["sensorId"]
                    )
                else:
                    raise ValueError
            elif obj["type"] == "AnnotationText" or obj["type"] == "AnnotationImage":
                return AnnotationObject.from_json(obj)
            else:
                raise ValueError

        return obj


__all__ = [
    "AnnotationObject", "AnnotationPoint", "Annotation"
]
