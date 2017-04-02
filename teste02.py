import numpy as np
import matplotlib.pyplot as plt



dimensions  = [1000,1000]     #dimentions for box
door = dimensions[0]/10.  #dimentions for door
gridResol   = 1.           #grid resolution


class Ppl(object):
    """docstring for Ppl."""
    def __init__(self, x_=0.5, y_=0.5, a_=1, b_=1, v_=50):
        super(Ppl, self).__init__()
        self.x = int(x_*dimensions[0])
        self.y = int(y_*dimensions[1])
        self.newX =0
        self.newY=0
        self.a = a_
        self.b = b_
        self.v = v_
    def addToGrid(self):
        for x, l in enumerate(grid):
            dx = abs(x-self.x)
            if  dx < 0.8*dimensions[0]:
                for y, c in enumerate(l):
                    dy = abs(y-self.y)
                    d  = np.sqrt(dx**2+dy**2)
                    if d > 10:
                        if not locked[x][y]:
                            grid[x][y]+=self.a/((d)**2)
                    else:
                        if not locked[x][y]:
                        #locked [x][y] = True
                            grid[x][y] +=self.a/((10)**2)
    def takeFromGrid(self):
        for x, l in enumerate(grid):
            dx = abs(x-self.x)
            if  dx < 0.8*dimensions[0]:
                for y, c in enumerate(l):
                    dy = abs(y-self.y)
                    d  = np.sqrt(dx**2+dy**2)
                    if d > 10:
                        if not locked[x][y]:
                            grid[x][y]-=self.a/((d)**2)
                    else:
                        if not locked[x][y]:
                        #locked [x][y] = True
                            grid[x][y] -=self.a/((10)**2)

    def step(self):
        self.takeFromGrid()
        oldX=self.x
        oldY=self.y
        self.x=int(round(self.x-gradx[oldX][oldY]*self.v))
        self.y=int(round(self.y-grady[oldX][oldY]*self.v))
        self.addToGrid()

    def getNewCoordinates(self):
        self.newX=int(round(self.x-gradx[self.x][self.y]*self.v))
        self.newY=int(round(self.y-grady[self.x][self.y]*self.v))
    def step2(self):
        self.takeFromGrid()
        self.x=self.newX
        self.y=self.newY
        self.addToGrid()



Nx      = int((dimensions[0])/gridResol) #number of grid points
Ny      = int((dimensions[1])/gridResol) #number of grid points
Npoints     = Nx*Ny
grid    = np.zeros(Npoints, dtype=np.float64 ).reshape(Nx, Ny)
locked  = np.zeros(Npoints, dtype=np.bool ).reshape(Nx, Ny)
gradx   = np.zeros(Npoints, dtype=np.float64 ).reshape(Nx, Ny)
grady   = np.zeros(Npoints, dtype=np.float64 ).reshape(Nx, Ny)
print "Nx,Ny= ",Nx," , ",Ny
time=0

def setLims(field_, value1_, value2_):
    for x, l in enumerate(field_):
        if x <= Nx/2. :
            for y, c in enumerate(l):
                if y >= x + (Ny+door)/2. or y < -x + (Ny-door)/2.:
                    field_[x][y]=value1_
                if x == 0 and y>= (Ny-door)/2. and y<(Ny+door)/2:
                    field_[x][y]=value2_


def plot(id_):
    fig = plt.figure()
    plt.contourf(np.transpose(grid))
    plt.colorbar()
    plt.grid()


def plotGrad():
    fig = plt.figure(1)
    dy,dx= np.gradient(grid)
    skip = (slice(None, None, 10), slice(None, None, 10))
    dx=dx[10:]
    dy=dy[10:]
    plt.quiver(dx[skip],dy[skip])
    plt.grid()
    plt.show()

def plotGrad2():
    global gradx, grady, grid
    fig = plt.figure(2)
    plt.subplot(3, 1, 1)
    plt.plot(grid[300])

    plt.subplot(3, 1, 2)
    plt.plot(gradx[300])

    plt.subplot(3, 1, 3)
    plt.plot(grady[300])

    plt.grid()
    plt.show()

def plotY(y_):
    fig=plt.figure()
    plt.plot(grid[y_])

def timeStep(dt_):
    global time, gradx, grady
    time+=dt_
    gradx,grady = np.gradient(grid)
    print "\tCOMPUTING NEW COORDINATES"
    for peep in peepz:
        peep.getNewCoordinates()
    print "\tSTEPPING"
    for peep in peepz:
        peep.step2()

def printY():
    yy=[]
    for peep in peepz:
        yy.append(peep.y)
    print "\tY:", yy

setLims(grid,100, -100)
#setLims(gradx,100, -100)
#setLims(grady,100, -100)
setLims(locked, True, True)

#asdrubal    = Ppl(0.3,0.3, 1e4, 5e-8,20)
#anibal      = Ppl(0.3,0.34, 1e4, 5e-8,20)
#amilcar      = Ppl(0.32,0.32, 1e4, 5e-8,20)

print "ADDING AGENTS"
peepz=[]
for i in range(5):
    y=0.1+0.07*i
    print "i=",i, "y=",y
    peepz.append(Ppl(0.5,y,2e4,5e-8,20))
    peepz[i].addToGrid()

#print "GENERATING PLOT"
#plot(1)
#plotY(500)
for i in range(20):
    print "TIME STEPPING", i+1
    timeStep(1)
    printY()

print "GENERATING PLOT"
plotY(500)

print "SHOWING PLOTS"
plt.show()


#asdrubal.addToGrid()
#anibal.addToGrid()
#amilcar.addToGrid()
#for i in range(5):
#    timeStep(1)
#    asdrubal.step()
#    anibal.step()
#    amilcar.step()

#plotGrad2()

#print np.gradient(grid)
#plotGrad2()
#plot()
