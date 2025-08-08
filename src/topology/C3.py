# [0, N] x [0, N] x [0, N]
class C3:
    @classmethod
    def iter(cls, N : tuple[int,int,int]):
        for w in range( N[2] ):
            for v in range( N[1] ):
                for u in range( N[0] ):
                    yield u,v,w
  
    @classmethod
    def map(cls,
            N : tuple[int,int,int],
            D : tuple[float,float,float,float,float,float],
            u : int, v : int, w : int,
            du : float = 0,
            dv : float = 0,
            dw : float = 0,
        ):
        return (
            D[0] + ( u + du + 0.5 ) * (D[1] - D[0])/N[0],
            D[2] + ( v + dv + 0.5 ) * (D[3] - D[2])/N[1],
            D[4] + ( w + dw + 0.5 ) * (D[5] - D[4])/N[2],
        )

    @classmethod
    def getC0(cls, u : int, v : int, w : int):
        return (
            (  u,  v,  w), 
            (u+1,  v,  w), 
            (u+1,v+1,  w), 
            (  u,v+1,  w), 

            (  u,  v,w+1),
            (u+1,  v,w+1),        
            (u+1,v+1,w+1),
            (  u,v+1,w+1)
        )

    @classmethod
    def getC1(cls, u : int, v : int, w : int):
        return (
            (  u,  v,  w,  0),
            (  u,v+1,  w,  0),
            (  u,v+1,w+1,  0),
            (  u,  v,w+1,  0),

            (  u,  v,  w,  1),
            (  u,  v,w+1,  1),
            (u+1,  v,w+1,  1),
            (u+1,  v,  w,  1),

            (  u,  v,  w,  2),
            (u+1,  v,  w,  2),
            (u+1,v+1,  w,  2),
            (  u,v+1,  w,  2),
        )

    @classmethod
    def getC2(cls, u : int, v : int, w : int):
        return (
            (  u,  v,  w,  2),
            (  u,  v,w+1,  2),
            (  u,  v,  w,  1),
            (  u,v+1,  w,  1),
            (  u,  v,  w,  0),
            (u+1,  v,  w,  0),
        )
