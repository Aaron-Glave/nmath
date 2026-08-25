"""Defines a constant for pi with 314 decimal points"""
from math import pi


PI_STR = ("3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803"
          "4825342117067982148086513282306647093844609550582231725359408128481117450284102701938521"
          "1055596446229489549303819644288109756659334461284756482337867831652712019091456485669234"
          "6034861045432664821339360726024914127372458700660631")
FLOAT_APPROX_PI = float(PI_STR)
if __name__ == '__main__':
    print("First 314 decimal points of Pi:", PI_STR)
    if FLOAT_APPROX_PI == pi:
        print('\nThe First 314 decimal points' ,
        'of pi are good enough,',
        'according to Python on this computer!')
    else:
        print("Missed pi by approximately", pi - FLOAT_APPROX_PI)
