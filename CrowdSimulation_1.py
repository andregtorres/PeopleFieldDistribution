import numpy as np
import level0 as l0
import outputs as out
from agent import Agent
import outputs

print "Nx,Ny= ",l0.Nx," , ",l0.Ny

def setLims(field_, value1_, value2_):
    for x, l in enumerate(field_):
        if x <= l0.Nx/2. :
            for y, c in enumerate(l):
                if y >= x + (l0.Ny+l0.door)/2. or y < -x + (l0.Ny-l0.door)/2.:
                    field_[x][y]=value1_
                if x == 0 and y>= (l0.Ny-l0.door)/2. and y<(l0.Ny+l0.door)/2:
                    field_[x][y]=value2_





def timeStep(dt_):
    l0.time+=dt_
    l0.gradx,l0.grady = np.gradient(l0.grid)
    print "\tCOMPUTING NEW COORDINATES"
    for peep in peepz:
        peep.getNewCoordinates()
    print "\tSTEPPING"
    for peep in peepz:
        peep.step2()



setLims(l0.grid,100, -100)
#setLims(l0.gradx,100, -100)
#setLims(l0.grady,100, -100)
setLims(l0.locked, True, True)

#asdrubal    = Agent(0.3,0.3, 1e4, 5e-8,20)
#anibal      = Agent(0.3,0.34, 1e4, 5e-8,20)
#amilcar      = Agent(0.32,0.32, 1e4, 5e-8,20)

print "ADDING AGENTS"
peepz=[]
for i in range(1):
    y=0.1+0.07*i
    print "i=",i, "y=",y
    peepz.append(Agent(0.5,y,2e4,5e-8,20))
    peepz[i].addToGrid()

#print "GENERATING PLOT"
#out.plot(1)
#out.plotY(500)
for i in range(1):
    print "TIME STEPPING", i+1
    timeStep(1)
    out.printY(peepz)

print "GENERATING PLOT"
out.plotY(500)

print "SHOWING PLOTS"
out.show()
