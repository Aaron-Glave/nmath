#pylint:disable=E0401
from main import factor, factors_as_string
#pylint:enable=E0401

numtofactor = int(input("Number you want to factor? "))
print("Factors of", numtofactor, end=":\n")
print(factors_as_string(factor(numtofactor)))
