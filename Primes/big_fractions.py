"""Basically a test to verify Python's fractions work well mathematically."""

from fractions import Fraction
import sys

import hugeNumber


def create_fraction(upper: int = 1, lower: int = 1):
    """Create a fraction. This function requires the lowercase argument not to be 0"""
    if lower == 0:
        raise ZeroDivisionError(f'{upper} / {lower}')
    return Fraction(upper, lower)


def mixed_fraction(unsimple_fraction: Fraction) -> str:
    """Writes a huge fraction as an integer plus a fraction whose absolute value is less than 1."""
    if unsimple_fraction == 0:
        return "0"
    numerator = abs(unsimple_fraction.numerator)
    denominator = abs(unsimple_fraction.denominator)
    abs_fraction = divmod(
        numerator, denominator
    )
    str_to_return = ""
    if unsimple_fraction < 0:
        str_to_return += "-"
    if abs_fraction[0] != 0:
        str_to_return += f"{abs_fraction[0]}"
    fraction_part = ""
    if abs_fraction[1] != 0:
        fraction_part = f"{abs_fraction[1]}/{denominator}"
    if abs_fraction[0] != 0 and abs_fraction[1] != 0:
        str_to_return += f" {fraction_part}"
    elif abs_fraction[1] != 0:
        str_to_return += f"{fraction_part}"
    return str_to_return


# noinspection unreachable-code
def test_huge_number() -> None:
    """Verifies that hugeNumber works as expected, and that fractions work as expected."""
    hugeNumber.huge_number()
    huge_denomitator = sys.maxsize ** 1000
    try:
        very_close_to_1 = create_fraction(huge_denomitator - 1, huge_denomitator)
        print(very_close_to_1.numerator, "\\", very_close_to_1.denominator, "plus 1 is",
              sep="\n", end=" ")
        #print(very_close_to_1, "plus 1 is", end=" ")
        should_be_1 = very_close_to_1 + create_fraction(1, huge_denomitator)
        assert should_be_1 == 1
        print(should_be_1, ". All good!", sep="")
        should_be_bigger = very_close_to_1 + create_fraction(2, huge_denomitator)
        assert should_be_bigger > 1
    except AssertionError as e:
        print("Error: Addition didn't work")
        raise e


if __name__ == '__main__':
    print("10/3:", mixed_fraction(create_fraction(10, 3)))
    print("-10/3:", mixed_fraction(create_fraction(-10, 3)))
    print("2/3:", mixed_fraction(create_fraction(2, 3)))
    print("-2/3:", mixed_fraction(create_fraction(-2, 3)))
    print("0:", mixed_fraction(create_fraction(0, 3)))
    if input("Do you want to test your hugeNumber import? [Yes/No]: ").lower() == "yes":
        test_huge_number()
