from src.topology.C0 import C0
from src.topology.C1 import C1
from src.topology.C2 import C2
from src.topology.C3 import C3

from src.topology.Opt import Opt
from src.topology.Math import Math

import numpy as np

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
        self.r = max( (D[1]-D[0])/self.N[0], (D[3]-D[2])/self.N[1],(D[5]-D[4])/self.N[2] )
        self.L = 1.0
        print( self.r, self.L )

    def evalC1( self, u : int, v : int, w : int, d : int ):
        if C1.bool( self.N, self.D, u,v,w,d, self.f ):
            return C1.getC3( u,v,w,d )
        return None

    def optC1( self, u : int, v : int, w : int, d : int ):
        f  = lambda dx : self.f( *self.M[1]( (u,v,w,d), ( dx, ) ) )
        dx = Opt.C1( -0.5, 0.5, f )
        if dx > 0.5 or dx < -0.5: print( dx )
        p  = self.M[1]( (u,v,w,d), ( dx, ) )
        return p, Math.diffN( *p, self.f )

    def optC3( self, u : int, v : int, w : int ):
        A = []; b = []
        for c1 in C3.getC1( u,v,w ):
            if C1.bool( self.N, self.D, *c1, self.f ):
                p, n = self.optC1( *c1 )
                A.append( n ); b.append( Math.dot( *n, *p ) )
        x, rank = Opt.C3( A, b )
        if rank: 
            return x
        else:
            L = self.L
            A = A + [ (L,0,0), (0,L,0), (0,0,L) ]
            b = b + list( self.M[3]( (u,v,w) ) )
            x, rank = Opt.C3( A, b )
            if rank:
                return x
            else:
                return Math.clampCircular( x, self.M[3]( (u,v,w) ), self.r )
                #return self.M[3]( (u,v,w) )

    def OptimizeSurface(
        self,
        nodes : list[ tuple[ int, int, int ] ]
    ):
        opt_nodes = []
        for node in nodes:
            opt_nodes.append( self.optC3( *node ) )
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



