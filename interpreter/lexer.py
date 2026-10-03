import re
from dataclasses import dataclass

KEYWORDS = {
    "maan", "rakho", "likha", "yadi", "agar",
    "anyatha", "warna", "satya", "asatya", "shunya",
    "aur", "ya", "nahi", "wapas", "karya",
    "yavyat", "jabtak"
}

TOKEN_PATTERN = re.compile(
    r"(?P<WHITESPACE>\s+)"
    r"|(?P<NUMBER>\d+(?:\.\d+)?)"
    r"|(?P<STRING>\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*')"
    r"|(?P<IDENTIFIER>[a-zA-Z_][a-zA-Z0-9_]*)"
    r"|(?P<OPERATOR>==|!=|<=|>=|[=+\-*/%<>])"
    r"|(?P<PUNCTUATION>[(){};,])"
)

OPERATORS = {
    "=": "EQUAL",
    "==": "EQUAL_EQUAL",
    "!=": "NOT_EQUAL",
    "<": "LESS",
    ">": "GREATER",
    "<=": "LESS_EQUAL",
    ">=": "GREATER_EQUAL",
    "+": "PLUS",
    "-": "MINUS",
    "*": "MULTIPLY",
    "/": "DIVIDE",
    "%": "MODULO"
}

PUNCTUATION = {
    "(": "LEFT_PAREN",
    ")": "RIGHT_PAREN",
    "{": "LEFT_BRACE",
    "}": "RIGHT_BRACE",
    ";": "SEMICOLON",
    ",": "COMMA"
}


@dataclass
class Token:
    type: str
    lexeme: str
    line: int
    column: int


def tokenize(source):
    tokens = []
    position = 0
    line = 1
    column = 1

    while position < len(source):
        match = TOKEN_PATTERN.match(source, position)

        if not match:
            character = source[position]
            raise SyntaxError(
                f"Unexpected character {character!r} "
                f"at line {line}, column {column}"
            )

        lexeme = match.group()
        token_type = match.lastgroup
        token_line = line
        token_column = column

        if token_type != "WHITESPACE":
            if token_type == "IDENTIFIER" and lexeme in KEYWORDS:
                token_type = lexeme.upper()
            elif token_type == "OPERATOR":
                token_type = OPERATORS[lexeme]
            elif token_type == "PUNCTUATION":
                token_type = PUNCTUATION[lexeme]

            tokens.append(
                Token(token_type, lexeme, token_line, token_column)
            )

        newlines = lexeme.count("\n")

        if newlines:
            line += newlines
            column = len(lexeme) - lexeme.rfind("\n")
        else:
            column += len(lexeme)

        position = match.end()

    tokens.append(Token("EOF", "", line, column))
    return tokens
