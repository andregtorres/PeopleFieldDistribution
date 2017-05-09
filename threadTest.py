from thread import start_new_thread, allocate_lock
#from affinity import set_process_affinity_mask, get_process_affinity_mask
import os
#print get_process_affinity_mask(os.getpid())
import psutil

p=psutil.Process(os.getpid())
print p.cpu_affinity()
p.cpu_affinity([2,3])
print p.cpu_affinity()

globVar=0
done=2
lock = allocate_lock()


def worker (a):
    global globVar, done
    #os.sched_setaffinity()
    lock.acquire()
    p.cpu_affinity([a])
    print p.cpu_affinity()
    globVar += a
    print "thread with ", a, "globvar: ", globVar
    done-=1
    lock.release()



start_new_thread(worker,(2,))
start_new_thread(worker,(3,))

while done > 0:
    pass
