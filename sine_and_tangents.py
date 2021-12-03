import numpy as np
import matplotlib.pyplot as plt

lims_y = 4                                   # Limits on y-axis                
lims_x = 15                                  # Limits on x-axis
n_points = 10000                             # Density of tangent lines and resolution of the original curve
x = np.linspace(-lims_x, lims_x, n_points)   # Array of x points
y = np.sin(x)                                # Array of y points - your function is here
slopes = np.cos(x)                           # Array of slopes at point x - first derivative of your function

fig = plt.figure(figsize = (20,18))           # Chart object


plt.ylim(-lims_y,lims_y)                     # Assign limits of y-axis

plt.plot(x,y, c='black', lw = 2)             # Original line equation

clr = ['r','g','y']                          #Colorize lines if you want

for i in range(len(x)):
    y_min = slopes[i]*(x_min- x[i]) + y[i]   # Calculate y_min for a tangent line
    y_max = slopes[i]*(x_max- x[i]) + y[i]   # Calculate y_max for a tangent line
    
    cl = clr[i%len(clr)]                     # Pick a color
    
    plt.plot([x_min,x_max],[y_min,y_max], c=cl, alpha=0.1)   # plot tangent lines, alpha makes lines more transparent

plt.axis('off')
plt.show()
