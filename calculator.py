"""A very simple calculator"""
from numbers import Number

def eval_expression(exp: str):
    safe_chars = (set('0123456789()^+-*/\\')
        .issubset(exp))
    error_msg_chars = ("Error: Unexpected char.\n"
    "Expressions are numbers or"
    " operators: . + - * / ^\n"
    "Parentheses () are OK.")
    assert safe_chars, error_msg_chars
    exp = exp.replace('\\', '/')
    output = eval(exp)
    assert isinstance(output, Number)
    return output



def safe_eval(exp, retry_interactive=False):
    if not retry_interactive:
        return eval_expression(exp)
    while True:
        try:
            return eval_expression(exp)
        except AssertionError as ae:
            print(ae)


if __name__ == '__main__':
    safe_eval('x=2')
valid_chars = set(" (0.123456789)+-**/")
"""while True:
    print("
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
        print("Invalid characters.")"""

