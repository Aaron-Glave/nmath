#NOTE: Every line in this file is an integer referring to which prime number is listed,
# followed by a space, followed by a prime number, followed by a newline character.
from typing import Optional

#Set this to False on your phone!
SHOULD_WRITE = True
SPRIMELIST = "sprimelist.txt"
ALL_PRIMES_UNDER_100 = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
    53, 59, 61, 67, 71, 73,
    79, 83, 89, 97
]

def under_or_at_limit(_current_guess: int, upto: Optional[int]) -> bool:
    """Used internally to return True if upto is null OR _current_guess <= upto"""
    if upto is None:
        return True
    return _current_guess <= upto
