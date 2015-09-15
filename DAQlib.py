import PyDAQmx  as PDm
import numpy    as np
import contextlib, collections, functools

@contextlib.contextmanager
def opentask():
    
    task = PDm.Task()
    print("open task ->", task)

    try:
        yield task

    finally:
        print("close task ->", task)
        task.ClearTask()

def inputconfig(task):
    task.CreateAIVoltageChan("Dev1/ai0",
                             "AIF64",
                             PDm.DAQmx_Val_Cfg_Default,
                             -10.0,10.0,
                             PDm.DAQmx_Val_Volts,
                             None)

    task.CfgSampClkTiming("",
                          1000.0,
                          PDm.DAQmx_Val_Rising,
                          PDm.DAQmx_Val_FiniteSamps,
                          100000)

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


with opentask() as analogF64:
    inputconfig(analogF64)
    result          = ReadTask(analogF64,10)
    result_average  = VoltageFloat(np.average(result))
    result_std      = VoltageFloat(np.std(result))


