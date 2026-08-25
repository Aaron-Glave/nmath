"""Program designed to talk about prime numbers."""
import sys
from io import TextIOWrapper

from typing import Optional, Tuple, Generator
import warnings

from phone_banned import PhoneBanned

sys.path.pop()
sys.set_int_max_str_digits(100000)

#NOTE: Every line in this file is an integer referring to which prime number is listed,
# followed by a space, followed by a prime number, followed by a newline character.
SPRIMELIST = "sprimelist.txt"

#Set this to False on your phone!
SHOULD_WRITE = True

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


def write_prime(prime_to_write: Tuple[int, int], save_to: TextIOWrapper) -> None:
    """Used internally to write a prime number to the open IMPORTANT_NAME file"""
    if save_to is not None:
        save_to.write(str(prime_to_write[0]) + " " + str(prime_to_write[1]) + '\n')


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


#I don't care that this is a complex function.
#pylint: disable=R0911,R0912,R0913,R0914,R0915
def yield_and_write_primes(upto: Optional[int] = None, *,
                           save_to: Optional[TextIOWrapper] = None,
                           list_all: bool = False,
                           first_greater: bool = False,
                           target_n: Optional[int] = None,
                           comments: Optional[dict[str, str]] = None) -> Generator[
    tuple[int, int], None, None]:
    """A function to iterate through a file instead of a list.
    Arguments:
        upto: int -> The highest number you want to investigate
        save_to: TextIOWrapper -> The file to write the prime numbers to
        list_all: bool -> Whether to write a list of primes
        first_greater: bool -> Whether to write the first prime number greater than upto
        target_n: Optional[int] -> The index of the prime you're looking for
        comments: A dictionary for additional comments, mainly used for testing.

    Throws a PhoneBanned exception if you even try to run this on your phone.
    Returns a list of tuples [(1-based prime index, prime number)].
    I typically call those nth_prime, prime.
    Note that unless you specify list_all to be true,
    this only yields newly discovered primes!
    If you do set list_all to True and don't specify a target,
      only known primes will be yielded."""
    save_to: Optional[TextIOWrapper] = None
    #You are only trying to read through the list when:
    # You want to look through your existing list
    # You didn't specify that you're looking for a particular prime.
    # - This weird logic is because when we're looking for a specific prime,
    #   we don't know whether we already know our target until we start reading through our list.
    read_only = list_all and upto is None and target_n is None
    try:
        if not SHOULD_WRITE:
            raise PhoneBanned()
        if read_only:
            save_to = open(SPRIMELIST, mode="r", encoding="ascii")
        else:
            save_to = open(SPRIMELIST, mode="a+", encoding='ascii')
        assert save_to is not None

        if not under_or_at_limit(2, upto):
            warnings.warn("Smallest prime is 2.")
            return

        nth_prime = 1
        for prime in ALL_PRIMES_UNDER_100:
            is_over = not under_or_at_limit(prime, upto)
            if first_greater:
                if prime == target_n and comments is not None:
                    comments['nth_prime'] = f"{nth_prime} is ${prime}"
                if is_over:
                    yield nth_prime, prime
                    first_greater = False
            elif is_over:  #Stop when we're done listing low prime numbers.
                return
            yield nth_prime, prime
            #Doing this every time we yield guarantees that we will always start with nth_prime
            # larger than the length of all_primes_under_100.
            nth_prime += 1

        save_to.seek(0)
        any_primes_found = False
        guess = 101  #NOTE: 101 is the default because 101 is the first prime after 97.
        # ^ That's the last prime in the default list.
        #prime_to_start helps us figure out what the first guess should be.
        # We set prime_to_start to the last prime we found in the file,
        # so if prime_to_start is 0 at the end of our loop,
        # we shouldn't change our initial guess of 101.
        prime_to_start = 0

        for line in save_to:
            any_primes_found = True
            nth_prime, prime = map(int, line.strip('\n').split(" "))

            prime_to_start = prime

            #Depending on the arguments, we may or may not yield primes in our file.
            if target_n is not None and nth_prime >= target_n:
                if comments is not None:
                    comments['already_there'] = 'already there'
                yield nth_prime, prime
                save_to.close()
                return
            if first_greater:
                if not under_or_at_limit(prime, upto):
                    yield nth_prime, prime
                    return
            #At this point we know we DON'T care about primes greater than upto
            #Yield the last prime if we guessed it.
            elif prime == upto:
                yield nth_prime, prime
                return
            elif not under_or_at_limit(prime, upto):
                return
            if list_all:
                yield nth_prime, prime
        if any_primes_found:
            nth_prime += 1

        #Return early if the read_only flag is set.
        if read_only:
            return

        #YOU NEED TO START WHERE YOU LEFT OFF LAST TIME
        #Done scanning the existing file, now we figure out more.
        # NOTE: I WILL TO LOOP THROUGH THE ENTIRE FILE I STORED WHEN I CHECK MY GUESS IS PRIME!
        # You don't need to worry about start_at anymore!
        if prime_to_start != 0:
            guess = prime_to_start + 2
        calculate_more = True
        divisible_by_prime_under_100 = False
        while calculate_more:
            isprime = True
            divisible_by_prime_under_100 = False
            for prime in ALL_PRIMES_UNDER_100:
                if guess % prime == 0:
                    divisible_by_prime_under_100 = True
                    break
            if divisible_by_prime_under_100:
                divisible_by_prime_under_100 = False
                if not under_or_at_limit(guess, upto):
                    if not first_greater:
                        calculate_more = False
                guess += 2
                save_to.seek(0)
                #Don't even bother reading the file
                continue

            save_to.seek(0)

            #The Sieve of Eratosthenes:
            # After testing divisibility by every prime number
            # less than the SQUARE ROOT of the guess we're testing,
            # we know for sure that it's prime!
            square_is_bigger = False

            for line in save_to:
                _no_need, prime = map(int, line.strip('\n').split(" "))
                if guess % prime == 0:
                    isprime = False
                    break
                if prime * prime > guess:
                    square_is_bigger = True
                    break
            if square_is_bigger:
                square_is_bigger = False
                #We already know the prime in our loop > guess/2, so we know our guess is prime.
                isprime = True
            if isprime:
                next_prime = (nth_prime, guess)
                write_prime(next_prime, save_to)
                yield next_prime
                if comments is not None:
                    if nth_prime == target_n:
                        comments['already_there'] = 'Had to be found.'
                nth_prime += 1

                if first_greater and not under_or_at_limit(next_prime[1], upto):
                    first_greater = False

            if not under_or_at_limit(guess, upto):
                if not first_greater:
                    calculate_more = False
            guess += 2
    finally:
        if save_to is not None:
            save_to.close()


#pylint: enable=R0911,R0912,R0913,R0914,R0915


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


def correct_factor_list(to_factor: int) -> Generator[int, None, None]:
    """Returns a correct list of factors of the number to_factor,
    whether you SHOULD_WRITE or not."""
    if SHOULD_WRITE:
        yield from ALL_PRIMES_UNDER_100
        try:
            with open(SPRIMELIST, mode='r', encoding='ascii') as sprimelist:
                for line in sprimelist:
                    yield int(list(line.strip('\n').split(' '))[1])
        except FileNotFoundError:
            print("Creating list...")
            sprimelist = open(SPRIMELIST, mode="w", encoding='ascii')
            sprimelist.close()
            correct_factor_list(to_factor)
        return None
    #We know SHOULD_WRITE is False, so yield from memory.
    yield from memory_factor_list(to_factor)
    return None


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

    def __init__(
            self, to_factor: int,
            prime_source: Generator[
                tuple[int, int], None, None
            ] = correct_prime_guess(list_all=True),
    ) -> None:
        """Factorizes the passed integer using a Callable[
            [int], Generator[tuple[int, int], None, None]
        ] to factor it. The default factorization method is """
        self.factors: list[tuple[int, int]] = []
        self.factor_failure = None
        if to_factor < 0:
            self.factors.append((-1, 1))
            to_factor *= -1
        elif to_factor == 0:
            self.factors = [(0, 1)]
        elif to_factor == 1:
            self.factors = [(1, 1)]
        done_factoring = False
        while to_factor > 1 and not done_factoring:
            for _, prime in prime_source:
                if to_factor % prime == 0:
                    to_factor, number_of_divisions = Factorized.reduce(to_factor, prime)
                    self.factors.append((prime, number_of_divisions))
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
        for factor in self.factors:
            factor_count += 1
            if strs_to_list == len(self.factors):
                ending = ""
            strs_to_list.append(f"{factor[0]} ^ {factor[1]}{ending}")
        return "".join(strs_to_list)


'''def factor(
    to_factor: int,
    method= correct_prime_guess
) -> List[Tuple[int, int]]:
    """Returns a list of factors for it's input.
    For example, passing 12 should return [(2, 2), (3, 1)].
    The method should be a prime generator with an argument to set the highest prime to guess."""

    def reduce(number: int, divisor: int) -> Tuple[int, int]:
        """Returns (a, n) where number == a*(divisor ^ n) and a is not divisible by the divisor.
        Basically factors out the divisor raised to the highest possible power."""
        n = 0
        while number % divisor == 0:
            n += 1
            number //= divisor
        return number, n

    factors = []
    if to_factor < 0:
        factors.append((-1, 1))
        to_factor *= -1
    elif to_factor == 0:
        return [(0, 1)]
    elif to_factor == 1:
        return [(1, 1)]
    done_factoring = False
    while to_factor > 1 and not done_factoring:
        for _, prime in method(to_factor, list_all=True):
            if to_factor % prime == 0:
                to_factor, number_of_divisions = reduce(to_factor, prime)
                factors.append((prime, number_of_divisions))
                if to_factor == 1:
                    done_factoring = True
                break

    if to_factor > 1:
        factor_failure = "I couldn't find a factor for " + str(
            to_factor) + ".\nIt might be divisible by prime numbers I haven't discovered."
        warnings.warn(factor_failure, UserWarning)
        return factors
    return factors'''


'''def factors_as_string(factors: List[Tuple[int, int]]):
    """Given a list of factors for a number (often found with the factor(...) function),
    nicely prints the number represented as a product of its factors."""
    factor_count = 0
    strs_to_return = []
    for found_factor in factors:
        factor_count += 1
        if factor_count == len(factors):
            ending = ""
        else:
            ending = " * "
        strs_to_return.append(
            str(found_factor[0]))
        strs_to_return.append('^')
        strs_to_return.append(
            str(found_factor[1]))
        strs_to_return.append(ending)
    return "".join(strs_to_return)'''


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


#I run EITHER yield_primes_memory OR yield_and_write_primes DEPENDING ON PHONE USAGE!
if __name__ == '__main__':
    A = 11 ** 10000
    SLIGHTLY_SMALLER_A = 11 ** (10000 - 6)
    print("Huge number:", A)
    print("Slightly smaller:", SLIGHTLY_SMALLER_A)
    B = A // SLIGHTLY_SMALLER_A
    print(B,
          "was calculated by dividing that huge number by a slightly smaller but still huge number."
          )
    print("It's factors are", end=" ")
    print(Factorized(B))
    print(-15, "'s factors are", sep="", end=" ")
    print(Factorized(-15))
    print(36, "'s factors are", sep="", end=" ")
    print(Factorized(36))
    print(63, "'s factors are", sep="", end=" ")
    print(Factorized(63))
    print(147, "'s factors are", sep="", end=" ")
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
        TARGET = get_int()
        for _prime in correct_prime_guess(target_n=TARGET):
            if _prime[0] % 1000 and _prime[1] < TARGET:
                print(_prime[0], _prime[1])
            if _prime[0] == TARGET:
                print(_prime[0], "th prime is ", _prime[1], sep="", end=".\n")
                break
