"""Hopefully a faster storage base for your prime numbers.
"""
import atexit
import sqlite3
import logging
import time
from pathlib import Path

MYDIR = Path(__file__).resolve().parent
_connections: dict[str, sqlite3.Connection] = {}
DATABASE = str((Path(MYDIR) / 'primes.db').resolve())
TEST_DATABASE = str((Path(MYDIR) / 'tprimes.db').resolve())
CREATION_COMMAND = """CREATE TABLE IF NOT EXISTS primes (
    nth_prime INTEGER NOT NULL PRIMARY KEY,
    prime INTEGER NOT NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_primes_value ON primes (prime);"""


def make_prime_column_unique(db: str) -> None:
    """Makes the prime column unique."""
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    logger.info("Checking %s for duplicate prime values...", db)

    with get_connection(db) as conn:
        duplicate = conn.execute("""
            SELECT prime, COUNT(*) AS occurrences
            FROM primes
            GROUP BY prime
            HAVING COUNT(*) > 1
            LIMIT 1
        """).fetchone()

        if duplicate is not None:
            prime, occurrences = duplicate
            raise sqlite3.IntegrityError(
                f"Cannot create unique index: {prime=} appears {occurrences} times."
            )

        logger.info("No duplicates found. Replacing index idx_primes_value...")

        conn.execute("DROP INDEX IF EXISTS idx_primes_value")

        started_at = time.perf_counter()
        last_message_at = started_at
        callback_count = 0

        def report_progress() -> int:
            nonlocal last_message_at, callback_count

            callback_count += 1
            now = time.perf_counter()

            if now - last_message_at >= 2:
                logger.info(
                    "Still creating unique index; elapsed %.1f seconds "
                    "(progress callbacks: %d).",
                    now - started_at,
                    callback_count,
                )
                last_message_at = now

            return 0  # 0 = allow SQLite to continue

        conn.set_progress_handler(report_progress, 100_000)

        try:
            conn.execute("""
                CREATE UNIQUE INDEX idx_primes_value
                ON primes (prime)
            """)
        finally:
            conn.set_progress_handler(None, 0)

        logger.info(
            "Unique index created successfully in %.2f seconds.",
            time.perf_counter() - started_at,
        )

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


def prime_that_equals(guess: int, db: str) -> tuple[int, int] | None:
    """Returns the index of the passed prime if it's there, or else None."""
    with get_connection(db) as conn:
        return conn.execute("""
        SELECT nth_prime, prime
        FROM primes
        WHERE prime = ?
        ORDER BY prime ASC
        LIMIT 1;""", (guess,)).fetchone()


def prime_1_after(lower_bound: int, db: str) -> tuple[int, int] | None:
    """Returns the first prime greater than the given lower bound."""
    with get_connection(db) as conn:
        return conn.execute("""
        SELECT nth_prime, prime
        FROM primes
        WHERE prime > ?
        ORDER BY prime ASC
        LIMIT 1;""", (lower_bound,)).fetchone()


def delete_all_primes_after(lower_bound: int, db: str) -> tuple[int, int] | None:
    with get_connection(db) as conn:
        return conn.execute("""
        DELETE FROM primes
        WHERE prime > ?
        """, (lower_bound,)).fetchone()
