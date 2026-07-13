"""A single function to calculate statistical z-values"""

from statistics import NormalDist

def get_z_value(confidence_level):
    """Calculates a z-value such that:
    Integral from -infinity to z
      of the normal distribution
    equals the passed confidence level."""
    alpha = 1 - confidence_level
    # inv_cdf(p) calculates the inverse cumulative distribution function:
    # P(x < X) <= p
    return NormalDist().inv_cdf(1 - alpha / 2)

if __name__ == "__main__":
    print("The maximum you can pass is roughly 0.99999999999999")
    print("z-value for 0.9 confidence"
    " rounded to 3 digits:",
    round(get_z_value(0.9), 3))
    max_confidence_level = 0.99999999999999
    print("Maximum confidence level this code accepts:",
    max_confidence_level)
    print("Maximum computable z_value:",
    round(get_z_value(max_confidence_level)))
    yourval = get_z_value(
        float(input("Your turn. Enter a"
        " confidence level in [0.5, 1) ")))
    if input("Round? [y/n] ") == 'y':
        numdigits = int(input("Number of digits: "))
        print("Rounded Z value:",
           round(yourval, numdigits))
    else:
        print("Computed Z value:", yourval)
