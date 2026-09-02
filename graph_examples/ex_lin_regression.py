"""Linear regression model!"""


import numpy as np
import matplotlib.pyplot as plt


class LinearRegression:
    """Create a linear regression model based on 2 arrays.
    Note that the 2 arrays must have the same length."""
    def __init__(self, xpoints: list[float], ypoints: list[float]):
        """Args: xpoints, ypoints"""
        self.xpoints = xpoints
        self.ypoints = ypoints
        self.n = len(xpoints)
        assert len(ypoints) == self.n
        sum_x = sum(xpoints)
        sum_y = sum(ypoints)
        sum_xy = np.sum(np.fromiter(
            map(lambda xpoint, ypoint: xpoint * ypoint,
                xpoints, ypoints), dtype=float, count=self.n)
        )
        sum_x_squared = np.sum(np.fromiter(
                map(lambda xpoint: xpoint**2, xpoints), dtype=float, count=self.n)
        )
        self.b = (sum_xy - sum_x*sum_y/self.n)/(sum_x_squared - sum_x**2/self.n)
        self.a = (sum_y - self.b*sum_x)/self.n

    def __call__(self, x_used_to_estimate: float) -> float:
        """Returns an estimate for y based on a given x"""
        return self.b*x_used_to_estimate + self.a

    def r_squared(self) -> float:
        ss_res = sum((self.ypoints[i] - self(self.xpoints[i]))**2 for i in range(self.n))
        observed_mean = sum(self.ypoints) / self.n
        ss_tot = sum((self.ypoints[i] - observed_mean)**2 for i in range(self.n))
        return 1 - (ss_res/ss_tot)


if __name__ == '__main__':
    _xpoints = [5, 9, 10, 3, 5, 7]
    _ypoints = [6, 11, 6, 4, 6, 9]
    estimator = LinearRegression(_xpoints, _ypoints)
    xaxis = np.linspace(1, 10, 100)
    yaxis = [estimator(x) for x in xaxis]
    print("Estimated y = b*x + a")
    print('a:', estimator.a)
    print('b:', estimator.b)
    print("R^2:", estimator.r_squared())
    plt.title("Linear Regression from https://www.youtube.com/watch?v=YC0bvIxR6t4")
    plt.plot(xaxis, yaxis, color='r')
    plt.plot(_xpoints, _ypoints, marker='o', color='k', linestyle='')
    plt.show()
