from lrtableelemtype import LRTableElemType
from dataclasses import dataclass


@dataclass
class LRTableElement:
    elem_type: LRTableElemType
    elem_param: int | None
    left: str | None
    action: str
