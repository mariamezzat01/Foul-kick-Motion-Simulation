# imports

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# inputs
try:
    u = float(input('Enter initial velocity (m/s): '))
    theta = float(input('Enter angle (deg): '))
except ValueError:
    print('Invalid input.')
else:
    theta = np.deg2rad(theta)

# variables decleration
g = 9.8                                             
t_flight = 2*u*np.sin(theta)/g
t = np.linspace(0, t_flight, 100)
x = u*np.cos(theta)*t
y = u*np.sin(theta)*t - 0.5*g*t**2

fig, ax = plt.subplots()
line, = ax.plot(x, y, color='k')


# initializing the soccer ball
xmin = x[0]
ymin = y[0]
xmax = max(x)
ymax = max(y)
xysmall = min(xmax,ymax)
circle = plt.Circle((xmin, ymin), radius=np.sqrt(xysmall))
ax.add_patch(circle)


# plotting simulation
def update(num, x, y, line, circle):
    line.set_data(x[:num], y[:num])
    circle.center = x[num],y[num]
    line.axes.axis([0, max(np.append(x,y)), 0, max(np.append(x,y))])

    return line,circle

ani = animation.FuncAnimation(fig, update, len(x), fargs=[x, y, line, circle],
                              interval=25, blit=True)

ani.save('projectile.gif')
plt.show()