import unittest
from interpreter.lexer import tokenize


class TestLexer(unittest.TestCase):
    def test_variable_declaration(self):
        tokens = tokenize("maan age = 14;")
        types = [token.type for token in tokens]

        self.assertEqual(
            types,
            ["MAAN", "IDENTIFIER", "EQUAL", "NUMBER", "SEMICOLON", "EOF"]
        )

    def test_keywords(self):
        tokens = tokenize("satya asatya shunya")
        types = [token.type for token in tokens]

        self.assertEqual(types, ["SATYA", "ASATYA", "SHUNYA", "EOF"])

    def test_arithmetic(self):
        tokens = tokenize("2 + 3 * 4")
        types = [token.type for token in tokens]

        self.assertEqual(
            types,
            ["NUMBER", "PLUS", "NUMBER", "MULTIPLY", "NUMBER", "EOF"]
        )

    def test_invalid_character(self):
        with self.assertRaisesRegex(SyntaxError, "Unexpected character"):
            tokenize("maan age = @;")


if __name__ == "__main__":
    unittest.main()