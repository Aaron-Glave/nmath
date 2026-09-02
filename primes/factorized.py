import warnings
from typing import Tuple, Callable, Generator

from .main import correct_prime_guess


class Factorized:
    """Factors an integer and displays the factors"""

    @staticmethod
    def reduce(number: int, divisor: int) -> Tuple[int, int]:
        """Returns (a, n) where number == a*(divisor ^ n) and a is not divisible by the divisor.
        Basically factors out the divisor raised to the highest possible power."""
        n = 0
        while number % divisor == 0:
            n += 1
            number //= divisor
        return number, n

#
    def __init__(self, to_factor: int,
                 method: Callable[...,
                 Generator[tuple[int, int], None, None]] = correct_prime_guess) -> None:
        """Factorizes the passed integer using a Callable[
            [int], Generator[tuple[int, int], None, None]
        ] to factor it. The default factorization method is """
        self._factors: list[tuple[int, int]] = []
        self.factor_failure = None
        prime_source = method(list_all=True)
        if to_factor < 0:
            self._factors.append((-1, 1))
            to_factor *= -1
        elif to_factor == 0:
            self._factors = [(0, 1)]
        elif to_factor == 1:
            self._factors = [(1, 1)]
        done_factoring = False
        while to_factor > 1 and not done_factoring:
            for _, prime in prime_source:
                if to_factor % prime == 0:
                    to_factor, number_of_divisions = Factorized.reduce(to_factor, prime)
                    self._factors.append((prime, number_of_divisions))
                    if to_factor == 1:
                        done_factoring = True
                    break
        if to_factor > 1:
            self.factor_failure = (f"I couldn't find a factor for ${to_factor}.\n"
                                   "It might be divisible by prime numbers I haven't discovered.")
            warnings.warn(self.factor_failure, UserWarning)

    def __str__(self) -> str:
        """Represents the factors of an integer nicely in a string."""
        factor_count = 0
        strs_to_list = []
        ending = " * "
        for factor in self._factors:
            factor_count += 1
            if factor_count == len(self._factors):
                ending = ""
            strs_to_list.append(f"{factor[0]} ^ {factor[1]}{ending}")
        return "".join(strs_to_list)

    @property
    def factors(self) -> list[tuple[int, int]]:
        return self._factors
