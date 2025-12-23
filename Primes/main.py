"""Program designed to talk about prime numbers."""
#pylint: disable=C0301
import sys
from io import TextIOWrapper
from pathlib import Path
from typing import Optional, Tuple, List, Generator
import warnings
#pylint: disable=C0413,E0401
sys.path.append(str(Path(__file__).parent.resolve()))

from phone_banned import PhoneBanned
sys.path.pop()
#pylint: enable=C0413,E0401

sys.set_int_max_str_digits(100000)

#NOTE: Every line in this file is an integer referring to which prime number is listed, followed by a space, followed by a prime number, followed by a newline character.
SPRIMELIST = "sprimelist.txt"

#Set this to False on your phone!
SHOULD_WRITE = True

ALL_PRIMES_UNDER_100 = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
    53, 59, 61, 67, 71, 73,
    79, 83, 89, 97
]


#We don't even have a function to read the whole file into a list because that would use a TON of memory.


def under_or_at_limit(_current_guess: int, upto: Optional[int]) -> bool:
    """Used internally to return True if upto is null OR _current_guess <= upto"""
    if upto is None:
        return True
    return _current_guess <= upto


def write_prime(prime_to_write: Tuple[int, int], save_to: TextIOWrapper) -> None:
    """Used internally to write a prime number to the open IMPORTANT_NAME file"""
    if save_to is not None:
        save_to.write(str(prime_to_write[0]) + " " + str(prime_to_write[1]) + '\n')


def yield_primes_memory(upto: Optional[int] = None, print_specific: Optional[int] = None, first_greater: bool = False) -> Generator[tuple[int, int], None, None]:
    """Returns list of tuples [(1-based prime index, prime number)].
        Note that all known primes are created in memory,
          so the list is r-created for every iterator you create."""
    memory_list = ALL_PRIMES_UNDER_100.copy()
    found_first_greater = False
    #remember_first_greater = first_greater
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
        if isprime:
            if print_specific == nth_prime:
                print(str(nth_prime) + " prime is", guess)
            memory_list.append(guess)
            if len(memory_list) % 100 == 0:
                print(len(memory_list), "th prime is ", guess, sep='')
            yield nth_prime, guess
            if first_greater and not under_or_at_limit(nth_prime, upto):
                #Set first_greater to False because the next prime we will yield should be the first greater prime.
                found_first_greater = True
            #elif not under_or_at_limit(nth_prime, upto):
                #pass
            #Only increment the nth_prime value AFTER printing the current nth_prime you figured out.
            nth_prime += 1

        if not under_or_at_limit(guess, upto) and not found_first_greater and (
                not first_greater or memory_list[-1] >= guess):
            #if not first_greater:
            #    if memory_list[-1] >= guess:
            return
        guess += 2

#A FUNCTION TO ITERATE THROUGH A FILE INSTEAD OF A LIST. NOTE: DON'T RUN THIS ON YOUR PHONE! TEST THIS TO MAKE SURE IT WORKS!
#I don't care that this is a complex function.
#pylint: disable=R0911,R0912,R0913,R0914,R0915
def yield_and_write_primes(upto: Optional[int] = None, *,
                           list_all: bool = False,
                           print_guesses: bool = False,
                           first_greater: bool = False,
                           target_n: Optional[int] = None,
                           comments: Optional[dict[str, str]] = None) -> Generator[tuple[int, int], None, None]:
    """Returns list of tuples [(1-based prime index, prime number)].
    Note that unless you specify list_all to be true, I will start yielding newly discovered primes only"""
    save_to: Optional[TextIOWrapper] = None
    try:
        if not SHOULD_WRITE:
            raise PhoneBanned()
        save_to = open(SPRIMELIST, mode="a+", encoding='ascii')
        print_specific = False
        if first_greater:
            print_specific = True

        if not under_or_at_limit(2, upto):
            if print_specific:
                print("Smallest prime is 2.")
            return

        nth_prime = 1
        for prime in ALL_PRIMES_UNDER_100:
            if print_specific:
                if prime == target_n:
                    print(nth_prime, "prime is", prime)
            is_over = not under_or_at_limit(prime, upto)
            if first_greater and is_over:
                yield nth_prime, prime
                first_greater = False
            elif is_over:  #Stop when we're done listing low prime numbers.
                return
            yield nth_prime, prime
            #Doing this every time we yield guarantees that we will always start with nth_prime larger than the length of all_primes_under_100.
            nth_prime += 1


        save_to.seek(0)

        any_primes_found = False

        guess = 101 #NOTE: 101 is the default because 101 is the first prime after 97, the last in the default list
        #prime_to_start helps us figure out what the first guess should be.
        # We set prime_to_start to the last prime we found in the file,
        # so if prime_to_start is 0 at the end of our loop, we shouldn't change our initial guess of 101.
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

        #YOU NEED TO START WHERE YOU LEFT OFF LAST TIME
        #Done scanning the existing file, now we figure out more.
        # NOTE: I WILL TO LOOP THROUGH THE ENTIRE FILE I STORED WHEN I CHECK MY GUESS IS PRIME!
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
            #At this point we know the guess ISN'T divisible by 2, so we can stop once the prime in our loop > guess/2
            #We add 1 after shifting to guarantee that half_guess*2 > guess.
            half_guess = (guess >> 1) + 1
            greater_than_half = False
            for line in save_to:
                _no_need, prime = map(int, line.strip('\n').split(" "))
                if guess % prime == 0:
                    isprime = False
                    break
                if prime > half_guess:
                    greater_than_half = True
                    break
            if greater_than_half:
                greater_than_half = False
                #We already know the prime in our loop > guess/2, so we know our guess is prime.
                isprime = True
            if isprime:
                next_prime = (nth_prime, guess)
                if print_guesses and nth_prime % 10 == 0:
                    print(nth_prime, "th prime: ", guess, sep="")
                if print_specific == nth_prime:
                    print(str(nth_prime) + " prime is", guess)
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

def correct_prime_guess(upto: Optional[int] = None, *,
                        list_all: bool = False,
                        print_guesses: bool = False,
                        first_greater: bool = False,
                        target_n: Optional[int] = None,
                        comments: Optional[dict[str, str]] = None) -> Generator[tuple[int, int], None, None]:
    """If you're using a phone (SHOULD_WRITE is False), we look for primes using nothing but memory. Else, we use our "sprimelist.txt" file."""
    if SHOULD_WRITE:
        yield from yield_and_write_primes(
            upto=upto,
            list_all=list_all,
            print_guesses=print_guesses,
            first_greater=first_greater,
            target_n=target_n,
            comments=comments
        )
    else: yield from yield_primes_memory(
        upto=upto,
        print_specific=print_guesses,
        first_greater=first_greater,
    )


def get_last_prime() -> Tuple[int, int]:
    """Returns the biggest prime number in the list."""
    biggest_prime = (len(ALL_PRIMES_UNDER_100), ALL_PRIMES_UNDER_100[-1])
    if SHOULD_WRITE:
        sprimelist = open(SPRIMELIST, encoding='ascii')
        for line in sprimelist:
            biggest_prime = tuple(map(int, line.strip('\n').split(" ")))
    return biggest_prime


def primes_up_to100():
    """Creates a primes.txt file with the first 100 primes."""
    amaximum = 100
    primes = []
    try:
        primefile = open("primes.txt", mode="r", encoding='ascii')
    except FileNotFoundError:
        print("Creating list...")
        primefile = open("primes.txt", mode="x", encoding='ascii')
        primefile.close()
        primefile = open("primes.txt", mode="r", encoding='ascii')
        print("File listing primes was created")
    for line in primefile:
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
    primefile.close()
    primefile = open("primes.txt", mode='a', encoding='ascii')

    for i in range(start, amaximum + 1):
        isprime = True
        for prime in primes:
            if i % prime == 0:
                isprime = False
                break
        if isprime:
            primes.append(i)
            print(i, "is prime.")
            primefile.write(str(i) + '\n')
    primefile.close()
    print("Calculated primes <= ", amaximum, ": ", primes, sep="")


def gen_primes_up_to(max_prime=2):
    """Returns a list of primes up to max_prime."""
    return list(correct_prime_guess(max_prime, list_all=True))


def correct_factor_list(to_factor: int) -> Generator[int]:
    """Returns a correct list of factors, whether you SHOULD_WRITE or not."""
    if SHOULD_WRITE:
        yield from ALL_PRIMES_UNDER_100
        try:
            sprimelist = open(SPRIMELIST, mode="r", encoding='ascii')
            for line in sprimelist:
                yield int(list(line.strip('\n').split(' '))[1])
            sprimelist.close()
        except FileNotFoundError:
            print("Creating list...")
            sprimelist = open(SPRIMELIST, mode="w", encoding='ascii')
            sprimelist.close()
            correct_factor_list(to_factor)
        return None
    #We know the file exists, so read it.
    for mprime in yield_primes_memory(to_factor):
        yield mprime[1]
    return None


def factor(to_factor: int) -> List[Tuple[int, int]]:
    """Returns a list of factors for it's input.
    For example, passing 12 should return [(2, 2), (3, 1)].
    Note that on the PC, this function can only factor integers perfectly divisible by the prime numbers I've discovered so far in the list."""
    factors = []
    if to_factor < 0:
        factors.append((-1, 1))
        to_factor *= -1
    elif to_factor == 0:
        return [(0, 1)]
    elif to_factor == 1:
        return [(1, 1)]
    for prime in correct_factor_list(to_factor):
        if to_factor % prime == 0:
            number_of_divisions = 0
            while (to_factor % prime == 0) and (to_factor >= prime):
                number_of_divisions += 1
                to_factor //= prime
            factors.append((prime, number_of_divisions))
        if to_factor <= 1:
            break
    if to_factor > 1:
        factor_failure = "I couldn't find a factor for " + str(to_factor) + ".\nIt might be divisible by prime numbers I haven't discovered."
        warnings.warn(factor_failure, UserWarning)
        return factors
    return factors


def factors_as_string(factors: List[Tuple[int, int]]):
    """Given a list of factors for a number (often printed by the factor(...) function, nicely prints the number represented as a product of its factors)."""
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
        #print(found_factor[0], found_factor[1], sep="^", end=ending)
    return "".join(strs_to_return)

def say_gap_message(gap_to_print: Tuple[Tuple[Tuple[int, int], Tuple[int, int]], int]):
    """Prints info about the gap passed
    Organization: ((previous_prime_tuple, next_prime_tuple), next_prime_tuple[1] - previous_prime_tuple[1])
        Each prime_tuple: (
            index of the prime number starting at 1 and increasing by 1 for each prime,
            the prime number itself
        )."""
    print("Found a gap of", end=" ")
    print(gap_to_print[0][1][0], "th prime to ", gap_to_print[0][0][0], "th prime:\n",
          gap_to_print[0][1][1], "-", gap_to_print[0][0][1], ": ", gap_to_print[1], sep="", end=".\n")

def largest_gap_1000() -> Tuple[Tuple[Tuple[int, int], Tuple[int, int]], int]:
    """Prints and returns the largest gap between adjacent prime numbers we know,
    returning the first 2 prime numbers which are that far apart, as well as the size of the gap.
    Note that the gap this function finds CAN appear again in my list beyond the prime numbers I return."""
    previous_prime = (1, ALL_PRIMES_UNDER_100[0])
    next_prime = (2, ALL_PRIMES_UNDER_100[1])
    current_greatest_gap: Tuple[Tuple[Tuple[int, int], Tuple[int, int]], int] = (((1, 2), (1, 2)), 0)
    nth_prime = 2

    for i in range(1, len(ALL_PRIMES_UNDER_100)):
        next_prime = (i + 1, ALL_PRIMES_UNDER_100[i])
        gap  = next_prime[1] - previous_prime[1]
        if gap > current_greatest_gap[1]:
            current_greatest_gap = ((previous_prime, next_prime), next_prime[1] - previous_prime[1])
            say_gap_message(current_greatest_gap)
        previous_prime = next_prime

    if SHOULD_WRITE:
        found100 = False
        first_pair100: Tuple[Tuple[Tuple[int, int], Tuple[int, int]], int] = (((-1, -1), (-1, -1)), 0)
        primelist = open(SPRIMELIST, mode="r", encoding='ascii')
        previous_prime = tuple(map(int, primelist.readline().strip('\n').split(' ')))
        for line in primelist:
            nth_prime, prime = map(int, line.strip('\n').split(' '))
            next_prime = (nth_prime, prime)
            gap = next_prime[1] - previous_prime[1]
            if gap > current_greatest_gap[1] or ((not found100) and gap == 100):
                current_greatest_gap = ((previous_prime, next_prime), next_prime[1] - previous_prime[1])
                if gap == 100 and not found100:
                    print("Found the first gap of 100")
                    found100 = True
                    first_pair100 = current_greatest_gap
                say_gap_message(current_greatest_gap)
            previous_prime = next_prime
        if found100:
            print("First gap of 100:")
            say_gap_message(first_pair100)
    return current_greatest_gap

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

def print_next_prime_greater(target: int) -> None:
    """Interactive. Method to determine a prime number greater than the input."""
    for prime in correct_prime_guess(
            upto=target,
            first_greater=True,
            list_all=True,
            print_guesses=True
    ):
        if prime[1] >= target:
            if prime[1] == target:
                print(prime[1], " is the ", prime[0], "th prime.", sep='')
            if prime[1] > target:
                print("Higher prime:", end=" ")
                print(prime[0], "th prime: ", prime[1], sep="")
                return

#I run EITHER yield_primes_memory OR yield_and_write_primes DEPENDING ON PHONE USAGE!
if __name__ == '__main__':
    A = 11 ** 10000
    SLIGHTLY_SMALLER_A = 11 ** (10000 - 6)
    print("Huge number:", A)
    print("Slightly smaller:", SLIGHTLY_SMALLER_A)
    B = A // SLIGHTLY_SMALLER_A
    print(B, "was calculated by dividing that huge number by a slightly smaller but still huge number.")
    print("It's factors are", end=" ")
    print(factors_as_string(factor(B)))
    print(-15, "'s factors are", sep="", end=" ")
    print(factors_as_string(factor(-15)))
    print(36, "'s factors are", sep="", end=" ")
    print(factors_as_string(factor(36)))
    print(63, "'s factors are", sep="", end=" ")
    print(factors_as_string(factor(63)))
    print(147, "'s factors are", sep="", end=" ")
    print(factors_as_string(factor(147)))

    print("I will ask you a series of questions about what you want to do.")
    print("Say Yes if you want to do the thing I asked you about.")
    if input("Generate text file of first 100 primes? ").lower() == "yes":
        primes_up_to100()
    elif input("Want to know the last known prime I found? ").lower() == "yes":
        last_known_prime = get_last_prime()
        print("Last known prime is the ", last_known_prime[0], "th prime number: ", last_known_prime[1], sep="")
    elif input("Factor a number? ").lower() == "yes":
        if SHOULD_WRITE:
            print("Warning: On CPU mode you only know the prime numbers in " + SPRIMELIST)
        _S = factors_as_string(
                factor(get_int())
            )
        print(_S)
    elif input("Do you want to find a prime greater than a target number N?\nSay Yes if so, then I'll ask you for your target number. ").lower() == "yes":
        print_next_prime_greater(get_int())
    elif input("Do you want to know the biggest gap between prime numbers you know? ").lower() == "yes":
        _biggest_gap = largest_gap_1000()
        print("\nBiggest gap found:")
        say_gap_message(_biggest_gap)
    else:
        # Guess Nth prime
        print("Name N as the Nth prime number you want to guess")
        TARGET = get_int()
        for _prime in correct_prime_guess(print_guesses=True, target_n=TARGET):
            if _prime[0] == TARGET:
                print(_prime[0], "th prime is ", _prime[1], sep="", end=".\n")
                break
