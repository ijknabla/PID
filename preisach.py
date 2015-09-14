import numpy as np
import scipy as sp
import scipy.interpolate as ip
import itertools, functools, operator

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
        basefunc = ip.CloughTocher2DInterpolator(points, values)

        def integral_func(xu, xd):
            if xu >= xd:
                try:
                    xu_ = (xu - xd) * self.dist_x / (self.max_x - xd)
                    xu_ += self.min_x
                except ZeroDivisionError:
                    xu_ = self.min_x
                return 0 + basefunc(xu_, xd)
            else:#xu < xd
                return 0 + basefunc(0, xu)
        return integral_func 

    def __call__(self, x):
        if not self.min_x <= x <= self.max_x:
            raise ValueError("domain error, x must be within \
[{self.min_x}, {self.max_x}] got {x}".format(**locals()))

        if self.last_x < x:
            if not self.edges:
                self.edges.append(PreisachEdge((x, self.max_x), +1))
            else:
                new_edges = []
                for edge in self.edges:
                    if x < edge.pos[0]:
                        new_edge.append(edge)
                new_edges.append(PreisachEdge((x, self.max_x), +1))
                self.edges = new_edges
        elif x < self.last_x:
            new_edges = []
            for edge in self.edges:
                if edge.pos[1] < x:
                    new_edge.append(edge)
            new_edges[-1].pos[1] = x
            self.edges = new_edges
        
        
        print(self.edges)
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
    def __init__(self, pos, sign):
        self.pos    = pos
        self.sign   = sign

    def __repr__(self):
        return "{self.__class__.__name__} object {self.sign}, {self.pos}"\
               .format(**locals())

if __name__ == "__main__":
    a = Preisach(
        [
            [1,2,3],
            [0,4,5],
            [0,0,6],
            ],
        range_x = (-1, 1)
        )

    b = a.get_integral_func()

find = lambda name, obj : ["{1}".format(obj, i) for i in dir(obj) if name in i]
