#from Primes import main as primes
from Primes.main import factors_as_string, factor, yield_primes_memory
expression1 = '6*9*10'
expression2 = '6*9*10-3'
expression3 = '3*(6*3*10-1)'
print(factors_as_string(factor(537, method = yield_primes_memory)))
print(factors_as_string(factor(540, method = yield_primes_memory)))
assert 540 == eval(expression1)
assert 537 == eval(expression2)
#We know eval(expression1) - 3 == eval(expression2) just from basic math.
print('One way to get 537 is to subtract 3 from 540, meaning you evaluate ', expression2)
assert 537 == eval(expression3)
print('Or you can factor out a 3 and evaluate', expression3)
