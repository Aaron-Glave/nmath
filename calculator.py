"""A very simple calculator"""
from numbers import Number

def eval_expression(exp: str):
    """Evaluate a mathematical expression.
    Arguments:
        exp: str for a mathematical expression
    Potential exceptions:
        AssertionError if exp is not a mathematical expression
        SyntaxError if exp is an invalid mathematical expression"""
    safe_chars = (set('0123456789()^+-*/\\')
        .issubset(exp))
    error_msg_chars = (f"Error: {exp} contains invalid chars.\n"
    "Expressions are numbers 0-9 or"
    " operators like . + - * / \\ ^\n"
    "Parentheses () are OK.")
    assert safe_chars, error_msg_chars
    exp = exp.replace('\\', '/').replace('^', '**')
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


if __name__ == '__main__':
    try:
        safe_eval('x=2')
    except AssertionError as ae:
        print(ae)
