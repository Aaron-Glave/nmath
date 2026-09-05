from . import prime_db_code


def reset_test_database():
    with prime_db_code.get_connection(prime_db_code.TEST_DATABASE) as conn:
        conn.executescript(f"""
            DROP TABLE IF EXISTS primes;
            {prime_db_code.CREATION_COMMAND};
        """)
        print("Database cleared.")
        conn.executescript(prime_db_code.CREATION_COMMAND)
        conn.commit()
