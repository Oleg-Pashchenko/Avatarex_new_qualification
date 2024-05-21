from enum import Enum
import dataclasses

class FieldType(Enum):
    TEXT = "text"
    ENUM = "enum"


@dataclasses.dataclass
class FieldValue:
    id: int
    name: str


@dataclasses.dataclass
class Field:
    type: FieldType
    id: int
    name: str
    content: list
    description: str
