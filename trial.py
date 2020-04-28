

from graphics import * 
from queue import Queue  # use for thread-safe communications
from random import randint
import math
import time
from threading import Thread, Lock


actions = Queue()
def drawPoint(lat, long):
    x = int(long * 5.3 + 960)
    y = int(lat * -5.92 + 540)

    point = Point(x, y)
    circle = Circle(point, 5)
    circle.setFill(color_rgb(255, 0, 0))

    circles_lock.acquire()
    circles.append(circle)
    circles_lock.release()

    actions.put((circle.draw, win))

def deletePoint(lat, long):
    global circles

    x = int(long * 5.3 + 960)
    y = int(lat * -5.92 + 540)

    keep_circles = []

    circles_lock.acquire()
    for circle in circles:
        center = circle.getCenter()

        if center.getX() == x and center.getY() == y:
            actions.put((circle.undraw,))
        else:
            keep_circles.append(circle)

    circles = keep_circles
    circles_lock.release()


def deleteDots():
    global dots

    while True:
        keep_dots = []

        dots_lock.acquire()
        now = time.time()

        for dot in dots:
            lat, long, then = dot

            if now - then >= 1.0:
                deletePoint(lat, long)
            else:
                keep_dots.append(dot)

        dots = keep_dots
        dots_lock.release()

        time.sleep(0.5)

def addDots():
    while True:
        lat = randint(-90, 90)
        long = randint(-180, 180)

        drawPoint(lat, long)

        dots_lock.acquire()
        dots.append((lat, long, time.time()))
        dots_lock.release()

        time.sleep(0.25)


def draw_windows(w,h):
    #create windows
    print('create windows with name : swarm, width : ',w,', height : ',h)
    return GraphWin('swarm',w,h)
    pass

def draw_center(win):
    center = Circle(Point(win.getWidth()/2,win.getHeight()/2),10)
    center.setFill('red')
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

    x,y = distance_vector(robot.getCenter(),center.getCenter())
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
            time.sleep(0.1)
            pass
        pass
    pass

def move_robot(r, loc_x, loc_y, win):
    actions.put(r.move(loc_x, loc_y), win)
    

    r.move(loc_x, loc_y)
    print("called")
    action, *arguments = actions.get()
    action(*arguments)     

    
    time.sleep(0.125)
    pass

def meeting_point(r,center,win):
    x,y = relative_distance_to_center(r,center)
    distance = distance_magnitude(x, y)
    while distance>40.5:
        loc_x = -x/10.0
        loc_y = -y/10.0
        
        lock.acquire()
        move_robot(r, loc_x, loc_y, win)
        x,y = relative_distance_to_center(r,center)
        distance = distance_magnitude(x, y)
        time.sleep(0.1)
        lock.release()
        pass
    pass



circles_lock = Lock()

win = draw_windows(700,600)
center = draw_center(win)
# robots = draw_swarm(2,win)

def draw_swarm_multi(n,win):
    #draw n number of robot in window win
    
    robot = []
    for x in range(0,n):
        circles_lock.acquire()
        robot.append(Circle(Point(randint(20,win.getWidth()-20),randint(20,win.getHeight()-20)),10))
        circles_lock.release()
        
        # print('create robot with number ',x,' point x : ',x*200+40,', y : 200 , r : 20')
        robot[x].setFill('red')
        robot[x].draw(win)
        pass
    return robot
    pass

def drawPoint(lat, long):
    x = int(long * 5.3 + 960)
    y = int(lat * -5.92 + 540)

    point = Point(x, y)
    circle = Circle(point, 5)
    circle.setFill(color_rgb(255, 0, 0))

    circles_lock.acquire()
    circles.append(circle)
    circles_lock.release()

    actions.put((circle.draw, win))

win.getMouse()
# for r in robots:
#     threading.Thread(target=meeting_point, args=(r,center, win), daemon=True).start()
#     pass
threading.Thread(target=draw_swarm_multi, args=(2, win), daemon=True).start()
win.getMouse()
# circles = []


# dots = []
# dots_lock = Lock()



# Thread(target=addDots, daemon=True).start()
# Thread(target=deleteDots, daemon=True).start()