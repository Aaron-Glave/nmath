import os
import sys

fluxx_path = os.path.dirname(os.path.realpath(__file__))
print(fluxx_path)
prime_path = fluxx_path + "\\Primes"
print(prime_path)
sys.path.append(prime_path)
#os.chdir(os.getcwd()+prime_path)
from main import factor, factors_as_string
#help(main)
expression1 = '6*9*10'
#expression2 = '6*9*10-3'
expression3 = '3*(6*3*10-1)'
print(factor(537))
print(factors_as_string(factor(540)))
assert 540 == eval(expression1)
assert 537 == eval(expression1) - 3
print('One way to get 537 is to subtract 3 from 540, meaning you evaluate (', expression1,')-3', sep='')
assert 537 == eval(expression3)
print('Or you can factor out a 3 and evaluate', expression3)
