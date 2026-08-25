"""Defines a constant for pi with 314 decimal points"""
from math import pi


#pylint:disable=C0301
#pylint:disable=C0103
pi_str = "3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196442881097566593344612847564823378678316527120190914564856692346034861045432664821339360726024914127372458700660631"
#pylint:enable=C0301
float_pi_str = float(pi_str)
if __name__ == '__main__':
    print(pi_str)
    if float_pi_str == pi:
        print('\nThe First 314 decimal points' ,
        'of pi are good enough,',
        'according to Python on this computer!')
    else:
        print("Missed pi by approximately", pi-eval(pi_str))
#pylint:enable=C0103
