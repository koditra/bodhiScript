from dataclasses import dataclass
from interpreter.lexer import tokenize, Token

@dataclass
class Program:
    statements: list

@dataclass
class VariableDeclaration:
    name: str
    value: object

@dataclass
class PrintStatement:
    value: object

@dataclass
class NumberLiteral:
    value: int | float

@dataclass
class StringLiteral:
    value: str

@dataclass
class Variable:
    name: str

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        statements = []

        while not self.check("EOF"):
            statements.append(self.statement())
        return Program(statements)

    def statement(self):
        if self.match("MAAN", "RAKHO"):
            return self.variable_declaration()

        if self.match("LIKHA"):
            return self.print_statement()

        token = self.peek()
        raise SyntaxError(
            f"Unexpected token {token.lexeme!r} "
            f"at line {token.line}, column {token.column}"
        )

    def variable_declaration(self):
        name = self.consume(
            "IDENTIFIER", "Expected a variable name."
        )
        self.consume("EQUAL", "Expected '=' after the variable name.")
        value = self.expression()
        self.consume("SEMICOLON", "Expected ';' after the declaration.")

        return VariableDeclaration(name.lexeme, value)

    def print_statement(self):
        self.consume("LEFT_PAREN", "Expected '(' after likha.")
        value = self.expression()
        self.consume("RIGHT_PAREN", "Expected ')' after the value.")
        self.consume("SEMICOLON", "Expected ';' after likha.")

        return PrintStatement(value)

    def expression(self):
        token = self.peek()

        if self.match("NUMBER"):
            value = token.lexeme
            if "." in value:
                return NumberLiteral(float(value))
            return NumberLiteral(int(value))

        if self.match("STRING"):
            return StringLiteral(token.lexeme[1:-1])

        if self.match("IDENTIFIER"):
            return Variable(token.lexeme)

        raise SyntaxError(
            f"Expected a value at line {token.line}, "
            f"column {token.column}"
        )

    def match(self, *types):
        if self.peek().type in types:
            self.advance()
            return True
        return False

    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()

        token = self.peek()
        raise SyntaxError(
            f"{message} Got {token.lexeme!r} at "
            f"line {token.line}, column {token.column}"
        )

    def check(self, token_type):
        return self.peek().type == token_type

    def advance(self):
        if not self.check("EOF"):
            self.current += 1
        return self.previous()

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]


def parse(source):
    tokens = tokenize(source)
    parser = Parser(tokens)
    return parser.parse()