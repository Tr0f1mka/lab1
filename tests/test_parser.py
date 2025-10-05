import unittest


from src.parser import tokens

class TestParser(unittest.TestCase):
    def test_simple_expr(self):
        self.assertEqual(tokens("1+2"), ['1', '+', '2'])
        self.assertEqual(tokens("-5+2*3"), ['-5', '+', '2', '*', '3'])
        self.assertEqual(tokens("     2 **3 **  4//sd"), ['2', '**', '3', '**', '4', '//', 'sd'])

    def test_pars_with_bracket(self):
        self.assertEqual(tokens("(-2+3   ) *4"), ['(', '-2', '+', '3', ')', '*', '4'])
        self.assertEqual(tokens("12/-3*(+2)"), ['12', '/', '-', '3', '*', '(', '+2', ')'])
        self.assertEqual(tokens("( r+ 54% 6.7 -(6// 2 %post)) **5"), ['(', 'r', '+', '54', '%', '6.7', '-', '(', '6', '//', '2', '%', 'post', ')', ')', '**', '5'])

    def test_with_func(self):
        self.assertEqual(tokens("abs(-7 *4) /max(56, 1)+ sqrt(1    ) //min(87)**pow(9, 5*7)"), ['abs( -7 * 4 )', '/', 'max( 56 , 1 )', '+', 'sqrt( 1 )', '//', 'min( 87 )', '**', 'pow( 9 , 5 * 7 )'])
        self.assertEqual(tokens("pow( min(9, -6,  max(), sqrt(9 * abs(-(5)))))"), ['pow( min ( 9 , - 6 , max ( ) , sqrt ( 9 * abs ( - ( 5 ) ) ) ) )'])
        self.assertEqual(tokens("max((  54% 6.7 -(6// qwe rty)) **5) + min(sqrt(- 7 *y)  )/ pow(7, 7)"), ['max( ( 54 % 6.7 - ( 6 // qwe rty ) ) ** 5 )', '+', 'min( sqrt ( - 7 * y ) )', '/', 'pow( 7 , 7 )'])

    def test_errors(self):
        self.assertEqual(tokens("abs +7 (-90)"), "После названия функции должны идти аргументы(в скобках)")
        self.assertEqual(tokens("-90 *sqrt"), "После названия функции должны идти аргументы(в скобках)")
        self.assertEqual(tokens("abs(-ty"), "Аргументы функции должны быть в скобках")

    def test_rpn_pars(self):
        self.assertEqual(tokens("(56 7 - 9*) 8/"), ['(', '56', '7', '-', '9', '*', ')', '8', '/'])
        self.assertEqual(tokens("abs(76) pow(67,7) //"), ['abs( 76 )', 'pow( 67 , 7 )', '//'])
        self.assertEqual(tokens("rty qwe *"), ['rty', 'qwe', '*'])

unittest.main()
