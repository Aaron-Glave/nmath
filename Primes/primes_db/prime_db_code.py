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


def insert_prime(nth_prime, prime, db: str):
    verify_real_db(db)
    with sqlite3.connect(db) as conn:
        insert_prime_with_connection(nth_prime, prime, conn)


def get_min_prime_in_db(db: str) -> tuple[int, int] | None:
    with get_connection(db) as conn:
        return conn.execute(f"""
            SELECT nth_prime, prime FROM primes
            ORDER BY nth_prime ASC
            LIMIT 1
        """).fetchone()


def get_nth_prime_in_db(nth_prime: int, db: str) -> tuple[int, int] | None:
    with get_connection(db) as conn:
        return conn.execute("""
            SELECT nth_prime, prime FROM primes
            WHERE nth_prime = ?""", (nth_prime,)).fetchone()


def get_max_prime_in_db(db: str) -> tuple[int, int] | None:
    with get_connection(db) as conn:
        return conn.execute(f"""
            SELECT nth_prime, prime FROM primes
            ORDER BY nth_prime DESC
            LIMIT 1
        """).fetchone()


def read_all_prime_records(connection: sqlite3.Connection) -> sqlite3.Cursor:
    """Loops through all prime numbers in the database.
    Returns a sqlite3.Cursor object."""
    return connection.execute("""
    SELECT nth_prime, prime
    FROM primes
    ORDER BY nth_prime ASC;""")


def all_primes_skip_first_n(
        num_to_skip: int, connection: sqlite3.Connection
) -> sqlite3.Cursor:
    """Loops through all primes after the first num_to_skip"""
    return connection.execute("""
    SELECT nth_prime, prime
    FROM primes
    WHERE nth_prime > ?
    ORDER BY nth_prime ASC;""", (num_to_skip,))


def first_prime_greater(lower_bound: int, db: str) -> tuple[int, int]:
    with get_connection(db) as conn:
        return conn.execute("""
        SELECT nth_prime, prime
        FROM primes
        WHERE prime > ?
        ORDER BY prime ASC
        LIMIT 1;""", (lower_bound,)).fetchone()


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
    last_prime = get_max_prime_in_db(TEST_DATABASE)
    if last_prime is not None:
        print("Final prime:", )
    else:
        raise sqlite3.ProgrammingError("Empty database! Shouldn't happen!")


def test_lowest_main():
    last_prime = get_min_prime_in_db(DATABASE)
    if last_prime is not None:
        print(last_prime)
    else:
        print("Your prime database is empty.")


def test_highest_main() -> tuple[int, int] | None:
    last_prime = get_max_prime_in_db(DATABASE)
    if last_prime is not None:
        print(last_prime)
        return last_prime
    print("Your prime database is empty.")
    return None


def test_pragma(db: str) -> None:
    """Just prints info about your database. Doesn't return anything."""
    with get_connection(db) as conn:
        print("Database indexes info:", conn.execute("PRAGMA index_list(primes);").fetchall())
        print("idx_primes_value info:",
              conn.execute("PRAGMA index_info(idx_primes_value);").fetchall())


def all_tests():
    test_simple()
    test_highest_main()
    test_lowest_main()
    test_pragma(db=DATABASE)
    print("This should be QUICK: Find the first prime number bigger than 5000000.")
    print(first_prime_greater(5000000, db=DATABASE))

if __name__ == "__main__":
    all_tests()
