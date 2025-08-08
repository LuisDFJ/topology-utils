from src.topology.Domain import Domain
from src.utils.WavefrontParser import WavefrontParser

domain = Domain( lambda x,y,z : x**2 + y**2 + z**2 - 0.9, ( -1.0,1.0,-1.0,1.0,-1.0,1.0 ), (10,10,10) )
nodes, elements = domain.DualContour2D()
WavefrontParser.parse( "mesh.obj", nodes, elements )
