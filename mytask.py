import PyDAQmx  as PDm
import numpy    as np
import contextlib, collections, functools, sys, inspect
import threading
from prefixedunit import VoltageFloat
from argstools import *


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
        super().WriteAnalogF64(numSampsPerChan,
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
        super().ReadAnalogF64(numSampsPerChan,
                              timeout,
                              fillMode,
                              readArray,
                              arraySizeInSamps,
                              PDm.byref(sampsPerChanRead),
                              reserved)
        return readArray[:sampsPerChanRead.value]

@argssetter
class AIO_Base(AIO_Interface, PDm.Task):
    def __init__(self, *args, **kwrds):
        super().__init__()
        self.attrs = []
        for attr, value in kwrds.items():
            self.attrs.append(attr)
            setattr(self, attr, value)

    
    def __repr__(self):
        return "{self.__class__.__name__}({})".format(
            ", ".join("{} = {}".format(attr, getattr(self, attr))
                      for attr in self.attrs),
            **locals()
            )
    
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
            raise NameError("Val(given is {name})must be in {selector}"\
                            .format(**vars()))
        try:
            return self.getVal(name)
        except:
            raise

    

    def getpysicalChannel(self, name):
        if name.lower() == "ai":
            return "{self.device}/{self.AIChan}".format(**vars())
        elif name.lower() == "ao":
            return "{self.device}/{self.AOChan}".format(**vars())    

    @argsdescriptor
    def CfgSampClkTiming(self, rate, *,
                         #defaultarguement
                         source = None,
                         activeEdge = PDm.DAQmx_Val_Rising,
                         sampleMode = PDm.DAQmx_Val_ContSamps,
                         sampsPerChan = 10):
        return vars()
            
            


@argssetter
class AO_F64(AIO_Base):
    

    @argsdescriptor
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
        

    @argsdescriptor
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

    @argsdescriptor
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

@argssetter
class AI_F64(AIO_Base):

    @argsdescriptor
    def CreateAIVoltageChan(self, minVal, maxVal, *,
                            units = "Volts",
                            customScaleName = None,
                            terminalConfig = "Cfg_Default",
                            nameToAssignToChannel = None):
        terminalConfig = self.selectVal(
            "Cfg_Default, RSE, NRSE, Diff, PseudoDiff", terminalConfig)
        units = self.selectVal("Volts, FromCustomScale", units)
        
        physicalChannel = self.getpysicalChannel("AI")
        if nameToAssignToChannel is None:
            nameToAssingnToChannel = "Analog Output of {self}"\
                                     .format(**vars())
        return vars()

    
    @argsdescriptor
    def ReadAnalogF64(self, numSampsPerChan,  *,
                      timeout = -1,
                      fillMode = "GroupByChannel",
                      #readArray,
                      arraySizeInSamps = None
                      #sampsPerChanRead,
                      #reserved,
                      ):
        fillMode = self.selectVal("GroupByChannel, GroupByScanNumber", fillMode)
        if arraySizeInSamps is None:
            arraySizeInSamps = numSampsPerChan
        return vars()

    def read(self, num):
        return self.ReadAnalogF64(num)

class AIO_F64(AI_F64, AO_F64):
    def readwrite(self, data):
        num = len(data)
        writeT = threading.Thread(target = self.write, args = (data,))
        readT  = threading.Thread(target = self.read,  args = (num,) )
        writeT.start()
        readT.start()
        writeT.join()
        return readT.join()
        
        
