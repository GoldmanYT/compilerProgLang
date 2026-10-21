from codes import Code
from attribute import Attribute


class Token:
    def __init__(
            self,
            code: Code,
            attr: Attribute | int | str | None = None,
            start: int = 0,
            end: int = 0,
    ):
        self.code: Code = code
        self.attr: Attribute | int | None = attr
        self.start: int = start
        self.end: int = end
        self.lex: str | None = None

    def __str__(self):
        attr: str = 'null'

        if isinstance(self.attr, Attribute):
            attr: int = self.attr.value

        if isinstance(self.attr, int):
            attr: int = self.attr

        lex: str = ''
        if self.lex is not None:
            lex = f'\t(Лексема: {self.lex})'

        return f'<{self.code.value},\t{attr}>{lex}'

    def __repr__(self):
        return str(self)
