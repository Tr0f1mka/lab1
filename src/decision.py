"""----------------------
   ---решает выражение---
   ----------------------"""

"""------библиотеки------"""

import re                                       # noqa: E402
import src.patterns as patterns                                 #type: ignore  # noqa: E402
import src.parser as parser                                   #type: ignore  # noqa: E402
import src.reverse_poland_notation as reverse_poland_notation                  #type: ignore  # noqa: E402
import src.calc as calc                                     #type: ignore  # noqa: E402



"""-------функции--------"""

def decision(stroka: str, infix: bool, variables: dict) -> float | int | str:
    #print()
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
    if re.search(patterns.BAN_NUM, stroka):
        return "Вещественные числа должны не содержать пробелов и иметь вещественную и целые части"
    else:     #Если строка не пустая, обрабатываем её
        if infix:
            stroka_tokens = ""
            for x in stroka.split():
                stroka_tokens += x
            #print(stroka_tokens)
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

        #print(stroka, "u")

        stroka_tokens = parser.tokens(stroka)   #type: ignore
        #print("tokens", stroka_tokens)
        if type(stroka_tokens) is str:
            #print(0)
            return stroka_tokens
        #Если в строке есть функции, обрабатываем их и заменяем на их значения
        if ("abs" in stroka) or ("sqrt" in stroka) or ("pow" in stroka) or ("max" in stroka) or ("min" in stroka) or (re.search(patterns.NAME_PATT, stroka)):
            #print("func")
            for i in range(len(stroka_tokens)):
                #print("for", stroka_tokens[i])
                #Обработка модуля
                if "abs" in stroka_tokens[i][:3]:
                    #print("1", stroka_tokens[i])
                    if re.fullmatch(r"\s*", stroka_tokens[i][4:-1]):    #Проверка на пустой аргумент
                        return "Функция abs должна содержать 1 аргумент"
                    if parser.tokens(stroka_tokens[i][4:-1]).count(',') != 0:   #Проверка на лишний аргумент
                        return "Функция abs должна содержать 1 аргумент"
                    #print(stroka_tokens[i][4:-1], "ab")
                    a = decision(stroka_tokens[i][4:-1], infix, variables)    #Ищем значение выражения в скобках
                    try:       #Подставляем значение функции, если решение её аргумента - число, или возвращаем сообщение об ошибке
                        if type(a) is int:
                            stroka_tokens[i] = str(abs(int(a)))    #type: ignore
                        else:
                            stroka_tokens[i] = str(abs(float(a)))    #type: ignore
                    except(TypeError):
                        return a
                    except(ValueError):
                        return a

                #Обработка возведения в степень
                elif "pow" in stroka_tokens[i][:3]:
                    #print("2", stroka_tokens[i])
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
                                    c = str(a**b)   #type: ignore
                                    if c[0] == '-':
                                        c = c[1:]+'~'
                                    stroka_tokens[i] = c   #type: ignore
                                except(TypeError):
                                    return b
                                except(ValueError):
                                    return b
                    else:    #Если больше 2 аргументов, возвращаем ошибку
                        return "Функция pow должна иметь 2 аргумента"

                #Обработка корня
                elif "sqrt" in stroka_tokens[i][:4]:
                    #print("3", stroka_tokens[i])
                    if re.fullmatch(r"\s*", stroka_tokens[i][5:-1]):    #Проверка на пустой аргумент
                        return "Функция sqrt должна содержать 1 аргумент"
                    if parser.tokens(stroka_tokens[i][5:-1]).count(',') != 0:   #Проверка на лишний аргумент
                        return "Функция sqrt должна содержать 1 аргумент"

                    a = decision(stroka_tokens[i][5:-1], infix, variables)
                    try:     #Если аргумент - не сообщение об ошибке, вставляем значение функции на её место
                        c = str(a**0.5)   #type: ignore
                        if c[0] == '-':
                            c = c[1:]+'~'
                        stroka_tokens[i] = c   #type: ignore
                    except(TypeError):  #Иначе возвращаем ошибку
                        return a
                    except(ValueError):
                        return a

                #Обработка максимума
                elif "max" in stroka_tokens[i][:3]:
                    #print("4", stroka_tokens[i])
                    if re.fullmatch(r"\s*", stroka_tokens[i][4:-1]):     #Проверка на пустой(-ые) аргумент(-ы)
                        return "Функция max должна содержать минимум 1 аргумент"
                    expr = parser.tokens(stroka_tokens[i][4:-1])     #Парсим выражение функции, чтобы найти запятые, разделяющие аргументы
                    #print(expr)
                    elements = []     #Список аргументов функции
                    elem = ""         #Переменная, в которой "сшиваются" токены аргументов
                    for j in range(len(expr)):
                        if expr[j] != ",":     #Если текущий токен - не ",", сшиваем его с остальными текущего аргумента
                            elem += expr[j]
                            elem += " "
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
                            #print("max_elem", elem)
                            elements.append(elem)
                            elem = ""
                    #print("max_arr", elements)
                    c = str(max(elements))
                    if c[0] == '-':
                        c = c[1:] + '~'
                    stroka_tokens[i] = c   #type: ignore     #Заменяем функцию на результат


                #Обработка минимума
                elif "min" in stroka_tokens[i][:3]:
                    #print("5", stroka_tokens[i])
                    if re.fullmatch(r"\s*", stroka_tokens[i][4:-1]):     #Проверка на пустой(-ые) аргумент(-ы)
                        return "Функция min должна содержать минимум 1 аргумент"
                    expr = parser.tokens(stroka_tokens[i][4:-1])     #Парсим выражение функции, чтобы найти запятые, разделяющие аргументы
                    elements = []     #Список аргументов функции
                    elem = ""         #Переменная, в которой "сшиваются" токены аргументов
                    for j in range(len(expr)):
                        if expr[j] != ",":     #Если текущий токен - не ",", сшиваем его с остальными текущего аргумента
                            elem += expr[j]
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

                    c = str(min(elements))
                    if c[0] == '-':
                        c = c[1:] + '~'
                    #print("token", c)
                    #print(stroka_tokens, "include")
                    stroka_tokens[i] = c   #type: ignore     #Заменяем функцию на результат
                    #print(stroka_tokens, "include")

                #Обработка переменных
                elif re.fullmatch(patterns.NAME_PATT, stroka_tokens[i]):
                    #print(1)
                    try:
                        c = variables[stroka_tokens[i]]
                        if c[0] == '-':
                            c = c[1:] + '~'
                        stroka_tokens[i] = c   #type: ignore
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
                        stroka_tokens[i] = variables[stroka_tokens[i]]   #type: ignore
                    except(KeyError):
                        return f"Переменная {stroka_tokens[i]} не задана"
                    except():
                        #print(2)
                        return "Ошибка ввода"

        #print(stroka_tokens)
        stroka_rpn = reverse_poland_notation.to_reverse_poland_notation(stroka_tokens)   #type: ignore
        if type(stroka_rpn) is str:
            #print("!")
            return stroka_rpn
        else:
            check = [x for x in stroka_tokens if ((x != '(') and (x != ')'))]
            if not infix:
                #print(stroka_tokens, stroka_rpn)
                if '(' in stroka_tokens or ')' in stroka_tokens:
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
                    #print(calc.calc(stroka_tokens), 'ab')
                    return calc.calc(stroka_tokens)   #type: ignore
            else:
                #print(stroka, stroka_tokens, stroka_rpn)
                #print(check)
                if len(check) > 1:
                    for i in range(len(check)-1):
                        #print("i =", i, "check =", check[i], check[i+1], reverse_poland_notation.is_operator(check[i]), reverse_poland_notation.is_operator(check[i+1]))
                        #print(stroka, stroka_tokens)

                        if not((check[i] in ['$', '~'] and check[i+1] in ['$', '~']) or (check[i] in ['+', '-', '*', '/', '//', '%', '**'] and check[i+1] in ['$', '~'])):
                            if (reverse_poland_notation.is_operator(check[i]) == reverse_poland_notation.is_operator(check[i+1])):
                                return "Ошибка ввода"
                    return calc.calc(stroka_rpn)   #type: ignore

    return calc.calc(stroka_rpn)   #type: ignore



test = [
    "(56*67)-          abs() + sqrt(56, 67)",
    "(56*67)-          abs(-56) + sqrt(56, 67)",
    "pow(56, 67)-          abs(-7) + sqrt(56)"
]

#for i in test:
#print(decision("56 + x", True, {"x": "56"}), end="\n\n")

#print(decision("max(abs(1 - 2), sqrt(pow(a, 2) + pow(b, 2))) + (c // d) - (e%f) + (1 ** 7.0) + min(-12, 0) / (98 + 1)", True, {"a": "2", "b": "3", "c":"4", "d":"1", "e":"0", "f":"7"}))
