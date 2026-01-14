import unittest

import main
from main import correct_prime_guess, get_last_prime

class AllPrimesInOrder(unittest.TestCase):
    def test_in_order(self):
        """Verifies that your list of prime numbers looks right.
        Use https://t5k.org/nthprime/index.php to check it out."""
        main.SHOULD_WRITE = True
        last_p = 0
        last_n = 0
        # We have 25 lines in memory already, so after running through them line_in_list should get to 1.
        line_in_list = -1 * len(main.ALL_PRIMES_UNDER_100)
        for nprime, prime in correct_prime_guess(upto=get_last_prime()[1], list_all=True):
            line_in_list += 1
            self.assertEqual(nprime, last_n + 1, msg=f"Error on line {line_in_list}")
            self.assertGreater(prime, last_p,
                               msg=f"Error: prime located at {nprime} was less than the prime located at {last_n}")
            if line_in_list % 10000 == 0:
                print("Tested", line_in_list, "lines so far.")
            last_n = nprime
            last_p = prime
        print("Tested", line_in_list, "lines and they all looked good.")


if __name__ == '__main__':
    unittest.main()
