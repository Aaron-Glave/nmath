"""Just simple questions you can ask about the primes you know."""

from . import main

def simple_main():
    print("I will ask you a series of questions about what you want to do.")
    print("Say Yes if you want to do the thing I asked you about.")
    if input("Generate text file of all primes less than 100? ").lower() == "yes":
        main.primes_up_to100()
    elif input(
            "Do you want to know the biggest gap between prime numbers you know? "
    ).lower() == "yes":
        _biggest_gap = main.largest_gap_of_primes()
        main.say_gap_message(_biggest_gap)
    elif input(
            "Do you want to find the first gap of 100 primes? "
    ).lower() == "yes":
        main.say_gap_of_100()
    elif input(
            "Do you want to know the chance a random number isn't fully divisible"
            " by the primes you know? ").lower() == "yes":
        print(main.percent_integers_unknown_factors() * 100,
              "% of numbers aren't divisible by any of the primes you know.", sep='')

if __name__ == '__main__':
    simple_main()
