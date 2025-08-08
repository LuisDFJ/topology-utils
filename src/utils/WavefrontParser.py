class WavefrontParser:
    @classmethod
    def parse(
        cls,
        filename : str,
        nodes : list[ tuple[ float, float, float ] ],
        elements : list[ tuple[ int, ... ] ]
    ):
        with open( filename, "w" ) as pFile:
            print( f"\n# Vertices [{len(nodes)}]:\n", file=pFile )
            for n in nodes:
                print( f"v {n[0]:0.4f} {n[1]:0.4f} {n[2]:0.4f}", file=pFile )

            print( f"\n# Elements [{len(elements)}]:\n", file=pFile )
            for element in elements:
                print( "f " + " ".join( [ str( e + 1 ) for e in element ] ), file=pFile )
        
