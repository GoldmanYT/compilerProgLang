from typing import Any, Callable, Iterator
from xml.etree.ElementTree import fromstring as parse_xml

from category import Category
from tokens import Token
from lrtableelement import LRTableElement
from lrtableelemtype import LRTableElemType
from identifier import Identifier
from codes import Code
from scanner import find_in_id_table


class Sct:
    """
    Syntactically controlled translation
    """

    GRAMMAR_PATH = 'content/LR_Table.xml'

    def __init__(
            self,
            tokens: Iterator[Token],
            id_table: list[Identifier],
    ):
        self.tokens: Iterator = tokens
        self.id_table = id_table
        self.grammar = {}
        self.actions: dict[str, Callable[[list[Any], Token], None | Token]] = {
            'CheckRedeclaration': self.check_redeclaration,
            'DeclareVariable': self.declare_variable,
            'DeclareType': self.declare_type,
        }
        self.load_grammar()

    @staticmethod
    def set_error_message(token, expected):
        token.lex = '{pos}: Встречено "{lex}", ожидалось: {expected}'
        token.kwargs = {'expected': expected}

    def check_redeclaration(
            self,
            stack: list[Any],
            token: Token,
    ) -> None | Token:

        i: int = find_in_id_table(self.id_table, token.lex)

        if i != -1 and self.id_table[i].category != Category.NO_CAT:
            token.lex = '{pos}: ' f'Переобъявление идентификатора: {token.lex}'
            return token

        stack.append(i)

    def declare_variable(
            self,
            stack: list[Any],
            token: Token,
    ) -> None | Token:

        i: int = find_in_id_table(self.id_table, token.lex)

        if i != -1:
            var_i: int = stack.pop()
            self.id_table[var_i].category = Category.VAR_NAME
            if self.id_table[i].category != Category.TYPE_NAME:
                token.lex = '{pos}: ' f'Идентификатор не является именем типа: {token.lex}'
                return token
            # FIXME: для структур
            self.id_table[var_i].type_code = self.id_table[i].type_code

    def declare_type(
            self,
            stack: list[Any],
            token: Token,
    ) -> None | Token:

        i: int = find_in_id_table(self.id_table, token.lex)

        if i != -1:
            var_i: int = stack.pop()
            self.id_table[var_i].category = Category.TYPE_NAME
            # FIXME: для структур
            self.id_table[var_i].type_code = self.id_table[i].type_code

        return

    def scan(self) -> None | Token:
        state: int = 1
        state_stack: list[int] = [state]
        attr_stack: list[Any] = []
        token: Token = next(self.tokens)
        prev_token: Token = token
        next_lexeme: str = token.code.value
        left: str | None = None

        while state != 0:
            if left is None:
                lr_table_elem: LRTableElement = self.grammar[state][next_lexeme]
            else:
                lr_table_elem: LRTableElement = self.grammar[state][left]

            expected = ' или '.join(
                f'"{lexeme}"' for lexeme in self.grammar[state]
                if self.grammar[state][lexeme].elem_type != LRTableElemType.ERROR
                and lexeme in (code.value for code in Code.__members__.values())
            )

            elem_param: int | None = lr_table_elem.elem_param

            if lr_table_elem.elem_type == LRTableElemType.SHIFT:
                state = elem_param
                state_stack.append(state)
                if left is None:
                    prev_token = token
                    token: Token = next(self.tokens)
                    next_lexeme = token.code.value
                else:
                    left = None

            elif lr_table_elem.elem_type == LRTableElemType.FOLD:
                pop_count: int = elem_param
                left = lr_table_elem.left

                if len(state_stack) <= pop_count:
                    self.set_error_message(token, expected)
                    return token

                state_stack = state_stack[:-pop_count if pop_count > 0 else None]
                state = state_stack[-1]

                action = self.actions.get(lr_table_elem.action)

                if action is not None:
                    error_token: Token | None = action(attr_stack, prev_token)
                    if error_token is not None:
                        return error_token

            elif lr_table_elem.elem_type == LRTableElemType.STOP:
                state = 0

            elif lr_table_elem.elem_type == LRTableElemType.ERROR:
                self.set_error_message(token, expected)
                return token

    def load_grammar(self):
        xml_content: str = ''
        try:
            with open(self.GRAMMAR_PATH, 'r', encoding='utf-8') as file:
                xml_content = file.read()
        except FileNotFoundError:
            pass

        self.grammar = {}
        root = parse_xml(xml_content)

        col_num_to_lexeme = {}

        for column in root.iter('Column'):
            col_num = column.get('ColNum')
            lexeme = column.get('Lexeme')
            col_num_to_lexeme[col_num] = lexeme

        for row in root.findall('Row'):
            state: int = int(row.get('NSost'))
            self.grammar[state] = {}
            for elem in row:
                col_num = elem.get('ColNum')
                lexeme = col_num_to_lexeme[col_num]

                elem_type = LRTableElemType(elem.get('ElType'))

                if elem_type in (LRTableElemType.SHIFT, LRTableElemType.FOLD):
                    elem_param: int | None = int(elem.get('ElPar'))
                else:
                    elem_param = None

                if elem_type == LRTableElemType.FOLD:
                    left: str | None = elem.get('Left')
                else:
                    left = None

                action: str = elem.get('Act')

                self.grammar[state][lexeme] = LRTableElement(elem_type, elem_param, left, action)
