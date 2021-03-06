import numpy as np
import scipy as sp
import scipy.interpolate as ip
import matplotlib.pyplot as plt
import itertools, functools, collections

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
        self.integral_func = self.get_integral_func()

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
        return map(lambda i : self.i2x(i), self.i_range())
        
    def sumup_matrix(self):
        return np.matrix(
            [
                [self[:i,:j].sum() for j in self.i_range()]
                for i in self.i_range()
                ]
            )

    def points_values4integral_func(self):
        for xd_xu, sumup in zip(
            itertools.product(self.x_range(), self.x_range()),
            np.nditer(self.sumup_matrix())
            ):
            yield xd_xu[::-1], sumup

    def get_integral_func(self):
        points, values = map(
            np.array,
            zip(*self.points_values4integral_func())
            )
        return ip.CloughTocher2DInterpolator(points, values)

    def __call__(self, x):
        
        if not self.min_x <= x <= self.max_x:
            raise ValueError("domain error, x must be within \
[{self.min_x}, {self.max_x}] got {x}".format(**locals()))

        if self.last_x < x:
            self.edges = list(self.up_edges_gen(x))
        elif x < self.last_x:
            self.edges = list(self.down_edges_gen(x))

        self.last_x = x
        return sum(edge.sign * self.integral_func(*edge.pos)
                   for edge in self.edges)

    def up_edges_gen(self, xu):
        xd_ = self.min_x
        for edge in self.edges:
            if xu < edge.pos.xu:
                xd_ = edge.pos.xd
                yield edge
            else:# edge.pos.xu <= xu
                pass
        if not xd_ == self.min_x:
            yield PreisachEdge((xu, xd_), -1)
        yield PreisachEdge((xu, self.max_x), +1)

    def down_edges_gen(self, xd):
        xu_ = None
        for edge in self.edges:
            if edge.pos.xd < xd:
                yield edge
                xu_ = edge.pos.xu 
            else:# xd <= edge.pos.xd
                if xu_ == None:
                    xu_ = edge.pos.xu
        if not (xu_ is None or xd == self.min_x):
            yield PreisachEdge((xu_, xd), +1)

class PreisachEdge():
    Position = collections.namedtuple("Position", "xu, xd")
    def __init__(self, pos, sign):
        self.pos    = self.Position(*pos)
        self.sign   = sign

    def __repr__(self):
        return "{self.__class__.__name__} object {0}, {self.pos}"\
               .format(
                   "+" if self.sign == +1 else "-"
                   **locals()
                   )


#testcode
if __name__ == "__main__":
    def test(preisach, N = 15, dx = 0.05):
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
    
    example = Preisach(
        [
            [1,1,2,3,2],
            [0,1,3,5,3],
            [0,0,2,3,2],
            [0,0,0,1,1],
            [0,0,0,0,1]
            ],
        range_x = (0, 10)
        )
    test(example)
