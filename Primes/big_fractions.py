import fractions

import hugeNumber

def create_fraction(upper: int = 1, lower: int = 1):
    if lower == 0:
        raise ZeroDivisionError(f'{upper} / {lower}', upper=upper, lower=lower)
    return fractions.Fraction(upper, lower)


if __name__ == '__main__':
    import sys
    hugeNumber.huge_number()
    huge_denomitator = sys.maxsize**1000
    try:
        very_close_to_1 = create_fraction(huge_denomitator - 1, huge_denomitator)
        print(very_close_to_1.numerator, "\\", very_close_to_1.denominator, "plus 1 is", sep="\n\n", end=" ")
        #print(very_close_to_1, "plus 1 is", end=" ")
        should_be_1 = very_close_to_1 + create_fraction(1, huge_denomitator)
        assert should_be_1 == 1
        print(should_be_1, ". All good!", sep="")
    except AssertionError as e:
        print("Error: Addition didn't work")
        raise e
