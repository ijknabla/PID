import PyDAQmx  as PDm
import numpy    as np
import contextlib, collections, functools, sys, inspect
from prefixedunit import VoltageFloat

def defaultargs_methodwrapper(meth):
    methname = meth.__name__
    
    #@functools.wraps(meth)
    def wrapped(self, *args, **kwrds):
        nonlocal methname
        print(meth, args, kwrds)
        cls = self.__class__ if not isinstance(self, type) else self
        super_ = super(cls, self)
        super_meth = getattr(super_, methname)

        try:
            argspec = inspect.getfullargspec(super_meth)
        except:
            argspec = None
            raise
        
        argsname = argspec.args #[self, arg0, arg1, ...]
        argsname = argsname[1:] #[arg0, arg1, ...      ]
        
        kwargsname = argspec.kwonlyargs
        kwargsname = kwargsname if kwargsname is not None else []

        print("yeah")
        varsdict = meth(self, *args, **kwrds)

        try:
            return super_meth(
                *(varsdict[arg] for arg in argsname),
                **dict((arg, varsdict[arg]) for arg in kwargsname)
                )
        except:
            raise
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

class AIO_Interface():
    
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
        return sampsPerChanWritten.value

    def ReadAnalogF64(self,
                      numSampsPerChan,
                      timeout,
                      fillMode,
                      #readArray,
                      arraySizeInSamps
                      #sampsPerChanRead,
                      #reserved)
                      ):
        readArray = np.zeros((numSampsPerChan,), dtype = np.float64)
        sampsPerChanRead = PDm.int32()
        reserved = None
        super().ReadAnalogF64(
            self,
            numSampsPerChan,
            timeout,
            fillMode,
            readArray,
            arraySizeInSamps,
            sampsPerChanRead,
            reserved)
        return readArray, sampsPerChanRead.value

class AIO_Base(AIO_Interface, PDm.Task):
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
            
            



class AO_F64(AIO_Base):
    

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
    def CreateAOFuncGenChan(self, type, freq, amplitude, offset, *, 
                            nameToAssignToChannel = None):
        types = "Sine,Triangle,Sawtooth,Square".split(",")
        try:
            type = getattr(PDm, "DAQmx_Val_{}".format(Type))
        except:
            raise ValueError("Choose Type in {Types}".format(**vars()))
        physicalChannel = self.getpysicalChannel("AO")
        if nameToAssignToChannel is None:
            nameToAssingnToChannel = "Analog FuncGen Output of {self}"\
                                     .format(**vars())
        return vars()

    @defaultargs_methodwrapper
    def WriteAnalogF64(self, writeArray, *,
                       autoStart = True,
                       timeout = -1,
                       dataLayout = "GroupByChannel"):
        if not isinstance(writeArray, np.ndarray):
            if not isinstance(writeArray, collections.abc.Sequence):
                raise TypeError("data must be sequence")
            writeArray = np.array(tuple(map(float, writeArray)))
        numSampsPerChan = len(writeArray)
        dataLayout = self.selectVal("GroupByChannel, GroupByScanNumber",
                                    dataLayout)
        reserved = None
        
        return vars()    

    def write(self, data):
        return self.WriteAnalogF64(data)


class AI_F64(AIO_Base):
    @defaultargs_methodwrapper
    def ReadAnalogF64(self, numSampsPerChan,  *,
                      timeout = -1,
                      fillmode = "GroupByChannel",
                      #readArray,
                      arraySizeInSamps = None
                      #sampsPerChanRead,
                      #reserved,
                      ):
        fillmode = selectVal("GroupByChannel, GroupByScanNumber", fillmode)
        if arraySizeInSamps is None:
            arraySizeInSamps = numSampsPerChan
        return vars()

    def read(self, num):
        return self.ReadAnalogF64(num)

class AIO_F64(AI_F64, AO_F64):pass
