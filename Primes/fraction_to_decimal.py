"""A function to create a fraction represented by a long, possibly repeating decimal."""
import long_repeating_decimal

def decimal_representation_of_fraction(
        top_question: str = "Number to divide? ",
        bottom_question: str = "Divisor? ",
):
    upper = int(input(top_question))
    lower = int(input(bottom_question))
    if lower == 0:
        raise ValueError("Can't divide by 0.")
    return upper, lower

if __name__ == "__main__":
    print("Result:", long_repeating_decimal.DecimalRepresentationOfFrac(
        *decimal_representation_of_fraction()
    ))
