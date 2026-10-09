from dataclasses import dataclass
from interpreter.lexer import tokenize

# these dataclasses are the parsers output shape
#each one represents one parsed piece of bodhiscript code

@dataclass
class Program:
    statements: list

@dataclass
class Block:
    statements: list

@dataclass
class VariableDeclaration:
    name: str
    value: object

@dataclass
class PrintStatement:
    value: object

@dataclass
class ExpressionStatement:
    expression: object

@dataclass
class IfStatement:
    condition: object
    then_branch: object
    else_branch: object | None

@dataclass
class WhileStatement:
    condition: object
    body: object

@dataclass
class FunctionDeclaration:
    name: str
    parameters: list
    body: object

@dataclass
class ReturnStatement:
    value: object | None

@dataclass
class NumberLiteral:
    value: int | float

@dataclass
class StringLiteral:
    value: str

@dataclass
class BooleanLiteral:
    value: bool

@dataclass
class NoneLiteral:
    pass

@dataclass
class Variable:
    name: str

@dataclass
class BinaryExpression:
    left: object
    operator: str
    right: object

@dataclass
class UnaryExpression:
    operator: str
    operand: object

@dataclass
class CallExpression:
    name: str
    arguments: list

class Parser:
    # the parser walks the token stream one by one and turns it into
    # a tree of statements and expressions
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        # a program is just a list of top-level statements.
        statements = []

        while not self.check("EOF"):
            statements.append(self.statement())

        return Program(statements)

    def statement(self):
        # top level statements are the main grammar branches
        # they decide what kind of command we are parsing

        if self.match("MAAN", "RAKHO"):
            return self.variable_declaration()

        if self.match("LIKHA"):
            return self.print_statement()

        if self.match("YADI", "AGAR"):
            return self.if_statement()

        if self.match("JABTAK", "YAVYAT"):
            return self.while_statement()

        if self.match("KARYA"):
            return self.function_declaration()

        if self.match("WAPAS"):
            return self.return_statement()

        return self.expression_statement()

    def variable_declaration(self):
        # example: maan age = 14;
        # grammar: identifier '=' expression ';'

        name = self.consume(
            "IDENTIFIER",
            "Expected a variable name."
        )

        self.consume(
            "EQUAL",
            "Expected '=' after the variable name."
        )

        value = self.expression()

        self.consume(
            "SEMICOLON",
            "Expected ';' after the declaration."
        )

        return VariableDeclaration(name.lexeme, value)

    def print_statement(self):
        # example: likha("hi");
        self.consume(
            "LEFT_PAREN",
            "Expected '(' after likha."
        )

        value = self.expression()

        self.consume(
            "RIGHT_PAREN",
            "Expected ')' after the value."
        )

        self.consume(
            "SEMICOLON",
            "Expected ';' after likha."
        )

        return PrintStatement(value)

    def if_statement(self):
        # example: yadi age > 10 { ... } anyatha { ... }
        condition = self.expression()

        self.consume(
            "LEFT_BRACE",
            "Expected '{' after condition."
        )

        then_branch = self.block()

        else_branch = None

        if self.match("ANYATHA", "WARNA"):
            self.consume(
                "LEFT_BRACE",
                "Expected '{' after anyatha."
            )

            else_branch = self.block()

        return IfStatement(
            condition,
            then_branch,
            else_branch
        )

    def while_statement(self):
        # example: jabtak x < 10 { ... }
        condition = self.expression()

        self.consume(
            "LEFT_BRACE",
            "Expected '{' after while condition."
        )

        body = self.block()

        return WhileStatement(condition, body)

    def function_declaration(self):
        # example: karya greet(a, b) { ... }
        name = self.consume(
            "IDENTIFIER",
            "Expected a function name."
        )

        self.consume(
            "LEFT_PAREN",
            "Expected '(' after function name."
        )

        parameters = []

        if not self.check("RIGHT_PAREN"):
            while True:
                parameter = self.consume(
                    "IDENTIFIER",
                    "Expected parameter name."
                )

                parameters.append(parameter.lexeme)

                if not self.match("COMMA"):
                    break

        self.consume(
            "RIGHT_PAREN",
            "Expected ')' after parameters."
        )

        self.consume(
            "LEFT_BRACE",
            "Expected '{' before function body."
        )

        body = self.block()

        return FunctionDeclaration(
            name.lexeme,
            parameters,
            body
        )

    def return_statement(self):
        # example: wapas value;
        if self.check("SEMICOLON"):
            self.advance()
            return ReturnStatement(None)

        value = self.expression()

        self.consume(
            "SEMICOLON",
            "Expected ';' after return value."
        )

        return ReturnStatement(value)

    def block(self):
        # A block is just a list of statements inside { ... }.
        statements = []

        while not self.check("RIGHT_BRACE") and not self.check("EOF"):
            statements.append(self.statement())

        self.consume(
            "RIGHT_BRACE",
            "Expected '}' after block."
        )

        return Block(statements)

    def expression_statement(self):
        # A bare expression like "x + 1;" is treated as a statement.
        expression = self.expression()

        self.consume(
            "SEMICOLON",
            "Expected ';' after expression."
        )

        return ExpressionStatement(expression)

    def expression(self):
        # Expression parsing is layered by precedence.
        # The lower-precedence operator is parsed first.
        return self.logical_or()

    def logical_or(self):
        expression = self.logical_and()

        while self.match("OR"):
            operator = self.previous().lexeme
            right = self.logical_and()

            expression = BinaryExpression(
                expression,
                operator,
                right
            )

        return expression

    def logical_and(self):
        expression = self.equality()

        while self.match("AND"):
            operator = self.previous().lexeme
            right = self.equality()

            expression = BinaryExpression(
                expression,
                operator,
                right
            )

        return expression

    def equality(self):
        expression = self.comparison()

        while self.match("EQUAL_EQUAL", "NOT_EQUAL"):
            operator = self.previous().lexeme
            right = self.comparison()

            expression = BinaryExpression(
                expression,
                operator,
                right
            )

        return expression

    def comparison(self):
        expression = self.addition()

        while self.match(
            "LESS",
            "GREATER",
            "LESS_EQUAL",
            "GREATER_EQUAL"
        ):
            operator = self.previous().lexeme
            right = self.addition()

            expression = BinaryExpression(
                expression,
                operator,
                right
            )

        return expression

    def addition(self):
        expression = self.multiplication()

        while self.match("PLUS", "MINUS"):
            operator = self.previous().lexeme
            right = self.multiplication()

            expression = BinaryExpression(
                expression,
                operator,
                right
            )

        return expression

    def multiplication(self):
        expression = self.unary()

        while self.match(
            "MULTIPLY",
            "DIVIDE",
            "MODULO"
        ):
            operator = self.previous().lexeme
            right = self.unary()

            expression = BinaryExpression(
                expression,
                operator,
                right
            )

        return expression

    def unary(self):
        if self.match("NOT", "MINUS"):
            operator = self.previous().lexeme
            operand = self.unary()

            return UnaryExpression(
                operator,
                operand
            )

        return self.primary()

    def primary(self):
        # Base values: numbers, strings, booleans, null, variables, calls,
        # and parenthesized expressions.
        token = self.peek()

        if self.match("NUMBER"):
            value = token.lexeme

            if "." in value:
                return NumberLiteral(float(value))

            return NumberLiteral(int(value))

        if self.match("STRING"):
            return StringLiteral(token.lexeme[1:-1])

        if self.match("SATYA"):
            return BooleanLiteral(True)

        if self.match("ASATYA"):
            return BooleanLiteral(False)

        if self.match("SHUNYA"):
            return NoneLiteral()

        if self.match("IDENTIFIER"):
            name = token.lexeme

            if self.match("LEFT_PAREN"):
                arguments = []

                if not self.check("RIGHT_PAREN"):
                    while True:
                        arguments.append(self.expression())

                        if not self.match("COMMA"):
                            break

                self.consume(
                    "RIGHT_PAREN",
                    "Expected ')' after arguments."
                )

                return CallExpression(
                    name,
                    arguments
                )

            return Variable(name)

        if self.match("LEFT_PAREN"):
            expression = self.expression()

            self.consume(
                "RIGHT_PAREN",
                "Expected ')' after expression."
            )

            return expression

        raise SyntaxError(
            f"Expected a value at line {token.line}, "
            f"column {token.column}"
        )

    def match(self, *types):
        # Quick helper: if the next token matches any of these types,
        # consume it and return True. Otherwise leave the stream alone.
        if self.peek().type in types:
            self.advance()
            return True

        return False

    def consume(self, token_type, message):
        # like match(), but raises a parser error if the expected token is missing.
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
    # Entry point for the parser: convert raw source text into a program tree.
    parser = Parser(tokens)
    return parser.parse()