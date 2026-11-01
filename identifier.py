from category import Category
from typecode import TypeCode
from dataclasses import dataclass


@dataclass
class Identifier:
    lex: str
    category: Category = Category.NO_CAT
    type_code: TypeCode = TypeCode.NO_TYPE
    width: int = len(type_code)
