"""----------------------------
   --------главный файл--------
   ----------------------------
"""



"""---------библиотеки---------"""

import re                        # noqa: E402
import parser                    # noqa: E402
import reverse_poland_notation   # noqa: E402
import calc                      # noqa: E402



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
    print("exit - выход из Калькулятора")


def main() -> None:
    """
    Главная функция. Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """
    start()

    working = True
    infix = True
    while working:
        print()
        cin = input("Введите выражение/команду: ")
        print()
        if cin == "help":
            help()
        elif cin == "infix":
            print("Калькулятор переведён в инфиксный режим")
            infix = True
        elif cin == "postfix":
            print("Калькулятор переведён в постфиксный режим")
            infix = False
        elif cin == "exit":
            working = False
        else:
            if re.search(r"[A-z]+", cin) is not None:
                print("Ошибка ввода. Вводите только цифры, +, -, *, /, %, (, ).")
            else:
                cin = parser.tokens(cin)
                #print(cin)
                if infix:
                    cin = reverse_poland_notation.to_reverse_poland_notation(cin)
                #print(cin)
                if type(cin) is not type("abc"):
                    cin = calc.calc(cin)
                    if len(cin) == 1:
                        print(cin[0])
                    else:
                        print(cin)
                else:
                    print(cin)
    
    print("Good bye")
                

    

if __name__ == "__main__":
    main()
