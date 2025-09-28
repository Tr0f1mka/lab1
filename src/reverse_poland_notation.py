import re

class CalcError(Exception):
    pass

def prior_operator(str_operator: str) -> int:
    """ Функция расстановки приоритетов операторов"""
    match str_operator:
        case "*": return 5
        case "/": return 5
        case "%": return 5
        case "+": return 3
        case "-": return 3
        case _: return

def is_operator(stroka: str) -> bool:
    """является ли символ оператором"""
    for i in ['+', '-', '*', '/', '%']:
        if stroka == i: return True
    return False

isa = isinstance

def to_reverse_poland_notation(stroka: list) -> list:
    """перевод в обратную польскую нотацию"""

    stack = []     #стек операторов
    out_arr = []   #итоговый список
    
    i = 0
    while (i < len(stroka)):
        elem = stroka[i]
        i += 1

        if re.fullmatch("[+-]?[0-9]+([.][0-9]+)?", elem):
            assert (re.fullmatch("[+-]?[0-9]+([.][0-9]+)?", elem) != None)

            out_arr.append(elem)
        elif re.match("[A-Za-z]+", str(elem)):
            assert isa(elem, str)

            out_arr.append(elem)

        elif is_operator(elem):
            is_stack_not_empty = len(stack) > 0

            if is_stack_not_empty:

                no_skobka_on_top = stack[-1] != '('
                is_operator_prior_less_operator_on_tprior_operator = prior_operator(elem) <= prior_operator(stack[-1])

            while (is_stack_not_empty and no_skobka_on_top and is_operator_prior_less_operator_on_tprior_operator):
                """вставляем оператор в стек"""
                out_arr.append(stack.pop())
                is_stack_not_empty = len(stack) > 0

                if is_stack_not_empty:
                    is_stack_not_empty = len(stack) > 0
                    no_skobka_on_top = stack[-1] != '('
                    is_operator_prior_less_operator_on_tprior_operator = prior_operator(elem) <= prior_operator(stack[-1])
            
            stack.append(elem)
        
        elif elem == ')':

            is_stack_not_empty = len(stack) > 0
            while is_stack_not_empty:
                op = stack.pop()
                if op == '(':
                    break
                out_arr.append(op)

                is_stack_not_empty = len(stack) > 0
        elif elem == '(':
            stack.append(elem)
        
    is_stack_not_empty = len(stack) > 0
    while is_stack_not_empty:

        out_arr.append(stack.pop())

        is_stack_not_empty = len(stack) > 0
        
    return out_arr








def test():
    print(to_reverse_poland_notation("1 + 2"))
    print(to_reverse_poland_notation("1 + 12 * 3"))
    print(to_reverse_poland_notation("3 + 3 / -7"))
    print(to_reverse_poland_notation("3 % 33.3 * +8 + 5 + 6"))

test()

#print([x for x in '12  + 45   - 7'.split()])