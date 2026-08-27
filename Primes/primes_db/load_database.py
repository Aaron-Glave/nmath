"""Run this module from the nmath directory:
    python -m Primes.primes_db.load_database

TODO: Import all the prime numbers in your sprimelist.txt file to primes.db
TODO: INSERT 2500 Primes into primes.db at a time..."""
from pathlib import Path
from Primes.primes_db import primedatabase
from Primes import main


assert Path.cwd() == Path(__file__).parent.parent.parent

n = 0
try:
    insert_list = []
    primedatabase.gen_db()
    last_known_prime = primedatabase.get_max_prime()
    for nth_prime, prime in main.yield_and_write_primes(list_all=True):
        if nth_prime > last_known_prime[0]:
            last_known_prime = (nth_prime, prime)
            #primedatabase.insert_prime(nth_prime, prime)
            #TODO ADD TO LIST
            insert_list.append(last_known_prime)
        n += 1
        if n % 2500 == 0:
            #TODO ADD ALL OF LIST TO DATABASE AND CLEAR IT
            conn = primedatabase.get_connection(primedatabase.DATABASE)
            with conn:
                conn.executemany(
                    """INSERT OR IGNORE INTO primes (nth_prime, prime_value) VALUES (?, ?)""",
                insert_list)
            insert_list.clear()
            primedatabase.end_connection(primedatabase.DATABASE)

            print("I imported nth_prime | prime to my database", nth_prime, "|", prime)


    assert last_known_prime is not None
    print("Last known prime is the ", last_known_prime[0], "th prime number: ",
          last_known_prime[1], sep="")
finally:
    primedatabase.disconnect()
