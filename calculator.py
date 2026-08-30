"""A very simple calculator"""
from numbers import Number

def eval_expression(exp: str):
    """Evaluate a mathematical expression.
    Arguments:
        exp: str for a mathematical expression
    Potential exceptions:
        AssertionError if exp is not a mathematical expression
        SyntaxError if exp is an invalid mathematical expression"""
    exp = (exp.replace('\\', '/').replace('^', '**')
           .replace('\t', '').replace(' ', ''))

    safe_chars = set('0123456789()^+-*/\\ \t')
    is_safe = set(exp).issubset(safe_chars)
    error_msg_chars = (f"Error: {exp} contains invalid chars.\n"
    "Expressions are numbers 0-9 or"
    " operators like . + - * / \\ ^\n"
    "Parentheses () are OK.")
    assert is_safe, error_msg_chars
    try:
        # pylint:disable=eval-used
        # We know exp can only be a (possibly invalid) mathematical expression.
        output = eval(exp)
        # pylint:enable=eval-used
    except SyntaxError as se:
        se.add_note(f"{exp} is an invalid mathematical expression.")
        raise se
    assert isinstance(output, Number)
    return output



def safe_eval(exp: str):
    """Evaluates the string exp,
    looping with user input until the expression is valid."""
    while True:
        try:
            return eval_expression(exp)
        except AssertionError as ae:
            print(ae)
            exp = input("Please enter a valid mathematical expression: ")


if __name__ == '__main__':
    x = input("Please enter a valid mathematical expression: ")
    print(safe_eval(x))
