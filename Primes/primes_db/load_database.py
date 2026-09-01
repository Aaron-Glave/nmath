"""Run this module from the nmath directory:
    python -m Primes.primes_db.load_database

This program imports all the prime numbers in your sprimelist.txt file to primes.db"""
import sqlite3
from pathlib import Path
from . import prime_db_code
from .. import main as prime_main


assert Path.cwd() == Path(__file__).parent.parent.parent

def add_list_to_db(insert_list: list[tuple[int, int]]):
    """Adds all the prime numbers in insert_list to primedatabase.DATABASE"""
    conn = prime_db_code.get_connection(prime_db_code.DATABASE)
    try:
        conn.executemany(
            """INSERT OR IGNORE INTO primes (nth_prime, prime) VALUES (?, ?)""",
            insert_list)
        conn.commit()
    except sqlite3.Error:
        conn.rollback()
        raise
    finally:
        prime_db_code.disconnect_specific_db(prime_db_code.DATABASE)

def main():
    try:
        n = 0
        insert_list = []
        prime_db_code.gen_db(prime_db_code.DATABASE)
        last_known_prime = prime_db_code.get_max_prime_in_db(prime_db_code.DATABASE)
        if last_known_prime is not None:
            print(f'Last known prime: {last_known_prime[0]}th prime number: {last_known_prime[1]}')
            input("Enter to continue")
        for nth_prime, prime in prime_main.yield_and_write_primes(list_all=True):
            n += 1
            if last_known_prime is not None and nth_prime > last_known_prime[0]:
                last_known_prime = (nth_prime, prime)
                #Add the prime we found to our list.
                insert_list.append(last_known_prime)
            elif last_known_prime is None:
                last_known_prime = (nth_prime, prime)
            if n % 2500 == 0:
                print(n, "primes read so far...")
            if len(insert_list) == 10000:
                add_list_to_db(insert_list)
                insert_list.clear()
                print("I imported nth_prime | prime to my database", nth_prime, "|", prime)
        #Cleanup phase: Make sure to post the remaining primes in the list to the database
        add_list_to_db(insert_list)
        insert_list.clear()
        assert last_known_prime is not None
        print("Last known prime is the ", last_known_prime[0], "th prime number: ",
              last_known_prime[1], sep="")
    finally:
        prime_db_code.disconnect_all()

if __name__ == "__main__":
    main()
