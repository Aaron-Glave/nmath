"""Helps you calculate weird fractions manually."""


def print_digits_of_divisions(divisor: int, base: int = 10) -> list[int]:
    """Prints and returns the single digit multiples of the passed base.
    Optional arguments: base: int -> The base of your digit system. The default is 10."""
    multiplications: list[int] = []
    print(f"Base {base} multiples of {divisor}:", end=":\n")
    for i in range(0, base + 1):
        multiplications.append(divisor * i)
        if i < base:
            print(i, multiplications[i], sep=": ")
        else:
            print(f"{base} times {divisor} is {multiplications[i]}.")
    return multiplications


if __name__ == '__main__':
    _divisor = int(input("What divisor do you want to know the 1-digit multiples of? "))
    print_digits_of_divisions(_divisor)
    print_digits_of_divisions(_divisor, 16)
