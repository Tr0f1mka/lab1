"""-----------------------------------
   -считает обратную польскую нотацию-
   -----------------------------------"""



"""------------библиотеки-------------"""

import re           # noqa: E402
import src.patterns as patterns     #type: ignore  # noqa: E402



"""--------------словари--------------"""

#словарь с функциями операторов
operations = {"+": lambda x, y: x+y, "-": lambda x, y: x-y,
              "*": lambda x, y: x*y, "/": lambda x, y: x/y,
              "//": lambda x, y: x//y, "%": lambda x, y: x%y,
              "**": lambda x, y: x**y, "$": lambda x: +x,
              "~": lambda x: -x}



"""--------------функции--------------"""

def calc(arr: list[str]) -> int | float | str:
    """
    считает значение математического выражения в постфиксной форме
    :param arr: Список, являющийся математичким выражением в постфиксной форме
    :return: Вещественное или целое число, являющееся значением выражения, или строка - сообщение об ошибке
    """
    #print(arr)
    ans: list[float|int] = []            #стек ответа

    for i in range(len(arr)):
        #print(arr[i])
        if re.fullmatch(patterns.UNARY_NUM, arr[i]):
            #print('aboba', arr[i][:-1])
            a = '-'+arr[i][:-1]
            a = float(a)   #type: ignore
            if a % 1 == 0:
                ans.append(int(a))
            else:
                ans.append(a)   #type: ignore
        elif re.fullmatch(patterns.SIGNED_NUM, arr[i]):         #если текущий элемент - число, кладём в стек ответа
            a = float(arr[i])   #type: ignore
            if a % 1 == 0:
                ans.append(int(a))
            else:
                ans.append(a)   #type: ignore
        elif re.fullmatch(patterns.UNARY_NUM, arr[i]):
            a = '-'+arr[i][:-1]
            a = float(arr[i])   #type: ignore
            if a % 1 == 0:
                ans.append(int(a))
            else:
                ans.append(a)   #type: ignore
        else:                                 #иначе - выполняем операцию, соответствующую текущему элементу, если это возможно
            if arr[i] == "~" or arr[i] == "$":
                #print("op =", arr[i])
                try:
                    op1 = ans.pop()
                    ans.append(operations[arr[i]](op1))   #type: ignore
                except(IndexError):
                    #print("Err")
                    return "Недостаточно операнд"
                except():
                    return "Ошибка ввода"
            else:
                try:
                    op2, op1 = ans.pop(), ans.pop()
                    if (arr[i] in ["//", "%"]):
                        if (op1 % 1 != 0 or op2 % 1 != 0):
                            return '"//" и "%" только для целых чисел'
                        else:
                            ans.append(operations[arr[i]](int(op1), int(op2)))   #type: ignore
                    else:
                        ans.append(operations[arr[i]](op1, op2))   #type: ignore
                except(ZeroDivisionError):
                    return "Деление на ноль"
                except(IndexError):
                    #print("Err")
                    return "Недостаточно операнд"
                except():
                    return "Ошибка ввода"

    if len(ans) != 1:     #Если в итоговом списке больше одного оператора - значит в выражении слишком много операнд
        return "Недостаточно операторов"
    #print("Answer", ans[0])
    return ans[0]
