from DAQlib.mytask import *
from util.argstools import *

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



class AIO_Base(AIO_Interface, MyTask, Analog):
    def __init__(self, device, channel, minVal, maxVal, rate):
        super().__init__(**self.getattrs(vars()))
    


@argssetter
class AO_F64(AIO_Base, Output):
        
    

    @argsdescriptor
    def CreateAOVoltageChan(self, minVal, maxVal, *,
                            units = "Volts",
                            customScaleName = None,
                            nameToAssignToChannel = None):
        
        units = self.selectVal("Volts, FromCustomScale", units)
        
        physicalChannel = self.getPhysicalChan()
        if nameToAssignToChannel is None:
            nameToAssingnToChannel = "Analog Output of {self}"\
                                     .format(**vars())
        return vars()
        

    #@argsdescriptor
    #def CreateAOFuncGenChan(self, type, freq, amplitude, offset, *, 
    #                        nameToAssignToChannel = None):
    #    types = "Sine,Triangle,Sawtooth,Square".split(",")
    #    try:
    #        type = getattr(PDm, "DAQmx_Val_{}".format(Type))
    #    except:
    #        raise ValueError("Choose Type in {Types}".format(**vars()))
    #    physicalChannel = self.getPhysicalChan("AO")
    #    if nameToAssignToChannel is None:
    #        nameToAssingnToChannel = "Analog FuncGen Output of {self}"\
    #                                 .format(**vars())
    #    return vars()

    @argsdescriptor
    def WriteAnalogF64(self, writeArray, *,
                       autoStart = True,
                       timeout = -1,
                       dataLayout = "GroupByChannel"):
        if not isinstance(writeArray, np.ndarray):
            if not isinstance(writeArray, collections.abc.Sequence):
                raise TypeError("data must be sequence")
            writeArray = np.array(writeArray, dtype = np.floatf64)
        numSampsPerChan = len(writeArray)
        dataLayout = self.selectVal("GroupByChannel, GroupByScanNumber",
                                    dataLayout)
        reserved = None
        
        return vars()    

    def write(self, data):
        return self.WriteAnalogF64(data)

    def setup(self):
        self.CreateAOVoltageChan(self.minVal, self.maxVal)
        self.CfgSampClkTiming()

@argssetter
class AI_F64(AIO_Base, Input):

    @argsdescriptor
    def CreateAIVoltageChan(self, minVal, maxVal, *,
                            units = "Volts",
                            customScaleName = None,
                            terminalConfig = "Cfg_Default",
                            nameToAssignToChannel = None):
        terminalConfig = self.selectVal(
            "Cfg_Default, RSE, NRSE, Diff, PseudoDiff", terminalConfig)
        units = self.selectVal("Volts, FromCustomScale", units)
        
        physicalChannel = self.getPhysicalChan()
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

    def setup(self):
        self.CreateAIVoltageChan(self.minVal, self.maxVal)
        self.CfgSampClkTiming()

#class AIO_F64(AI_F64, AO_F64):
#    def readwrite(self, data):
#        num = len(data)
#        writeT = threading.Thread(target = self.write, args = (data,))
#        readT  = threading.Thread(target = self.read,  args = (num,) )
#        writeT.start()
#        readT.start()
#        writeT.join()
#        return readT.join()
