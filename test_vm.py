import unittest
from interpreter.compiler import compile_source
from interpreter.vm import run


class TestVM(unittest.TestCase):
    def test_number(self):
        instructions = compile_source(
            "maan x = 14;"
        )

        run(instructions)

    def test_arithmetic(self):
        instructions = compile_source(
            "maan x = 2 + 3 * 4; likha(x);"
        )

        run(instructions)


if __name__ == "__main__":
    unittest.main()