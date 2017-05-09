import argparse
import sys
import numpy as np

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

#TERMINAL PARSER
parser = argparse.ArgumentParser(description='Crowd Simulation 1.')
parser.add_argument("-a","--agents", type=int,
                    help='number of agents to add')
parser.add_argument("-s","--steps", type=int,
                    help='number of time steps')
parser.add_argument("-v","--verbosity", type=int, choices=[0, 1, 2], help="increase output verbosity")
parser.add_argument("-V","--video", action='store_true',
                    help='Export video')


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


if (verbose > 1) : print "Nx,Ny= ",l0.Nx," , ",l0.Ny

def setLims(field_, value1_, value2_):
    for x, l in enumerate(field_):
        if x <= l0.Nx/2. :
            for y, c in enumerate(l):
                if y >= x + (l0.Ny+l0.door)/2. or y < -x + (l0.Ny-l0.door)/2.:
                    #walls
                    field_[x][y]=value1_
                if x==0 and  y>= (l0.Ny-l0.door)/2. and y<(l0.Ny+l0.door)/2:
                    #door
                    field_[x][y]=value2_



def timeStep(dt_):
    l0.time+=dt_
    l0.gradx,l0.grady = np.gradient(l0.grid)
    if (verbose > 1) : print "\tCOMPUTING NEW COORDINATES"
    q=Queue()
    npeepz=0
    for peep in peepz:
        Process(target=peep.getNewCoordinates, args=(q,npeepz)).start()
        npeepz+=1
    for i in range(npeepz):
        (putOrder, newX, newY)= q.get()
        peepz[putOrder].x=newX
        peepz[putOrder].y=newY

    if (verbose > 1) : print "\tSTEPPING"
    l0.grid    = np.zeros(l0.Npoints, dtype=np.float64 ).reshape(l0.Nx, l0.Ny)
    setLims(l0.grid,1000, -10000)
    npeepz=0
    for peep in peepz:
        Process(target=peep.step, args=(q,npeepz)).start()
        npeepz+=1
    for i in range(npeepz):
        (putOrder, peepz[putOrder].grid)= q.get()
        l0.grid+=peepz[putOrder].grid



psutil.Process(os.getpid()).cpu_affinity([1,2,3])

setLims(l0.grid,1000, -10000)
setLims(l0.newGrid,1000, -10000)
setLims(l0.locked, True, True)



if (verbose > 0) : print "ADDING AGENTS"
peepz=[]

for i in range(nAgents):
    y=0.45+0.05*i
    if (verbose > 1) : print "i=",i, "y=",y
    peepz.append(Agent(0.1,y,2e4,5e-8,20))
    peepz[i].addToGrid()


if (verbose > 0) : out.printY(peepz)

for i in range(nSteps):
    if (verbose > 0) : print "TIME STEPPING", i+1
    timeStep(1)
    if (verbose > 0) : out.printY(peepz)
    if video:
        out.save_plot(str(i))

#if (verbose > 0) : print "GENERATING PLOT"

#out.plotY(500)

#if (verbose > 0) : print "SHOWING PLOTS"
#out.show([2])
if video :
    print " +++++++  VIDEO  ++++++++"
    out.video_01("outputVideo2", 10)
