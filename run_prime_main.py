"""Make sure to run this in the nmath directory."""
from Primes import main as m

def fun_facts():
    A = 11 ** 10000
    SLIGHTLY_SMALLER_A = 11 ** (10000 - 6)
    print("Huge number:", A)
    print("Slightly smaller:", SLIGHTLY_SMALLER_A)
    B = A // SLIGHTLY_SMALLER_A
    print(B,
          "was calculated by dividing that huge number by a slightly smaller but still huge number."
          )
    print("It's _factors are", end=" ")
    print(m.Factorized(B))
    print(-15, "'s _factors are", sep="", end=" ")
    print(m.Factorized(-15))
    print(36, "'s _factors are", sep="", end=" ")
    print(m.Factorized(36))
    print(63, "'s _factors are", sep="", end=" ")
    print(m.Factorized(63))
    print(147, "'s _factors are", sep="", end=" ")
    print(m.Factorized(147), end="\n\n")

def last_prime_found():
    last_known_prime = m.get_max_prime()
    print("Last known prime is the ", last_known_prime[0], "th prime number: ",
          last_known_prime[1], sep="")


def factor_a_number():
    print(m.Factorized(m.get_int()))

def find_greater_prime():
    m.print_next_prime_greater(m.get_int())

def prime_main():
    try:
        fun_facts()
        print("I will ask you a series of questions about what you want to do.")
        print("Say Yes if you want to do the thing I asked you about.")
        if input("Want to know the last known prime I found? ").lower() == "yes":
            last_prime_found()
        elif input("Factor a number? ").lower() == "yes":
            factor_a_number()
        elif input(
                "Do you want to find a prime greater than a target number N?\n"
                + "Say Yes if so, then I'll ask you for your target number. "
        ).lower() == "yes":
            find_greater_prime()
        elif input("Are you looking for a the Nth prime number?\n").lower() == "yes":
            # Guess Nth prime
            print("Name N as the Nth prime number you want to guess")
            m.search_for_nth_prime(m.get_int())
        else:
            comments: dict[str, str] = {}
            next_prime_n, next_prime = next(m.correct_prime_guess(comments=comments))
            print(f"{next_prime_n}th prime number: {next_prime}",
                  comments['already_there'], sep='\n')
    finally:
        m.close_real_db()
