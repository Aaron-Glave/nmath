"""A program to test that you correctly loop through primes in increasing order of prime numbers."""
import unittest

from . import main
from .main import correct_prime_guess, yield_and_write_primes, yield_primes_memory

class AllPrimesInOrder(unittest.TestCase):
    """Verifies that your list of prime numbers looks right.
            Use https://t5k.org/nthprime/index.php to check it out."""
    def test_in_order(self):
        """The one test checks every prime we know,
        checking that we yield primes in increasing order
        and that we don't skip any."""
        last_p = 0
        last_n = 0
        record_count = 0
        comments: dict[str, str] = {}
        #TODO ERROR: Error on record 26. Expected 26, but got 1.
        prime_iter = correct_prime_guess(list_all=True, comments=comments)
        nprime, prime = next(prime_iter)
        self.assertEqual(nprime, 1)
        self.assertEqual(prime, 2)
        record_count += 1
        self.assertEqual(nprime, last_n + 1)
        self.assertEqual(prime, 2)
        last_n, last_p = nprime, prime
        self.assertEqual(comments['prime_guess_func'], yield_and_write_primes.__name__)
        for nprime, prime in prime_iter:
            record_count += 1
            self.assertEqual(nprime, last_n + 1,
                             msg=(
                                 f"Error on record {record_count}. "
                                 f"Expected {last_n + 1}, but got {nprime}."
                             ))
            self.assertGreater(prime, last_p,
                               msg=(
                                   f"Error: {nprime} prime located at line {record_count}" +
                                   f" was less than the prime located at {last_n}"
                               ))
            if record_count % 500000 == 0 and record_count > 0:
                print("Tested", record_count, "records so far.")
            last_n, last_p = nprime, prime
        print("Tested", record_count, "lines and they all looked good.")
        print("Check your highest known prime:",
              f"The {last_n}nth prime is: {last_p}.", sep="\n")


if __name__ == '__main__':
    unittest.main()
