"""----------------------
   ---решает выражение---
   ----------------------"""

"""------библиотеки------"""

import re                                       # noqa: E402
import patterns                                 #type: ignore  # noqa: E402
import parser                                   #type: ignore  # noqa: E402
import reverse_poland_notation                  #type: ignore  # noqa: E402
import calc                                     #type: ignore  # noqa: E402



"""-------функции--------"""

def decision(stroka: str, infix: bool, variables: dict) -> float | int | str:
    #print('start')
    #print(stroka)
    """
    Функция, решающая выражение
    :param stroka: Строка - введённое пользователем выражение
    :param infix: Логический тип - форма введённого выражения
    :param variables: Словарь - список переменных
    :return: Вещественное число - решение выражения или строка - сообщение об ошибке
    """

    if re.fullmatch(r"\s*", stroka):      #Проверка введения пустой строки
        return "Введена пустая строка"

    else:     #Если строка не пустая, обрабатываем её
        while re.search(patterns.UNARY_MINUS, stroka):    #Замена унарных знаков перед скобкой в начале выражения или в скобках на удобные
            try:
                a, b = re.search(patterns.UNARY_MINUS, stroka).span()   #type: ignore
                stroka = stroka[:a] + "~" + stroka[b:]
            except(AttributeError):
                return "Ошибка ввода"

        while re.search(patterns.UNARY_PLUS, stroka):
            try:
                a, b = re.search(patterns.UNARY_PLUS, stroka).span()   #type: ignore
                stroka = stroka[:a] + "$" + stroka[b:]
            except(AttributeError):
                return "Ошибка ввода"

        stroka_tokens = parser.tokens(stroka)
        #print(stroka_tokens)
        if type(stroka_tokens) is str:
            print(0)
            return stroka_tokens
        #Если в строке есть функции, обрабатываем их и заменяем на их значения
        if ("abs" in stroka) or ("sqrt" in stroka) or ("pow" in stroka) or ("max" in stroka) or ("min" in stroka) or (re.search(patterns.NAME_PATT, stroka)):
            #print("func")
            for i in range(len(stroka_tokens)):

                #Обработка модуля
                if "abs" in stroka_tokens[i]:
                    if re.fullmatch(r"\s*", stroka_tokens[i][4:-1]):    #Проверка на пустой аргумент
                        return "Функция abs должна содержать 1 аргумент"
                    if parser.tokens(stroka_tokens[i][4:-1]).count(',') != 0:   #Проверка на лишний аргумент
                        return "Функция abs должна содержать 1 аргумент"
                    a = decision(stroka_tokens[i][4:-1], infix, variables)    #Ищем значение выражения в скобках
                    try:       #Подставляем значение функции, если решение её аргумента - число, или возвращаем сообщение об ошибке
                        if type(a) is int:
                            stroka_tokens[i] = str(abs(int(a)))
                        else:
                            stroka_tokens[i] = str(abs(float(a)))
                    except(TypeError):
                        return a

                #Обработка возведения в степень
                elif "pow" in stroka_tokens[i]:
                    expr = parser.tokens(stroka_tokens[i][4:-1])    #Парсим выражение в скобках,чтобы узнать количество аргументов по запятым
                    if expr.count(',') == 1:    #2 аргумента разделяются 1 запятой
                        #Сшиваем аргументы функции
                        a = ""
                        b = ""
                        for j in range(expr.index(',')):
                            a += expr[j]
                        for j in range(expr.index(',')+1, len(expr)):
                            b += expr[j]

                        if re.fullmatch(r"\s*", a) or re.fullmatch(r"\s*", b):    #Если аргументы пустые, вернуть ошибку
                            return "Функция pow должна содержать непустой(-ые) аргумент(-ы)"
                        else:      #Иначе считаем аргументы
                            a = decision(a, infix, variables)
                            if type(a) is str:     #Если в первом аргументе ошибка, возвращаем её
                                return a
                            else:
                                b = decision(b, infix, variables)
                                try:
                                    if type(a) is float:
                                        a = float(a)
                                    else:
                                        a = int(a)
                                    if type(b) is float:
                                        b = float(b)
                                    else:
                                        b = int(b)
                                    stroka_tokens[i] = str(a**b)
                                except(TypeError):
                                    return b


                                if type(b) is str:     #Если во втором аргументе ошибка, возвращаем её
                                    return b
                                else:     #Иначе заменяем функцию на её значение
                                    stroka_tokens[i] = str(a ** b)
                    else:    #Если больше 2 аргументов, возвращаем ошибку
                        return "Функция pow должна иметь 2 аргумента"

                #Обработка корня
                elif "sqrt" in stroka_tokens[i]:
                    if re.fullmatch(r"\s*", stroka_tokens[i][5:-1]):    #Проверка на пустой аргумент
                        return "Функция sqrt должна содержать 1 аргумент"
                    if parser.tokens(stroka_tokens[i][5:-1]).count(',') != 0:   #Проверка на лишний аргумент
                        return "Функция sqrt должна содержать 1 аргумент"
                    a = decision(stroka_tokens[i][5:-1], infix, variables)
                    try:     #Если аргумент - не сообщение об ошибке, вставляем значение функции на её место
                        if type(a) is float:
                            a = float(a)
                        else:
                            a = int(a)

                        stroka_tokens[i] = str(a**0.5)
                    except(TypeError):  #Иначе возвращаем ошибку
                        return a

                #Обработка максимума
                elif "max" in stroka_tokens[i]:
                    if re.fullmatch(r"\s*", stroka_tokens[i][4:-1]):     #Проверка на пустой(-ые) аргумент(-ы)
                        return "Функция max должна содержать минимум 1 аргумент"
                    expr = parser.tokens(stroka_tokens[i][4:-1])     #Парсим выражение функции, чтобы найти запятые, разделяющие аргументы
                    elements = []     #Список аргументов функции
                    elem = ""         #Переменная, в которой "сшиваются" токены аргументов
                    for j in expr:
                        if j != ",":     #Если текущий токен - не ",", сшиваем его с остальными текущего аргумента
                            elem += j
                        else:            #Иначе проверяем аргумент на ошибки и добавляем в список аргументов в случае корректности
                            if elem == "":
                                return "Функция max должна содержать непустой(-ые) аргумент(-ы)"

                            elem = decision(str(elem), infix, variables)    #type: ignore
                            if type(elem) is str:
                                return elem
                            else:
                                elements.append(elem)
                                elem = ""

                    if elem == "":     #Отдельно обрабатываем последний элемент, та как он не проходит проверку в цикле
                        return "Функция max должна содержать непустой(-ые) аргумент(-ы)"
                    else:
                        elem = decision(elem, infix, variables)    #type: ignore
                        if type(elem) is str:
                            return elem
                        else:
                            elements.append(elem)
                            elem = ""
                    stroka_tokens[i] = str(max(elements))     #Заменяем функцию на результат


                #Обработка минимума
                elif "min" in stroka_tokens[i]:
                    if re.fullmatch(r"\s*", stroka_tokens[i][4:-1]):     #Проверка на пустой(-ые) аргумент(-ы)
                        return "Функция max должна содержать минимум 1 аргумент"
                    expr = parser.tokens(stroka_tokens[i][4:-1])     #Парсим выражение функции, чтобы найти запятые, разделяющие аргументы
                    elements = []     #Список аргументов функции
                    elem = ""         #Переменная, в которой "сшиваются" токены аргументов
                    for j in expr:
                        if j != ",":     #Если текущий токен - не ",", сшиваем его с остальными текущего аргумента
                            elem += j
                        else:            #Иначе проверяем аргумент на ошибки и добавляем в список аргументов в случае корректности
                            if elem == "":
                                return "Функция min должна содержать непустой(-ые) аргумент(-ы)"

                            elem = decision(elem, infix, variables)    #type: ignore
                            if type(elem) is str:
                                return elem
                            else:
                                elements.append(elem)
                                elem = ""

                    if elem == "":     #Отдельно обрабатываем последний элемент, та как он не проходит проверку в цикле
                        return "Функция min должна содержать непустой(-ые) аргумент(-ы)"
                    else:
                        elem = decision(elem, infix, variables)    #type: ignore
                        if type(elem) is str:
                            return elem
                        else:
                            elements.append(elem)
                            elem = ""

                    stroka_tokens[i] = str(min(elements))     #Заменяем функцию на результат

                #Обработка переменных
                elif re.fullmatch(patterns.NAME_PATT, stroka_tokens[i]):
                    #print(1)
                    try:
                        stroka_tokens[i] = variables[stroka_tokens[i]]
                    except(KeyError):
                        return f"Переменная {stroka_tokens[i]} не задана"
                    except():
                        #print(1)
                        return "Ошибка ввода"

        if re.match(patterns.NAME_PATT, str(stroka_tokens)):
            for i in range(len(stroka_tokens)):
                #Обработка переменных
                if re.fullmatch(patterns.NAME_PATT, stroka_tokens[i]):
                    try:
                        stroka_tokens[i] = variables[stroka_tokens[i]]
                    except(KeyError):
                        return f"Переменная {stroka_tokens[i]} не задана"
                    except():
                        #print(2)
                        return "Ошибка ввода"

        #print(stroka_tokens)
        stroka_rpn = reverse_poland_notation.to_reverse_poland_notation(stroka_tokens)
        if type(stroka_rpn) is str:
            #print("!")
            return stroka_rpn
        else:
            check = [x for x in stroka_tokens if ((x != '(') and (x != ')'))]
            if not infix:
                if '(' in stroka_tokens or ')' in stroka_tokens:
                    if check != stroka_rpn:
                        #print(3)
                        return "Ошибка ввода"
                    else:
                        ans = ""
                        elem = ""
                        flag = False
                        cnt_bracket = 0
                        for i in range(len(stroka_tokens)):
                            if flag:
                                elem += stroka_tokens[i]
                                elem += " "
                                if stroka_tokens[i] == "(":
                                    cnt_bracket += 1
                                elif stroka_tokens[i] == ")":
                                    cnt_bracket -= 1
                                    if cnt_bracket == 0:
                                        #print(elem, type(elem))
                                        elem_ans = decision(elem[1:-2], infix, variables)
                                        if type(elem_ans) is str:
                                            return elem_ans
                                        ans += str(elem_ans)
                                        ans += " "
                                        elem = ""
                                        flag = False
                            else:
                                if stroka_tokens[i] == "(":
                                    flag = True
                                    cnt_bracket += 1
                                    elem += stroka_tokens[i]
                                    #print(elem, flag)
                                else:
                                    ans += stroka_tokens[i]
                                    ans += " "
                        #print(f"{ans}, 1")
                        return decision(ans, infix, variables)
                else:
                    #print(stroka_tokens)
                    if check != stroka_rpn:
                        return "Ошибка ввода"
                    return calc.calc(stroka_tokens)
            else:
                #print(stroka, stroka_tokens, stroka_rpn)
                if len(check) > 1:
                    for i in range(len(check)-1):
                        #print("i =", i, "check =", check[i], check[i+1], reverse_poland_notation.is_operator(check[i]), reverse_poland_notation.is_operator(check[i+1]))
                        #print(stroka, stroka_tokens)

                        if reverse_poland_notation.is_operator(check[i]) == reverse_poland_notation.is_operator(check[i+1]):
                            return "Ошибка ввода"
                        return calc.calc(stroka_rpn)

    return calc.calc(stroka_rpn)



test = [
    "(56*67)-          abs() + sqrt(56, 67)",
    "(56*67)-          abs(-56) + sqrt(56, 67)",
    "pow(56, 67)-          abs(-7) + sqrt(56)"
]

#for i in test:
#print(decision("56 + x", True, {"x": "56"}), end="\n\n")

print(decision("(-(6) +9) *2", True, {}))
