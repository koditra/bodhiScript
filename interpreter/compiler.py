from interpreter.parser import (
    Program,
    VariableDeclaration,
    PrintStatement,
    NumberLiteral,
    StringLiteral,
    Variable,
    BinaryExpression,
)


class Compiler:
    def __init__(self):
        self.instructions = []

    def compile(self, node):
        if isinstance(node, Program):
            for statement in node.statements:
                self.compile(statement)

            self.emit("HALT")
            return self.instructions

        if isinstance(node, VariableDeclaration):
            self.compile(node.value)
            self.emit("STORE", node.name)
            return

        if isinstance(node, PrintStatement):
            self.compile(node.value)
            self.emit("PRINT")
            return

        if isinstance(node, NumberLiteral):
            self.emit("PUSH", node.value)
            return
from interpreter.parser import (
    Program,
    VariableDeclaration,
    PrintStatement,
    NumberLiteral,
    StringLiteral,
    Variable,
    BinaryExpression,
)


class Compiler:
    def __init__(self):
        self.instructions = []

    def compile(self, node):
        if isinstance(node, Program):
            for statement in node.statements:
                self.compile(statement)

            self.emit("HALT")
            return self.instructions

        if isinstance(node, VariableDeclaration):
            self.compile(node.value)
            self.emit("STORE", node.name)
            return

        if isinstance(node, PrintStatement):
            self.compile(node.value)
            self.emit("PRINT")
            return

        if isinstance(node, NumberLiteral):
            self.emit("PUSH", node.value)
            return

        if isinstance(node, StringLiteral):
            self.emit("PUSH", node.value)
            return

        if isinstance(node, Variable):
            self.emit("LOAD", node.name)
            return

        if isinstance(node, BinaryExpression):
            self.compile(node.left)
            self.compile(node.right)

            operators = {
                "+": "ADD",
                "-": "SUBTRACT",
                "*": "MULTIPLY",
                "/": "DIVIDE",
                "%": "MODULO",
            }

            self.emit(operators[node.operator])
            return

        raise RuntimeError(
            f"Unknown node: {type(node).__name__}"
        )

    def emit(self, instruction, operand=None):
        if operand is None:
            self.instructions.append((instruction,))
        else:
            self.instructions.append((instruction, operand))


def compile_source(source):
    from interpreter.parser import parse

    program = parse(source)
    compiler = Compiler()

    return compiler.compile(program)