"""Prints out the longest decimal representation of a prime number under 1000."""

import os
import sys

#pylint:disable=C0413
print("Current path:", os.path.abspath(os.path.curdir))
parentpath = os.path.dirname(os.path.dirname(__file__))
print('Parent path:', parentpath)
sys.path.append(parentpath)
#PYLINT:ENABLE=C0413
import main as primegenerator
import long_repeating_decimal

denominators = [
    prime_tuple[-1]
    for prime_tuple in
    primegenerator.correct_prime_guess(999, list_all=True)
]
inverses = [
    long_repeating_decimal.DecimalRepresentationOfFrac(
        1, demonitator) for demonitator in denominators
]
print(repr(inverses[-1])) #Use this to see the inverses of all known primes
original_fractions = list(inverses)
if original_fractions is not inverses:
    print("Made a copy before sorting.")
inverses.sort(key=lambda f: len(f.repeating_string()), reverse=True)
#for fraction in inverses[:5]:
#    fraction_string = fraction.repeating_string()
#    print(repr(fraction), "has a string of", len(fraction.repeating_string()),
#         "characters:", fraction.repeating_string())
#print("\n")
#print(Fraction(original_fractions[-1].upper, original_fractions[-1].lower),
#      "has a string of", len(original_fractions[-1].repeating_string()), "characters.\n")

print("\nOriginal prime list:")
for i in range(0, 5):
    print(repr(original_fractions[-1 - i]),
          "with", len(original_fractions[-1 - i].repeating_string()), 'digits.')

print("\nCalculated prime list:")
for i in range(0, 5):
    print(repr(inverses[i]),
          "with", len(inverses[i].repeating_string()), 'digits.')

assert all(len(inverses[_a_index].repeating_string())
           >= len(inverses[_a_index+1].repeating_string())
           for _a_index in range(len(inverses)-1))
print()
for i in range(0, 5):
    for j in range(0, 5):
        if original_fractions[-1 - i]  == inverses[j]:
            print(
                repr(original_fractions[-1 - i]),
                  "is one of the last 5 integers in the original list and one of the top 5 longest!"
            )

print("\nThe largest repeating decimal string representing an inverse of a prime number under 1000 is",
      repr(inverses[0]),
      end=":\n")
print(inverses[0])
print("It has", len(inverses[0].repeating_string()), "digits!")
