import unittest
from interpreter.evaluator import evaluate


class TestEvaluator(unittest.TestCase):
    def test_number(self):
        result = evaluate("maan x = 14;")
        self.assertEqual(result, 14)

    def test_variable(self):
        result = evaluate(
            "maan age = 14; likha(age);"
        )
        self.assertEqual(result, 14)

    def test_arithmetic(self):
        result = evaluate(
            "maan x = 2 + 3 * 4;"
        )
        self.assertEqual(result, 14)

    def test_string(self):
        result = evaluate(
            'maan naam = "Aashvik";'
        )
        self.assertEqual(result, "Aashvik")

    def test_multiple_operations(self):
        result = evaluate(
            "maan x = 10 + 5 * 2 - 4;"
        )
        self.assertEqual(result, 16)


if __name__ == "__main__":
    unittest.main()