class C2:
    @classmethod
    def iter(cls, N : tuple[int,int,int]):
        for d in range( 3 ):
            for w in range( N[2] + ( 1 if d == 2 else 0 ) ):
                for v in range( N[1] + ( 1 if d == 1 else 0 ) ):
                    for u in range( N[0] + ( 1 if d == 0 else 0 ) ):
                        yield ( u,v,w,d )

    @classmethod
    def map(cls,
            N : tuple[int,int,int],
            D : tuple[float,float,float,float,float,float],
            u : int, v : int, w : int, d : int,
            du : float = 0,
            dv : float = 0,
        ):
        if d == 0:
            return (
                D[0] + u * (D[1] - D[0])/(N[0]+1),
                D[2] + ( v + du + 0.5 ) * (D[3] - D[2])/(N[1]+1),
                D[4] + ( w + dv + 0.5 ) * (D[5] - D[4])/(N[2]+1),
            )
        if d == 1:
            return (
                D[0] + ( u + dv + 0.5 ) * (D[1] - D[0])/(N[0]+1),
                D[2] + v * (D[3] - D[2])/(N[1]+1),
                D[4] + ( w + du + 0.5 ) * (D[5] - D[4])/(N[2]+1),
            )
        if d == 2:
            return (
                D[0] + ( u + du + 0.5 ) * (D[1] - D[0])/(N[0]+1),
                D[2] + ( v + dv + 0.5 ) * (D[3] - D[2])/(N[1]+1),
                D[4] + w * (D[5] - D[4])/(N[2]+1),
            )

    @classmethod
    def getC0(cls, u : int, v : int, w : int, d : int):
        if d == 0:
            return (
                (  u,  v,  w),
                (  u,  v,w+1),
                (  u,v+1,w+1),
                (  u,v+1,  w),
            )
        if d == 1:
            return (
                (  u,  v,  w),
                (  u,  v,w+1),
                (u+1,  v,w+1),
                (u+1,  v,  w),
            )
        if d == 2:
            return (
                (  u,  v,  w),
                (u+1,  v,  w),
                (u+1,v+1,  w),
                (  u,v+1,  w),
            )

    @classmethod
    def getC1(cls, u : int, v : int, w : int, d : int):
        if d == 0:
            return (
                (  u,  v,  w,  2), (  u,v+1,  w,  2),
                (  u,  v,  w,  1), (  u,  v,w+1,  1),
            )
        if d == 1:
            return (
                (  u,  v,  w,  2), (u+1,  v,  w,  2),
                (  u,  v,  w,  0), (  u,  v,w+1,  0),
            )
        if d == 2:
            return (
                (  u,  v,  w,  1), (u+1,  v,  w,  1),
                (  u,  v,  w,  0), (  u,v+1,  w,  0),
            )

    @classmethod
    def getC3(cls, u : int, v : int, w : int, d : int):
        if d == 0:
            return (  u,  v,  w), (u-1,  v,  w)
        if d == 1:
            return (  u,  v,  w), (  u,v-1,  w)
        if d == 2:
            return (  u,  v,  w), (  u,  v,w-1)
