from Primes.main import factor, factors_as_string

num_to_factor = int(input("Number you want to factor? "))
print("Factors of", num_to_factor, end=":\n")
print(factors_as_string(factor(num_to_factor)))
