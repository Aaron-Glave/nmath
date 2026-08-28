"""Hopefully a faster storage base for your prime numbers.
"""
import atexit
import sqlite3
from pathlib import Path

MYDIR = Path(__file__).resolve().parent
_connections: dict[str, sqlite3.Connection] = {}
DATABASE = str((Path(MYDIR) / 'primes.db').resolve())
TEST_DATABASE = str((Path(MYDIR) / 'tprimes.db').resolve())
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
    if db in _connections:
        return _connections[db]
    _connections[db] = sqlite3.connect(db)
    return _connections[db]


def gen_db(database_name: str):
    verify_real_db(database_name)
    with get_connection(database_name) as conn:
        cursor = conn.cursor()
        cursor.executescript(CREATION_COMMAND)
        conn.commit()

def disconnect_specific_db(db: str) -> None:
    conn = _connections.pop(db, None)
    if conn is not None:
        conn.close()

@atexit.register
def disconnect_all():
    for db in _connections.values():
        db.close()
    _connections.clear()


def insert_prime_with_connection(
        nth_prime: int, prime: int, conn: sqlite3.Connection
):
    conn.execute(f"""
            INSERT INTO primes (nth_prime, prime)
            VALUES (?, ?)
            ON CONFLICT (nth_prime) DO NOTHING;""", (nth_prime, prime))
    conn.commit()

def insert_prime(nth_prime, prime, db=DATABASE):
    verify_real_db(db)
    with sqlite3.connect(db) as conn:
        insert_prime_with_connection(nth_prime, prime, conn)


def get_max_prime(db: str) -> tuple[int, int] | None:
    with get_connection(db) as conn:
        return conn.execute(f"""
            SELECT nth_prime, prime FROM primes
            ORDER BY nth_prime DESC
            LIMIT 1
        """).fetchone()


def read_all_prime_records(connection: sqlite3.Connection) -> sqlite3.Cursor:
    return connection.execute("""
    SELECT nth_prime, prime
    FROM primes
    ORDER BY nth_prime ASC;""")


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
    last_prime = get_max_prime(TEST_DATABASE)
    if last_prime is not None:
        print("Final prime:", )
    else:
        raise sqlite3.ProgrammingError("Empty database! Shouldn't happen!")

def test_highest_main():
    last_prime = get_max_prime(DATABASE)
    if last_prime is not None:
        print(last_prime)
    else:
        print("Your prime database is empty.")


if __name__ == '__main__':
    try:
        test_simple()
        test_highest_main()
    finally:
        disconnect_all()
