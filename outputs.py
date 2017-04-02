import matplotlib.pyplot as plt
from agent import Agent
import level0 as l0

def show():
    plt.show()

#PLOTS FULL GRID
def plot(id_):
    fig = plt.figure()
    plt.contourf(np.transpose(l0.grid))
    plt.colorbar()
    plt.grid()

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
def plotY(x_):
    fig=plt.figure()
    plt.plot(l0.grid[x_])

#PRINTS ALL Y COORDINATES
def printY(peepz_):
    yy=[]
    for peep in peepz_:
        yy.append(peep.y)
    print "\tY:", yy
