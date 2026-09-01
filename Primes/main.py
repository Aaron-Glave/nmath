"""Program designed to talk about prime numbers."""
import sys
from io import TextIOWrapper
from time import time
from typing import Tuple, Generator, Optional

from .phone_banned import PhoneBanned
from .shared_ph_pc import (SHOULD_WRITE, ALL_PRIMES_UNDER_100, under_or_at_limit,
                           desc_prime_with_index)

sys.set_int_max_str_digits(100000)
if SHOULD_WRITE:
    try:
        from .cpu_write import (yield_and_write_primes, close_real_db as close_db, get_max_prime,
                                get_nth_prime_in_db)
    except ModuleNotFoundError as me:
        raise me
else:
    def yield_and_write_primes(upto: Optional[int] = None, *,
                               save_to: Optional[TextIOWrapper] = None,
                               list_all: bool = False,
                               first_greater: bool = False,
                               target_n: Optional[int] = None,
                               comments: Optional[dict[str, str]] = None)\
    -> Generator[tuple[int, int], None, None]:
        raise PhoneBanned()


    def get_nth_prime_in_db(nth_prime, db: str) -> tuple[int, int] | None:
        raise PhoneBanned()


    def get_max_prime() -> tuple[int, int]:
        return len(ALL_PRIMES_UNDER_100), ALL_PRIMES_UNDER_100[-1]


    def close_db():
        pass


#We don't even have a function to read the whole file into a list.
# That would use a TON of memory.
def yield_primes_memory(upto: Optional[int] = None, print_specific: Optional[int] = None,
                        first_greater: bool = False,
                        comments: Optional[dict[str, str]] = None
                        ) -> Generator[tuple[int, int], None, None]:
    """Returns list of tuples [(1-based prime index, prime number)].
        Note that all known primes are created in memory,
          so the list is r-created for every iterator you create."""
    memory_list = list(ALL_PRIMES_UNDER_100)
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
        if comments is not None:
            comments['prime_guess_func'] = yield_and_write_primes.__name__
        yield from yield_and_write_primes(
            upto=upto,
            list_all=list_all,
            first_greater=first_greater,
            target_n=target_n,
            comments=comments
        )
    else:
        if comments is not None:
            comments['prime_guess_func'] = yield_primes_memory.__name__
        yield from yield_primes_memory(
            upto=upto,
            first_greater=first_greater,
            comments=comments
        )
#pylint:enable=R0913


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
        n = 0
        for _, prime in yield_and_write_primes(list_all=True):
            probability *= 1 - (1 / prime)
            n += 1
            if n % 20000 == 0:
                print(f"Ran through {n} primes so far...")
    return probability


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
    print("Found a gap of 100 between the", end=" ")
    print(gap_to_print[0][1][0], "th prime and the ", gap_to_print[0][0][0], "th prime.")
    print(f"Subtracting the {gap_to_print[0][0][0]}th prime from"
          f"the {gap_to_print[0][1][0]}th prime yields exactly 100.\n",
          gap_to_print[0][1][1], "-", gap_to_print[0][0][1], "=", gap_to_print[1],
          sep='', end=".\n")


def largest_gap_of_primes() -> Tuple[Tuple[Tuple[int, int], Tuple[int, int]], int]:
    """Prints and returns the largest gap between adjacent prime numbers we know,
    returning the first 2 prime numbers which are that far apart, as well as the size of the gap.
    Note that the gap this function finds CAN repeat;
    I just return a reference to the first time I find that gap."""
    benchmark = time()
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
        nread = 0
        for nth_prime, prime in yield_and_write_primes(list_all=True):
            if time() - benchmark >= 15:
                print("Currently looking at", desc_prime_with_index((nth_prime, prime)))
                benchmark = time()
            next_prime = (nth_prime, prime)
            nread += 1
            #if nread % 20000 == 0:
            #    print(nread, "reads so far")
            gap = next_prime[1] - previous_prime[1]
            if gap > current_greatest_gap[1]:
                current_greatest_gap = ((previous_prime, next_prime),
                                        next_prime[1] - previous_prime[1])

                print("Found new gap.", current_greatest_gap)
            previous_prime = next_prime
    assert isinstance(current_greatest_gap, tuple) and len(
        current_greatest_gap) == 2 and isinstance(current_greatest_gap[1], int)
    return current_greatest_gap


def say_gap_of_100():
    """We know there's a gap of 100 between adjacent primes at some point,
    but it's not in the strictly increasing list of gaps."""
    found_gap_100: Tuple[Tuple[Tuple[int, int], Tuple[int, int]], int] = (
        ((-1, -1), (-1, -1)), 0)

    if SHOULD_WRITE:
        nth_prime = -1
        #This might throw an exception, don't care
        generator = yield_and_write_primes(list_all=True)
        first_line = next(generator)
        previous_prime = (first_line[0], first_line[1])
        for nth_prime, prime in generator:
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
    if SHOULD_WRITE:
        #TODO INSERT A NEW METHOD TO SELECT THE FIRST prime higher
        raise NotImplementedError("I can find the higher prime a lot faster via a smart SQL query")
    for prime in correct_prime_guess(
            upto=target,
            first_greater=True,
            list_all=True,
    ):
        if prime[1] >= target:
            if prime[1] == target:
                print(target, "is a prime number!")
                print(desc_prime_with_index(prime))
            if prime[1] > target:
                print("Higher prime:", end=" ")
                print(desc_prime_with_index(prime))
                return prime
    return -1, -1


def search_for_nth_prime(target: int) -> None:
    # TODO WRITE A FASTER WAY TO FIND THIS
    if SHOULD_WRITE:
        result = get_nth_prime_in_db(target)
    else:
        for _prime in yield_primes_memory():
            if _prime[0] % 1000 and _prime[1] < target:
                print(_prime[0], _prime[1])
            if _prime[0] == target:
                print(desc_prime_with_index(_prime))
                break

#See run_prime_main.py in the parent directory for user interaction.
