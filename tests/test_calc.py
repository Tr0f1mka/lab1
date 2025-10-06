import unittest

from src.calc import calc

class TestCalc(unittest.TestCase):

    def test_simple(self):
        self.assertEqual(calc(['2', '7', '-', '8', '/']), -0.625)
        self.assertEqual(calc(['-6.7', '9', '*', '2', '**']), 3636.0900000000006)
        self.assertEqual(calc(['9', '1', '+', '7', '//']), 1)
        self.assertEqual(calc(['9']), 9)
        self.assertEqual(calc(['-7.8']), -7.8)

    def test_unary(self):
        self.assertEqual(calc(['7', '~']), -7)
        self.assertEqual(calc(['5.0', '$', '9', '%']), 5)
        self.assertEqual(calc(['5', '6.7', '+', '~']), -11.7)

    def test_errors(self):
        self.assertEqual(calc(['~']), "Недостаточно операнд")
        self.assertEqual(calc(['4', '5', '+', '-']), "Недостаточно операнд")
        self.assertEqual(calc(['6.7', '7', '//']), '"//" и "%" только для целых чисел')
        self.assertEqual(calc(['1', '2', '3', '/']), "Недостаточно операторов")
        self.assertEqual(calc(['4', '1', '1', '~', '+', '/']), "Деление на ноль")

unittest.main()
