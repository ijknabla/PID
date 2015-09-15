import numpy as np
import scipy as sp
import scipy.interpolate as ip
import matplotlib.pyplot as plt
import itertools, functools, collections, operator

class Triangular:
    pass

class LowwerTriangular(Triangular):
    pass

class UpperTriangular(Triangular):
    pass

class Preisach(np.matrix):
    def __new__(cls,
                data, *args,
                **kwrds):
        
        return super(Preisach, cls).__new__(
            cls, data,
            **dict((key, value)
                   for key, value in kwrds.items()
                   if key in {"dtype", "copy"})
            )
    
    def __init__(self,
                 data, *,
                 range_x = (0.0, 1.0),
                 isPositive = True,
                 **kwrds):

        if not self.ndim == 2:
            raise ValueError("data.ndim must be 2 got {self.ndim}"\
                             .format(**locals()))
        if not self.shape[0] == self.shape[1]:
            raise ValueError(
                "data must be interpreted as square matrix, \
data.size = {self.shape}".format(**locals())
                )
        
        self.mask = np.zeros(self.shape, dtype = np.bool)

        self.min_x = range_x[0]
        self.max_x = range_x[1]
        #self.dist_x == (self.max_x - self.min_x) / self.shape[0]
        self.last_x = self.min_x
        self.edges = []
        self.isPositive = isPositive

    def __getattr__(self, attr):
        if attr == "dist_x":
            return (self.max_x - self.min_x)
        elif attr == "dim":
            return self.shape[0]
        else:
            raise AttributeError(
                "'{self.__class__.__name__}' object has no attribute '{attr}'"\
                .format(**locals())
                )
    
    def i_range(self):
        return range(self.dim+1)

    def i2x(self, i):
        if 0 < i < self.dim:
            return ((self.dim - i) * self.min_x + i * self.max_x) / self.dim
        else:
            return self.max_x if i else self.min_x

    def x_range(self):
        return map(lambda i : self.i2x(i), self.irange())
        
    def sumup_matrix(self):
        return np.matrix(
            [
                [self[:i,:j].sum() for j in self.i_range()]
                for i in self.i_range()
                ]
            )

    def points_values4integral_func(self):
        for i, row in enumerate(self.sumup_matrix().A):
            xd = self.i2x(i)
            for j, value in enumerate(row[i:]):
                try:
                    xu = self.i2x(j * self.dim / (self.dim - i))
                    yield (xu, xd), value
                except ZeroDivisionError:
                    yield (self.min_x, xd), value
        yield (xd, xd), value

    def get_integral_func(self):
        points, values = map(
            np.array,
            zip(*self.points_values4integral_func())
            )
        
        #basefunc = ip.CloughTocher2DInterpolator(points, values)
        basefunc = lambda x : x

        def integral_func(xu, xd):
            if xu > xd:
                if self.max_x - xd:
                    xu_ = (xu - xd) * self.dist_x / (self.max_x - xd)
                    xu_ += self.min_x
                else:
                    xu_ = self.min_x
                return 0 + basefunc(xu_, xd)
            elif xu == xd:
                return 0 + basefunc(self.min_x,   xd)
            else:#xu < xd
                return 0 + basefunc(self.min_x,   xu)
        return integral_func 

    def __call__(self, x):
        if not self.min_x <= x <= self.max_x:
            raise ValueError("domain error, x must be within \
[{self.min_x}, {self.max_x}] got {x}".format(**locals()))

        if self.last_x < x:
            new_edges = []
            xd_ = self.min_x
            for edge in self.edges:
                if x < edge.pos.xu:
                    xd_ = edge.pos.xd
                    new_edges.append(edge)
                else:# edge.pos.xu <= x
                    pass
            if not xd_ == self.min_x:
                new_edges.append(PreisachEdge((x, xd_),      -1))
            new_edges.append(PreisachEdge((x, self.max_x),  +1))
            self.edges = new_edges
        elif x < self.last_x:
            new_edges = []
            xu_ = None
            for edge in self.edges:
                if edge.pos.xd < x:
                    new_edges.append(edge)
                    xu_ = edge.pos.xu 
                else:# x <= edge.pos.xd
                    if xu_ == None:
                        xu_ = edge.pos.xu
            if not xu_ is None and x != 0:
                new_edges.append(PreisachEdge((xu_, x), +1))
            self.edges = new_edges
        
        integral_func = self.get_integral_func()

        self.last_x = x
        return sum(edge.sign * integral_func(*edge.pos)
                   for edge in self.edges)
        """
        index, rest = self.getindex(x)
        print("index =", index)
        if index < self.last_index:
            self.mask[index:self.last_index+1].fill(False)
        elif self.last_index < index:
            self.mask[:,:index].fill(True)
        self.last_index = index

        return self.sum_by_mask()
        
    def sum_by_mask(self):
        return np.sum(self.getA() * self.mask)

    def getindex(self, x):
        div_mod = np.array(divmod(x - self.min_x, self.dist_x))
        div_mod += (1, -1) if round(div_mod[1]) == 1 else (0, 0)
        return int(div_mod[0]), div_mod[1]
    """


class PreisachEdge():
    Position = collections.namedtuple("Position", "xu, xd")
    def __init__(self, pos, sign):
        self.pos    = self.Position(*pos)
        self.sign   = sign

    def __repr__(self):
        return "{self.__class__.__name__} object {self.sign}, {self.pos}"\
               .format(**locals())

def test(preisach, N = 10, dx = 0.05):
    sumples = []
    for i in range(N, -1, -1):
        propotion = i / N
        sumples.extend([preisach.min_x,
                        preisach.min_x + propotion * preisach.dist_x])
    sumples = np.array(sumples) // dx * dx
    
    def xlist_gen():
        for i, j in zip(sumples, sumples[1:]):
            result = []
            if i < j:
                while i < j:
                    result.append(i)
                    i += dx
            elif i > j:
                while  i > j:
                    result.append(i)
                    i -= dx
            yield result
            
    for xlist in xlist_gen():        
        points  = np.array(tuple(xlist))
        results = np.array(tuple(map(preisach, xlist)))
        plt.plot(points, results)
    plt.show()
    return sumples, points, results
    


if __name__ == "__main__":
    example = Preisach(
        [
            [1,1,1,1,1],
            [0,1,1,1,1],
            [0,0,1,1,1],
            [0,0,0,1,1],
            [0,0,0,0,1]
            ],
        range_x = (0, 10)
        )
    test(example)


    

    

find = lambda name, obj : ["{1}".format(obj, i) for i in dir(obj) if name in i]
