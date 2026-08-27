"""Run this module from the nmath directory:
    python -m Primes.primes_db.load_database

TODO: Import all the prime numbers in your sprimelist.txt file to primes.db"""
from pathlib import Path
from Primes.primes_db import primedatabase
from Primes import main


input(f"cd: {Path.cwd()}. Should run in {Path(__file__).absolute().parent.parent.parent}"
      f"Cancel if they don't match, hit Enter if they do.")
assert Path.cwd() == Path(__file__).parent.parent.parent

n = 0
try:
    primedatabase.gen_db()
    last_known_prime = primedatabase.get_max_prime()
    for nth_prime, prime in main.yield_and_write_primes(list_all=True):
        if nth_prime > last_known_prime[0]:
            last_known_prime = (nth_prime, prime)
            primedatabase.insert_prime(nth_prime, prime)
        n += 1
        if n % 2500 == 0:
            print("I imported nth_prime | prime to my database", nth_prime, "|", prime)

    assert last_known_prime is not None
    print("Last known prime is the ", last_known_prime[0], "th prime number: ",
          last_known_prime[1], sep="")
finally:
    primedatabase.disconnect()
