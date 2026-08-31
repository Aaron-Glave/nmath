from factorized import Factorized
from calculator import safe_eval

num_to_factor = safe_eval(input("Number you want to factor? "))
print("Factors of", num_to_factor, end=":\n")
print(Factorized(num_to_factor))
