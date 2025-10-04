"""----------------------------
   --------главный файл--------
   ----------------------------
"""



"""---------библиотеки---------"""

import re                        # noqa: E402
import patterns                  #type: ignore  # noqa: E402
import decision                  #type: ignore  # noqa: E402



"""----------Словари-----------"""

variables = {}     #Словарь переменных



"""----------функции-----------"""

def start() -> None:
    """
    Функция, выводящая приветственное сообщение
    :return: Данная функция ничего не возвращает
    """

    print('Добро пожаловать в "Калькулятор"')
    print('Для помощи с поиском команд введите "help"')


def help() -> None:
    """
    Выводит список поддерживаемых команд
    :return: Данная функция ничего не возвращает
    """

    print("help - выводит информацию о командах")
    print("infix - переводит калькулятор в режим работы с инфиксными выражениями")
    print("postfix - переводит калькулятор в режим работы с постфиксными выражениями")
    print("let name = value - создаёт/перезаписывает переменную name со значением value")
    print("show_variables - показывает существующие переменные")
    print("abs(a) - вычисляет модуль выражения a")
    print("sqrt(a) - вычисляет корень выражения a")
    print("pow(a, b) - возводит a в степень b")
    print("max(a[, b, ...]) - ищет максимум из чисел")
    print("min(a[, b, ...]) - ищет минимум из чисел")
    print("exit - выход из Калькулятора")

def let(stroka: str, infix: bool):
    """
    Функция объявления переменной
    :param stroka: Строка - введённое пользователем выражение
    :param infix: Логический тип, задающий режим ввода
    :param variables: Словарь, хранящий переменные и их значения
    :return: Данная функция ничего не возвращает
    """

    global variables    #Делаем словарь глобальным

    a = stroka[stroka.find("let")+3:].split("=")      #Создаём список, в который входят название переменной и её значение
    if len(a) != 2:
        print("Ошибка объявления переменной")
    else:
        name_var = a[0].split()
        if len(name_var) == 1:
            if re.fullmatch(r"\s*((abs)|(sqrt)|(pow)|(max)|(min)|(let)|(help)|(infix)|(postfix)|(exit)|(show_variables))\s*", name_var[0]):
                print("Названия функций не могут быть именем переменной")
            elif re.fullmatch(patterns.NAME_PATT, name_var[0]):
                name_var_str = name_var[0]
                #print(a, a[1])
                value = decision.decision(a[1], infix, {})
                if type(value) is str:
                    if value.find("Переменная") != -1:
                        print("Нельзя задавать переменные через переменные")
                    else:
                        print("Ошибка объявления переменной:", value.lower())
                else:
                    variables[name_var_str] = str(value)
                    print(f"Переменная {name_var_str} успешно задана")
            else:
                print("Ошибка ввода имени переменной")
        else:
            print("Ошибка ввода имени переменной")




def main() -> None:
    """
    Главная функция, связывающая все функции и предоставляющая пользовательский интерфейс. Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """
    start()

    working = True      #Переменная работы цикла
    infix = True        #Переменная режима работы калькулятора

    while working:      #Основной цикл
        print()
        cin = input("Введите выражение/команду: ")
        print()

        if cin == "help":       #Вывод списка команд
            help()

        elif cin == "infix":    #Переключение на инфиксную нотацию
            print("Калькулятор переведён в инфиксный режим")
            infix = True

        elif cin == "postfix":  #Переключение на постфиксную нотацию
            print("Калькулятор переведён в постфиксный режим")
            infix = False

        elif re.match(patterns.LET_WORD_PATT, cin):      #Объявление переменной
            if re.fullmatch(patterns.LET_PATT, cin):
                let(cin, infix)  # noqa: F823
            else:
                print("Неправильное объявление переменной")

        elif cin == "show_variables":      #Вывод названий переменных и их значений
            if len(variables) == 0:
                print("Переменные отсутствуют")
            else:
                for i in variables.keys():
                    print(f"{i}: {variables[i]}")

        elif cin == "exit":     #Выход из программы
            working = False

        elif re.search(patterns.BAN_SYMBOLS_PATT, cin):
            print("Вводите только буквы, числа и установленные операторы")
            continue

        else:                   #Попытка решения выражения
            print(decision.decision(cin, infix, variables))

    print("Завершение работы")




if __name__ == "__main__":
    main()
