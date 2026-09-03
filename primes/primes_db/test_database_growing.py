import sqlite3
import unittest

from primes.cpu_write import yield_and_write_primes

from primes.shared_ph_pc import desc_prime_with_index
from primes.primes_db import prime_db_code
from primes.primes_db.clear_test_db import reset_test_database


# noinspection method-may-be-static
class DBTestCases(unittest.TestCase):
    """Tests that the database is working as expected.
    Uses TEST_DATABASE so that even if there are mistakes in the test,
        your real data isn't hurt."""
    def test_db_expands(self):
        reset_test_database()
        target_n = None
        comments = {}
        max_prime_db = prime_db_code.get_max_prime_in_db(prime_db_code.TEST_DATABASE)
        if max_prime_db is None:
            target_n = 26
        else:
            target_n = max_prime_db[0] + 2

        for nth_prime, prime in yield_and_write_primes(
                target_n=target_n,
                db_to_connect_to=prime_db_code.TEST_DATABASE,
                comments=comments
        ):
            print(desc_prime_with_index((nth_prime, prime)))
        self.assertEqual('Had to be found.', comments['already_there'])

    def test_simple(self):
        reset_test_database()
        prime_db_code.insert_prime(1, 2, db=prime_db_code.TEST_DATABASE)
        prime_db_code.insert_prime(2, 3, db=prime_db_code.TEST_DATABASE)
        rlist = []
        with prime_db_code.get_connection(prime_db_code.TEST_DATABASE) as conn:
            rlist = conn.execute('SELECT nth_prime, prime FROM primes').fetchall()
        print(rlist)
        last_prime = prime_db_code.get_max_prime_in_db(prime_db_code.TEST_DATABASE)
        if last_prime is not None:
            print("Final prime:", )
        else:
            raise sqlite3.ProgrammingError("Empty database! Shouldn't happen!")

    def test_lowest_main(self):
        last_prime = prime_db_code.get_min_prime_in_db(prime_db_code.DATABASE)
        if last_prime is not None:
            print(last_prime)
        else:
            self.fail("Your prime database is empty.")

    def test_highest_main(self) -> tuple[int, int] | None:
        last_prime = prime_db_code.get_max_prime_in_db(prime_db_code.DATABASE)
        if last_prime is not None:
            print(last_prime)
            return last_prime
        else:
            self.fail("Your prime database is empty.")

    def test_pragma(self, db: str = prime_db_code.DATABASE) -> None:
        """Just prints info about your database. Doesn't return anything."""
        with prime_db_code.get_connection(db) as conn:
            print("Database indexes info:",
                  conn.execute(f"""PRAGMA index_list(primes);""").fetchall())
            print("idx_primes_value info:",
                  conn.execute(f"""PRAGMA index_info(idx_primes_value);""").fetchall())


    TEST_SPEED_MIN_VALUE = 500000
    def test_speed(self):
        """Tests the speed of queries to look for large prime numbers.
        May fail if your database isn't big enough.
            If that happens, run the main program until
            you discover TEST_SPEED_MIN_VALUE + 1 prime numbers"""
        print("This should be QUICK: Find the first prime number bigger than 500000.")
        one_greater = prime_db_code.prime_1_after(DBTestCases.TEST_SPEED_MIN_VALUE,
                                                  db=prime_db_code.DATABASE)
        if one_greater is None:
            self.fail(f"Not that many primes in {prime_db_code.DATABASE}.")
        else:
            print(desc_prime_with_index(one_greater))
        print("Finding the highest prime number you now should be quick too.")
        max_prime = prime_db_code.get_max_prime_in_db(prime_db_code.DATABASE)
        if max_prime is None:
            self.fail(f"{prime_db_code.DATABASE} is empty!")
        else:
            print(desc_prime_with_index(max_prime))


if __name__ == '__main__':
    unittest.main()
