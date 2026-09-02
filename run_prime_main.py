"""Make sure to run this in the nmath directory."""
from primes.factorized import Factorized
from primes import main as m
from pathlib import Path
import os


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
    print(Factorized(B))
    print(-15, "'s _factors are", sep="", end=" ")
    print(Factorized(-15))
    print(36, "'s _factors are", sep="", end=" ")
    print(Factorized(36))
    print(63, "'s _factors are", sep="", end=" ")
    print(Factorized(63))
    print(147, "'s _factors are", sep="", end=" ")
    print(Factorized(147), end="\n\n")


def last_prime_found() -> tuple[int, int]:
    last_known_prime = m.get_max_prime()
    print("Last known prime is the ", last_known_prime[0], "th prime number: ",
          last_known_prime[1], sep="")
    return last_known_prime


def factor_a_number():
    print(Factorized(m.get_int()))


def find_greater_prime():
    m.print_next_prime_greater(m.get_int())


def find_nth_prime():
    # Guess Nth prime
    print("Name N as the Nth prime number you want to guess")
    m.search_for_nth_prime(m.get_int())


def find_next_prime():
    comments: dict[str, str] = {}
    last_known_prime = last_prime_found()
    for next_prime, prime in m.correct_prime_guess(comments=comments):
        if prime > last_known_prime[1]:
            print(f"{next_prime}th prime number: {prime}",
                  comments['already_there'], sep='\n')
            return
    return


def cd_and_generate():
    folder = Path(__file__).resolve().parent
    prime_dir = folder / 'primes'
    os.chdir(prime_dir.resolve())
    m.primes_up_to100()
    os.chdir(folder.resolve())


def say_biggest_gap():
    _biggest_gap = m.largest_gap_of_primes()
    m.say_gap_message(_biggest_gap)
    print(f"Subtracting the {_biggest_gap[0][0][0]}th prime from"
          f"the {_biggest_gap[0][1][0]}th prime yields exactly 100.\n",
          f"{_biggest_gap[0][1][1]} - {_biggest_gap[0][0][1]} = {_biggest_gap[1]}",
          sep='', end=".\n")


def probability_to_factor():
    print(m.percent_integers_unknown_factors() * 100,
          "% of numbers aren't divisible by any of the primes you know.", sep='')


def prime_main():
    try:
        fun_facts()
        options = []
        print("I will give you an indexed list of possible actions.")
        #print("Say Yes if you want to do the thing I asked you about.")
        options.append(("Tell me the last known prime I found", last_prime_found))
        options.append(("Factor a number", factor_a_number))
        options.append(("Find a prime greater than a target number N", find_greater_prime))
        options.append(("Find the Nth prime number", find_nth_prime))
        options.append(("Find the next highest prime number", find_next_prime))
        options.append(("Generate text file of all primes less than 100 in the primes folder",
                        cd_and_generate))
        options.append(("Find the biggest gap between prime numbers you know", say_biggest_gap))
        options.append(
            ("Find the first gap of 100 between adjacent prime numbers", m.say_gap_of_100))
        options.append(("Find the probability that a random integer isn't fully divisible"
                        "by the primes you know", probability_to_factor))
        i = 0
        for option in options:
            print(i + 1, options[i][0], sep=": ")
            i += 1
        print()
        i = int(input("Type the number corresponding to what you want to do. "))
        options[i - 1][1]()
    finally:
        m.close_db()


if __name__ == "__main__":
    prime_main()
