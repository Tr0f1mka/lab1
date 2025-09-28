import re

class CalcError(Exception):
    pass

def prior_operator(str_operator: str) -> int:
    """ Функция расстановки приоритетов операторов"""
    match str_operator:
        case "**": return 3  # noqa: E701
        case "*": return 2  # noqa: E701
        case "/": return 2  # noqa: E701
        case "//": return 2  # noqa: E701
        case "%": return 2  # noqa: E701
        case "+": return 1  # noqa: E701
        case "-": return 1  # noqa: E701
        case _: return 0     # noqa: E701

def is_operator(stroka: str) -> bool:
    """является ли символ оператором"""
    for i in ['+', '-', '*', '/', '**', '//', '%']:
        if stroka == i: return True  # noqa: E701
    return False

def to_reverse_poland_notation(stroka: list[str]) -> list[str]:
    """перевод в обратную польскую нотацию"""

    stack = []     #стек операторов
    out_arr = []   #итоговый список
    
    i = 0
    while (i < len(stroka)):
        elem = stroka[i]
        i += 1

        if re.fullmatch("[+-]?[0-9]+([.][0-9]+)?", elem):
            out_arr.append(elem)
        
        elif is_operator(elem):
            is_stack_not_empty = len(stack) > 0

            if is_stack_not_empty:

                no_skobka_on_top = stack[-1] != '('
                is_operator_prior_less_operator_on_top_prior = prior_operator(elem) <= prior_operator(stack[-1])

            while (is_stack_not_empty and no_skobka_on_top and is_operator_prior_less_operator_on_top_prior):
                """выталкиваем в выход предыдущие операторы"""
                out_arr.append(stack.pop())
                is_stack_not_empty = len(stack) > 0

                if is_stack_not_empty:
                    is_stack_not_empty = len(stack) > 0
                    no_skobka_on_top = stack[-1] != '('
                    is_operator_prior_less_operator_on_top_prior = prior_operator(elem) <= prior_operator(stack[-1])
            
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
        
        #print(elem, stack, out_arr)
    
    is_stack_not_empty = len(stack) > 0
    while is_stack_not_empty:

        out_arr.append(stack.pop())

        is_stack_not_empty = len(stack) > 0
        
    return out_arr




def test():
    print(to_reverse_poland_notation("1 + 2".split()))
    print(to_reverse_poland_notation("1 + 12 * 3".split()))
    print(to_reverse_poland_notation("3 + 3 / -7".split()))
    print(to_reverse_poland_notation("3 % 33.3 * +8 + 5 + 6".split()))
    print(to_reverse_poland_notation("3 % 33.3 * ( +8 + 5 ) * 6".split()))

test()

#print([x for x in '12  + 45   - 7'.split()])