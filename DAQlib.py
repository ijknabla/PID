import PyDAQmx  as PDm
import numpy    as np
import contextlib, collections, functools, sys, inspect
from prefixedunit import VoltageFloat

def defaultargs_methodwrapper(meth):
    methname = meth.__name__
    
    @functools.wraps(meth)
    def wrapped(self, *args, **kwrds):
        nonlocal methname
        cls = self.__class__ if not isinstance(self, type) else self
        super_ = super(cls, self)
        super_meth = getattr(super_, methname)
        
        varsdict = dict(
            (key.lower(), val)
            for key, val in meth(self, *args, **kwrds).items()
            )
        try:
            argspec = inspect.getargspec(meth)[0]
        except ValueError:
            argspec = meth.__code__.co_varnames
        varnames = map(
            lambda x : x.lower(),
            argspec[1:]
            )
        varnames = tuple(varnames)
        print(varnames, meth)
        return super_meth(*[varsdict[varname]
                            for varname in varnames])
    return wrapped

def ReadTask(task, num):
    read = PDm.int32()
    data = (np.zeros((num,), dtype=np.float64))
    task.ReadAnalogF64(num,
                       1000.0,
                       PDm.DAQmx_Val_GroupByChannel,
                       data,
                       num,
                       PDm.byref(read),
                       None)
    return data[:read.value]

class MyTask_AIO_Interface():
    
    def WriteAnalogF64(self,
                       numSampsPerChan,
                       autoStart,
                       timeout,
                       dataLayout,
                       writeArray
                       #sampsPerChanWritten
                       #reserved
                       ):
        sampsPerChanWritten = PDm.int32()
        reserved = None
        result = super().WriteAnalogF64(numSampsPerChan,
                               autoStart,
                               timeout,
                               dataLayout,
                               writeArray,
                               PDm.byref(sampsPerChanWritten),
                               reserved)
        return result, sampsPerChanWritten

class MyTask_AIO_Base(MyTask_AIO_Interface, PDm.Task):
    def __enter__(self):
        print("open  task ->", self)
        return self
    def __exit__(self, typ, args, tb):
        print("close rask ->", self)
        self.ClearTask()
        if typ is not None:
            raise

    def getVal(self, name):
        try:
            return getattr(PDm, "DAQmx_Val_{}".format(name))
        except:
            raise

    def selectVal(self, selector, name, *, delimiter = ","):
        selector = set(
            map(
                lambda name : name.strip(),
                selector.split(delimiter)
                )
            )
        if name not in selector:
            raise NameError("Val(given is {name})must be within {selector}"\
                            .format(**vars()))
        try:
            return self.getVal(name)
        except:
            raise
            
            



class MyTask_AIO_F64(MyTask_AIO_Base):
    attrs = set()
    def __init__(self, *args, **kwrds):
        super().__init__()
        for attr, value in kwrds.items():
            self.attrs.add(attr)
            setattr(self, attr, value)

    
    def __repr__(self):
        return "{self.__class__.__name__}({})".format(
            ", ".join("{} = {}".format(attr, getattr(self, attr))
                      for attr in self.attrs),
            **locals()
            )

    def getpysicalChannel(self, name):
        if name.lower() == "ai":
            return "{self.device}/{self.AIChan}".format(**vars())
        elif name.lower() == "ao":
            return "{self.device}/{self.AOChan}".format(**vars())    

    @defaultargs_methodwrapper
    def CfgSampClkTiming(self, rate, *,
                         #defaultarguement
                         source = None,
                         activeEdge = PDm.DAQmx_Val_Rising,
                         sampleMode = PDm.DAQmx_Val_ContSamps,
                         sampsPerChan = 10):
        return vars()

    @defaultargs_methodwrapper
    def CreateAOVoltageChan(self, minVal, maxVal, *,
                            units = "Volts",
                            customScaleName = None,
                            nameToAssignToChannel = None):
        
        units = self.selectVal("Volts, FromCustomScale", units)
        
        physicalChannel = self.getpysicalChannel("AO")
        if nameToAssignToChannel is None:
            nameToAssingnToChannel = "Analog Output of {self}"\
                                     .format(**vars())
        return vars()
        

    @defaultargs_methodwrapper
    def CreateAOFuncGenChan(self, Type, freq, amplitude, offset, *, 
                            nameToAssignToChannel = None):
        Types = "Sine,Triangle,Sawtooth,Square".split(",")
        try:
            Type = getattr(PDm, "DAQmx_Val_{}".format(Type))
        except:
            raise ValueError("Choose Type in {Types}".format(**vars()))
        physicalChannel = self.getpysicalChannel("AO")
        if nameToAssignToChannel is None:
            nameToAssingnToChannel = "Analog FuncGen Output of {self}"\
                                     .format(**vars())
        return vars()

    @defaultargs_methodwrapper
    def WriteAnalogF64(self, writeArray, *,
                       autostart = True,
                       timeout = -1,
                       dataLayout = "GroupByChannel"):
        if not isinstance(writeArray, np.ndarray):
            if not isinstance(writeArray, collections.abc.Sequence):
                raise TypeError("data must be sequence")
            writeArray = np.array(tuple(map(float, writeArray)))
            print(writeArray)
        numsampsperchan = len(writeArray)
        dataLayout = self.selectVal("GroupByChannel, GroupByScanNumber",
                                    dataLayout)
        reserved = None
        
        return vars()

    def read(self):
        NotImplemented

    def write(self, data):
        NotImplemented

with MyTask_AIO_F64(
    device = "Dev1",
    AIChan = "ai0",
    AOChan = "ao0") as task:

    task.CreateAOVoltageChan(0, 10)
    #task.CreateAOFuncGenChan("Triangle", 100, 1, 2)
    task.CfgSampClkTiming(1000)
    task.WriteAnalogF64(range(10))
