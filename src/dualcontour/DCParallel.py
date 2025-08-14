from ctypes import Array
import ctypes
from src.topology.C1 import C1
from src.dualcontour.DCGeneric import DCGeneric

from typing import Callable
from multiprocessing import Process, RawArray, cpu_count

CPU = cpu_count()

class DCParallel( DCGeneric ):
    def __init__(self,
        f: Callable[[float, float, float], float],
        D: tuple[float, float, float, float, float, float] = (-1.0,1.0,-1.0,1.0,-1.0,1.0),
        N: tuple[int, int, int] = (10,10,10) ) -> None:
        super().__init__(f, D, N)

    def OptimizeSurfaceTask(
        self,
        nodes : list[ tuple[ int, int, int ] ],
        idx0 : int, idxf : int,
        array : tuple[ Array, Array, Array ] ,
        cpu : int
    ):
        print( f"Running Task ({cpu})" )
        for i in range( idx0, idxf ):
            x,y,z = self.optC3( *nodes[ i ] )
            array[0][i] = x; array[1][i] = y; array[2][i] = z;
        print( f"Finishing Task ({cpu})" )

    def OptimizeSurface(
        self,
        nodes : list[ tuple[ int, int, int ] ]
    ):
        N = len( nodes ); N_CPU = N // CPU; R_CPU = N % CPU
        idxf = N_CPU + R_CPU; idx0 = 0
        shared_memory = (
            RawArray( ctypes.c_double, N ),
            RawArray( ctypes.c_double, N ),
            RawArray( ctypes.c_double, N )
        )
        pool = []
        for cpu in range( CPU ):
            pool.append(
                Process( target=self.OptimizeSurfaceTask, name=f"Subprocess {cpu}/{CPU}", args=( nodes, idx0, idxf, shared_memory, cpu ) )
            )
            idx0  = idxf; idxf += N_CPU

        for p in pool: p.start()
        for p in pool: p.join()

        return [ ( x,y,z ) for x,y,z in zip( *shared_memory ) ]

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



