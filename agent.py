# CLASS Agent
import level0 as l0
import outputs as out
import numpy as np
import os
import psutil

class Agent(object):
    def __init__(self, x_=0.5, y_=0.5, a_=1, b_=1, v_=50):
        super(Agent, self).__init__()
        self.x = int(x_*l0.dimensions[0])
        self.y = int(y_*l0.dimensions[1])
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

    def computeGrid(self):
        self.grid=np.zeros(l0.Npoints, dtype=np.float64 ).reshape(l0.Nx, l0.Ny)
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


    def getNewCoordinates(self, q, putOrder):
        #SET AFFINITY
        psutil.Process(os.getpid()).cpu_affinity([1,2,3])

        newX=int(round(self.x-l0.gradx[self.x][self.y]*self.v))
        newY=int(round(self.y-l0.grady[self.x][self.y]*self.v))
        if newX > l0.dimensions[0] or newX < 0:
            l0.lockPrint.acquire()
            print "ERROR getNewCoordinates() out of bounds: newX= ",newX
            l0.lockPrint.release()
            newX = self.x
        if newY > l0.dimensions[1] or newY < 0:
            l0.lockPrint.acquire()
            print "ERROR getNewCoordinates() out of bounds: newY= ",newY
            l0.lockPrint.release()
            newY = self.y

        q.put((putOrder,newX,newY))

    def step(self, q, putOrder):
        #SET AFFINITY
        psutil.Process(os.getpid()).cpu_affinity([1,2,3])
        self.computeGrid()
        q.put((putOrder,self.grid))
