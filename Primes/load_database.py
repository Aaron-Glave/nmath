import shutil

from primes_db import primedatabase
import main


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
