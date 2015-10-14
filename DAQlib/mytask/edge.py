from DAQlib.mytask import *
from util.argstools import *


__all__ = ["StartEdge"]

class EdgeBase(MyTask, Counter):
    pass


@argssetter
class StartEdge(EdgeBase, Output):
    def __init__(self, device, channel, rate):
        super().__init__(**self.getattrs(vars()))
        self.tasks = []

    def setTask(self, Task, triggerEdge = "Rising"):
        if not isinstance(Task, MyTask):
            raise TypeError("Task must be instance of MyTask")
        triggerEdge = self.selectVal("Rising, Falling", triggerEdge)
        Task.CfgDigEdgeStartTrig(self.getOutChan(), triggerEdge)
        self.tasks.append(Task)


        
    @argsdescriptor
    def CreateCOPulseChanFreq(self, initialDelay, freq, dutyCycle, *,
                              #counter = self.channel
                              nameToAssignToChannel = "", 
                              units = "Hz",
                              idleState = "Low"
                              ):
        counter = self.getPhysicalChan()
        units       = self.selectVal("Hz", units)
        idleState   = self.selectVal("Low, High", idleState)
        return vars()

    def getOutChan(self):
        return self.getPhysicalChan() + "out"

    def setup(self):
        initialdelay = 0.0
        dutyCycle = 0.01
        self.CreateCOPulseChanFreq(initialdelay, self.rate, dutyCycle)
        self.CfgImplicitTiming()
