import functools, inspect, collections
__all__ = ('argsdescriptor', 'argssetter')

def argssetter(obj):
    if isinstance(obj, type):
        cls = obj
        for attr, content in cls.__dict__.items():
            if isinstance(content, argsdescriptor):

                methname, descriptor = attr, content
                wrapped = descriptor.wrap_supermethod(cls, methname)

                setattr(cls, methname, wrapped)
        return cls

class argsdescriptor:
    def __init__(self, descriptor):
        self.descriptor = descriptor

    def __call__(self, *args, **kwrds):
        raise NotImplementedError(
            "can't call argsdescriptor"
            )

    def convertargs(self, *args, **kwrds):
        converted = self.descriptor(*args, **kwrds)
        args, kwrds = None, None
        if isinstance(converted, collections.abc.Sized)\
           and len(converted) == 2:
            obj0, obj1 = converted
            if isinstance(obj0, collections.abc.Sequence)\
               and isinstance(obj1, (dict, collections.abc.Mapping)):
                args, kwrds = obj0, obj1
        if args is None and kwrds is None:
            if isinstance(converted, (dict, collections.abc.Mapping)):
                args, kwrds = (), converted
            else:
                raise TypeError(
                    """argsdescriptor returns {converted} return must be
(Sequence_of_positional, dict_or_Mapping_of_keyword)"""\
                    .format(**locals())
                    )
        return args, kwrds

    def wrap_supermethod(self, cls, methname):
        @functools.wraps(self.descriptor)
        def resultmethod(self_, *args, **kwrds):
            boundmethod = getattr(super(cls, self_), methname)
            fullargspec = inspect.getfullargspec(boundmethod)
            
            args, kwrds = self.convertargs(self_, *args, **kwrds)
            
            if fullargspec.varkw is None:
                allvarnames = fullargspec.args[1:] + fullargspec.kwonlyargs
                kwrds = dict((key, val) for key, val in kwrds.items()
                             if key in allvarnames)
                
            return boundmethod(*args, **kwrds)
        
        return resultmethod
    

    def wrap(self, func):
        fullargspec = inspect.getfullargspec(func)
        allvarnames = fullargspec.args + fullargspec.kwonlyargs
        
        @functools.wraps(self.descriptor)
        def returnfunc(*args, **kwrds):
            nonlocal fullargspec, allvarnames    
            
            args, kwrds = self.convertargs(*args, **kwrds)
            kwrds = dict((key, val) for key, val in kwrds.items()
                         if key in allvarnames)
            
            return func(*args, **kwrds)
        
        return resultfunc


if __name__ == "__main__":
    arg = list(range(3))

    class A():
        def meth(self, a, b, c):
            return a + b + c

    @argssetter
    class B0(A):
        @argsdescriptor
        def meth(self, seq):
            a, b, c = seq
            return a, b, c

    @argssetter
    class B1(A):
        @argsdescriptor
        def meth(self, seq):
            a, b, c = seq
            return vars()

    @argssetter
    class B2(A):
        @argsdescriptor
        def meth(self, seq):
            a, b, c = seq
            return (a,), {"b" : b, "c" : c}

    a, b0, b1, b2 = A(), B0(), B1(), B2()
