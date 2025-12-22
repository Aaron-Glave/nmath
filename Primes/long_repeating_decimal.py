"""Translates fractions into repeating decimals."""
from fractions import Fraction
from typing import Optional, List, Tuple
import sys
from pathlib import Path
path_to_add = Path(__file__).resolve().parent
print(path_to_add)
sys.path.append(str(Path(__file__).parent.resolve()))
import hugeNumber
sys.path.pop()

hugeNumber.huge_number()


#pylint:disable=C0301
#Look at https://math.stackexchange.com/questions/2845984/how-to-calculate-a-repeating-decimal-for-any-fraction
#pylint:enable=C0301
#pylint:disable=R0902
class DecimalDigit:
    """Represent a single digit of a long decimal number"""
    digit: int = 0
    remainder: int = 0

    def __init__(self, digit: int, remainder: int):
        self.digit = digit
        self.remainder = remainder

    def __str__(self):
        return str(self.digit)

    def set_to(self, other: 'DecimalDigit'):
        """Copies the exact state of another DecimalDigit."""
        self.digit = other.digit
        self.remainder = other.remainder


#pylint:enable=R0903


class DecimalRepresentationOfFrac:
    """Represents a fraction of 2 Integers,
    and prints them as a decimal representation, possibly repeating.
    NOTE that negative fractions are represented by positive fractions with is_negative=True."""

    @staticmethod
    def assert_non_zero_divisor(divisor: int) -> None:
        """Asserts that the divisor is legal (non-zero)."""
        if divisor == 0:
            raise ZeroDivisionError()

    def reset_and_recalculate(self):
        """Mainly a helper """
        self.head: int = 0
        self.finite: bool = False
        self.negative: bool = False
        self.start_repeat: Optional[int] = None
        self.end_repeat: Optional[int] = None
        self.digits: List[DecimalDigit] = []
        self._compute()

    def __init__(self, upper: int = 1, lower: int = 1):
        self._original_upper = upper
        self._original_lower = lower
        self.upper: int = upper
        self.assert_non_zero_divisor(lower)
        self.lower: int = lower
        self.head: int = 0
        self.finite: bool = False
        self.start_repeat: Optional[int] = None
        self.end_repeat: Optional[int] = None
        self.digits: List[DecimalDigit] = []
        self.negative = False
        self._compute()

    def __repr__(self):
        return ("DecimalRepresentationOfFrac(" +
                str(self._original_upper) + ", " +
                str(self._original_lower) + ")")

    def __str__(self):
        """Represents the fraction upper/lower as a repeating decimal."""
        mystring = "-" if self.negative else ""
        mystring += self.head.__str__()
        repeating = False
        if len(self.digits) != 0:
            mystring += "."
            #Special case for repeating single digits?
            if self.start_repeat is not None:
                ##CHECK this:
                # 1. Your second repeating digit's index is 1 after the first repeating digit's index
                # 2. They each represent the same digit
                if self.end_repeat - self.start_repeat == 1:
                    if self.digits[self.end_repeat].digit == self.digits[self.start_repeat].digit:
                        #We already know we're repeating!
                        repeating = True
            dindex: int = 0
            for digit in self.digits:
                if dindex == self.start_repeat and not self.finite:
                    mystring += "_"
                    if repeating:
                        mystring += digit.__str__() + "_"
                        return mystring
                mystring += digit.__str__()
                dindex += 1
            if not self.finite:
                mystring += "_"
        return mystring

    def change_upper(self, new_upper: int):
        """Update the top of the fraction representation."""
        self.upper = new_upper
        self._original_upper = new_upper
        self.reset_and_recalculate()

    def change_lower(self, new_lower: int):
        """Update the bottom of the fraction representation."""
        DecimalRepresentationOfFrac.assert_non_zero_divisor(new_lower)
        self.assert_non_zero_divisor(new_lower)
        self.lower = new_lower
        self._original_lower = new_lower
        self.reset_and_recalculate()

    def swap_sign(self) -> None:
        """Invert the sign of the fraction (a/b <-> -a/b)"""
        self._original_upper = -self._original_upper
        self.upper = self._original_upper
        self.reset_and_recalculate()

    def is_negative(self) -> bool:
        """Read-only function to check if the fraction is negative."""
        return self.negative

    def repeating_string_start_and_end(self) -> Tuple[int, int]:
        """Returns (starting point of repeating string, ending point).
        Starting point is the number after the _ character,
        and ending point is the second _.
        Returns (-1, -1) if the digits don't repeat!"""
        myname = str(self)
        if self.start_repeat is not None:
            namechar = 0
            while myname[namechar] != "_":
                namechar += 1
            namechar += 1
            realstart = namechar
            namechar += 1
            while myname[namechar] != "_":
                namechar += 1
            return realstart, namechar
        return -1, -1

    def repeating_string(self) -> str:
        """Returns a string containing only the repeating digits, in order."""
        result = self.repeating_string_start_and_end()
        myname = str(self)
        #Remember, repeating_string_start_and_end() returns (-1, -1)...
        # ..iff the digit string is finite.
        if result[0] == -1:
            return ""
        return myname[result[0]:result[1]]

    def longer_repeating(self, other):
        """Returns True a DecimalRepresentationOfFrac has more repeating characters
        than the argument passed, and False otherwise."""
        assert isinstance(other, DecimalRepresentationOfFrac)
        mystring = self.repeating_string()
        theirstring = other.repeating_string()
        if len(mystring) < len(theirstring):
            return False
        if len(mystring) > len(theirstring):
            return True
        return (self.upper / self.lower) < (other.upper / self.lower)

    def __eq__(self, other):
        if isinstance(other, DecimalRepresentationOfFrac):
            return ((Fraction(self.upper, self.lower) == Fraction(other.upper, other.lower))
                    and self.negative == other.negative)
        return False

    def _compute(self):
        if self.lower < 0:
            self.lower = -self.lower
            self.upper = -self.upper
        if self.upper < 0:
            self.negative = True
            #Mark that the fraction is negative, then imagine it was positive.
            #This simplifies the decimal calculation process.
            self.upper = -self.upper

        # NOTE: upper and lower will always be positive when you get to these steps.
        self.head = self.upper // self.lower
        remainder = self.upper - (self.head * self.lower)
        done = remainder == 0
        index: int = 0
        remainders = {}  #Maps remainders to indexes.
        while not done:
            #Check whether or not I've already seen this divisor BEFORE I find out what's next.
            starting_remainder = remainder
            if starting_remainder in remainders:
                self.start_repeat = remainders[remainder]

            whats_left = remainder * 10
            next_digit = 0
            while whats_left >= self.lower:
                next_digit += 1
                whats_left -= self.lower
            remainder = whats_left
            if whats_left not in remainders:
                remainders[starting_remainder] = index
            else:
                self.start_repeat = remainders[whats_left]
                self.end_repeat = index
                if next_digit == 0:
                    self.finite = True
                self.digits.append(DecimalDigit(
                    next_digit, remainder
                ))
                done = True
            if not done:
                created_digit = DecimalDigit(
                    digit=next_digit, remainder=whats_left
                )
                if whats_left == 0:
                    self.finite = True
                    done = True
                else:
                    index += 1
                    remainder = whats_left
                self.digits.append(created_digit)


if __name__ == "__main__":
    _HEADFRAC = 330 + 29
    _TAILFRAC = 33000
    _FRACTEST = DecimalRepresentationOfFrac(_HEADFRAC, _TAILFRAC)
    print(_HEADFRAC, " / ", _TAILFRAC, ": ", _FRACTEST, sep='')
    print("Repeating chars:", _FRACTEST.repeating_string())
    inttest = DecimalRepresentationOfFrac(9, 3)
    print("9 / 3:", inttest)
    finitedecimal: DecimalRepresentationOfFrac = (
        DecimalRepresentationOfFrac(9000 + 31 * 90, 90 * 100)
    )
    print(finitedecimal.upper, " / ", finitedecimal.lower, ": ", finitedecimal, sep="")
    third = DecimalRepresentationOfFrac(1, 3)
    print(third.upper, " / ", third.lower, ": ", third, sep="")

    print("Repeating chars in 1/3:", third.repeating_string())
    seventies = DecimalRepresentationOfFrac(1 + 3 * 7, 70)
    print("22 / 70 (which is 11 / 35):", seventies,
          "\nRepeating chars:", seventies.repeating_string())
    #pylint:disable=C0301
    #Credit: https://goodcalculators.com/repeating-decimal-to-fraction-conversion-calculator/ .1881 repeating
    #pylint:enable=C0301
    foundfrac = DecimalRepresentationOfFrac(19, 101)
    print("19 / 101:", foundfrac)
    assert str(foundfrac) == "0._1881_"
    assert (DecimalRepresentationOfFrac(1881, 9999)
            == DecimalRepresentationOfFrac(19, 101))
    proof_zero = DecimalRepresentationOfFrac(0, 13)
    print(repr(proof_zero), proof_zero, sep=": ")
    third = DecimalRepresentationOfFrac(1, 3)
    print(third, "SHOULD only have 1 repeating digit.")
    twodigit_one_repeat = DecimalRepresentationOfFrac(111, 999)
    print("Big representation of 1/9th:\n", repr(twodigit_one_repeat) + ":", twodigit_one_repeat)
    sevendy_eight = DecimalRepresentationOfFrac(78, 99)
    assert str(sevendy_eight) == "0._78_"
    longstring = DecimalRepresentationOfFrac(1881, 9999)
    print(longstring.upper, "/", str(longstring.lower) + ":", longstring)
    assert (DecimalRepresentationOfFrac(9, 3) == DecimalRepresentationOfFrac(3, 1)) and (
            DecimalRepresentationOfFrac(9, 3) != DecimalRepresentationOfFrac(4, 2))

    onesevenfive = DecimalRepresentationOfFrac(1, 75)
    print(repr(onesevenfive), str(onesevenfive), sep=": ")
    bigrepeat = DecimalRepresentationOfFrac(3133, 9999)
    print(repr(bigrepeat), str(bigrepeat), sep=": ")
    smallerrepeat = DecimalRepresentationOfFrac(525, 999)
    assert smallerrepeat == DecimalRepresentationOfFrac(175, 333)
    assert str(smallerrepeat) == "0._525_"
    print(repr(smallerrepeat), str(smallerrepeat), sep=": ")

    print("\n\nTesting changing the upper and lower parts of the fraction:")
    print("First, let's make sure that dividing by 0 is NOT allowed.")
    caught_error = False
    try:
        seventy_one = DecimalRepresentationOfFrac(71, 0)
    except ZeroDivisionError:
        caught_error = True
    assert caught_error is True
    caught_error = False
    try:
        bigrepeat.change_lower(0)
    except ZeroDivisionError:
        caught_error = True
    assert caught_error is True
    print("Yeah, it's not allowed. Good.")
    #Now we change the fraction legitimately.
    print("Changed 3133/9999 to 9999/9999:")
    bigrepeat.change_upper(9999)
    print(repr(bigrepeat), str(bigrepeat), sep=": ")
    print("Changed 9999/9999 to 9999/1:")
    bigrepeat.change_lower(1)
    print(repr(bigrepeat), str(bigrepeat), sep=": ")
    print("Now let's try making it an infinitely repeating decimal.")
    bigrepeat.change_lower(7)
    print(repr(bigrepeat), str(bigrepeat), sep=": ")
    negative_frac = DecimalRepresentationOfFrac(8, -7)
    print(repr(negative_frac), str(negative_frac), sep=": ")
    print("Integer part of 8/-7:", negative_frac.head)
    assert negative_frac == DecimalRepresentationOfFrac(8, -7)
    print("Fractions look alright.")
