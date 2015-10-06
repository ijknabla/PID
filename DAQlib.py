import PyDAQmx  as PDm
import numpy    as np
import contextlib, collections, functools, sys, inspect
from prefixedunit import VoltageFloat
import mytask

def getargsinfo(name):
    doc = getattr(PDm.Task, name).__doc__
    doc = "(self, {})".format(doc.split("(")[1].split(")")[0])
    print(doc)

with mytask.AIO_F64(
    device = "Dev1",
    AIChan = "ai0",
    AOChan = "ao0") as task:
    print("hey")
    task.CreateAOVoltageChan(0, 10)
    print("how")
    #task.CreateAIVoltageChan(0, 10)
    #task.CreateAOFuncGenChan("Triangle", 100, 1, 2)
    task.CfgSampClkTiming(1000)
    data = []
    i = 0
    while i <= 10:
        data.append(i)
        i+= 0.05
    print(task.WriteAnalogF64(data))
