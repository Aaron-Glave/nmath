"""Helps you calculate weird fractions manually."""


def print_digits_of_divisions(divisor: int, base: int = 10) -> list[int]:
    """Prints and returns the single digit multiples of the passed base.
    Optional arguments: base: int -> The base of your digit system. The default is 10."""
    multiplications: list[int] = []
    print(f"Base {base} multiples of {divisor}:")
    for i in range(1, base + 1):
        multiplications.append(divisor * i)
        print(i, multiplications[-1], sep=": ")
    return multiplications


if __name__ == '__main__':
    _divisor = int(input("What divisor do you want to know the 1-digit multiples of? "))
    print_digits_of_divisions(_divisor)
    print_digits_of_divisions(_divisor, 16)
