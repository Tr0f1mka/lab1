"""-----------------------------------
   -считает обратную польскую нотацию-
   -----------------------------------"""


"""------------библиотеки-------------"""
import operator
import re


"""---------словари и шаблоны---------"""


num = r"[+\-]?\d+(\.\d+)?"

operations = {"+": operator.add, "-": operator.sub,
              "*": operator.mul, "/": operator.truediv,
              "//": operator.floordiv, "%": operator.mod,
              "**": operator.pow}




def calc(arr: list[str]) -> float:
    ans = []
    flag_error = False

    for i in range(len(arr)):
        if re.fullmatch(num, arr[i]):
            ans.append(float(arr[i]))
        else:
            op2, op1, = ans.pop(), ans.pop()
            if arr[i] == "/" and op2 == 0:
                print("Деление на ноль")
                flag_error = True
                break
            if (arr[i] == "//" or arr[i] == "%") and (not((op1 == int(op1)) and (op2 == int(op2)))):
                print("// и % только для целых")
                flag_error = True
                break
            ans.append(operations[arr[i]](op1, op2))

    if not(flag_error): return ans  # noqa: E701


def test():
    print(calc(['1', '2', '+']))
    print(calc(['1', '12', '3', '*', '+']))
    print(calc(['3', '3', '-7', '/', '+']))
    print(calc(['3', '33.3', '%', '+8', '*', '5', '+', '6', '+']))
    print(calc(['3', '33.3', '%', '+8', '5', '+', '*', '6', '*']))
    print(calc(['3', '33.3', '/', '+8', '0', '+', '/', '0', '/']))


test()