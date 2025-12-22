from collections.abc import Callable
from typing import Tuple

def find_f_prime(f: Callable[[float], float]) -> Callable[[float], float]:
    """Accepts a function and returns an approximation of it derivative."""
    #Smaller deltas seem to cause more problems.
    delta = 1e-8
    def derivative_f(x: float) -> float:
        return round((f(x+delta) - f(x))/delta, ndigits=8)
    derivative_f.__doc__ = f"Approximate rate that {f.__name__} changes"
    derivative_f.__name__ = f"derivative_{f.__name__}"
    return derivative_f

def minimize(f: Callable[[float], float], initial_x: float,
             learning_rate: float = 0.1, max_iter: int = 1000) -> Tuple[float, float]:
    """Returns a tuple (x, y) where x is the location of the minimum value of the function and y is the minimum result.
    For functions with a bounded maximum, you can find the maximum by minimizing the negated version.
    Warning: Potentially the minimum could only be a local minimum!
    f: Function to minimize.
    initial_x: Initial guess for the function argument.
    learning_rate: Affects the speed at which the function approaches its minimum. Default value: 0.1
    max_iter: Number of steps in the loop to approach the minimum. Default value: 1000"""
    f_prime = find_f_prime(f)
    x = initial_x
    prints = 0
    for i in range(max_iter):
        gradient = f_prime(x)
        if prints > 0:
            print("Guess x gradient", x, gradient)
            prints -= 1
        x -= learning_rate*gradient
    return x, f(x)

def integrate(f, start, end, nsteps = 8):
    width = (end-start)/nsteps
    integral_left = sum(f(start + width*i)*width for i in range(nsteps))
    integral_right = sum(f(start + width*i)*width for i in range(1, nsteps+1))
    return integral_left, integral_right

if __name__ == '__main__':
    #I have to round in this program because I'm doing computer approximation.
    def x_quadratic(x: float):
        """Function to square numbers."""
        return (x-3)*(x+2)
    derivative_quadratic = find_f_prime(x_quadratic)
    print("Approximate derivative of (x-3)(x+2)at 10:", derivative_quadratic(10.0))
    #Minimum is when  2x -1 = 0
    #x = 1/2
    #f(x) = -(6+(1/4)) = -6.25
    
    solution_quadratic = minimize(x_quadratic, -100)
    solution_quadratic = (round(solution_quadratic[0], ndigits=7),
                          round(solution_quadratic[1], ndigits=7))
    print("Minimum of (x-3)(x+2):", solution_quadratic)
    help(derivative_quadratic)
    import math
    approx_sine = find_f_prime(math.cos)
    def sine_minus_one(x):
        return math.sin(x) - 1
    def negative_sine_plus_one(x):
        return -sine_minus_one(x)
    max_sine = minimize(negative_sine_plus_one, 3, learning_rate=0.1, max_iter=1000)
    estimate_pi_half = round(max_sine[0], ndigits=8)
    print("Maximum of sine - 1:", estimate_pi_half)
    assert estimate_pi_half - round(math.pi/2, ndigits=8) == 0
    print("I figured out pi/2!")
    
