


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
    for i in "+-*/%":
        if stroka == i: return True
    return False

