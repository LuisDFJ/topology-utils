from src.dualcontour.DCGeneric import DCGeneric
from src.topology.C1 import C1

from typing import Callable

class DCSerial( DCGeneric ):
    def __init__(self,
        f: Callable[[float, float, float], float],
        D: tuple[float, float, float, float, float, float] = (-1.0,1.0,-1.0,1.0,-1.0,1.0),
        N: tuple[int, int, int] = (10,10,10) ) -> None:
        super().__init__(f, D, N)

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



