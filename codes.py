from enum import Enum


class Code(Enum):
    PROG = 'prog'  # procedure15
    USING = 'using'  # using15
    CLASS = 'class'  # class15
    VAR = 'var'  # var15
    WHILE = 'while'  # while15
    TRUE = 'true'
    FALSE = 'false'
    FULLNAME = 'FIO'
    SEMI = ';'
    COLON = ':'
    DOT = '.'
    OP_PAR = '('
    CL_PAR = ')'
    OP_CUR_BR = '{'
    CL_CUR_BR = '}'
    ASS = 'ass'  # <-
    ADD = '+'  # + | -
    MULT = '*'  # * | /
    NOT = '!'
    AND = '&&'
    OR = '||'
    REL = 'rel'  # < | <= | = | >= | > | /=
    ID = 'id'  # identifier
    NUM = 'num'  # number
    SP = 'sp'  # space | tab | new line
    COM = 'com'  # commentary
    EOF = 'eof'  # end of file
    ERR = 'err'  # error
    GOTO = 'goto'
    IF = 'if'
    IF_FALSE = 'ifFalse'
