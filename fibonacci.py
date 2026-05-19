import math
from typing import Generator


def fib_factory(a: float, b: float) -> Generator[float, None, None]:
    """Calculates the Fibonacci numbers concretely.
    This will become incorrect after a while.
    Computers round when they calculate with noninteger numbers."""
    golden_ratio = (1+math.sqrt(5))/2
    golden_conjugate = (1-math.sqrt(5))/2
    def fib_ish_generator() -> Generator[float, None, None]:
        n = 0
        while True:
            yield a*golden_ratio**n + b*golden_conjugate**n
            n += 1
            if n > 71:
                break
        return None

    return fib_ish_generator()

def main2() -> None:
    _fibgen = fibonacci_generator()
    '''Fixed form:
    
    approximate = True
    else:
        _fibgen = '''
    approximate = False
    if input("Estimate via fixed form? ").lower()[:1] == "y":
        _fibgen = fib_factory(1/(5**(1/2)), -1/(5**(1/2)))
        approximate = True
        print("Warning: Computers approximate when they work with the golden ratio!",
              "Every guess after the 70th approximate Fibonacci number is wrong.",
              sep='\n', end=' ')

    print("How many Fibonacci numbers do you want after the 0th one?")
    wantedlength = int(input())
    print("Calculated Fibonacci sequence:")
    length = 0
    while length < wantedlength+1:
        one_fib_num = next(_fibgen)
        if approximate:
            print("Approximate", end=' ')
        print(f"Fibonacci number {length}:", one_fib_num)
        length += 1

def fibonacci_generator():
    """Warning: Infinite Fibonacci sequence generator function!"""
    a = 0
    b = 1
    temp = a

    yield a; yield b
    while True:
        temp = a
        a = b
        b = temp + b
        yield b


if __name__ == "__main__":
    main2()
