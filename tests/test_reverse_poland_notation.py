import unittest


from src.reverse_poland_notation import is_operator, prior_operator, to_reverse_poland_notation

class TestRPN(unittest.TestCase):

    def test_is_operator(self):
        self.assertTrue(is_operator('+'), True)
        self.assertTrue(is_operator('-'), True)
        self.assertTrue(is_operator('*'), True)
        self.assertTrue(is_operator('/'), True)
        self.assertTrue(is_operator('**'), True)
        self.assertTrue(is_operator('//'), True)
        self.assertTrue(is_operator('%'), True)
        self.assertTrue(is_operator('~'), True)
        self.assertTrue(is_operator('$'), True)
        self.assertFalse(is_operator('7654'))
        self.assertFalse(is_operator('-67.8'))

    def test_prior_operator(self):
        self.assertEqual(prior_operator('+'), 1)
        self.assertEqual(prior_operator('-'), 1)
        self.assertEqual(prior_operator('*'), 2)
        self.assertEqual(prior_operator('/'), 2)
        self.assertEqual(prior_operator('//'), 2)
        self.assertEqual(prior_operator('%'), 2)
        self.assertEqual(prior_operator('**'), 4)
        self.assertEqual(prior_operator('~'), 3)
        self.assertEqual(prior_operator('$'), 3)
        self.assertEqual(prior_operator('+3'), 0)
        self.assertEqual(prior_operator('a'), 0)
        self.assertEqual(prior_operator('1'), 0)

    def test_simple_rpn(self):
        self.assertEqual(to_reverse_poland_notation(['2', '*', '1']), ['2', '1', '*'])
        self.assertEqual(to_reverse_poland_notation(['2', '*', '1', '+', '5']), ['2', '1', '*', '5', '+'])
        self.assertEqual(to_reverse_poland_notation(['6', '+', '2', '*', '1']), ['6', '2', '1', '*', '+'])

    def test_rpn_with_bracket(self):
        self.assertEqual(to_reverse_poland_notation(['4', '//', '6', '*', '(', '3', '+', '1', '-', '0', ')']), ['4', '6', '//', '3', '1', '+', '0', '-', '*'])
        self.assertEqual(to_reverse_poland_notation(['4', '+', '6', '*', '(', '~', '3', '+', '1', '/', '(', '7', '%', '6', ')', ')']), ['4', '6', '3', '~', '1', '7', '6', '%', '/', '+', '*', '+'])
        self.assertEqual(to_reverse_poland_notation(['(', '5', '+', '1', ')', '/', '(', '3', '%', '4', ')']), ['5', '1', '+', '3', '4', '%', '/'])

    def test_rpn_error(self):
        self.assertEqual(to_reverse_poland_notation(['(', '4', '+', '5']), "Недостаточно скобок")
        self.assertEqual(to_reverse_poland_notation(['4', '+', '5', ')']), "Недостаточно скобок")

unittest.main()
