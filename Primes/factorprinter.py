from main import factor, factors_as_string


numtofactor = int(input("Number you want to factor? "))
print("Factors of", numtofactor, end=":\n")
print(factors_as_string(factor(numtofactor)))
