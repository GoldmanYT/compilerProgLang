from typing import Iterable
from xml.etree.ElementTree import fromstring as parse_xml
from tokens import Token
from lrtableelement import LRTableElement
from lrtableelemtype import LRTableElemType
from identifier import Identifier


class Sct:
    """
    Syntactically controlled translation
    """

    GRAMMAR_PATH = 'content/LR_Table.xml'

    def __init__(
            self,
            tokens: Iterable[Token],
            id_table: list[Identifier],
    ):
        self.tokens: Iterable = tokens
        self.id_table = id_table
        self.grammar = {}
        self.actions = {}
        self.load_grammar()

    @staticmethod
    def set_error_message(token, expected):
        token.lex = '{pos}: Встречено "{lex}", ожидалось: {expected}'
        token.kwargs = {'expected': expected}

    def scan(self) -> None | Token:
        state: int = 1
        stack: list[int] = [state]
        token: Token = next(self.tokens)
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
            )

            elem_param: int | None = lr_table_elem.elem_param

            if lr_table_elem.elem_type == LRTableElemType.SHIFT:
                state = elem_param
                stack.append(state)
                if left is None:
                    token: Token = next(self.tokens)
                    next_lexeme = token.code.value
                else:
                    left = None

            elif lr_table_elem.elem_type == LRTableElemType.FOLD:
                pop_count: int = elem_param
                left = lr_table_elem.left

                if len(stack) <= pop_count:
                    self.set_error_message(token, expected)
                    return token

                stack = stack[:-pop_count]
                state = stack[-1]

                action = self.actions.get(lr_table_elem.action)

                if action is not None:
                    action()

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
        xml_content = xml_content.replace('"&&"', '"&amp;&amp;"')
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
                    elem_param: int = int(elem.get('ElPar'))
                else:
                    elem_param = None

                if elem_type == LRTableElemType.FOLD:
                    left: str = elem.get('Left')
                else:
                    left = None

                action: str = elem.get('Act')

                self.grammar[state][lexeme] = LRTableElement(elem_type, elem_param, left, action)


if __name__ == '__main__':
    Sct([], [])
