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
        plt.contourf(np.clip(np.transpose(field),0,l0.a/100.))
    else:
        plt.contourf(np.transpose(field))
    plt.colorbar()
    plt.grid()

#PLOTS FULL GRID AND SAVES PNG
def save_plot(name_):
    fig = plt.figure(figsize=(l0.dimensions[0]/100,l0.dimensions[1]/100))
    plt.contourf(np.clip(np.transpose(l0.grid-l0.doorField),0,l0.a/100.))
    plt.colorbar()
    plt.grid()
    plt.axes().set_aspect('equal')
    name="aux/png/"+name_+".png"
    plt.savefig(name, dpi=100)
    #plt.clf()
    plt.close()


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
        yy.append(int(round(peep.y)))
    print "\t\tY:", yy

#PRINTS ALL X COORDINATES
def printX(peepz_):
    xx=[]
    for peep in peepz_:
        xx.append(int(round(peep.x)))
    print "\t\tX:", xx

#CREATES VIDEO FROM NUMERAL
def video_01(output_,fps_):
    cmd= "ffmpeg -framerate "+str(fps_)+" -i aux/png/%d.png aux/" + output_ + ".mp4"
    os.system(cmd)
    os.system("rm aux/png/*")

#PLOT ROH AND J
def plotGraphs(n=5, m=0, save=False):
    fig=plt.figure()
    timeN=[x*l0.dt for x in range((n-1)/2,len(l0.JBuffer)-(n-1)/2,1)]
    if m != 0: timeM=[x*l0.dt for x in range((m-1)/2,len(l0.JBuffer)-(m-1)/2,1)]
    ax=plt.subplot(211)
    plt.setp(ax.get_xticklabels(), visible=False)
    ax.set_ylabel(r" J $(s^{-1})$")
    if m != 0:
        plt.plot(timeN,movingAverage(l0.JBuffer,n),'k-',timeM,movingAverage(l0.JBuffer,m),'k--',alpha=0.7)
    else:
        plt.plot(timeN,movingAverage(l0.JBuffer,n))
    ax=plt.subplot(212)
    ax.set_ylabel(r'$\rho (m^{-2})$')
    ax.set_xlabel("t (s)")
    if m != 0:
        plt.plot(timeN,movingAverage(l0.rhoBuffer,n),'k-',timeM,movingAverage(l0.rhoBuffer,m),'k--',alpha=0.7)
    else:
        plt.plot(timeN,movingAverage(l0.rhoBuffer,n))
    name="aux/JRho_"+str(n)+"_"+str(m)+".png"
    if save: plt.savefig(name, dpi=100)

def movingAverage(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n
