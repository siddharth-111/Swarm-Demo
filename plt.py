import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import math


# Fixing random state for reproducibility
# np.random.seed(19680801)

fig = plt.figure(figsize = (5,5))
fig.add_subplot(20,20,1)

axes = fig.add_subplot(111)
axes.set_xlim(1, 20)
axes.set_ylim(1, 20)

N = 2
x = np.random.uniform(low=1, high=20, size=N)
y = np.random.uniform(low=1, high=20, size=N)

# collections = []

# for i, (x_c, y_c ) in enumerate(zip(x, y)):
# 	ax, = axes.plot(x_c,y_c, 'go')
# 	collections.append(ax)

sc = axes.scatter(x,y)

# def init():
#     return collections

# def animate(i):
#     #animate lines
#     collections[0].set_data([], [])
#     for i in range(10):
#     	plt.pause(0.5)
#     	collections[0].set_data([5, 2], [3, i])
    	
#     return collections

# anim = FuncAnimation(fig, animate, 1, init_func=init, interval=1000, repeat = False)

center = [10, 10]

def distance_magnitude(x,y):
	#calculate magnitude of distance vector
	return math.sqrt(x*x+y*y)
	pass


def distance_vector(P1,P2):
	#calculate distance in vector between two Point
	x = P1[0]-P2[0]
	y = P1[1]-P2[1]
	return x,y
	pass

def init():
    return sc

def animate(i, center):

    x_dist, y_dist = distance_vector([x[0], y[0]], center)

    distance = distance_magnitude(x_dist, y_dist)

    

    while distance > 0.1:
    	loc_x = x_dist/10
    	loc_y = y_dist/10

    	x[0] = x[0] - loc_x
    	y[0] = y[0] - loc_y
 
    	sc.set_offsets(np.c_[x,y])
    	x_dist, y_dist = distance_vector([x[0], y[0]], center)
    	distance = distance_magnitude(x_dist, y_dist)
    	plt.pause(0.0001)
    	pass

    return sc

anim = FuncAnimation(fig, animate, 1, init_func=init, interval=100, repeat = False, fargs = (center,))


# ani = FuncAnimation(fig, ani, frames=range(0,4), interval=1000, repeat=False)

# def animate_multi(j):
# 	def anim(coords):
# 		point.set_data([1, ],[coords[1]])
# 		return point

# 	def frames():
# 		for i, (x_c, y_c ) in enumerate(zip(x, y)):
# 			yield i,2

# 	anim = FuncAnimation(fig, anim,
#                                frames=frames, interval=100, blit=True,repeat=False)


# for j in range(5):
# 	try:
# 		print('Working on plot', j)
# 		animate_multi(j)
# 	except KeyboardInterrupt:
# 		plt.close()

# area = (30 * 1)**2  # 0 to 15 point radii

# axes.scatter(x, y, 20, color='red', alpha=0.5)


# d = axes.collections[0]

# print(d[0])

# d.set_offset_position('data')

# print(d.get_offsets()[0])


plt.show()
