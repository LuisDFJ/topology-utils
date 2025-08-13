from typing import Callable
import math

class Math:

    H = 1e-6

    @classmethod
    def diff(
        cls,
        x : float, y : float, z : float,
        f : Callable[ [float, float, float], float ]
    ):
        return (
            f( x + Math.H, y, z ) - f( x - Math.H, y, z ),
            f( x, y + Math.H, z ) - f( x, y - Math.H, z ),
            f( x, y, z + Math.H ) - f( x, y, z - Math.H ),
        )

    @classmethod
    def normal(
        cls,
        x : float, y : float, z : float
    ):
        n = math.sqrt( x**2 + y**2 + z**2 )
        return x/n, y/n, z/n


    @classmethod
    def diffN(
        cls,
        x : float, y : float, z : float,
        f : Callable[ [float, float, float], float ]
    ):
        return Math.normal( *Math.diff( x,y,z,f ) )

    @classmethod
    def dot(
        cls,
        a : tuple[ float, float, float ],
        b : tuple[ float, float, float ]
    ):
        return a[0]*b[0] + a[1]*b[1] + a[2]*b[2] 
