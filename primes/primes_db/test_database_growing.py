import sqlite3
import unittest

from primes.cpu_write import yield_and_write_primes
from primes.primes_db import prime_db_code
from primes.shared_ph_pc import desc_prime_with_index


class DBTestCases(unittest.TestCase):
    def clear_test_db(self):
        with prime_db_code.get_connection(prime_db_code.TEST_DATABASE) as conn:
            conn.executescript(f"""
                DROP TABLE IF EXISTS primes;
                {prime_db_code.CREATION_COMMAND};
            """)
            print("Database cleared.")
            conn.executescript(prime_db_code.CREATION_COMMAND)
            conn.commit()


    def test_db_expands(self):
        self.clear_test_db()
        target_n = None
        max_prime_db = prime_db_code.get_max_prime_in_db(prime_db_code.TEST_DATABASE)
        if max_prime_db is None:
            target_n = 2
        else:
            target_n = max_prime_db[0] + 2

        for nth_prime, prime in yield_and_write_primes(
                target_n=target_n,
                db_to_connect_to=prime_db_code.TEST_DATABASE
        ):
            print(desc_prime_with_index((nth_prime, prime)))


    def test_simple(self):
        self.clear_test_db()
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
            print("Your prime database is empty.")

    def test_highest_main(self) -> tuple[int, int] | None:
        last_prime = prime_db_code.get_max_prime_in_db(prime_db_code.DATABASE)
        if last_prime is not None:
            print(last_prime)
            return last_prime
        else:
            print("Your prime database is empty.")
        return None

    def test_pragma(self, db: str = prime_db_code.DATABASE) -> None:
        """Just prints info about your database. Doesn't return anything."""
        with prime_db_code.get_connection(db) as conn:
            print("Database indexes info:",
                  conn.execute(f"""PRAGMA index_list(primes);""").fetchall())
            print("idx_primes_value info:",
                  conn.execute(f"""PRAGMA index_info(idx_primes_value);""").fetchall())


    def test_speed(self):
        print("This should be QUICK: Find the first prime number bigger than 5000000.")
        one_greater = prime_db_code.prime_1_after(5000000, db=prime_db_code.DATABASE)
        if one_greater is None:
            print("Not that many primes in the database.")
        else:
            print(f"{one_greater[0]}th prime: {one_greater[1]}")



if __name__ == '__main__':
    unittest.main()
