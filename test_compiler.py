import unittest
from interpreter.compiler import compile_source


class TestCompiler(unittest.TestCase):
    def test_number(self):
        result = compile_source(
            "maan x = 14;"
        )

        self.assertEqual(
            result,
            [
                ("PUSH", 14),
                ("STORE", "x"),
                ("HALT",),
            ]
        )

    def test_print_variable(self):
        result = compile_source(
            "maan age = 14; likha(age);"
        )

        self.assertEqual(
            result,
            [
                ("PUSH", 14),
                ("STORE", "age"),
                ("LOAD", "age"),
                ("PRINT",),
                ("HALT",),
            ]
        )

    def test_arithmetic(self):
        result = compile_source(
            "maan x = 2 + 3 * 4;"
        )

        self.assertEqual(
            result,
            [
                ("PUSH", 2),
                ("PUSH", 3),
                ("PUSH", 4),
                ("MULTIPLY",),
                ("ADD",),
                ("STORE", "x"),
                ("HALT",),
            ]
        )


if __name__ == "__main__":
    unittest.main()