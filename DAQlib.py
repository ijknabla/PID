import PyDAQmx  as PDm
import numpy    as np
import contextlib, collections, functools, sys, inspect, threading, queue
from prefixedunit import VoltageFloat
import mytask

def getargsinfo(name):
    doc = getattr(PDm.Task, name).__doc__
    doc = "(self, {})".format(doc.split("(")[1].split(")")[0])
    print(doc)

with mytask.AI_F64(device = "Dev1", AIChan = "ai0") as Rtask,\
     mytask.AO_F64(device = "Dev1", AOChan = "ao0") as Wtask:

    Rtask.CreateAIVoltageChan(0, 10)
    Rtask.CfgSampClkTiming(1000)
    
    Wtask.CreateAOVoltageChan(0, 10)
    Wtask.CfgSampClkTiming(1000
                           )
    data = []
    i = 2
    while i <= 8:
        data.append(i)
        i+= 0.01

    num = len(data)

    Rqueue = queue.Queue()
    Wqueue = queue.Queue()
    
    def Rthread_func(q, num):
        result = Rtask.read(num)
        q.put(result)
    
    Rthread = threading.Thread(target = Rthread_func,
                               args = (Rqueue, num))
    Wthread = threading.Thread(target = Wtask.write,
                               args = (data,))

    Rthread.start()
    Wthread.start()

    Rthread.join()
    Wthread.join()

    
