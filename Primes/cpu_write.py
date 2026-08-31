"""A separate file to contain code you only need on your PC.
See https://www.perplexity.ai/search/2cf18bcc-25e1-4ef1-b0b2-892b6d061355 for sqlite help."""
from io import TextIOWrapper
import sqlite3
from typing import Optional, Generator, Tuple
import warnings

from .primes_db import prime_db_code
from .shared_ph_pc import under_or_at_limit, ALL_PRIMES_UNDER_100, desc_prime_with_index


def write_prime(prime_to_write: Tuple[int, int], save_to: TextIOWrapper) -> None:
    """Used internally to write a prime number to the open IMPORTANT_NAME file"""
    if save_to is not None:
        save_to.write(str(prime_to_write[0]) + " " + str(prime_to_write[1]) + '\n')

#I don't care that this is a complex function.
#pylint: disable=R0911,R0912,R0913,R0914,R0915
def yield_and_write_primes(upto: Optional[int] = None, *,
                           list_all: bool = False,
                           first_greater: bool = False,
                           target_n: Optional[int] = None,
                           comments: Optional[dict[str, str]] = None) -> Generator[
    tuple[int, int], None, None]:
    """A function to iterate through a file instead of a list.
    Reads the database primes.db in module primes_db.
    Arguments:
        upto: int -> The highest number you want to investigate
        list_all: bool -> Whether to write a list of primes
        first_greater: bool -> Whether to write the first prime number greater than upto
        target_n: Optional[int] -> The index of the prime you're looking for
        comments: A dictionary for additional comments, mainly used for testing.

    Throws a PhoneBanned exception if you even try to run this on your phone.
    Potentially throws sqlite3.Error as well
    Returns a list of tuples [(next_nth_prime, prime)].
    where next_nth_prime is the prime index and prime is the prime number itself.
    Note that unless you specify list_all to be true,
    this only yields newly discovered primes!
    If you do set list_all to True and don't specify a target,
      only known primes will be yielded."""
    #You don't want to find any new primes when:
    # You want to look through your existing list
    # You didn't specify that you're looking for a particular prime.
    read_only = list_all and upto is None and target_n is None
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
        if list_all:
            yield nth_prime, prime
        #Doing this every time we yield guarantees that we will always start with nth_prime
        # larger than the length of all_primes_under_100.
        nth_prime += 1

    any_primes_found = False
    #Look up your highest prime number in your database
    #guess helps us figure out what the first guess should be.
    max_prime_known_db = prime_db_code.get_max_prime_in_db(prime_db_code.DATABASE)
    #Handle the case where the database is empty.
    guess = 101  # NOTE: 101 is the default because 101 is the first prime after 97.
    next_nth_prime = len(ALL_PRIMES_UNDER_100) + 1
    if max_prime_known_db is not None:
        next_nth_prime = max_prime_known_db[0] + 1 # We're looking for the next highest prime
        guess = max_prime_known_db[1] + 2 # It's gotta be at least 2 higher...
    if list_all:
        our_primes_db = prime_db_code.get_connection(prime_db_code.DATABASE)
        try:
            # Basically loop through the database
            cursor = prime_db_code.all_primes_skip_first_n(len(ALL_PRIMES_UNDER_100), our_primes_db)
            for nth_prime, prime in cursor: #nth_prime is NOT the nth_prime you're searching for!
                # Depending on the arguments, we may or may not yield primes in our file.
                if target_n is not None and nth_prime >= target_n:
                    if comments is not None:
                        comments['already_there'] = 'already there'
                    yield nth_prime, prime
                    return
                if first_greater:
                    # Yield the first prime greater than upto.
                    if not under_or_at_limit(prime, upto):
                        yield nth_prime, prime
                        return
                # At this point we know we DON'T care about primes greater than upto
                # Yield the last prime if we guessed it.
                elif prime == upto:
                    yield nth_prime, prime
                    return
                elif not under_or_at_limit(prime, upto):
                    return
                if list_all:
                    yield nth_prime, prime
        except sqlite3.Error:
            prime_db_code.disconnect_specific_db(prime_db_code.DATABASE)
            raise

    #Now we're searching for new prime numbers...
    if read_only:
        return
    isprime = True
    our_primes_db = prime_db_code.get_connection(prime_db_code.DATABASE)
    try:
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
                continue
            # The Sieve of Eratosthenes:
            # After testing divisibility by every prime number
            # less than the SQUARE ROOT of the guess we're testing,
            # we know for sure that it's prime!
            square_is_bigger = False
            cursor = prime_db_code.read_all_prime_records(our_primes_db)
            #Test if guess is divisible by any primes in our database
            for _, prime in cursor:
                if guess % prime == 0:
                    isprime = False
                    break
                if prime * prime > guess:
                    square_is_bigger = True
                    break
            if square_is_bigger:
                square_is_bigger = False
                isprime = True
            if isprime:
                prime_db_code.insert_prime_with_connection(next_nth_prime, guess, our_primes_db)
                if comments is not None:
                    comments['already_there'] = 'Had to be found.'
                yield next_nth_prime, guess
                next_nth_prime += 1 #Now we're searching for the next one.
                if first_greater and not under_or_at_limit(guess, upto):
                    first_greater = False

            if not under_or_at_limit(guess, upto):
                if not first_greater:
                    calculate_more = False
            guess += 2
    except sqlite3.Error:
        raise
    finally:
        prime_db_code.disconnect_specific_db(prime_db_code.DATABASE)
#pylint: enable=R0911,R0912,R0913,R0914,R0915


def get_nth_prime_in_db(nth_prime, db: str) -> tuple[int, int] | None:
    nth_prime_in_db: tuple[int, int] | None = prime_db_code.get_nth_prime_in_db(nth_prime, db)
    if nth_prime_in_db is not None:
        return nth_prime_in_db[0], nth_prime_in_db[1]
    for nth_prime_found, prime in yield_and_write_primes(target_n=nth_prime):
        if nth_prime_found == nth_prime:
            return nth_prime_found, prime
    return None


def get_max_prime(db: str = prime_db_code.DATABASE) -> tuple[int, int]:
    max_memory = (len(ALL_PRIMES_UNDER_100), ALL_PRIMES_UNDER_100[-1])
    try:
        _get = prime_db_code.get_max_prime_in_db(db)
        if _get is not None:
            return _get
    except sqlite3.ProgrammingError:
        pass
    return max_memory

def close_real_db():
    prime_db_code.disconnect_specific_db(prime_db_code.DATABASE)

def test_db_expands():
    target_n = None
    max_prime_db = prime_db_code.get_max_prime_in_db(prime_db_code.DATABASE)
    if max_prime_db is None:
        target_n = 2
    else:
        target_n = max_prime_db[0] + 2

    for nth_prime, prime in yield_and_write_primes(target_n=target_n):
        print(desc_prime_with_index((nth_prime, prime)))
