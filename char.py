from enum import Enum


class Char(Enum):
    TAB = '\t'
    LF = '\n'
    SPACE = ' '
    EXCL = '!'
    AMP = '&'
    OP_PAR = '('
    CL_PAR = ')'
    STAR = '*'
    PLUS = '+'
    DASH = '-'
    DOT = '.'
    SLASH = '/'
    COLON = ':'
    SEMICOLON = ';'
    LESS = '<'
    EQUALS = '='
    GREATER = '>'
    DIGIT = '0'
    LETTER = 'A'
    OP_CUR_BR = '{'
    VERT_SLASH = '|'
    CL_CUR_BR = '}'
    EOF = '\3'
    OTHER = ''

    @staticmethod
    def get_char_class(char: str):
        if len(char) != 1:
            raise ValueError('Char must me length of 1')

        if char in (enum.value for enum in Char):
            return Char(char)

        if char.isdigit():
            return Char.DIGIT

        if char.isalpha():
            return Char.LETTER

        return Char.OTHER
