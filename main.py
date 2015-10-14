from DAQlib import *
from DAQlib.mytask      import *
from DAQlib.mytask.AIO  import *
from DAQlib.mytask.edge import *

MEASUREFREQ = 1000
SAMPLEFREQ = MEASUREFREQ * 100

with StartEdge(device = "Dev1", channel = "ctr0",
               rate = MEASUREFREQ)\
               as EdgeTask,\
     AO_F64(device = "Dev1", channel = "ao0",
            minVal = 0, maxVal = 10,
            rate = SAMPLEFREQ)\
            as WriteTask,\
     AI_F64(device = "Dev1", channel = "ai0",
            minVal = 0, maxVal = 10,
            rate = SAMPLEFREQ)\
            as ReadTask:

    RWTasks = ReadTask, WriteTask
    

    for task in RWTasks:
        task.setup()
        EdgeTask.setTask(task)
    
