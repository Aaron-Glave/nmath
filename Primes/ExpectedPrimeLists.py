import unittest

import main
from main import yield_and_write_primes, correct_prime_guess


class TestCorrectPrimes(unittest.TestCase):
    @staticmethod
    def prime_ints_up_to(max_of_primes: int, print_guesses: bool = False):
        return tuple(map(lambda result: result[1], yield_and_write_primes(max_of_primes, print_guesses=print_guesses)))

    @staticmethod
    def tuple_primes_up_to(max_of_primes: int, print_guesses: bool = False):
        return tuple(yield_and_write_primes(max_of_primes, print_guesses=print_guesses))

    def test_print_last_prime(self):
        pass

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
        primes = tuple(yield_and_write_primes(shouldnt_be_last, print_guesses=True, first_greater=True))
        self.assertGreater(primes[-1][1], shouldnt_be_last)
        print("Yes.")


    def test_guess_already_present(self):
        main.SHOULD_WRITE = True
        big_enough = 101
        comments = {}
        primes = tuple(correct_prime_guess(big_enough, list_all=True))
        self.assertEqual((26, 101), primes[26-1])
        #Re-run the search to check that our file already contains the prime we're looking for
        primes = tuple(correct_prime_guess(big_enough, comments=comments, target_n=26,list_all=True))
        print(primes[26-1])
        self.assertEqual((26, 101), primes[26 - 1])
        self.assertIn('already_there', comments)
        self.assertEqual(comments['already_there'], 'already there')

    @unittest.skipIf(False, "Takes a long time and rarely needed.\nSet the condition to True if you want to run this.")
    def test_in_order(self):
        main.SHOULD_WRITE = True
        last_p = 0
        last_n = 0
        #We have 25 lines in memory already, so after running through them line_in_list should get to 1.
        line_in_list = -1*len(main.ALL_PRIMES_UNDER_100)
        for nprime, prime in correct_prime_guess(list_all=True):
            line_in_list += 1
            self.assertEqual(nprime, last_n+1, msg=f"Error on line {line_in_list}")
            self.assertGreater(prime, last_p, msg=f"Error: prime located at {nprime} was less than the prime located at {last_n}")
            last_n = nprime
            last_p = prime




if __name__ == '__main__':
    unittest.main()
