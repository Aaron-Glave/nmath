"""Constants used in a couple different files,
    both on the phone and the PC."""
from typing import Optional

#Set this to False on your phone!
SHOULD_WRITE = True
#This tuple has to be in strictly increasing order.
ALL_PRIMES_UNDER_100: tuple[int, ...] = (
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
    53, 59, 61, 67, 71, 73,
    79, 83, 89, 97
)

def under_or_at_limit(_current_guess: int, upto: Optional[int]) -> bool:
    """Used internally to return True if upto is null OR _current_guess <= upto
    If upto is None, imagine you're looking for a number greater than ∞.
        You'll never reach your limit"""
    if upto is None:
        return True
    return _current_guess <= upto


def desc_prime_with_index(np: tuple[int, int]) -> str:
    return f"{np[0]}th prime: {np[1]}"
