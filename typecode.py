from enum import Enum


class TypeCode(Enum):
    NO_TYPE = 'no type'
    INT = 'int'
    FLOAT = 'float'
    BOOLEAN = 'boolean'

    def __len__(self):
        return {
            self.NO_TYPE: 0,
            self.INT: 4,
            self.FLOAT: 8,
            self.BOOLEAN: 1,
        }[self]
