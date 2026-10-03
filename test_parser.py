import unittest
from interpreter.parser import (
    parse,
    VariableDeclaration,
    PrintStatement,
    NumberLiteral,
    StringLiteral,
    Variable,
    BinaryExpression,
)

class TestParser(unittest.TestCase):
    def test_variable_declaration(self):
        program = parse("maan age = 14;")

        self.assertEqual(len(program.statements), 1)

        statement = program.statements[0]
        self.assertIsInstance(statement, VariableDeclaration)
        self.assertEqual(statement.name, "age")
        self.assertEqual(statement.value, NumberLiteral(14))

    def test_print_variable(self):
        program = parse("likha(age);")

        statement = program.statements[0]
        self.assertIsInstance(statement, PrintStatement)
        self.assertEqual(statement.value, Variable("age"))

    def test_string_declaration(self):
        program = parse('maan naam = "Aashvik";')

        statement = program.statements[0]
        self.assertEqual(statement.name, "naam")
        self.assertEqual(
            statement.value,
            StringLiteral("Aashvik")
        )

    def test_multiple_statements(self):
        program = parse(
            'maan age = 14; likha(age);'
        )

        self.assertEqual(len(program.statements), 2)

    def test_missing_semicolon(self):
        with self.assertRaises(SyntaxError):
            parse("maan age = 14")

    def test_arithmetic(self):
        program = parse("maan x = 2 + 3 * 4;")

        statement = program.statements[0]

        self.assertIsInstance(
            statement.value,
            BinaryExpression
        )

        self.assertEqual(statement.value.operator, "+")
        self.assertEqual(statement.value.left, NumberLiteral(2))

        right = statement.value.right

        self.assertIsInstance(
            right,
            BinaryExpression
        )

        self.assertEqual(right.operator, "*")
        self.assertEqual(right.left, NumberLiteral(3))
        self.assertEqual(right.right, NumberLiteral(4))

if __name__ == "__main__":
    unittest.main()