from src.topology.C1 import C1
from src.topology.C3 import C3
from src.topology.Opt import Opt
from src.topology.Math import Math
from src.dualcontour.DCGeneric import DCGeneric

from typing import Callable
from multiprocessing import Pool, Queue, cpu_count
from functools import partial

CPU = cpu_count()

def evalC1(
    u : int, v : int, w : int, d : int,
    f: Callable[[float, float, float], float],
    D: tuple[float, float, float, float, float, float],
    N: tuple[int, int, int]
):
    if C1.bool( N, D, u,v,w,d, f ):
        return C1.getC3( u,v,w,d )
    return None

def task(
    u : int, v : int, w : int, d : int,
    f: Callable[[float, float, float], float],
    D: tuple[float, float, float, float, float, float],
    N: tuple[int, int, int],
    queue : Queue
):
    facet = evalC1( u,v,w,d,f,D,N )
    if not isinstance( facet, type(None) ):
        queue.put( facet )



def optC1(
    u : int, v : int, w : int, d : int,
    f: Callable[[float, float, float], float],
    D: tuple[float, float, float, float, float, float],
    N: tuple[int, int, int]
):
    g  = lambda dx : f( *C1.map( N,D,u,v,w,d,dx ) ) 
    dx = Opt.C1( -0.5, 0.5, g )
    p  = C1.map( N,D,u,v,w,d,dx )
    return p, Math.diffN( *p, f )

def optC3(
    u : int, v : int, w : int,
    f: Callable[[float, float, float], float],
    D: tuple[float, float, float, float, float, float],
    N: tuple[int, int, int]
):
    A = []; b = []
    for c1 in C3.getC1( u,v,w ):
        if C1.bool( N, D, *c1, f ):
            p, n = optC1( *c1, f, D, N )
            A.append( n ); b.append( Math.dot( *n, *p ) )
    x, rank = Opt.C3( A, b )
    if rank: 
        return x
    else:
        #L = self.L
        #A = A + [ (L,0,0), (0,L,0), (0,0,L) ]
        #b = b + list( self.M[3]( (u,v,w) ) )
        #x, rank = Opt.C3( A, b )
        #if rank:
        #    return x
        #else:
            #return Math.clampCircular( x, self.M[3]( (u,v,w) ), self.r )
        return C3.map( N,D,u,v,w )

class DCParallel( DCGeneric ):
    def __init__(self,
        f: Callable[[float, float, float], float],
        D: tuple[float, float, float, float, float, float] = (-1.0,1.0,-1.0,1.0,-1.0,1.0),
        N: tuple[int, int, int] = (10,10,10) ) -> None:
        super().__init__(f, D, N)

    def OptimizeSurface(
        self,
        nodes : list[ tuple[ int, int, int ] ]
    ):
        with Pool( processes=cpu_count() ) as pool:
            opt_nodes = pool.starmap( partial( optC3, f = self.f, D = self.D, N = self.N ), nodes  )
        return opt_nodes

    def DualContour2D2( self ):
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
