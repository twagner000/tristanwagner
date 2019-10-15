from django.db import models
from django.db.models import F
import json

ADJ_RING = {0:0, 1:2, 2:1, 3:3}
TRI_NEIGHBORS = {
    'top_bot':{'angles':(180,0),'naive':lambda r,c,fpd: ((r+1,c-1) if c%2 else (r-1,c+1)) if fpd else ((r-1,c-1) if c%2 else (r+1,c+1))},
    'left':{'angles':(300,240),'naive':lambda r,c,fpd: (r, c-1)},
    'right':{'angles':(60,120),'naive':lambda r,c,fpd: (r, c+1)},}

class World(models.Model):
    #dimensions should be multiples of 3 for evenly distributed start locations
    major_dim = models.PositiveSmallIntegerField(help_text="Number of major triangles per face edge.")
    minor_dim = models.PositiveSmallIntegerField(help_text="Number of minor triangles per major triangle edge.")
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        ordering = ['-date_created']
        
    def __str__(self):
        return 'w{}'.format(self.pk)
        
    def home_face_id(self):
        return self.face_set.get(ring=1, ring_i=0).id
        
    def update_cache(self):
        #update cache for children
        for face in self.face_set.all():
            face.update_cache()
        
        
class Face(models.Model):
    world = models.ForeignKey('World', on_delete=models.CASCADE)
    ring = models.PositiveSmallIntegerField()
    ring_i = models.PositiveSmallIntegerField()
    
    #cached fields
    _neigh_top_bot = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, related_name='face_top_bot_set')
    _neigh_left = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, related_name='face_left_set')
    _neigh_right = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, related_name='face_right_set')
    
    class Meta:
        ordering = ['world','ring','ring_i']
        unique_together = ['world','ring','ring_i']
        indexes = [
            models.Index(fields=['world','ring','ring_i']),
            models.Index(fields=['world']),
        ]
    
    def __str__(self):
        return '{} f({},{})'.format(self.world, self.ring, self.ring_i)
        
    @staticmethod
    def static_fpd(ring):
        return ring%2>0
        
    def fpd(self): #face points down
        return self.static_fpd(self.ring)
            
    def update_cache(self):
        self._neigh_top_bot = None
        self._neigh_left = None
        self._neigh_right = None
        
        #populate neighbors
        r = self.ring
        i = self.ring_i
        self._neigh_top_bot = Face.objects.get(world=self.world, ring=r+1-2*(r%2), ring_i=i)
        self._neigh_left = Face.objects.get(world=self.world, ring=ADJ_RING[r], ring_i=i if r==2 else (i-1)%5)
        self._neigh_right = Face.objects.get(world=self.world, ring=ADJ_RING[r], ring_i=i if r==1 else (i+1)%5)
        self.save()
        
        #update cache for children
        for tri in self.majortri_set.all():
            tri.update_cache()
            
    def neighbors(self):
        return {'top_bot':self._neigh_top_bot, 'left':self._neigh_left, 'right':self._neigh_right}
        
    def neighbor_ids(self):
        return dict((k,v.pk) for k,v in self.neighbors().items())
        
    def majortris(self):
        return self.majortri_set.all().values('id', 'i', 'sea')

        

class MajorTri(models.Model):
    face = models.ForeignKey('Face', on_delete=models.CASCADE)
    i = models.PositiveSmallIntegerField() #index (in face)
    sea = models.BooleanField(default=True)
    
    #cached fields
    _ri = models.PositiveSmallIntegerField(null=True, blank=True)
    _ci = models.PositiveSmallIntegerField(null=True, blank=True)
    _neigh_0 = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, related_name='majortri_0_set')
    _neigh_60 = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, related_name='majortri_60_set')
    _neigh_120 = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, related_name='majortri_120_set')
    _neigh_180 = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, related_name='majortri_180_set')
    _neigh_240 = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, related_name='majortri_240_set')
    _neigh_300 = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, related_name='majortri_300_set')
    _map = models.TextField(blank=True)

    
    class Meta:
        ordering = ['face','i']
        unique_together = ['face','i']
        indexes = [
            models.Index(fields=['face','i']),
            models.Index(fields=['face']),
        ]
    
    def __str__(self):
        return '{} mj({})'.format(self.face, self.i)
        
    @staticmethod
    def static_rci(i, n, fpd): #from index in face to row,col
        ripu = int(i**0.5)
        ripd = n-1-int((n**2-1-i)**0.5)
        cipu = i-ripu*ripu
        cipd = i-(n**2-(n-ripd)**2)
        return (ripd if fpd else ripu, cipd if fpd else cipu)
        
    @staticmethod
    def static_i(ri,ci,n,fpd): #from row,col to index in face
        if fpd:
            return ri*(2*n-ri)+ci #derived from (n**2-(n-ri)**2)+ci
        else:
            return ri**2+ci
            
    def rci(self): #row column index
        if self._ri and self._ci:
            return (self._ri,self._ci)
        return self.static_rci(self.i, self.face.world.major_dim, self.face.fpd())
        
    def tpd(self): #assuming fpd is accurate
        _,ci = self.rci()
        return self.face.fpd() != (ci%2>0)
            
    def update_cache(self):
        self._neigh_0 = None
        self._neigh_60 = None
        self._neigh_120 = None
        self._neigh_180 = None
        self._neigh_240 = None
        self._neigh_300 = None
        self._map = ''
        
        n = self.face.world.major_dim
        nei_faces = self.face.neighbors()
        fpd = self.face.fpd()
        tpd = self.tpd()
        ri,ci = self.rci()
        self._ri = ri
        self._ci = ci
        
        #calculate neighbors
        for dir,dirdict in TRI_NEIGHBORS.items():
            #generate naive neighbors
            nei_face = self.face
            nei_ri,nei_ci = dirdict['naive'](ri,ci,fpd)
            
            #handle neighbors on adjacent faces
            if nei_ri == -1 or nei_ri == n:
                nei_face = nei_faces['top_bot']
                nei_ri = n-1 if fpd else 0
                nei_ci -= 1
            elif nei_ci == -1:
                nei_face = nei_faces['left']
                nei_ri = nei_ri+1
                nei_ci = -1
            elif nei_ci > (2*(n-1-nei_ri) if fpd else 2*nei_ri):
                nei_face = nei_faces['right']
                nei_ci = 0
            
            #update model
            nei_i=self.static_i(nei_ri,nei_ci,n,nei_face.fpd())
            setattr(self, '_neigh_{}'.format(dirdict['angles'][int(tpd)]), MajorTri.objects.get(face=nei_face, i=nei_i))
            setattr(self, '_neigh_{}'.format(dirdict['angles'][1-int(tpd)]), None)

        self.save()
            
    def neighbor_ids(self):
        neighbors = dict((angle,getattr(self, '_neigh_{}'.format(angle))) for angle in range(0,360,60))
        return dict((k,None if not v else v.pk) for k,v in neighbors.items())


class MinorTri(models.Model):
    major_tri = models.ForeignKey('MajorTri', on_delete=models.CASCADE)
    i = models.PositiveSmallIntegerField()
    #land_terrain
    #under_terrain
    
    def __str__(self):
        return '{} mn({})'.format(self.majortri, self.i)
    
    class Meta:
        ordering = ['major_tri','i']
        unique_together = ['major_tri','i']
        indexes = [
            models.Index(fields=['major_tri','i']),
            models.Index(fields=['major_tri']),
        ]