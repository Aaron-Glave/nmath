"""Hopefully a faster storage base for your prime numbers.
TODO: Import all the prime numbers in your sprimelist.txt file to primes.db"""
import atexit
import sqlite3

_connections: dict[str, sqlite3.Connection] = {}
DATABASE = 'primes.db'
TEST_DATABASE = 'tprimes.db'
CREATION_COMMAND = (
    """CREATE TABLE IF NOT EXISTS primes (
    nth_prime INTEGER NOT NULL PRIMARY KEY,
    prime INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_primes_value on primes (prime);""")


def verify_real_db(db: str):
    assert db in (DATABASE, TEST_DATABASE)


def get_connection(db: str):
    verify_real_db(db)
    if db not in _connections:
        _connections[db] = sqlite3.connect(db)
    return _connections[db]


def gen_db():
    with get_connection(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.executescript(CREATION_COMMAND)
        conn.commit()


@atexit.register
def disconnect():
    for db in _connections.values():
        db.close()


def insert_prime(nth_prime, prime, db=DATABASE):
    verify_real_db(db)
    with sqlite3.connect(db) as conn:
        conn.execute(f"""
        INSERT INTO primes (nth_prime, prime)
        VALUES (?, ?)
        ON CONFLICT (nth_prime) DO NOTHING;""", (nth_prime, prime))
        conn.commit()


def get_max_prime(db=DATABASE) -> tuple[int, int] | None:
    with get_connection(db) as conn:
        return conn.execute(f"""
            SELECT nth_prime, prime FROM primes
            ORDER BY nth_prime DESC
            LIMIT 1
        """).fetchone()


def test_simple():
    with get_connection(TEST_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.executescript(CREATION_COMMAND)
        conn.commit()

    insert_prime(1, 2, db=TEST_DATABASE)
    insert_prime(2, 3, db=TEST_DATABASE)
    rlist = []
    with get_connection(TEST_DATABASE) as conn:
        rlist = cursor.execute('SELECT nth_prime, prime FROM primes').fetchall()
    print(rlist)
    print("Final prime:", get_max_prime(TEST_DATABASE))


if __name__ == '__main__':
    try:
        test_simple()
    finally:
        disconnect()
