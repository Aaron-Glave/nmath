"""A program to test that you correctly loop through primes in increasing order of prime numbers."""
import unittest

from . import main
from .main import correct_prime_guess, yield_and_write_primes, yield_primes_memory

class AllPrimesInOrder(unittest.TestCase):
    """Verifies that your list of prime numbers looks right.
            Use https://t5k.org/nthprime/index.php to check it out."""
    def test_in_order(self):
        """The one test"""
        last_p = 0
        last_n = 0
        comments: dict[str, str] = {}
        # We have 25 lines in memory already,
        # so after running through them line_in_list should get to 1.
        line_in_list = -1 * len(main.ALL_PRIMES_UNDER_100)
        #Used for debugging. Requires reading the whole list of prime numbers.
        #target_last_prime = get_last_prime()
        prime_iter = correct_prime_guess(list_all=True, comments=comments)
        nprime, prime = next(prime_iter)
        self.assertEqual(nprime, last_n + 1)
        self.assertEqual(prime, 2)
        last_n, last_p= nprime, prime
        self.assertEqual(comments['prime_guess_func'], yield_and_write_primes.__name__)
        for nprime, prime in prime_iter:
            line_in_list += 1
            self.assertEqual(nprime, last_n + 1,
                             msg=(
                                 f"Error on line {line_in_list}. "
                                 "Expected {last_n + 1}, but got {nprime}."
                             ))
            self.assertGreater(prime, last_p,
                               msg=(
                                   f"Error: {nprime} prime located at line {line_in_list}" +
                                   f" was less than the prime located at {last_n}"
                               ))
            if line_in_list % 500000 == 0 and line_in_list > 0:
                print("Tested", line_in_list, "lines so far.")
            last_n, last_p = nprime, prime
        print("Tested", line_in_list, "lines and they all looked good.")
        print("Check your highest known prime:",
              f"The {last_n}nth prime is: {last_p}.", sep="\n")


if __name__ == '__main__':
    unittest.main()
