class C1:
    @classmethod
    def iter(cls, N : tuple[int,int,int]):
        for d in range( 3 ):
            for w in range( N[2] + ( 0 if d == 2 else 1 ) ):
                for v in range( N[1] + ( 0 if d == 1 else 1 ) ):
                    for u in range( N[0] + ( 0 if d == 0 else 1 ) ):
                        yield ( u,v,w,d )

    @classmethod
    def map(cls,
            N : tuple[int,int,int],
            D : tuple[float,float,float,float,float,float],
            u : int, v : int, w : int, d : int,
            du : float = 0,
        ):
        return (
            D[0] + ( u + ( du + 0.5 ) if d == 0 else 0 ) * (D[1] - D[0])/N[0],
            D[2] + ( v + ( du + 0.5 ) if d == 1 else 0 ) * (D[3] - D[2])/N[1],
            D[4] + ( w + ( du + 0.5 ) if d == 2 else 0 ) * (D[5] - D[4])/N[2],
        )

    @classmethod
    def getC0(cls, u : int, v : int, w : int, d : int):
        if d == 0:
            return (  u,  v,  w), (u+1,  v,  w)
        if d == 1:
            return (  u,  v,  w), (  u,v+1,  w)
        if d == 2:
            return (  u,  v,  w), (  u,  v,w+1)
        return (0,0,0),(0,0,0)

    @classmethod
    def getC2(cls, u : int, v : int, w : int, d : int):
        if d == 0:
            return (
                (  u,  v,  w,  1), (  u,v-1,  w,  1),
                (  u,  v,  w,  2), (  u,  v,w-1,  2),
            )
        if d == 1:
            return (
                (  u,  v,  w,  0), (u-1,  v,  w,  0),
                (  u,  v,  w,  2), (  u,  v,w-1,  2),
            )
        if d == 2:
            return (
                (  u,  v,  w,  0), (u-1,  v,  w,  0),
                (  u,  v,  w,  1), (  u,v-1,  w,  1),
            )
        return ( 0,0,0,0 ), ( 0,0,0,0 ), ( 0,0,0,0 ), ( 0,0,0,0 )
    @classmethod
    def getC3(cls, u : int, v : int, w : int, d : int):
        if d == 0:
            return (
                (  u,  v,  w),
                (  u,  v,w-1),
                (  u,v-1,w-1),
                (  u,v-1,  w),
            )
        if d == 1:
            return (
                (  u,  v,  w),
                (  u,  v,w-1),
                (u-1,  v,w-1),
                (u-1,  v,  w),
            )
        if d == 2:
            return (
                (  u,  v,  w),
                (u-1,  v,  w),
                (u-1,v-1,  w),
                (  u,v-1,  w),
            )
        return ( 0,0,0 ), ( 0,0,0 ), ( 0,0,0 ), ( 0,0,0 )
