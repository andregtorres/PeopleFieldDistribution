# CLASS Agent
import level0 as l0
import outputs as out
import numpy as np
import os
import psutil

agentCounter=0

class Agent(object):
    def __init__(self, x_=0.5, y_=0.5, a_=1, b_=1, v_=50):
        super(Agent, self).__init__()
        global agentCounter
        self.id=agentCounter
        agentCounter+=1
        self.x = int(x_*l0.Nx)
        self.y = int(y_*l0.Ny)
        self.a = a_
        self.b = b_
        self.v = v_
        self.grid = np.zeros(l0.Npoints, dtype=np.float64 ).reshape(l0.Nx, l0.Ny)
        self.safe=False
        self.radius=10.
    def __del__(self):
        self.grid=None

    def addToGrid(self):
        for x, l in enumerate(l0.grid):
            dx = abs(x-self.x)
            for y, c in enumerate(l):
                dy = abs(y-self.y)
                d  = np.sqrt(dx**2+dy**2)
                if d > self.radius:
                    if not l0.locked[x][y]:
                        l0.grid[x][y]+=self.a/((d)**2)
                else:
                    if not l0.locked[x][y]:
                    #l0.locked [x][y] = True
                        l0.grid[x][y] +=self.a/((self.radius)**2)

    def computeGrid(self):
        if not self.safe:
            self.grid=np.zeros(l0.Npoints, dtype=np.float64 ).reshape(l0.Nx, l0.Ny)
            for x, l in enumerate(self.grid):
                dx = abs(x-self.x)
                for y, c in enumerate(l):
                    dy = abs(y-self.y)
                    d  = np.sqrt(dx**2+dy**2)
                    if d > self.radius:
                        if not l0.locked[x][y]:
                            self.grid[x][y]+=self.a/((d)**2)
                        else:
                            if not l0.locked[x][y]:
                                #l0.locked [x][y] = True
                                self.grid[x][y] +=self.a/((self.radius)**2)


    def getNewCoordinates(self, q, putOrder, verbose):
        #SET AFFINITY
        psutil.Process(os.getpid()).cpu_affinity([1,2,3])

        newX=int(round(self.x-l0.gradx[self.x][self.y]*self.v))
        newY=int(round(self.y-l0.grady[self.x][self.y]*self.v))
        if newX > l0.dimensions[0] or newX < 0:
            if newX < 0 and newY > l0.Ny/2.-l0.door[2]/2. + self.radius and newY < l0.Ny/2.+l0.door[2]/2. - self.radius:
                self.safe=True
                self.grid=np.zeros(l0.Npoints, dtype=np.float64 ).reshape(l0.Nx, l0.Ny)
                self.newX=0
                self.newY=0
                l0.lockPrint.acquire()
                if (verbose > 1) : print "\t\tAgent",self.id,"safe"
                l0.lockPrint.release()
            else:
                l0.lockPrint.acquire()
                if (verbose > 1) :print "\t\tERROR getNewCoordinates() out of bounds: newX= ",newX
                if (verbose > 1) :print "\t\tERROR getNewCoordinates() out of bounds: newY= ",newY
                l0.lockPrint.release()
                newX = self.x
        if newY > l0.dimensions[1] or newY < 0:
            l0.lockPrint.acquire()
            print "ERROR getNewCoordinates() out of bounds: newX= ",newX
            print "ERROR getNewCoordinates() out of bounds: newY= ",newY
            l0.lockPrint.release()
            newY = self.y

        q.put((putOrder,newX,newY,self.safe))

    def step(self, q, putOrder):
        #SET AFFINITY
        psutil.Process(os.getpid()).cpu_affinity([1,2,3])
        self.computeGrid()
        q.put((putOrder,self.grid))
