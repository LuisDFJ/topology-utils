from typing import Callable
import numpy as np

class Opt:
    NMax = 5
    TOL  = 1e-5

    @classmethod
    def C1( cls, a : float, b : float, f : Callable[ [ float ], float ] ):
        x1,x0 = a, b 
        for _ in range( cls.NMax ):
            x1, x0 = x1 - f( x1 )/( (f(x1)-f(x0))/(x1-x0) ), x1
            if abs( f(x1) ) < cls.TOL: break 
        return x1

    @classmethod
    def C3( cls,
            A : list[ tuple[float, float, float] ],
            b : list[ float ] ):
        An = np.array( A ); bn = np.array( b )
        x, res, rank, s = np.linalg.lstsq( An, bn )
        return tuple( x.tolist() ), rank == 3
