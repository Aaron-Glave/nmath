"""A very simple calculator"""


valid_chars = set(" (0.123456789)+-**/")
while True:
    print("Expressions are numbers or"
    " operators: . + - * / ^",
    "Parentheses () are OK.",
    sep="\n")
    expression = input("Expression: ").replace("^", "**")
    if set(expression) <= valid_chars:
        try:
            #pylint:disable=W0123
            print("Result:", eval(expression))
            #pylint:enable=W0123
        except SyntaxError:
            print("Invalid expression")
    else:
        print("Invalid characters.")
