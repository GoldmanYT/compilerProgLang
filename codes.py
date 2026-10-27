from enum import Enum


class Code(Enum):
    LC_PROG = 'prog'  # procedure15
    LC_USING = 'using'  # using15
    LC_CLASS = 'class'  # class15
    LC_VAR = 'var'  # var15
    LC_WHILE = 'while'  # while15
    LC_TRUE = 'true'
    LC_FALSE = 'false'
    LC_FULLNAME = 'FIO'
    LC_SEMI = ';'
    LC_COLON = ':'
    LC_DOT = '.'
    LC_OP_PAR = '('
    LC_CL_PAR = ')'
    LC_OP_CUR_BR = '{'
    LC_CL_CUR_BR = '}'
    LC_ASS = 'ass'  # <-
    LC_ADD = '+'  # + | -
    LC_MULT = '*'  # * | /
    LC_NOT = '!'
    LC_AND = '&&'
    LC_OR = '||'
    LC_REL = 'rel'  # < | <= | = | >= | > | /=
    LC_ID = 'id'  # identifier
    LC_NUM = 'num'  # number
    LC_SP = 'sp'  # space | tab | new line
    LC_COM = 'com'  # commentary
    LC_EOF = 'eof'  # end of file
    LC_ERR = 'err'  # error
