import unittest

from src.decision import decision

class TestDecision(unittest.TestCase):

    def test_simple(self):
        self.assertEqual(decision("67+    6//7.0", True, {}), 67)
        self.assertEqual(decision("   7*  (-7 +1)", True, {}), -42)
        self.assertEqual(decision("(-(5*9.2)+2)/1", True, {}), -44.0)

    def test_with_func(self):
        self.assertEqual(decision("abs(-67.5+1)", True, {}), 66.5)
        self.assertEqual(decision("max(  pow(sqrt(5*5)  , 2)   ,min(1), abs(  -100.7654  ))", True, {}), 100.7654)
        self.assertEqual(decision("7-  min(3,2,1)*4", True, {}), 3)

    def test_with_variables(self):
        self.assertEqual(decision("x**2 -5.2*x +1", True, {"x": "5"}), 0.0)
        self.assertEqual(decision("max(x  , y)", True, {"x": "3", "y": "-1"}), 3)
        self.assertEqual(decision("min(x)", True, {}), "Переменная x не задана")

    def test_simple_postfix(self):
        self.assertEqual(decision("56 7**", False, {}), 1727094849536)
        self.assertEqual(decision("12 7.5 -", False, {}), 4.5)
        self.assertEqual(decision("7~ 5**", False, {}), -16807)

    def test_postfix_with_func(self):
        self.assertEqual(decision("abs(67.5 ~ 1 +)", False, {}), 66.5)
        self.assertEqual(decision("max(  pow(sqrt(5 5*)  , 2)   ,min(1), abs(  100.7654~  ))", False, {}), 100.7654)
        self.assertEqual(decision("7  min(3,2,1) 4 * -", False, {}), 3)

    def test_postfix_with_variables(self):
        self.assertEqual(decision("x 2** 5.2 x*-1+", False, {"x": "5"}), 0.0)
        self.assertEqual(decision("max(x  , x y -)", False, {"x": "3", "y": "-1.0"}), 4.0)
        self.assertEqual(decision("min(x)", False, {}), "Переменная x не задана")

    def test_hard(self):
        self.assertEqual(decision("max(abs(1 - 2), sqrt(pow(a, 2) + pow(b, 2))) + (c // d) - (e%f) + (1 ** 7.0) + min(-12, 0) / (98 + 1)", True, {"a": "2", "b": "3", "c":"4", "d":"1", "e":"0", "f":"7"}), 8.484339154251868)
        self.assertEqual(decision("max(abs(1 2 -), sqrt(pow(a, 2) pow(b, 2) +)) (c d //) + (e f %) - (1 7.0 **) + min(12 ~, 0) (98 1 +) / +", False, {"a": "2", "b": "3", "c":"4", "d":"1", "e":"0", "f":"7"}), 8.484339154251868)

    def test_error(self):
        self.assertEqual(decision("7.+1", True, {}), "Вещественные числа должны не содержать пробелов и иметь вещественную и целые части")
        self.assertEqual(decision("", True, {}), "Введена пустая строка")
        self.assertEqual(decision("abs(   )+1", True, {}), "Функция abs должна содержать 1 аргумент")
        self.assertEqual(decision("abs(pow(2))", True, {}), "Функция pow должна иметь 2 аргумента")
        self.assertEqual(decision("sqrt(7, 8, 0)", True, {}), "Функция sqrt должна содержать 1 аргумент")
        self.assertEqual(decision("max(,9,0)", True, {}), "Функция max должна содержать непустой(-ые) аргумент(-ы)")
        self.assertEqual(decision("(54+x)*         7", True, {}), "Переменная x не задана")
        self.assertEqual(decision("5 (6 + 7) 8 - +", False, {}), "Недостаточно операнд")
        self.assertEqual(decision("6 --7", True, {}), "Ошибка ввода")

unittest.main()
