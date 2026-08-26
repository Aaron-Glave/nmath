"""Hopefully a faster storage base for your prime numbers."""
import sqlite3

CREATION_COMMAND = (
"""CREATE TABLE IF NOT EXISTS primes (
    nth_prime INTEGER NOT NULL PRIMARY KEY,
    prime_n INTEGER NOT NULL
)
CREATE INDEX IF NOT EXISTS idx_primes_value on primes (prime_n)""")

def gen_db():
    with sqlite3.connect('primes.db') as conn:
        cursor = conn.cursor()
        cursor.execute(CREATION_COMMAND)

def test_simple():
    with sqlite3.connect('tprimes.db') as conn:
        cursor = conn.cursor()
