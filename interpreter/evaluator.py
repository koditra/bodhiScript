from interpreter.parser import (
    Program,
    VariableDeclaration,
    PrintStatement,
    NumberLiteral,
    StringLiteral,
    Variable,
    BinaryExpression,
)

class Evaluator:
    def __init__(self):
        self.variables = {}

    def evaluate(self, node):
        if isinstance(node, Program):
            return self.evaluate_program(node)

        if isinstance(node, VariableDeclaration):
            return self.evaluate_variable_declaration(node)

        if isinstance(node, PrintStatement):
            return self.evaluate_print(node)

        if isinstance(node, NumberLiteral):
            return node.value

        if isinstance(node, StringLiteral):
            return node.value

        if isinstance(node, Variable):
            return self.evaluate_variable(node)

        if isinstance(node, BinaryExpression):
            return self.evaluate_binary(node)

        raise RuntimeError(
            f"Unknown node: {type(node).__name__}"
        )

    def evaluate_program(self, program):
        result = None

        for statement in program.statements:
            result = self.evaluate(statement)

        return result

    def evaluate_variable_declaration(self, node):
        value = self.evaluate(node.value)
        self.variables[node.name] = value
        return value

    def evaluate_print(self, node):
        value = self.evaluate(node.value)
        print(value)
        return value

    def evaluate_variable(self, node):
        if node.name not in self.variables:
            raise RuntimeError(
                f"Variable '{node.name}' is not defined."
            )

        return self.variables[node.name]

    def evaluate_binary(self, node):
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)

        if node.operator == "+":
            return left + right

        if node.operator == "-":
            return left - right

        if node.operator == "*":
            return left * right

        if node.operator == "/":
            return left / right

        if node.operator == "%":
            return left % right

        raise RuntimeError(
            f"Unknown operator: {node.operator}"
        )

def evaluate(source):
    from interpreter.parser import parse

    program = parse(source)
    evaluator = Evaluator()

    return evaluator.evaluate(program)