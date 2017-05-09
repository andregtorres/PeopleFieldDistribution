# CLASS Agent
import level0 as l0
import outputs as out
import numpy as np
import os

class Agent(object):
    def __init__(self, x_=0.5, y_=0.5, a_=1, b_=1, v_=50):
        super(Agent, self).__init__()
        self.x = int(x_*l0.dimensions[0])
        self.y = int(y_*l0.dimensions[1])
        self.newX =0
        self.newY=0
        self.a = a_
        self.b = b_
        self.v = v_
        self.grid = l0.newGrid
    def addToGrid(self):
        for x, l in enumerate(l0.grid):
            dx = abs(x-self.x)
            for y, c in enumerate(l):
                dy = abs(y-self.y)
                d  = np.sqrt(dx**2+dy**2)
                if d > 10:
                    if not l0.locked[x][y]:
                        l0.grid[x][y]+=self.a/((d)**2)
                else:
                    if not l0.locked[x][y]:
                    #l0.locked [x][y] = True
                        l0.grid[x][y] +=self.a/((10)**2)

    def addToGrid2(self):
        self.grid=np.zeros(l0.Npoints, dtype=np.float64 ).reshape(l0.Nx, l0.Ny)
        #out.plot(self.grid)
        #out.show([5])
        for x, l in enumerate(self.grid):
            dx = abs(x-self.x)
            for y, c in enumerate(l):
                dy = abs(y-self.y)
                d  = np.sqrt(dx**2+dy**2)
                if d > 10:
                    if not l0.locked[x][y]:
                        self.grid[x][y]+=self.a/((d)**2)
                else:
                    if not l0.locked[x][y]:
                    #l0.locked [x][y] = True
                        self.grid[x][y] +=self.a/((10)**2)

    def takeFromGrid(self):
        for x, l in enumerate(l0.grid):
            dx = abs(x-self.x)
            if  dx < 0.8*l0.dimensions[0]:
                for y, c in enumerate(l):
                    dy = abs(y-self.y)
                    d  = np.sqrt(dx**2+dy**2)
                    if d > 10:
                        if not l0.locked[x][y]:
                            l0.grid[x][y]-=self.a/((d)**2)
                    else:
                        #if not l0.locked[x][y]:
                        #l0.locked [x][y] = True
                        l0.grid[x][y] -=self.a/((10)**2)

    def step(self):
        self.takeFromGrid()
        oldX=self.x
        oldY=self.y
        self.x=int(round(self.x-l0.gradx[oldX][oldY]*self.v))
        self.y=int(round(self.y-l0.grady[oldX][oldY]*self.v))
        self.addToGrid()

    def getNewCoordinates(self):
        l0.lockCounter.acquire()
        l0.activeThreads += 1
        l0.lockCounter.release()
        self.newX=int(round(self.x-l0.gradx[self.x][self.y]*self.v))
        self.newY=int(round(self.y-l0.grady[self.x][self.y]*self.v))
        if self.newX > l0.dimensions[0] or self.newX < 0:
            print "ERROR getNewCoordinates() out of bounds: newX= ",self.newX
            self.newX = self.x
        if self.newY > l0.dimensions[1] or self.newY < 0:
            print "ERROR getNewCoordinates() out of bounds: newY= ",self.newY
            self.newY = self.y

        l0.lockCounter.acquire()
        l0.activeThreads -= 1
        l0.lockCounter.release()
    def step2(self):
        self.takeFromGrid()
        self.x=self.newX
        self.y=self.newY
        self.addToGrid()
    def step3(self):
        l0.lockCounter.acquire()
        l0.activeThreads += 1
        l0.lockCounter.release()

        self.x=self.newX
        self.y=self.newY
        self.addToGrid2()

        l0.lockGrid.acquire()
        l0.grid += self.grid
        l0.lockGrid.release()

        l0.lockCounter.acquire()
        l0.activeThreads -= 1
        l0.lockCounter.release()
