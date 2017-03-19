import numpy as np
import matplotlib.pyplot as plt



dimensions  = [1000,1000]     #dimentions for box
door = dimensions[0]/10.  #dimentions for door
gridResol   = 1.           #grid resolution


class Ppl(object):
    """docstring for Ppl."""
    def __init__(self, x_=0.5, y_=0.5, a_=1, b_=1):
        super(Ppl, self).__init__()
        self.x = x_*dimensions[0]
        self.y = y_*dimensions[1]
        self.a = a_
        self.b = b_
    def addToGrid(self):
        for x, l in enumerate(grid):
            dx = abs(x-self.x)
            if  dx < 0.3*dimensions[0]:
                for y, c in enumerate(l):
                    dy = abs(y-self.y)
                    d  = np.sqrt(dx**2+dy**2)
                    if  d < 0.1*dimensions[0]:
                        if d != 0:
                            grid[x][y]+=self.a/((self.b*d)**2)
                        else:
                            grid[x][y]=grid[x-1][y]

Nx      = int((dimensions[0])/gridResol) #number of grid points
Ny      = int((dimensions[1])/gridResol) #number of grid points
Npoints     = Nx*Ny
grid    = np.zeros(Npoints, dtype=np.float64 ).reshape(Nx, Ny)
print "Nx,Ny= ",Nx," , ",Ny

def setLims():
    for x, l in enumerate(grid):
        if x <= Nx/2. :
            for y, c in enumerate(l):
                if y >= x + (Ny+door)/2. or y < -x + (Ny-door)/2.:
                    grid[x,y]=100
                if x == 0 and y>= (Ny-door)/2. and y<(Ny+door)/2:
                    grid[x,y]=-1e8


def plot():
    fig = plt.figure()
    plt.contourf(grid)
    plt.colorbar()
    plt.grid()
    plt.show()

def plotGrad():
    fig = plt.figure()
    dy,dx= np.gradient(grid)
    skip = (slice(None, None, 10), slice(None, None, 10))
    dx=dx[10:]
    dy=dy[10:]
    plt.quiver(dx[skip],dy[skip])
    plt.grid()
    plt.show()




setLims()
asdrubal    = Ppl(0.3,0.3, 1e-10, 5e-8)
anibal      = Ppl(0.4,0.4, 1e-10, 5e-8)
asdrubal.addToGrid()
anibal.addToGrid()


print np.gradient(grid)
plotGrad()
'''
fig = plt.figure()
plt.plot(grid[300])
plt.grid()
plt.show()
'''
