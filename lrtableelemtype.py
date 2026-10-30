from enum import Enum


class LRTableElemType(Enum):
    ERROR = '0'
    SHIFT = '1'
    FOLD = '2'
    STOP = '3'
