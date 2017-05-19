import matplotlib.pyplot as plt
from agent import Agent
import level0 as l0
import numpy as np
import os

def show(ii_):
    for i in ii_:
        plt.show(i)

#PLOTS FULL GRID
def plot(field,clip):
    fig = plt.figure()
    #plt.contourf(np.transpose(l0.grid))
    if clip:
        plt.contourf(np.clip(np.transpose(field),0,250))
    else:
        plt.contourf(np.transpose(field))
    plt.colorbar()
    plt.grid()

#PLOTS FULL GRID AND SAVES PNG
def save_plot(name_):
    fig = plt.figure(figsize=(l0.dimensions[0]/100,l0.dimensions[1]/100))
    plt.contourf(np.clip(np.transpose(l0.grid-l0.doorField),0,250))
    plt.colorbar()
    plt.grid()
    plt.axes().set_aspect('equal')
    name="aux/png/"+name_+".png"
    plt.savefig(name, dpi=100)
    plt.clf()


#PLOTS GRADIENT DECIMATED
def plotGrad():
    fig = plt.figure(1)
    dy,dx= np.gradient(l0.grid)
    skip = (slice(None, None, 10), slice(None, None, 10))
    dx=dx[10:]
    dy=dy[10:]
    plt.quiver(dx[skip],dy[skip])
    plt.grid()

#PLOTS GRID AND GRADIENTS AT X=300
def plotGrad2():
    fig = plt.figure(2)
    plt.subplot(3, 1, 1)
    plt.plot(l0.grid[300])

    plt.subplot(3, 1, 2)
    plt.plot(l0.gradx[300])

    plt.subplot(3, 1, 3)
    plt.plot(l0.grady[300])

    plt.grid()

#PLOTS GRID AT DESIRED X
def plotY(field,x_):
    fig=plt.figure()
    plt.plot(field[x_])

#PLOTS GRID AT DESIRED Y
def plotX(field, y_):
    fig=plt.figure()
    plt.plot(np.transpose(field)[y_])

#PRINTS ALL Y COORDINATES
def printY(peepz_):
    yy=[]
    for peep in peepz_:
        yy.append(peep.y)
    print "\tY:", yy

#PRINTS ALL X COORDINATES
def printX(peepz_):
    xx=[]
    for peep in peepz_:
        xx.append(peep.x)
    print "\tX:", xx

#CREATES VIDEO FROM NUMERAL
def video_01(output_,fps_):
    cmd= "ffmpeg -framerate "+str(fps_)+" -i aux/png/%d.png aux/" + output_ + ".mp4"
    os.system(cmd)
    os.system("rm aux/png/*")
