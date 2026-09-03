import unittest
import sys
import io
from typing import Callable

from .primes_db import prime_db_code
from . import main
from .main import correct_prime_guess
from .shared_ph_pc import desc_prime_with_index
from .primes_db.clear_test_db import clear_test_db


class TestIOPrimes(unittest.TestCase):
    """These tests will be finicky because I'm testing the printed console output."""
    def run_command(self, command: Callable, expected_output: str) -> None:
        real_stdout = sys.stdout
        sys.stdout = io.StringIO()
        command()
        output = sys.stdout.getvalue()
        sys.stdout = real_stdout
        print("----Output:", output, sep='\n')
        self.assertEqual(output, expected_output)

    def test_prime_greater_than_103(self):
        self.run_command(
            lambda: main.print_next_prime_greater(103),
            '27th prime: 103\nHigher prime: 28th prime: 107\n'

        )

    def test_prime_greater_than_102(self):
        self.run_command(
            lambda: main.print_next_prime_greater(102),
            'Higher prime: 27th prime: 103\n'
        )

    def test_prime_greater_than_104(self):
        self.run_command(
            lambda: main.print_next_prime_greater(104),
            "Higher prime: 28th prime: 107\n"
        )

    def test_prime_greater_than_1160(self):
        self.run_command(
            lambda: main.print_next_prime_greater(1160),
            "Higher prime: 192th prime: 1163\n"
        )

    def test_get_27th_prime(self):
        self.run_command(
            lambda: main.search_for_nth_prime(27),
            '27th prime: 103\n'
        )

    def test_get_28th_prime(self):
        self.run_command(
            lambda: main.search_for_nth_prime(28),
            '28th prime: 107\n'
        )

    def test_get_168th_prime(self):
        self.run_command(
            lambda: main.search_for_nth_prime(168),
            '168th prime: 997\n'
        )

class TestCorrectPrimes(unittest.TestCase):
    """Tests comments when prime numbers are found or discovered.
    BIG_ENOUGH has to be a prime number not in your in-memory list!"""
    BIG_ENOUGH = (26, 101)

    @staticmethod
    def prime_ints_up_to(max_of_primes: int):
        return tuple(map(lambda result: result[1],
                         correct_prime_guess(max_of_primes, list_all=True)))

    @staticmethod
    def tuple_primes_up_to(max_of_primes: int):
        return tuple(correct_prime_guess(max_of_primes, list_all=True))

    def test_no_primes(self):
        self.assertEqual((), self.prime_ints_up_to(-1000))

    def test_first_two(self):
        first_prime = self.prime_ints_up_to(2)
        print(first_prime)
        self.assertEqual(first_prime, (2,))
        second_prime = self.prime_ints_up_to(3)
        self.assertEqual((2, 3), second_prime)

    def test_first_three(self):
        primes = self.tuple_primes_up_to(5)
        print(*primes)
        self.assertEqual(primes, ((1, 2), (2, 3), (3, 5)))

    def test_bigger_prime(self):
        shouldnt_be_last = 5
        print("Bigger than 5?")
        primes = tuple(correct_prime_guess(shouldnt_be_last, first_greater=True))
        self.assertGreater(primes[-1][1], shouldnt_be_last)
        print("Yes.")

    def test_guess_already_present(self):
        if not main.SHOULD_WRITE:
            self.skipTest('Only works on PC.')
        clear_test_db()
        comments = {}
        primes = tuple(
            main.yield_and_write_primes(
                TestCorrectPrimes.BIG_ENOUGH[1], list_all=True,
                comments=comments, db_to_connect_to=prime_db_code.TEST_DATABASE
            )
        )
        self.assertEqual(TestCorrectPrimes.BIG_ENOUGH, primes[TestCorrectPrimes.BIG_ENOUGH[0] - 1])
        self.assertIn('already_there', comments)
        self.assertEqual( 'Had to be found.', comments['already_there'])
        #Re-run the search to check that our file already contains the prime we're looking for
        primes = tuple(correct_prime_guess(
            comments=comments, target_n=TestCorrectPrimes.BIG_ENOUGH[0], list_all=True
        ))
        print(desc_prime_with_index(primes[TestCorrectPrimes.BIG_ENOUGH[0] - 1]))
        self.assertEqual(TestCorrectPrimes.BIG_ENOUGH, primes[TestCorrectPrimes.BIG_ENOUGH[0] - 1])
        self.assertIn('already_there', comments)
        self.assertEqual( 'Already there.', comments['already_there'])
        print(comments['already_there'])

    def test_mem_guess_not_present(self):
        big_enough = TestCorrectPrimes.BIG_ENOUGH[1]
        comments = {}
        primes = tuple(main.yield_primes_memory(big_enough, comments=comments))
        self.assertEqual('Had to be found.', comments['already_there'])


if __name__ == '__main__':
    unittest.main()
