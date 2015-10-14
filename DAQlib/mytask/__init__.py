from util.argstools import *
from DAQlib import *
from abc import ABCMeta


__all__ = ["MyTaskInterface", "MyTaskBase", "MyTask", "Counter", "Input", "Output", "Analog", "Digital"]

class MyTaskInterface:
    pass

class MyTaskBase(PDm.Task):
    pass

@argssetter
class MyTask(MyTaskInterface, MyTaskBase):
    def __init__(self, *args, **kwrds):
        super().__init__()
        self.attrs = []
        for attr, value in kwrds.items():
            self.attrs.append(attr)
            setattr(self, attr, value)

    def getattrs(self, kwrds, option = []):
        return dict(
            (k, v) for k, v in kwrds.items()
            if (k not in {"self", "__class__"}
                and k not in option)
            )

    
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

    def getPhysicalChan(self):
        return "{self.device}/{self.channel}".format(**vars())

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

    @argsdescriptor
    def CfgSampClkTiming(self, rate = None, *,
                         #defaultarguement
                         source = None,
                         activeEdge = PDm.DAQmx_Val_Rising,
                         sampleMode = PDm.DAQmx_Val_ContSamps,
                         sampsPerChan = 0):
        try:
            rate = rate if rate else self.rate
        except AttributeError:
            passS
        return vars()

    @argsdescriptor
    def CfgImplicitTiming(self, *,
                          sampleMode = "ContSamps",
                          sampsPerChan = 0
                          ):
        sampleMode = self.selectVal(
            "FiniteSamps, ContSamps, HWTimedSinglePoint",
            sampleMode)
        return vars()

    @classmethod
    def inspectargsname(cls, name):
        doc = getattr(cls, name).__doc__
        doc = "(self, {})".format(doc.split("(")[1].split(")")[0])
        print(doc)

    @classmethod
    def inspectValbyDocument(cls, doc):
        result = doc.split("\n")
        result = map(lambda x : x.split("\t")[0], result)
        result = filter(lambda x : "DAQmx_Val" in x, result)
        result = map(lambda x : x[len("DAQmx_Val_"):], result)

        return ", ".join(result)

class Counter:
    __metaclass__ = ABCMeta

class Input:
    __metaclass__ = ABCMeta

class Output:
    __metaclass__ = ABCMeta

class Analog:
   __metaclass__ = ABCMeta

class Digital:
   __metaclass__ = ABCMeta