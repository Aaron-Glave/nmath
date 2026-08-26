"""Program designed to talk about prime numbers."""
import sys
from io import TextIOWrapper
from typing import Tuple, Generator
import warnings

from phone_banned import PhoneBanned
from shared_ph_pc import *

sys.set_int_max_str_digits(100000)
if SHOULD_WRITE:
    try:
        from cpu_write import yield_and_write_primes, cpu_factors, close_db
    except ModuleNotFoundError as me:
        raise me
else:
    def yield_and_write_primes(upto: Optional[int] = None, *,
                               save_to: Optional[TextIOWrapper] = None,
                               list_all: bool = False,
                               first_greater: bool = False,
                               target_n: Optional[int] = None,
                               comments: Optional[dict[str, str]]):
        raise PhoneBanned()


    def close_db():
        pass


#We don't even have a function to read the whole file into a list.
# That would use a TON of memory.
def yield_primes_memory(upto: Optional[int] = None, print_specific: Optional[int] = None,
                        first_greater: bool = False) -> Generator[tuple[int, int], None, None]:
    """Returns list of tuples [(1-based prime index, prime number)].
        Note that all known primes are created in memory,
          so the list is r-created for every iterator you create."""
    memory_list = ALL_PRIMES_UNDER_100.copy()
    found_first_greater = False
    nth_prime = 1
    for prime in memory_list:
        yield nth_prime, prime
        nth_prime += 1
    guess = 101
    calculate_more = True
    if upto is not None:
        if upto < guess:
            calculate_more = False
    while calculate_more:
        isprime = True
        for prime in memory_list:
            if guess % prime == 0:
                isprime = False
                break
            #Use the Sieve of Eratosthenes!
            if prime * prime > guess:
                isprime = True
                break
        if isprime:
            if print_specific == nth_prime:
                print(str(nth_prime) + " prime is", guess)
            memory_list.append(guess)
            if len(memory_list) % 10000 == 0 and print_specific is not None:
                print(len(memory_list), "th prime is ", guess, sep='')
            yield nth_prime, guess
            if first_greater and not under_or_at_limit(nth_prime, upto):
                found_first_greater = True
            #Only increment the nth_prime value AFTER printing the current nth_prime.
            nth_prime += 1
        if (not under_or_at_limit(guess, upto) and not found_first_greater and
                (not first_greater or memory_list[-1] >= guess)):
            return
        guess += 2


#pylint:disable=R0913
def correct_prime_guess(upto: Optional[int] = None, *,
                        list_all: bool = False,
                        first_greater: bool = False,
                        target_n: Optional[int] = None,
                        comments: Optional[dict[str, str]] = None) -> Generator[
    tuple[int, int], None, None]:
    """If you're using a phone (SHOULD_WRITE is False),
    we look for primes using nothing but memory.
    Else, we use our "sprimelist.txt" file."""
    if SHOULD_WRITE:
        yield from yield_and_write_primes(
            upto=upto,
            list_all=list_all,
            first_greater=first_greater,
            target_n=target_n,
            comments=comments
        )
    else:
        yield from yield_primes_memory(
            upto=upto,
            first_greater=first_greater,
        )


#pylint:enable=R0913


def get_last_prime() -> Tuple[int, int]:
    """Returns the biggest prime number in the list.
    It's a tuple: (nth_prime, prime)"""
    biggest_prime = (len(ALL_PRIMES_UNDER_100), ALL_PRIMES_UNDER_100[-1])
    if SHOULD_WRITE:
        try:
            with open(SPRIMELIST, encoding='ascii') as sprimelist:
                for line in sprimelist:
                    parsed_line = tuple(map(int, line.strip('\n').split(" ")))
                    biggest_prime: tuple[int, int] = (parsed_line[0], parsed_line[1])

        except FileNotFoundError:
            pass
    return biggest_prime


def primes_up_to100():
    """Creates a primes.txt file with the first 100 primes."""
    maximum = 100
    primes = []
    try:
        prime_source = open("primes.txt", mode="r", encoding='ascii')
    except FileNotFoundError:
        print("Creating list...")
        prime_source = open("primes.txt", mode="x", encoding='ascii')
        prime_source.close()
        prime_source = open("primes.txt", mode="r", encoding='ascii')
        print("File listing primes was created")
    for line in prime_source:
        try:
            primes.append(int(line))
        except ValueError:
            pass
    try:
        start = max(primes)
        print("Max prime I know is", start)
    except ValueError:
        print("List is empty.")
        start = 2
    prime_source.close()
    prime_source = open("primes.txt", mode='a', encoding='ascii')

    for i in range(start, maximum + 1):
        isprime = True
        for prime in primes:
            if i % prime == 0:
                isprime = False
                break
        if isprime:
            primes.append(i)
            print(i, "is prime.")
            prime_source.write(str(i) + '\n')
    prime_source.close()
    print("Calculated primes <= ", maximum, ": ", primes, sep="")


def gen_primes_up_to(max_prime=2):
    """Returns a list of primes up to max_prime."""
    return list(correct_prime_guess(max_prime, list_all=True))


def memory_factor_list(to_factor: int) -> Generator[int, None, None]:
    """Returns a correct list of factors of the number to_factor,
    using memory only."""
    for mprime in yield_primes_memory(to_factor):
        yield mprime[1]


def percent_integers_unknown_factors():
    """Returns the percentage chance that a number isn't divisible by any of our known primes."""
    probability = 1
    for prime in ALL_PRIMES_UNDER_100:
        probability *= 1 - (1 / prime)
    if SHOULD_WRITE:
        with open(SPRIMELIST, mode='r', encoding='ascii') as sprimelist:
            for line in sprimelist:
                prime = int(line.strip('\n').split(' ')[1])
                probability *= 1 - (1 / prime)
    return probability


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

    def __init__(self, to_factor: int) -> None:
        """Factorizes the passed integer using a Callable[
            [int], Generator[tuple[int, int], None, None]
        ] to factor it. The default factorization method is """
        self._factors: list[tuple[int, int]] = []
        self.factor_failure = None
        prime_source = correct_prime_guess(list_all=True)
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


def say_gap_message(gap_to_print: Tuple[Tuple[Tuple[int, int], Tuple[int, int]], int]):
    """Prints info about the gap passed
    Organization: (
        (previous_prime_tuple, next_prime_tuple),
        next_prime_tuple[1] - previous_prime_tuple[1]
    )
        Each prime_tuple: (
            index of the prime number starting at 1 and increasing by 1 for each prime,
            the prime number itself
        )."""
    print("Found a gap between the", end=" ")
    print(gap_to_print[0][1][0], "th prime and the ", gap_to_print[0][0][0], "th prime:\n",
          gap_to_print[0][1][1], "-", gap_to_print[0][0][1], "=", gap_to_print[1],
          sep='', end=".\n")


def largest_gap_of_primes() -> Tuple[Tuple[Tuple[int, int], Tuple[int, int]], int]:
    """Prints and returns the largest gap between adjacent prime numbers we know,
    returning the first 2 prime numbers which are that far apart, as well as the size of the gap.
    Note that the gap this function finds CAN repeat;
    I just return a reference to the first time I find that gap."""
    previous_prime = (1, ALL_PRIMES_UNDER_100[0])
    next_prime = previous_prime
    current_greatest_gap: Tuple[Tuple[
        Tuple[int, int], Tuple[int, int]
    ], int] = (((1, 2), (1, 2)), 0)

    for i in range(1, len(ALL_PRIMES_UNDER_100)):
        next_prime = (i + 1, ALL_PRIMES_UNDER_100[i])
        gap = next_prime[1] - previous_prime[1]
        if gap > current_greatest_gap[1]:
            current_greatest_gap = ((previous_prime, next_prime), next_prime[1] - previous_prime[1])

        previous_prime = next_prime

    if SHOULD_WRITE:
        nth_prime = 2
        primelist = open(SPRIMELIST, mode="r", encoding='ascii')
        first_line = tuple(map(int, primelist.readline().strip('\n').split(' ')))
        previous_prime: tuple[int, int] = (first_line[0], first_line[1])
        assert isinstance(previous_prime, tuple) and len(previous_prime) == 2
        for line in primelist:
            nth_prime, prime = map(int, line.strip('\n').split(' '))
            next_prime = (nth_prime, prime)
            gap = next_prime[1] - previous_prime[1]
            if gap > current_greatest_gap[1]:
                current_greatest_gap = ((previous_prime, next_prime),
                                        next_prime[1] - previous_prime[1])
            previous_prime = next_prime
    assert isinstance(current_greatest_gap, tuple) and len(
        current_greatest_gap) == 2 and isinstance(current_greatest_gap[1], int)
    return current_greatest_gap


def say_gap_of_100():
    """We know there's a gap of 100 primes at some point,
    but it's not in the strictly increasing list of gaps."""
    found_gap_100: Tuple[Tuple[Tuple[int, int], Tuple[int, int]], int] = (
        ((-1, -1), (-1, -1)), 0)

    if SHOULD_WRITE:
        nth_prime = -1
        primelist = open(SPRIMELIST, mode="r", encoding='ascii')
        first_line = tuple(map(int, primelist.readline().strip('\n').split(' ')))
        previous_prime = (first_line[0], first_line[1])
        for line in primelist:
            parsed_line = tuple(map(int, line.strip('\n').split(' ')))
            nth_prime, prime = (parsed_line[0], parsed_line[1])
            next_prime = (nth_prime, prime)
            gap = next_prime[1] - previous_prime[1]
            if gap == 100:
                found_gap_100 = ((previous_prime, next_prime),
                                 next_prime[1] - previous_prime[1])
                say_gap_message(found_gap_100)
                return found_gap_100
            previous_prime = next_prime
    print("Either you're using your phone or you don't know enough primes.")
    return found_gap_100


def get_int() -> int:
    """Get an integer from the user."""
    inputted = False
    target = 0
    while not inputted:
        try:
            target = int(input("N: "))
            inputted = True
        except ValueError:
            print("Invalid number.")
    return target


def print_next_prime_greater(target: int) -> tuple[int, int]:
    """Interactive. Method to determine a prime number greater than the input."""
    # This is an infinite loop of increasing numbers.
    # noinspection inconsistent-returns
    for prime in correct_prime_guess(
            upto=target,
            first_greater=True,
            list_all=True,
    ):
        if prime[1] >= target:
            if prime[1] == target:
                print(prime[1], " is the ", prime[0], "th prime.", sep='')
            if prime[1] > target:
                print("Higher prime:", end=" ")
                print(prime[0], "th prime: ", prime[1], sep="")
                return prime
    return -1, -1


def search_for_nth_prime(target: int) -> None:
    for _prime in correct_prime_guess(target_n=target):
        if _prime[0] % 1000 and _prime[1] < target:
            print(_prime[0], _prime[1])
        if _prime[0] == target:
            print(_prime[0], "th prime is ", _prime[1], sep="", end=".\n")
            break


#I run EITHER yield_primes_memory OR yield_and_write_primes DEPENDING ON PHONE USAGE!
if __name__ == '__main__':
    try:
        A = 11 ** 10000
        SLIGHTLY_SMALLER_A = 11 ** (10000 - 6)
        print("Huge number:", A)
        print("Slightly smaller:", SLIGHTLY_SMALLER_A)
        B = A // SLIGHTLY_SMALLER_A
        print(B,
              "was calculated by dividing that huge number by a slightly smaller but still huge number."
              )
        print("It's _factors are", end=" ")
        print(Factorized(B))
        print(-15, "'s _factors are", sep="", end=" ")
        print(Factorized(-15))
        print(36, "'s _factors are", sep="", end=" ")
        print(Factorized(36))
        print(63, "'s _factors are", sep="", end=" ")
        print(Factorized(63))
        print(147, "'s _factors are", sep="", end=" ")
        print(Factorized(147))

        print("I will ask you a series of questions about what you want to do.")
        print("Say Yes if you want to do the thing I asked you about.")
        if input("Want to know the last known prime I found? ").lower() == "yes":
            last_known_prime = get_last_prime()
            print("Last known prime is the ", last_known_prime[0], "th prime number: ",
                  last_known_prime[1], sep="")
        elif input("Factor a number? ").lower() == "yes":
            print(Factorized(get_int()))
        elif input(
                "Do you want to find a prime greater than a target number N?\n"
                + "Say Yes if so, then I'll ask you for your target number. "
        ).lower() == "yes":
            print_next_prime_greater(get_int())
        else:
            # Guess Nth prime
            print("Name N as the Nth prime number you want to guess")
            search_for_nth_prime(get_int())
    finally:
        close_db()
