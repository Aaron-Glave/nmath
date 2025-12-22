from math import e, factorial

fx = lambda x: (x**3)+(x**2)+x+1
fpx = lambda x: 3*x**2+2*x+1
fppx = lambda x: 6*x + 2
fpppx = lambda x: 6
def function_lieb3(x, a):
    gap = (x-a)
    return fx(a) + gap*fpx(a) + ((gap**2)/2)*fppx(a) + ((gap**3)/factorial(3))*fpppx(a)

if __name__ == "__main__":
    print("math.e minus estimation of e via Taylor series:", e-sum(1/factorial(n) for n in range(0,1000)))
    print("Sorry, computers aren't great at representing non-integers without rounding.")
    print("Value to compute x^3 + x^2 + x + 1 with: ")
    _x = int(input("Integer to calculate with: "))
    _a = fx(_x)
    _b = int(function_lieb3(_x, 3))
    print("Should be equal:", _a, _b)
    assert _a == _b
    print("They are.")
    print("Since 3x^2+2x+1 is never 0, the polynomial has no local minimum point.",
          "It's always increasing!",
          "It increases slowest at -1/3.",sep='\n')
    assert (fpx(-1/3+0.1) > fpx(-1/3)) and (fpx(-1/3-0.1) > fpx(-1/3))
    assert fppx(-1/3) == 0
