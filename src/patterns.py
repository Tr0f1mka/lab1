"""-------------------------
   ---константы и шаблоны---
   -------------------------"""

"""-------библиотеки--------"""
import re  # noqa: E402



"""---------шаблоны---------"""

NUM = r"\d+(?:\.\d+)?"                                                       #Шаблон числа без знака
SIGNED_NUM = rf"[+\-]?{NUM}"                                                 #Шаблон числа со знаком
SIGNED_AT_START = rf"(?<=^){SIGNED_NUM}"                                     #Шаблон числа с унарным знаком в начале выражения
SIGNED_AFTER_BRACKET = rf"(?<=\(){SIGNED_NUM}"                               #Шаблон числа с унарным знаком после '('
SIGNED_AFTER_OP = rf"(?<=([ + \- * / ( ]\s{0,9999999999})){SIGNED_NUM}"      #Шаблон числа с унарным знаком после оператора или '('
PLAIN_NUMBER    = rf"(?<![\d\)]){NUM}"                                       #Шаблон числа без унарного знака, если перед ним нет другого числа или '('

UNARY_MINUS_AT_START_BEFORE_BRACKET = r"(?<=^)\s*-\s*(?=\()"                 #Шаблон унарного минуса перед скобкой в начале выражения
UNARY_MINUS_AFTER_BRACKET_BEFORE_BRACKET = r"(?<=\()\s*-\s*(?=\()"           #Шаблон унарного минуса перед скобкой после открывающей скобки
UNARY_MINUS = rf"{UNARY_MINUS_AT_START_BEFORE_BRACKET}|{UNARY_MINUS_AFTER_BRACKET_BEFORE_BRACKET}"  #объединение предыдущих двух шаблонов

UNARY_PLUS_AT_START_BEFORE_BRACKET = r"(?<=^)\s*\+\s*(?=\()"                 #Шаблон унарного плюса перед скобкой в начале выражения
UNARY_PLUS_AFTER_BRACKET_BEFORE_BRACKET = r"(?<=\()\s*\+\s*(?=\()"           #Шаблон унарного плюса перед скобкой после открывающей скобки
UNARY_PLUS = rf"{UNARY_PLUS_AT_START_BEFORE_BRACKET}|{UNARY_PLUS_AFTER_BRACKET_BEFORE_BRACKET}"     #объединение предыдущих двух шаблонов

BAN_SYMBOLS_PATT = r"[^\w+\-*/~%$\(\)\.,\=\s]"     #Шаблон запрещённых символов

NAME_PATT = r"[A-Za-z_]\w*"      #Шаблон имени переменной
LET_WORD_PATT = r"\s*let\s+"
LET_PATT = rf"\s*let\s+{NAME_PATT}\s*=\s*.+"    #Шаблон объявления переменной

#Шаблон для пасинга строки
PATTERN = rf"""\s*(
  {SIGNED_AT_START}      |
  {SIGNED_AFTER_BRACKET} |
  {SIGNED_AFTER_OP}      |
  \*\*                   |
  //                     |
  [%()+\-*/~$,]          |
  {PLAIN_NUMBER}         |
  {NAME_PATT}
)
"""

TOKEN_RE = re.compile(PATTERN, re.VERBOSE)
