from identifier import Identifier
from operation import Operation
from codes import Code
from attribute import Attribute


class ThreeAddressCommand:
    def __init__(
            self,
            id_table: list[Identifier],
            operation: Operation,
            result: int,
            arg1: int = -1,
            arg2: int = -1,
    ):
        self.operation = operation

        if operation.code in (Code.GOTO, Code.IF, Code.IF_FALSE):
            self.result = result
        else:
            self.result = id_table[result].lex

        if arg1 != -1:
            self.arg1 = id_table[arg1].lex
        else:
            self.arg1 = None

        if arg2 != -1:
            self.arg2 = id_table[arg2].lex
        else:
            self.arg2 = None

    def __str__(self):
        return str(self.operation).format(result=self.result, arg1=self.arg1, arg2=self.arg2)


if __name__ == '__main__':
    id_table_: list[Identifier] = [Identifier('x'), Identifier('y'), Identifier('z'), ]
    print(ThreeAddressCommand(id_table_, Operation(Code.ASS), 0, 1))
    print(ThreeAddressCommand(id_table_, Operation(Code.ADD, Attribute.OP_ADD), 0, 1, 2))
    print(ThreeAddressCommand(id_table_, Operation(Code.ADD, Attribute.OP_SUB), 0, 1, 2))
    print(ThreeAddressCommand(id_table_, Operation(Code.GOTO), 50))
    print(ThreeAddressCommand(id_table_, Operation(Code.IF, Attribute.OP_LE), 50, 0, 1))
    print(ThreeAddressCommand(id_table_, Operation(Code.IF_FALSE, Attribute.OP_NE), 100, 0, 1))
