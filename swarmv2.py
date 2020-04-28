
from graphics import * #using library from mcsp.wartburg.edu/zelle/python/graphics.py
from queue import Queue
import time
import threading
import math
import json
from random import randint

lock = threading.Lock()



def draw_windows(w,h):
	#create windows
	print('create windows with name : swarm, width : ',w,', height : ',h)
	return GraphWin('swarm',w,h)
	pass

def draw_center(win):
	center = Point(win.getWidth()/2,win.getHeight()/2)
	center.draw(win)

	return center
	pass


def distance_magnitude(x,y):
	#calculate magnitude of distance vector
	return math.sqrt(x*x+y*y)
	pass

def distance_vector(P1,P2):
	#calculate distance in vector between two Point
	x = P1.getX()-P2.getX()
	y = P1.getY()-P2.getY()
	return x,y
	pass

def relative_distance(robot,robots):
	#calculate relative distance of a robot to all other robots
	x_total=0
	y_total=0
	for r in robots:
		x,y = distance_vector(robot.getCenter(),r.getCenter())
		x_total+=x
		y_total+=y
		pass
	return x_total,y_total
	pass

def relative_distance_to_center(robot,center):
	#calculate relative distance of a robot to all other robots
	x_total=0
	y_total=0

	x,y = distance_vector(robot.getCenter(),center)
	x_total+=x
	y_total+=y

	return x_total,y_total
	pass



def draw_swarm(n,win):
	#draw n number of robot in window win
	
	robot = []
	for x in range(0,n):
		robot.append(Circle(Point(randint(20,win.getWidth()-20),randint(20,win.getHeight()-20)),10))
		# print('create robot with number ',x,' point x : ',x*200+40,', y : 200 , r : 20')
		robot[x].setFill('red')
		robot[x].draw(win)
		pass
	return robot
	pass

def move_robots(robots):
	for r in robots:
		x,y = relative_distance(r,robots)
		distance = distance_magnitude(x, y)
		while distance>40.5:
			loc_x = -x/10.0
			loc_y = -y/10.0
			r.move(loc_x,loc_y)
			x,y = relative_distance(r,robots)
			distance = distance_magnitude(x, y)
			time.sleep(0.02)
			pass
		pass
	pass


def move_robot(r, loc_x, loc_y):
	if not actions.empty():
		action, *arguments = actions.get()
		action(*arguments)
	pass



def meeting_point(r,center,uDistance):
	x,y = relative_distance_to_center(r,center)
	distance = distance_magnitude(x, y)
	while distance>uDistance:
		loc_x = -x/10.0
		loc_y = -y/10.0
		r.move(loc_x, loc_y)
		x,y = relative_distance_to_center(r,center)
		distance = distance_magnitude(x, y)
		time.sleep(0.0005)
		pass
	pass


def update_center_line(center):
	center.move(0, 20)
	pass

def update_center_rhombus(center, index, interval):

	if(index >= interval[0]['min'] and index < interval[0]['max']):
		center.move(-20, 20)
	elif(index >= interval[1]['min'] and index < interval[1]['max']):
		center.move(20, 20)
	elif(index >= interval[2]['min'] and index < interval[2]['max']):
		center.move(20, -20)
	else:
		center.move(-20, -20)	
	pass

def update_interval(start, interval, counter):

	holder = start
	
	for current in interval:
		current['min'] = holder
		current['max'] = holder + counter
		holder += counter

	pass

def create_rhombus(robots, center, interval):
	uDistance = 0.5

	counter = 1
	lastIndex = 3

	for index,r in enumerate(robots):
		meeting_point(r, center, uDistance)
		update_center_rhombus(center, index, interval)

		if(index == lastIndex):
			counter += 1
			lastIndex += counter * 4

			update_interval(index + 1, interval, counter)
			center.move(0, -20)
	pass

def create_line(robots, center, win):
	uDistance = 0.5
	for index,r in enumerate(robots):
		meeting_point(r, center, uDistance)
		update_center_line(center)
	pass
	pass


def main():
	#main program
	win = draw_windows(700,600) #draw window with width = 700 and height = 600

	center = draw_center(win)
	robots = draw_swarm(40,win) #draw swarm in win

	win.getMouse() #blocking call

	# create_line(robots, center, win)
	interval = [{"min": 0, "max": 1}, {"min":1, "max" : 2}, {"min": 2, "max": 3}]

	create_rhombus(robots, center, interval)
	win.getMouse()
	pass

if __name__ == '__main__':
	main()