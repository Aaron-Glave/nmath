"""A single function to calculate statistical z-values"""

from statistics import NormalDist

def get_z_value(confidence_level):
    """Calculates a z-value such that:
    Integral from -infinity to z
      of the normal distribution
    equals the passed confidence level."""
    alpha = 1 - confidence_level
    # inv_cdf(p) calculates the inverse cumulative distribution function;
    # P(x < X) <= p
    return NormalDist().inv_cdf(1 - alpha / 2)

if __name__ == "__main__":
    print("The maximum you can pass is roughly 0.99999999999999")
    print(round(get_z_value(0.9), 3))
    print(round(get_z_value(0.99999999999999)))
