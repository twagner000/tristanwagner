ADJ_RING = {0:0, 1:2, 2:1, 3:3}
TRI_NEIGHBORS = {
    'top_bot':{'angles':(180,0),'naive':lambda r,c,fpd: ((r+1,c-1) if c%2 else (r-1,c+1)) if fpd else ((r-1,c-1) if c%2 else (r+1,c+1))},
    'left':{'angles':(300,240),'naive':lambda r,c,fpd: (r, c-1)},
    'right':{'angles':(60,120),'naive':lambda r,c,fpd: (r, c+1)},}
CONTINENT_SEED_RATIO = 0.2 #number of land seed tris as fraction of 1 face
CONTINENT_LAND_RATIO = 2.0 #number of faces covered

def row_list(n,pd):
    return [{'rn':2*(n-1-ri)+1 if pd else 2*ri+1, 'r0':n**2-(n-ri)**2 if pd else ri**2} for ri in range(n)]
    
def row_lists(n):
    return dict((pd,row_list(n,pd)) for pd in (True,False))
    
def i_from_rci(ri,ci,n,pd):
        if pd:
            return ri*(2*n-ri)+ci #derived from (n**2-(n-ri)**2)+ci
        else:
            return ri**2+ci
            
            
"""
def rci_from_i(i, n, fpd): #from index in face to row,col
    ripu = int(i**0.5)
    ripd = n-1-int((n**2-1-i)**0.5)
    cipu = i-ripu*ripu
    cipd = i-(n**2-(n-ripd)**2)
    return (ripd if fpd else ripu, cipd if fpd else cipu)
"""
    