"""---------------------------------------
   --перевод в обратную польскую нотацию--
   ---------------------------------------
"""


"""---------------библиотеки--------------"""

import re  # noqa: E402



"""----------------функции----------------"""

def prior_operator(str_operator: str) -> int:
    """
    Функция расстановки приоритетов операторов
    :param str_operator: Строка, являющаяся оператором
    :return: Число, указывающее приоритет оператора
    """
    
    match str_operator:
        case "**": return 3  # noqa: E701
        case "*": return 2   # noqa: E701
        case "/": return 2   # noqa: E701
        case "//": return 2  # noqa: E701
        case "%": return 2   # noqa: E701
        case "+": return 1   # noqa: E701
        case "-": return 1   # noqa: E701
        case _: return 0     # noqa: E701


def is_operator(symbol: str) -> bool:
    """
    Проверка на оператор
    :param symbol: Строка, являющаяся элементом математического выражения
    :return: Логический тип, определяющий, является ли строка оператором
    """

    for i in ['+', '-', '*', '/', '**', '//', '%']:
        if symbol == i: return True  # noqa: E701
    return False


def to_reverse_poland_notation(stroka: list[str]) -> list[str] | str:
    """
    Перевод в обратную польскую нотацию
    :param stroka: Список строк, являющийся математическим выражением в инфиксной форме
    :return out_arr: Список строк, являющийся математическим выражением в постфиксной(обратной польской) форме
    """

    stack = []     #стек операторов
    out_arr = []   #итоговый список    
    
    for i in range(len(stroka)):
        elem = stroka[i]

        if re.fullmatch("[+-]?[0-9]+([.][0-9]+)?", elem):   #если число, кладём в стек
            out_arr.append(elem)
        
        elif is_operator(elem):                             #если оператор, кладём в соответствующее место в стеке, при необходимости выталкивая операторы из стека в итоговый список
            is_stack_not_empty = len(stack) > 0

            if is_stack_not_empty:    #если стек не пуст, проверяем верх стека на '(' и приоритет текущего и последнего оператора
                no_skobka_on_top = stack[-1] != '('
                is_operator_prior_less_operator_on_top_prior = prior_operator(elem) <= prior_operator(stack[-1])

            while (is_stack_not_empty and no_skobka_on_top and is_operator_prior_less_operator_on_top_prior):       
                #выталкиваем в выход предыдущие операторы
                
                out_arr.append(stack.pop())
                is_stack_not_empty = len(stack) > 0

                if is_stack_not_empty:
                    is_stack_not_empty = len(stack) > 0
                    no_skobka_on_top = stack[-1] != '('
                    is_operator_prior_less_operator_on_top_prior = prior_operator(elem) <= prior_operator(stack[-1])
            
            stack.append(elem)    #кладём текущий элемент в стек
        
        elif elem == ')':                                   #если ')', выталкиваем операторы из стека в итоговый список до '('
            is_stack_not_empty = len(stack) > 0
            while is_stack_not_empty:
                op = stack.pop()
                if op == '(':
                    break
                out_arr.append(op)

                is_stack_not_empty = len(stack) > 0
            
            else:
                return "Недостаточно скобок"
        elif elem == '(':                                   #если '(' кладём в стек
            stack.append(elem)
        
        #print(elem, stack, out_arr)
    
    is_stack_not_empty = len(stack) > 0
    while is_stack_not_empty:
        #если в стеке есть операторы, кладём их в итоговый список
        out_arr.append(stack.pop())

        is_stack_not_empty = len(stack) > 0
    
    if '(' in out_arr:
        return "Недостаточно скобок"
    return out_arr