import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ax = plt.subplots()

x = np.arange(0, 2*np.pi, 0.01)        #defining 'x'

line, = ax.plot(x, np.sin(x))        
#text to display the current frame
time_text = ax.text(0.05, 0.95,'',horizontalalignment='left',verticalalignment='top', transform=ax.transAxes)

#Init function ti initialize variables 
def init():
    line.set_ydata(np.ma.array(x, mask=True))
    plt.title("Plot of a travelling sine wave")
    plt.xlabel("x")
    plt.ylabel("y")
    time_text.set_text('')
    return line ,time_text        #return the variables that will updated in each frame
    
def animate(i):                  # 'i' is the number of frames  
    line.set_ydata(np.sin(x-0.2*i))  # update the data
    time_text.set_text(' frame number = %.1d' % i)  
    return line , time_text

ani = animation.FuncAnimation(fig, animate, 200,init_func=init, interval=100, blit=True)
plt.show()