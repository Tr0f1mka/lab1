import unittest
from unittest.mock import patch
import io

from src.main import let

class TestLet(unittest.TestCase):

    def setUp(self):
        self.captured_output = io.StringIO()
        self.patched_stdout = patch('sys.stdout', self.captured_output)
        self.patched_stdout.start()

    def tearDown(self):
        self.patched_stdout.stop()

    def test_add(self):
        let("let x = 7", True)
        captured_output = self.captured_output.getvalue().strip()
        expected_output = "Переменная x успешно задана"
        self.assertEqual(captured_output, expected_output)

    def test_error_name(self):
        let("let 1xw = 7", True)
        captured_output = self.captured_output.getvalue().strip()
        expected_output = "Ошибка ввода имени переменной: неправильное название переменной"
        self.assertEqual(captured_output, expected_output)

    def test_error_split_name(self):
        let("let x w = 7", True)
        captured_output = self.captured_output.getvalue().strip()
        expected_output = "Ошибка ввода имени переменной: переменная должна быть одним словом"
        self.assertEqual(captured_output, expected_output)

    def test_error_inicialize(self):
        let("let x = 7 = -1", True)
        captured_output = self.captured_output.getvalue().strip()
        expected_output = "Ошибка объявления переменной"
        self.assertEqual(captured_output, expected_output)

    def test_error_func_name(self):
        let("let max = 7", True)
        captured_output = self.captured_output.getvalue().strip()
        expected_output = "Названия функций не могут быть именем переменной"
        self.assertEqual(captured_output, expected_output)

    def test_error_use_variable(self):
        let("let x = 7*w", True)
        captured_output = self.captured_output.getvalue().strip()
        expected_output = "Нельзя задавать переменные через переменные"
        self.assertEqual(captured_output, expected_output)

    def test_error_decision(self):
        let("let x = 7 8", False)
        captured_output = self.captured_output.getvalue().strip()
        expected_output = "Ошибка объявления переменной: недостаточно операторов"
        self.assertEqual(captured_output, expected_output)

unittest.main()
