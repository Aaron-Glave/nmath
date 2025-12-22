import main
numtofactor = int(input("Number you want to factor? "))
print("Factors of", numtofactor, end=":\n")
main.print_factors(main.factor(numtofactor))
