import unittest


from src.parser import tokens

class TestParser(unittest.TestCase):
    def test_simple_expr(self):
        self.assertEqual(tokens("1+2"), ['1', '+', '2'])

unittest.main()
