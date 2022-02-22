# -*- coding: utf-8 -*-
from multiprocessing import Process
from multiprocessing import Value, Array
from multiprocessing import BoundedSemaphore

N = 8

def task(semaphore,common, tid, critical):
    a = 0
    for i in range(100):
        print(f'{tid}−{i}: Non−critical Section')
        a += 1
        print(f'{tid}−{i}: End of non−critical Section')
        critical[tid] = 1
        semaphore.acquire()
        try:
            v = common.value + 1
            common.value = v
            critical[tid] = 0
        finally:
            semaphore.release()
        
def main():
    lp = []
    common = Value('i', 0)
    critical = Array('i', [0]*N)
    semaphore = BoundedSemaphore()
    for tid in range(N):
        lp.append(Process(target=task, args=(semaphore, common, tid, critical)))
    print (f"Valor inicial del contador {common.value}")
    for p in lp:
        p.start()
    for p in lp:
        p.join()
        
    print (f"Valor final del contador {common.value}")
    print ("fin")
    
if __name__ == "__main__":
    main()