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
        self.v = v_/l0.gridResol
        self.grid = np.zeros(l0.Npoints, dtype=np.float64 ).reshape(l0.Nx, l0.Ny)
        self.safe=False
        self.radius=l0.radius/l0.gridResol
    def __del__(self):
        self.grid=None

    def addToGrid(self):
        for x, l in enumerate(l0.grid):
            dx = abs(x-self.x)
            for y, c in enumerate(l):
                dy = abs(y-self.y)
                d  = np.sqrt(dx**2+dy**2)
                #if x==self.x : print x, y,d, self.radius , d > self.radius
                if d > self.radius:
                    if not l0.locked[x][y]:
                        l0.grid[x][y]+=self.a/((d*l0.gridResol)**2)
                else:
                    l0.grid[x][y] += self.a/((self.radius*l0.gridResol)**2)

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
                            self.grid[x][y]+=self.a/((d*l0.gridResol)**2)
                    else:
                        self.grid[x][y] +=self.a/((self.radius*l0.gridResol)**2)


    def getNewCoordinates(self, q, putOrder, verbose):
        #SET AFFINITY
        psutil.Process(os.getpid()).cpu_affinity([1,2,3])

        newX=self.x-l0.gradx[int(round(self.x))][int(round(self.y))]*self.v #grad already multiplyes py dt
        newY=self.y-l0.grady[int(round(self.x))][int(round(self.y))]*self.v

        #print (np.sqrt((self.x-newX)**2+(self.y-newY)**2)/l0.dt)

        if int(round(newX)) >= l0.Nx or newX < 0:
            if newX < l0.door[0] and newY > l0.door[1]-l0.door[2]/2. + self.radius/2. and newY < l0.door[1] +l0.door[2]/2.- self.radius/2.:
                self.safe=True
                self.grid=np.zeros(l0.Npoints, dtype=np.float64 ).reshape(l0.Nx, l0.Ny)
            else:
                if (verbose > 1) :l0.lockPrint.acquire()
                if (verbose > 1) :print "\t\t",self.id,"ERROR getNewCoordinates() out of bounds: newX= ",newX
                if (verbose > 1) :print "\t\t",self.id,"ERROR getNewCoordinates() out of bounds: newY= ",newY
                if (verbose > 1) :l0.lockPrint.release()
                newX = self.x #TODO
        if int(round(newY)) >= l0.Ny or newY < 0:
            if (verbose > 1) :l0.lockPrint.acquire()
            if (verbose > 1) :print "\t\t",self.id,"ERROR getNewCoordinates() out of bounds: newX= ",newX
            if (verbose > 1) :print "\t\t",self.id,"ERROR getNewCoordinates() out of bounds: newY= ",newY
            if (verbose > 1) :l0.lockPrint.release()
            newY = self.y  #TODO

        q.put((putOrder,newX,newY,self.safe))

    def step(self, q, putOrder):
        #SET AFFINITY
        psutil.Process(os.getpid()).cpu_affinity([1,2,3])
        self.computeGrid()
        q.put((putOrder,self.grid))
    def inExitArea(self):
        ret=np.sqrt((self.x-l0.door[0])**2+((self.y-l0.door[1]))**2)-l0.cm(l0.exitAreaR)
        if ret<=0:
            return True
        else:
            return False
