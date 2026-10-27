from typing import Iterable
from attribute import Attribute
from category import Category
from char import Char
from codes import Code
from state import State
from identifier import Identifier
from tokens import Token
from collections import defaultdict
from typecode import TypeCode


class Scanner:
    VARIANT: str = '15'
    KEYWORDS: dict[str, Code] = {
        'procedure' + VARIANT: Code.LC_PROG,
        Code.LC_USING.value + VARIANT: Code.LC_USING,
        Code.LC_CLASS.value + VARIANT: Code.LC_CLASS,
        Code.LC_VAR.value + VARIANT: Code.LC_VAR,
        Code.LC_WHILE.value + VARIANT: Code.LC_WHILE,
        Code.LC_TRUE.value: Code.LC_TRUE,
        Code.LC_FALSE.value: Code.LC_FALSE,
        'KuznetsovDA': Code.LC_FULLNAME,
    }
    STATE_TABLE: dict[Char, dict[State, State]] = {
        Char.TAB: {
            State.INITIAL: State.SPACE,
            State.SLASH: State.SLASH_OTHER,
            State.AMP: State.ERR_AMP,
            State.VERT_SLASH: State.ERR_VERT_SLASH,
            State.LESS: State.LESS_OTHER,
            State.LETTER: State.LETTER_OTHER,
            State.GREATER: State.GREATER_OTHER,
            State.DIGIT: State.DIGIT_OTHER,
            State.DIGIT_DOT: State.ERR_NUMBER,
            State.DIGIT_DOT_DIGIT: State.DIGIT_DOT_DIGIT_OTHER,
            State.SPACE: State.SPACE,
            State.DASH: State.DASH_OTHER,
            State.DASH_DASH: State.DASH_DASH,
            State.DASH_DASH_DASH: State.DASH_DASH,
        },
        Char.LF: {
            State.INITIAL: State.SPACE,
            State.SLASH: State.SLASH_OTHER,
            State.AMP: State.ERR_AMP,
            State.VERT_SLASH: State.ERR_VERT_SLASH,
            State.LESS: State.LESS_OTHER,
            State.LETTER: State.LETTER_OTHER,
            State.GREATER: State.GREATER_OTHER,
            State.DIGIT: State.DIGIT_OTHER,
            State.DIGIT_DOT: State.ERR_NUMBER,
            State.DIGIT_DOT_DIGIT: State.DIGIT_DOT_DIGIT_OTHER,
            State.SPACE: State.SPACE,
            State.DASH: State.DASH_OTHER,
            State.DASH_DASH: State.DASH_DASH,
            State.DASH_DASH_DASH: State.DASH_DASH,
        },
        Char.SPACE: {
            State.INITIAL: State.SPACE,
            State.SLASH: State.SLASH_OTHER,
            State.AMP: State.ERR_AMP,
            State.VERT_SLASH: State.ERR_VERT_SLASH,
            State.LESS: State.LESS_OTHER,
            State.LETTER: State.LETTER_OTHER,
            State.GREATER: State.GREATER_OTHER,
            State.DIGIT: State.DIGIT_OTHER,
            State.DIGIT_DOT: State.ERR_NUMBER,
            State.DIGIT_DOT_DIGIT: State.DIGIT_DOT_DIGIT_OTHER,
            State.SPACE: State.SPACE,
            State.DASH: State.DASH_OTHER,
            State.DASH_DASH: State.DASH_DASH,
            State.DASH_DASH_DASH: State.DASH_DASH,
        },
        Char.EXCL: {
            State.INITIAL: State.EXCL,
            State.SLASH: State.SLASH_OTHER,
            State.AMP: State.ERR_AMP,
            State.VERT_SLASH: State.ERR_VERT_SLASH,
            State.LESS: State.LESS_OTHER,
            State.LETTER: State.LETTER_OTHER,
            State.GREATER: State.GREATER_OTHER,
            State.DIGIT: State.DIGIT_OTHER,
            State.DIGIT_DOT: State.ERR_NUMBER,
            State.DIGIT_DOT_DIGIT: State.DIGIT_DOT_DIGIT_OTHER,
            State.SPACE: State.SPACE_OTHER,
            State.DASH: State.DASH_OTHER,
            State.DASH_DASH: State.DASH_DASH,
            State.DASH_DASH_DASH: State.DASH_DASH,
        },
        Char.AMP: {
            State.INITIAL: State.AMP,
            State.SLASH: State.SLASH_OTHER,
            State.AMP: State.AMP_AMP,
            State.VERT_SLASH: State.ERR_VERT_SLASH,
            State.LESS: State.LESS_OTHER,
            State.LETTER: State.LETTER_OTHER,
            State.GREATER: State.GREATER_OTHER,
            State.DIGIT: State.DIGIT_OTHER,
            State.DIGIT_DOT: State.ERR_NUMBER,
            State.DIGIT_DOT_DIGIT: State.DIGIT_DOT_DIGIT_OTHER,
            State.SPACE: State.SPACE_OTHER,
            State.DASH: State.DASH_OTHER,
            State.DASH_DASH: State.DASH_DASH,
            State.DASH_DASH_DASH: State.DASH_DASH,
        },
        Char.OP_PAR: {
            State.INITIAL: State.OP_PAR,
            State.SLASH: State.SLASH_OTHER,
            State.AMP: State.ERR_AMP,
            State.VERT_SLASH: State.ERR_VERT_SLASH,
            State.LESS: State.LESS_OTHER,
            State.LETTER: State.LETTER_OTHER,
            State.GREATER: State.GREATER_OTHER,
            State.DIGIT: State.DIGIT_OTHER,
            State.DIGIT_DOT: State.ERR_NUMBER,
            State.DIGIT_DOT_DIGIT: State.DIGIT_DOT_DIGIT_OTHER,
            State.SPACE: State.SPACE_OTHER,
            State.DASH: State.DASH_OTHER,
            State.DASH_DASH: State.DASH_DASH,
            State.DASH_DASH_DASH: State.DASH_DASH,
        },
        Char.CL_PAR: {
            State.INITIAL: State.CL_PAR,
            State.SLASH: State.SLASH_OTHER,
            State.AMP: State.ERR_AMP,
            State.VERT_SLASH: State.ERR_VERT_SLASH,
            State.LESS: State.LESS_OTHER,
            State.LETTER: State.LETTER_OTHER,
            State.GREATER: State.GREATER_OTHER,
            State.DIGIT: State.DIGIT_OTHER,
            State.DIGIT_DOT: State.ERR_NUMBER,
            State.DIGIT_DOT_DIGIT: State.DIGIT_DOT_DIGIT_OTHER,
            State.SPACE: State.SPACE_OTHER,
            State.DASH: State.DASH_OTHER,
            State.DASH_DASH: State.DASH_DASH,
            State.DASH_DASH_DASH: State.DASH_DASH,
        },
        Char.STAR: {
            State.INITIAL: State.STAR,
            State.SLASH: State.SLASH_OTHER,
            State.AMP: State.ERR_AMP,
            State.VERT_SLASH: State.ERR_VERT_SLASH,
            State.LESS: State.LESS_OTHER,
            State.LETTER: State.LETTER_OTHER,
            State.GREATER: State.GREATER_OTHER,
            State.DIGIT: State.DIGIT_OTHER,
            State.DIGIT_DOT: State.ERR_NUMBER,
            State.DIGIT_DOT_DIGIT: State.DIGIT_DOT_DIGIT_OTHER,
            State.SPACE: State.SPACE_OTHER,
            State.DASH: State.DASH_OTHER,
            State.DASH_DASH: State.DASH_DASH,
            State.DASH_DASH_DASH: State.DASH_DASH,
        },
        Char.PLUS: {
            State.INITIAL: State.PLUS,
            State.SLASH: State.SLASH_OTHER,
            State.AMP: State.ERR_AMP,
            State.VERT_SLASH: State.ERR_VERT_SLASH,
            State.LESS: State.LESS_OTHER,
            State.LETTER: State.LETTER_OTHER,
            State.GREATER: State.GREATER_OTHER,
            State.DIGIT: State.DIGIT_OTHER,
            State.DIGIT_DOT: State.ERR_NUMBER,
            State.DIGIT_DOT_DIGIT: State.DIGIT_DOT_DIGIT_OTHER,
            State.SPACE: State.SPACE_OTHER,
            State.DASH: State.DASH_OTHER,
            State.DASH_DASH: State.DASH_DASH,
            State.DASH_DASH_DASH: State.DASH_DASH,
        },
        Char.DASH: {
            State.INITIAL: State.DASH,
            State.SLASH: State.SLASH_OTHER,
            State.AMP: State.ERR_AMP,
            State.VERT_SLASH: State.ERR_VERT_SLASH,
            State.LESS: State.LESS_DASH,
            State.LETTER: State.LETTER_OTHER,
            State.GREATER: State.GREATER_OTHER,
            State.DIGIT: State.DIGIT_OTHER,
            State.DIGIT_DOT: State.ERR_NUMBER,
            State.DIGIT_DOT_DIGIT: State.DIGIT_DOT_DIGIT_OTHER,
            State.SPACE: State.SPACE_OTHER,
            State.DASH: State.DASH_DASH,
            State.DASH_DASH: State.DASH_DASH_DASH,
            State.DASH_DASH_DASH: State.DASH_DASH_DASH_DASH,
        },
        Char.DOT: {
            State.INITIAL: State.DOT,
            State.SLASH: State.SLASH_OTHER,
            State.AMP: State.ERR_AMP,
            State.VERT_SLASH: State.ERR_VERT_SLASH,
            State.LESS: State.LESS_OTHER,
            State.LETTER: State.LETTER_OTHER,
            State.GREATER: State.GREATER_OTHER,
            State.DIGIT: State.DIGIT_DOT,
            State.DIGIT_DOT: State.ERR_NUMBER,
            State.DIGIT_DOT_DIGIT: State.DIGIT_DOT_DIGIT_OTHER,
            State.SPACE: State.SPACE_OTHER,
            State.DASH: State.DASH_OTHER,
            State.DASH_DASH: State.DASH_DASH,
            State.DASH_DASH_DASH: State.DASH_DASH,
        },
        Char.SLASH: {
            State.INITIAL: State.SLASH,
            State.SLASH: State.SLASH_OTHER,
            State.AMP: State.ERR_AMP,
            State.VERT_SLASH: State.ERR_VERT_SLASH,
            State.LESS: State.LESS_OTHER,
            State.LETTER: State.LETTER_OTHER,
            State.GREATER: State.GREATER_OTHER,
            State.DIGIT: State.DIGIT_OTHER,
            State.DIGIT_DOT: State.ERR_NUMBER,
            State.DIGIT_DOT_DIGIT: State.DIGIT_DOT_DIGIT_OTHER,
            State.SPACE: State.SPACE_OTHER,
            State.DASH: State.DASH_OTHER,
            State.DASH_DASH: State.DASH_DASH,
            State.DASH_DASH_DASH: State.DASH_DASH,
        },
        Char.COLON: {
            State.INITIAL: State.COLON,
            State.SLASH: State.SLASH_OTHER,
            State.AMP: State.ERR_AMP,
            State.VERT_SLASH: State.ERR_VERT_SLASH,
            State.LESS: State.LESS_OTHER,
            State.LETTER: State.LETTER_OTHER,
            State.GREATER: State.GREATER_OTHER,
            State.DIGIT: State.DIGIT_OTHER,
            State.DIGIT_DOT: State.ERR_NUMBER,
            State.DIGIT_DOT_DIGIT: State.DIGIT_DOT_DIGIT_OTHER,
            State.SPACE: State.SPACE_OTHER,
            State.DASH: State.DASH_OTHER,
            State.DASH_DASH: State.DASH_DASH,
            State.DASH_DASH_DASH: State.DASH_DASH,
        },
        Char.SEMICOLON: {
            State.INITIAL: State.SEMICOLON,
            State.SLASH: State.SLASH_OTHER,
            State.AMP: State.ERR_AMP,
            State.VERT_SLASH: State.ERR_VERT_SLASH,
            State.LESS: State.LESS_OTHER,
            State.LETTER: State.LETTER_OTHER,
            State.GREATER: State.GREATER_OTHER,
            State.DIGIT: State.DIGIT_OTHER,
            State.DIGIT_DOT: State.ERR_NUMBER,
            State.DIGIT_DOT_DIGIT: State.DIGIT_DOT_DIGIT_OTHER,
            State.SPACE: State.SPACE_OTHER,
            State.DASH: State.DASH_OTHER,
            State.DASH_DASH: State.DASH_DASH,
            State.DASH_DASH_DASH: State.DASH_DASH,
        },
        Char.LESS: {
            State.INITIAL: State.LESS,
            State.SLASH: State.SLASH_OTHER,
            State.AMP: State.ERR_AMP,
            State.VERT_SLASH: State.ERR_VERT_SLASH,
            State.LESS: State.LESS_OTHER,
            State.LETTER: State.LETTER_OTHER,
            State.GREATER: State.GREATER_OTHER,
            State.DIGIT: State.DIGIT_OTHER,
            State.DIGIT_DOT: State.ERR_NUMBER,
            State.DIGIT_DOT_DIGIT: State.DIGIT_DOT_DIGIT_OTHER,
            State.SPACE: State.SPACE_OTHER,
            State.DASH: State.DASH_OTHER,
            State.DASH_DASH: State.DASH_DASH,
            State.DASH_DASH_DASH: State.DASH_DASH,
        },
        Char.EQUALS: {
            State.INITIAL: State.EQUALS,
            State.SLASH: State.SLASH_EQUALS,
            State.AMP: State.ERR_AMP,
            State.VERT_SLASH: State.ERR_VERT_SLASH,
            State.LESS: State.LESS_EQUALS,
            State.LETTER: State.LETTER_OTHER,
            State.GREATER: State.GREATER_EQUALS,
            State.DIGIT: State.DIGIT_OTHER,
            State.DIGIT_DOT: State.ERR_NUMBER,
            State.DIGIT_DOT_DIGIT: State.DIGIT_DOT_DIGIT_OTHER,
            State.SPACE: State.SPACE_OTHER,
            State.DASH: State.DASH_OTHER,
            State.DASH_DASH: State.DASH_DASH,
            State.DASH_DASH_DASH: State.DASH_DASH,
        },
        Char.GREATER: {
            State.INITIAL: State.GREATER,
            State.SLASH: State.SLASH_OTHER,
            State.AMP: State.ERR_AMP,
            State.VERT_SLASH: State.ERR_VERT_SLASH,
            State.LESS: State.LESS_OTHER,
            State.LETTER: State.LETTER_OTHER,
            State.GREATER: State.GREATER_OTHER,
            State.DIGIT: State.DIGIT_OTHER,
            State.DIGIT_DOT: State.ERR_NUMBER,
            State.DIGIT_DOT_DIGIT: State.DIGIT_DOT_DIGIT_OTHER,
            State.SPACE: State.SPACE_OTHER,
            State.DASH: State.DASH_OTHER,
            State.DASH_DASH: State.DASH_DASH,
            State.DASH_DASH_DASH: State.DASH_DASH,
        },
        Char.DIGIT: {
            State.INITIAL: State.DIGIT,
            State.SLASH: State.SLASH_OTHER,
            State.AMP: State.ERR_AMP,
            State.VERT_SLASH: State.ERR_VERT_SLASH,
            State.LESS: State.LESS_OTHER,
            State.LETTER: State.LETTER,
            State.GREATER: State.GREATER_OTHER,
            State.DIGIT: State.DIGIT,
            State.DIGIT_DOT: State.DIGIT_DOT_DIGIT,
            State.DIGIT_DOT_DIGIT: State.DIGIT_DOT_DIGIT,
            State.SPACE: State.SPACE_OTHER,
            State.DASH: State.DASH_OTHER,
            State.DASH_DASH: State.DASH_DASH,
            State.DASH_DASH_DASH: State.DASH_DASH,
        },
        Char.LETTER: {
            State.INITIAL: State.LETTER,
            State.SLASH: State.SLASH_OTHER,
            State.AMP: State.ERR_AMP,
            State.VERT_SLASH: State.ERR_VERT_SLASH,
            State.LESS: State.LESS_OTHER,
            State.LETTER: State.LETTER,
            State.GREATER: State.GREATER_OTHER,
            State.DIGIT: State.DIGIT_OTHER,
            State.DIGIT_DOT: State.ERR_NUMBER,
            State.DIGIT_DOT_DIGIT: State.DIGIT_DOT_DIGIT_OTHER,
            State.SPACE: State.SPACE_OTHER,
            State.DASH: State.DASH_OTHER,
            State.DASH_DASH: State.DASH_DASH,
            State.DASH_DASH_DASH: State.DASH_DASH,
        },
        Char.OP_CUR_BR: {
            State.INITIAL: State.OP_CUR_BR,
            State.SLASH: State.SLASH_OTHER,
            State.AMP: State.ERR_AMP,
            State.VERT_SLASH: State.ERR_VERT_SLASH,
            State.LESS: State.LESS_OTHER,
            State.LETTER: State.LETTER_OTHER,
            State.GREATER: State.GREATER_OTHER,
            State.DIGIT: State.DIGIT_OTHER,
            State.DIGIT_DOT: State.ERR_NUMBER,
            State.DIGIT_DOT_DIGIT: State.DIGIT_DOT_DIGIT_OTHER,
            State.SPACE: State.SPACE_OTHER,
            State.DASH: State.DASH_OTHER,
            State.DASH_DASH: State.DASH_DASH,
            State.DASH_DASH_DASH: State.DASH_DASH,
        },
        Char.VERT_SLASH: {
            State.INITIAL: State.VERT_SLASH,
            State.SLASH: State.SLASH_OTHER,
            State.AMP: State.ERR_AMP,
            State.VERT_SLASH: State.VERT_SLASH_VERT_SLASH,
            State.LESS: State.LESS_OTHER,
            State.LETTER: State.LETTER_OTHER,
            State.GREATER: State.GREATER_OTHER,
            State.DIGIT: State.DIGIT_OTHER,
            State.DIGIT_DOT: State.ERR_NUMBER,
            State.DIGIT_DOT_DIGIT: State.DIGIT_DOT_DIGIT_OTHER,
            State.SPACE: State.SPACE_OTHER,
            State.DASH: State.DASH_OTHER,
            State.DASH_DASH: State.DASH_DASH,
            State.DASH_DASH_DASH: State.DASH_DASH,
        },
        Char.CL_CUR_BR: {
            State.INITIAL: State.CL_CUR_BR,
            State.SLASH: State.SLASH_OTHER,
            State.AMP: State.ERR_AMP,
            State.VERT_SLASH: State.ERR_VERT_SLASH,
            State.LESS: State.LESS_OTHER,
            State.LETTER: State.LETTER_OTHER,
            State.GREATER: State.GREATER_OTHER,
            State.DIGIT: State.DIGIT_OTHER,
            State.DIGIT_DOT: State.ERR_NUMBER,
            State.DIGIT_DOT_DIGIT: State.DIGIT_DOT_DIGIT_OTHER,
            State.SPACE: State.SPACE_OTHER,
            State.DASH: State.DASH_OTHER,
            State.DASH_DASH: State.DASH_DASH,
            State.DASH_DASH_DASH: State.DASH_DASH,
        },
        Char.EOF: {
            State.INITIAL: State.EOF,
            State.SLASH: State.SLASH_OTHER,
            State.AMP: State.ERR_AMP,
            State.VERT_SLASH: State.ERR_VERT_SLASH,
            State.LESS: State.LESS_OTHER,
            State.LETTER: State.LETTER_OTHER,
            State.GREATER: State.GREATER_OTHER,
            State.DIGIT: State.DIGIT_OTHER,
            State.DIGIT_DOT: State.ERR_NUMBER,
            State.DIGIT_DOT_DIGIT: State.DIGIT_DOT_DIGIT_OTHER,
            State.SPACE: State.SPACE_OTHER,
            State.DASH: State.DASH_OTHER,
            State.DASH_DASH: State.ERR_COMMENT_NOT_CLOSED,
            State.DASH_DASH_DASH: State.ERR_COMMENT_NOT_CLOSED,
        },
        Char.OTHER: {
            State.INITIAL: State.ERR_START,
            State.SLASH: State.SLASH_OTHER,
            State.AMP: State.ERR_AMP,
            State.VERT_SLASH: State.ERR_VERT_SLASH,
            State.LESS: State.LESS_OTHER,
            State.LETTER: State.LETTER_OTHER,
            State.GREATER: State.GREATER_OTHER,
            State.DIGIT: State.DIGIT_OTHER,
            State.DIGIT_DOT: State.ERR_NUMBER,
            State.DIGIT_DOT_DIGIT: State.DIGIT_DOT_DIGIT_OTHER,
            State.SPACE: State.SPACE_OTHER,
            State.DASH: State.DASH_OTHER,
            State.DASH_DASH: State.DASH_DASH,
            State.DASH_DASH_DASH: State.DASH_DASH,
        },
    }
    ERROR_MESSAGES = {
        State.ERR_START: 'Встречен неожиданный символ: "{}"',
        State.ERR_AMP: 'Встречено: "{}", ожидалось: "&"',
        State.ERR_VERT_SLASH: 'Встречено: "{}", ожидалось: "|"',
        State.ERR_NUMBER: 'Встречено: "{}", ожидалась цифра',
        State.ERR_COMMENT_NOT_CLOSED: 'Встречен конец файла, ожидалось: "--"',
    }
    SHIFT_BACK_TABLE: dict[State, int] = defaultdict(int, {
        State.SLASH_OTHER: 1,
        State.LESS_OTHER: 1,
        State.LETTER_OTHER: 1,
        State.GREATER_OTHER: 1,
        State.DIGIT_OTHER: 1,
        State.DIGIT_DOT_DIGIT_OTHER: 1,
        State.SPACE_OTHER: 1,
        State.DASH_OTHER: 1,
    })
    STATE_TO_TOKEN_PARAMS: dict[State, tuple] = {
        State.SEMICOLON: (Code.LC_SEMI,),
        State.COLON: (Code.LC_COLON,),
        State.DOT: (Code.LC_DOT,),
        State.OP_PAR: (Code.LC_OP_PAR,),
        State.CL_PAR: (Code.LC_CL_PAR,),
        State.OP_CUR_BR: (Code.LC_OP_CUR_BR,),
        State.CL_CUR_BR: (Code.LC_CL_CUR_BR,),
        State.EXCL: (Code.LC_NOT,),
        State.EQUALS: (Code.LC_REL, Attribute.OP_EQ),
        State.PLUS: (Code.LC_ADD, Attribute.OP_ADD),
        State.STAR: (Code.LC_MULT, Attribute.OP_MULT),
        State.SLASH_OTHER: (Code.LC_MULT, Attribute.OP_DIV),
        State.SLASH_EQUALS: (Code.LC_REL, Attribute.OP_NE),
        State.AMP_AMP: (Code.LC_AND,),
        State.VERT_SLASH_VERT_SLASH: (Code.LC_OR,),
        State.LESS_OTHER: (Code.LC_REL, Attribute.OP_LT),
        State.LESS_EQUALS: (Code.LC_REL, Attribute.OP_LE),
        State.LESS_DASH: (Code.LC_ASS,),
        State.LETTER_OTHER: (Code.LC_ID,),
        State.GREATER_OTHER: (Code.LC_REL, Attribute.OP_GT),
        State.GREATER_EQUALS: (Code.LC_REL, Attribute.OP_GE),
        State.DIGIT_OTHER: (Code.LC_NUM,),
        State.DIGIT_DOT_DIGIT_OTHER: (Code.LC_NUM,),
        State.SPACE_OTHER: (Code.LC_SP,),
        State.DASH_OTHER: (Code.LC_ADD, Attribute.OP_SUB,),
        State.DASH_DASH_DASH_DASH: (Code.LC_COM,),
        State.EOF: (Code.LC_EOF,),
        State.ERR_START: (Code.LC_ERR,),
        State.ERR_AMP: (Code.LC_ERR,),
        State.ERR_VERT_SLASH: (Code.LC_ERR,),
        State.ERR_NUMBER: (Code.LC_ERR,),
        State.ERR_COMMENT_NOT_CLOSED: (Code.LC_ERR,),
    }

    def __init__(self, code: str):
        self.code: str = code
        self.state: State = State.INITIAL
        self.pos: int = 0
        self.id_table: list[Identifier] = [
            Identifier(TypeCode.INTEGER.value, Category.TYPE_NAME, TypeCode.INTEGER),
            Identifier(TypeCode.FLOAT.value, Category.TYPE_NAME, TypeCode.FLOAT),
            Identifier(TypeCode.BOOLEAN.value, Category.TYPE_NAME, TypeCode.BOOLEAN),
        ]

        if not self.code.endswith(Char.EOF.value):
            self.code += Char.EOF.value

    def form_token(self, start: int) -> Token:
        token: Token = Token(*self.STATE_TO_TOKEN_PARAMS[self.state])
        token.start = start
        token.end = self.pos

        if token.code == Code.LC_ERR:
            token.lex = self.ERROR_MESSAGES[self.state].format(self.code[token.end - 1:token.end])
            return token

        if token.code not in (Code.LC_NUM, Code.LC_ID):
            return token

        token.lex = self.code[token.start:token.end]

        if token.lex in self.KEYWORDS:
            token.code = self.KEYWORDS[token.lex]
            token.lex = None
            return token

        try:
            i: int = [symbol.lex for symbol in self.id_table].index(token.lex)
        except ValueError:
            i: int = -1

        if i != -1:
            token.attr = i
            return token

        if token.code == Code.LC_NUM and self.state == State.DIGIT_OTHER:
            symbol = Identifier(token.lex, Category.CONST, TypeCode.INTEGER)
        elif token.code == Code.LC_NUM and self.state == State.DIGIT_DOT_DIGIT_OTHER:
            symbol = Identifier(token.lex, Category.CONST, TypeCode.FLOAT)
        else:
            symbol = Identifier(token.lex)

        token.attr = len(self.id_table)
        self.id_table.append(symbol)

        return token

    def __iter__(self) -> Iterable[Token]:
        while self.pos < len(self.code):
            yield self.get_next_token()

    def get_tokens(self) -> list[Token]:
        return [token for token in self]

    def get_next_token(self) -> Token:
        start = self.pos

        while self.pos < len(self.code):
            char: Char = Char.get_char_class(self.code[self.pos])
            self.state: State = self.STATE_TABLE[char][self.state]
            self.pos += 1

            if self.state.is_final():
                self.pos -= self.SHIFT_BACK_TABLE[self.state]
                token: Token = self.form_token(start)
                self.state = State.INITIAL

                if token.code == Code.LC_SP:
                    start = self.pos
                    continue

                return token

        return self.form_token(start)


if __name__ == '__main__':
    scanner = Scanner('procedure15 var15 while15 true false integer float boolean')
    print(scanner.get_tokens())
    print(list(Scanner.KEYWORDS.keys()))
