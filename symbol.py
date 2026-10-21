from category import Category
from typecode import TypeCode


class Symbol:
    def __init__(
            self,
            lex: str,
            category: Category = Category.NO_CAT,
            type_code: TypeCode = TypeCode.NO_TYPE,
            width: int = 0,
    ):
        self.lex: str = lex
        self.category: Category = category
        self.type_code: TypeCode = type_code
        self.width: int = width
