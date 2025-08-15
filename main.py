from src.dualcontour.DCSerial import DCSerial
from src.dualcontour.DCParallel import DCParallel
from src.utils.WavefrontParser import WavefrontParser

from math import sin,cos,pi
def f( x,y,z ):
    w = pi
    return sin(w*x)*cos(w*y) + sin(w*y)*cos(w*z) + sin(w*z)*cos(w*x)
#f = lambda x,y,z : x**2 + y**2 + z**2 - 0.9


domain = DCParallel( f , ( -1.0,1.0,-1.0,1.0,-1.0,1.0 ), (40,40,40) )
nodes, elements = domain.DualContour2D()
WavefrontParser.parse( "mesh.obj", nodes, elements )
