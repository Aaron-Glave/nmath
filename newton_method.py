"""Use Newton's method to solve an equation"""


def newton_method(initial, f, fprime,
maxsteps=1000):
    """Returns a tuple[float, int]:
       0: the x-value solution,
       1: the number of steps I took."""
    x = initial
    x2 = None
    n_steps = 0
    while n_steps < maxsteps:
        x2 = x - f(x)/fprime(x)
        if x2 == x:
            break
        x = x2
        n_steps += 1
    return x, n_steps

if __name__ == '__main__':
    from math import sin, cos, pi
    print("Using Netwon's method to find x where sin(x)=0")
    solution = newton_method(3, sin, cos)
    if solution[0] == pi:
        print("I found", pi, "after",
        solution[1], "steps!")
    else:
        print("Estimate:", solution[0])
