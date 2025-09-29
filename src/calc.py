"""-----------------------------------
   -считает обратную польскую нотацию-
   -----------------------------------"""



"""------------библиотеки-------------"""

import operator  # noqa: E402
import re        # noqa: E402



"""---------словари и шаблоны---------"""

num = r"[+\-]?\d+(\.\d+)?"      #шаблон числа с унарным знаком

#словарь с функциями операторов
operations = {"+": operator.add, "-": operator.sub,
              "*": operator.mul, "/": operator.truediv,
              "//": operator.floordiv, "%": operator.mod,
              "**": operator.pow}



"""--------------функции--------------"""

def calc(arr: list[str]) -> list[float] | str:
    """
    считает значение математического выражения в постфиксной форме
    :param arr: Список, являющийся математичким выражением в постфиксной форме
    :return: Вещественное число, являющееся значением выражения, или сообщение об ошибке
    """

    ans = []            #стек ответа
    flag_error = False  #флаг ошибки

    for i in range(len(arr)):
        if re.fullmatch(num, arr[i]):         #если текущий элемент - число, кладём в стек ответа
            ans.append(float(arr[i]))
        else:                                 #иначе - выполняем операцию, соответствующую текущему элементу, если это возможно
            if len(ans) >= 2:
                op2, op1, = ans.pop(), ans.pop()
                if (arr[i] == "/" or arr[i] == "//" or arr[i] == "%") and op2 == 0:   #если происходит деление на ноль, отправляем ошибку и выходим из цикла
                    err = "Деление на ноль"
                    flag_error = True
                    break
                if (arr[i] == "//" or arr[i] == "%") and (not((op1 == int(op1)) and (op2 == int(op2)))):   #если выполняется '//' и '%' с дробными числами, отправляем ошибку и выходим из цикла
                    err = "// и % только для целых"
                    flag_error = True
                    break
                ans.append(operations[arr[i]](op1, op2))
            else:
                flag_error = True
                err = "Введено математически неверное выражение"
                break

    if len(ans) != 1:
        flag_error = True
        err = "Введено математически неверное выражение"

    if not(flag_error): 
        return ans
    else: 
        return err