import matplotlib.pyplot as plt
import numpy as np
    
xaxis = np.linspace(0, np.pi * 2, 100)
yaxis = np.sin(xaxis) + 0.4
plt.xlabel('x')
plt.plot(xaxis, yaxis)
plt.ylabel('sin(x)+0.4')
#Credit: https://stackoverflow.com/questions/33382619/plot-a-horizontal-line-on-a-given-plot
yaxis2 = np.linspace(-0.6, -0.6, 100)
plt.plot(xaxis, yaxis2, color='r')
yaxis3 = np.linspace(1.4, 1.4, 100)
plt.plot(xaxis, yaxis3, color='g')
plt.show()
