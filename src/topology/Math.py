from typing import Callable, Self
import math

class Vec:
    def __init__( self,
        x : float, y : float, z : float
    ):
        self.x = x; self.y = y; self.z = z

    def toTuple( self ):
        return self.x, self.y, self.z

    def __iter__( self ):
        yield self.x
        yield self.y
        yield self.z

    def __add__( self, B : Self ):
        return Vec( self.x+B.x, self.y+B.y, self.z+B.z )

    def __sub__( self, B : Self ):
        return Vec( self.x-B.x, self.y-B.y, self.z-B.z )

    def __rmul__( self, a : float ):
        return Vec( a*self.x, a*self.y, a*self.z )

    def __truediv__( self, a : float ):
        return Vec( self.x/a, self.y/a, self.z/a )

    def __pow__( self, B : Self ):
        return self.x*B.x + self.y*B.y + self.z*B.z

    def __invert__( self ):
        return self / self.norm()

    def norm( self ):
        return math.sqrt( self.x**2 + self.y**2 + self.z**2 )

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
    def diffN(
        cls,
        x : float, y : float, z : float,
        f : Callable[ [float, float, float], float ]
    ):
        return ( ~Vec( *Math.diff( x,y,z,f ) ) ).toTuple()

    @classmethod
    def dot(
        cls,
        xa : float, ya : float, za : float,
        xb : float, yb : float, zb : float,
    ):
        return Vec(xa,ya,za) ** Vec(xb,yb,zb)

    @classmethod
    def clampCircular(
        cls,
        x : tuple[ float, float, float ],
        xc: tuple[ float, float, float ],
        r : float
    ):
        v = Vec( *x ); u = Vec( *xc )
        return ( u - min( ( u - v ).norm(), r ) * ~( u - v ) ).toTuple()
