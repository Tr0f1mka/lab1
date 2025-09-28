
"""------------------------------------
   --парсер арифметического выражения--
   ------------------------------------"""



"""-------------библиотеки-------------"""

import re




"""--------------паттерны---------------"""

NUM = r"\d+(?:\.\d+)?"
SIGNED_AT_START = rf"(?<=^) [+\-]?{NUM}"
SIGNED_AFTER_OP = rf"(?<=[ + \- * / ( ]) [+\-]?{NUM}"
PLAIN_NUMBER    = rf"(?<![\d\)]) {NUM}"

pattern = rf"""\s*(
  {SIGNED_AT_START}   |
  {SIGNED_AFTER_OP}   |
  \*\*              |
  //                  |
  [%()+\-*/]         |
  {PLAIN_NUMBER}
)
"""

TOKEN_RE = re.compile(pattern, re.VERBOSE)

def demo_tokens(s: str) -> list[str]:
    return [m.group(1) for m in TOKEN_RE.finditer(s)]

tests = [
    "-5+2*3",
    "+7- -2*3",
    "( -2 + 3 ) * 4",
    "2**3**2",
    "7//3 + 7%3",
    "12 / -3 * (+2)",
]
for t in tests:
    print(t, "=>", *demo_tokens(t))