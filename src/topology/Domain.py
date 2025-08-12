from src.topology.C0 import C0
from src.topology.C1 import C1
from src.topology.C2 import C2
from src.topology.C3 import C3

from src.topology.Opt import Opt
from src.topology.Math import Math

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

        self.C1_record = {}

    def evalC1( self, u : int, v : int, w : int, d : int ):
        def wrapper( u : int, v : int, w : int, d : int ):
            p, q = C1.getC0( u,v,w,d )
            P, Q = self.f( *self.M[0]( p ) ), self.f( *self.M[0]( q ) )
            if ( P >= 0 ) != ( Q >= 0 ):
                return C1.getC3( u,v,w,d )
            return None

        if not (u,v,w,d) in self.C1_record.keys(): self.C1_record[ (u,v,w,d) ] = wrapper( u,v,w,d )
        return self.C1_record[ (u,v,w,d) ]

    def optC1( self, u : int, v : int, w : int, d : int ):
        f  = lambda dx : self.f( *self.M[1]( (u,v,w,d), ( dx, ) ) )
        dx = Opt.C1( 0, 1, f )
        p  = self.M[1]( (u,v,w,d), ( dx, ) )
        return p, Math.diffN( *p, self.f )

    def OptimizeSurface(
        self,
        nodes : list[ tuple[ int, int, int ] ]
    ):
        opt_nodes = []
        keys = self.C1_record.keys()
        for node in nodes:
            pivots = []
            for c1 in C3.getC1( *node ):
                if c1 in keys: pivots.append( self.optC1( *c1 ) )
            #opt_nodes.append( self.M[3]( node ) )
        return opt_nodes

    def DualContour2D( self ):
        nodes    = []
        elements = []
        for c1 in C1.iter( self.N ):
            facet = self.evalC1( *c1 )
            if not isinstance( facet, type( None ) ):
                element = []
                for n in facet:
                    if not n in nodes: nodes.append( n )
                    element.append( nodes.index( n ) )
                elements.append( tuple( element ) )
        return self.OptimizeSurface( nodes ), elements



