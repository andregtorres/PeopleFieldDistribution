import argparse
import sys
import numpy as np
import random

#FOR MULTITHREADING
from thread import start_new_thread, allocate_lock
import psutil
import os
from multiprocessing import Process, Queue

#LOCAL HEADERS
import level0 as l0
import outputs as out
from agent import Agent
import outputs

#DEFAULTS
verbose     = 0
nAgents     = 1
nSteps      = 0
video       = False
cpus        = [1,2,3]
exitAreaR   = 30 #cm
dt          = 1 #s
wallPot     =1000

#TERMINAL PARSER
parser = argparse.ArgumentParser(description='Crowd Simulation 1.')
parser.add_argument("-a","--agents", type=int,
                    help='number of agents to add')
parser.add_argument("-s","--steps", type=int,
                    help='number of time steps')
parser.add_argument("-v","--verbosity", type=int, choices=[0, 1, 2], help="increase output verbosity")
parser.add_argument("-V","--video", action='store_true',
                    help='Export video')
parser.add_argument("-r","--exitArea", type=float,
                    help='Radius of the exit area')
parser.add_argument("-t","--dt", type=float,
                    help='Time step in s')


args = parser.parse_args()
if len(sys.argv) < 2:
    parser.print_help()
    sys.exit(2)
if args.verbosity:
    verbose = args.verbosity
if args.agents:
    nAgents = args.agents
if args.steps:
    nSteps = args.steps
if args.video:
    video = True
if args.exitArea:
    exitAreaR = args.exitArea
if args.exitArea:
    dt = args.dt


if (verbose > 1) : print "Nx,Ny= ",l0.Nx," , ",l0.Ny
if (verbose > 1) : print "time resolution= ",dt, "s"
if (verbose > 1) : print "time steps", nSteps

def SetLims(field_, value1_, value2_):
    for x, l in enumerate(field_):
        for y, c in enumerate(l):
            #Triangular ramp walls
            #if y >= x + (l0.Ny+l0.door[2])/2. or y < -x + (l0.Ny-l0.door[2])/2.:
            #    if x <= l0.Nx/2. : field_[x][y]=value1_

            #OBSTACLE
            #if x>0.3*l0.Nx and x< 0.4*l0.Nx and y>0.45*l0.Ny and y< 0.55*l0.Ny:
            #    field_[x][y]=value1_

            #STRAIGHT walls
            if (x >= l0.door[0] and x < l0.door[0] + l0.cm(5) ) and (y>l0.door[1]+l0.door[2]/2 or y<l0.door[1]-l0.door[2]/2) :
                field_[x][y]=value1_

def setWallField():
    for x, l in enumerate(l0.locked):
        if (x %50 == 0 and verbose > 1 ): print x
        for y, point in enumerate(l):
            if point:
                applyField(x,y,wallPot, 25)

def applyField(x0,y0,a, ran):
    for x in range(x0-ran,x0 + ran):
        if x>0:
            for y in range(y0-ran,y0 + ran):
                if y>0:
                    try:
                        if (not l0.locked[x][y]) :
                            d=np.sqrt((x0-x)**2+(y0-y)**2)
                            if d > 0:
                                wallField[x][y]+=a/((d)**2)/(2*ran+1.0)

                    except:
                        pass
def getDoorField(value2_):
    for x, l in enumerate(l0.doorField):
        for y, c in enumerate(l):
            if not l0.locked[x][y]:
                dDoor= np.sqrt((x-l0.door[0])**2+(y- l0.door[1])**2)
                l0.doorField[x][y]=(value2_ + dDoor)


def inside(x_,y_):
    x=int(x_*l0.Nx)
    y=int(y_*l0.Ny)
    ok = not l0.locked[x,y-10]
    ok = ok and (not l0.locked[x,y+10])
    ok = ok and (not l0.locked[x,y])
    ok = ok and (not l0.locked[x-10,y])
    ok = ok and (not l0.locked[x+10,y])
    return ok

def inExitArea(x,y):
    if np.sqrt((x-l0.door[0])**2+((y-l0.door[1]))**2)<=exitAreaR:
        return True
    else:
        return False

def timeStep(dt_):
    l0.time+=dt_
    l0.gradx,l0.grady = np.dot(np.gradient(l0.grid),dt_)
    if (verbose > 1) : print "\tCOMPUTING NEW COORDINATES"
    q=Queue()
    npeepz=0
    for peep in peepz:
        if not peep.safe:
            Process(target=peep.getNewCoordinates, args=(q,npeepz,verbose)).start()
            npeepz+=1

    for i in range(npeepz):
        (putOrder, newX, newY, safe)= q.get()
        peepz[putOrder].x=newX
        peepz[putOrder].y=newY
        peepz[putOrder].safe=safe

    for peep in peepz:
        if peep.safe:
            peepz.remove(peep)
            del peep

    if (verbose > 1) : print "\tSTEPPING"
    #RESET GRID
    l0.grid=blank.copy()
    npeepz=0
    for peep in peepz:
        Process(target=peep.step, args=(q,npeepz)).start()
        npeepz+=1
    for i in range(npeepz):
        (putOrder, peepz[putOrder].grid)= q.get()
        l0.grid+=peepz[putOrder].grid


psutil.Process(os.getpid()).cpu_affinity(cpus)

wallField  = np.zeros(l0.Npoints, dtype=np.float64 ).reshape(l0.Nx, l0.Ny)
SetLims(l0.grid,wallPot, -wallPot)
SetLims(l0.locked, True, True)
out.plotX(l0.grid,30)
getDoorField(-wallPot)
l0.grid+=l0.doorField
out.plotX(l0.grid,30)
print "SET WALLFIELD"
setWallField()
print "DONE"
#out.plotX(wallField, 500)
l0.grid+=wallField
out.plotX(l0.grid,30)
blank=l0.grid.copy()
#out.plot(l0.grid, False)
#out.show([1])

if (verbose > 0) : print "ADDING AGENTS"
peepz=[]
for i in range(nAgents):
    while True:
        y = random.uniform(0.25,0.75)
        x = random.uniform(0.55,0.95)
        if inside(x,y): break
    v = random.uniform(9.8,10.2)
    peepz.append(Agent(x,y,2e4,5e-8,v))
    peepz[i].addToGrid()
    if (verbose > 1) : print "i=",i, "x=",peepz[i].x, "y=",peepz[i].y,"v=",v

if (verbose > 0) : out.printX(peepz)
if (verbose > 0) : out.printY(peepz)

out.plotY(l0.grid,4)
out.plotY(l0.grid,5)
out.plotY(l0.grid,6)

out.show([1])

for i in range(nSteps):
    if (verbose > 0) : print "TIME STEPPING", i+1
    timeStep(dt)
    if (verbose > 0) : out.printX(peepz)
    if (verbose > 0) : out.printY(peepz)
    if video:
        out.save_plot(str(i))

#if (verbose > 0) : print "GENERATING PLOT"

#out.plotY(l0.grid,peepz[0].x)
#if (verbose > 0) : print "SHOWING PLOTS"
#out.show([2])
if video :
    print " +++++++  VIDEO  ++++++++"
    out.video_01("outputVideo2", 10)
