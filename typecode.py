from enum import Enum


class TypeCode(Enum):
    NO_TYPE = 'no type'
    INTEGER = 'integer'
    FLOAT = 'float'
    BOOLEAN = 'boolean'

    def __len__(self):
        return {
            self.NO_TYPE: 0,
            self.INTEGER: 4,
            self.FLOAT: 8,
            self.BOOLEAN: 1,
        }[self]
