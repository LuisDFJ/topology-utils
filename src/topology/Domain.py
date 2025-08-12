from src.topology.C0 import C0
from src.topology.C1 import C1
from src.topology.C2 import C2
from src.topology.C3 import C3

from typing import Callable

class Domain:
    def __init__(
            self,
            f : Callable[ [ float, float, float ], float ],
            D : tuple[ float, float, float, float, float, float ] = ( -1, 1, -1, 1, -1, 1 ),
            N : tuple[ int, int, int ] = ( 4, 4, 4 )
        ) -> None:
        self.D = D
        self.N = N
        self.f = f
        self.M = (
            lambda x     : C0.map( N, D, *x ),
            lambda x, dx = ( 0, ) : C1.map( N, D, *x, *dx ),
            lambda x, dx = ( 0,0 ) : C2.map( N, D, *x, *dx ),
            lambda x, dx = ( 0,0,0 ) : C3.map( N, D, *x, *dx ),
        )

    def evalC1( self, u : int, v : int, w : int, d : int ):
        p, q = C1.getC0( u,v,w,d )
        P, Q = self.f( *self.M[0]( p ) ), self.f( *self.M[0]( q ) )
        if ( P >= 0 ) != ( Q >= 0 ):
            A,B,C,D = C1.getC3( u,v,w,d )
            return (
                self.M[3]( A ),
                self.M[3]( B ),
                self.M[3]( C ),
                self.M[3]( D ),
            )
        return None

    @classmethod
    def OptimizeSurface(
        cls,
        nodes : list[ tuple[ float, float, float ] ],
        elements : list[ tuple[ int, ... ] ],
    ):
        pass

    def DualContour2D( self ):
        nodes = []
        elements = []
        for c1 in C1.iter( self.N ):
            facet = self.evalC1( *c1 )
            if not isinstance( facet, type( None ) ):
                element = []
                for n in facet:
                    if not n in nodes: nodes.append( n )
                    element.append( nodes.index( n ) )
                elements.append( tuple( element ) )
        return nodes, elements



