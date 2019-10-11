from django.db import models
from django.db.models import F
import json

ADJ_RING = {0:0, 1:2, 2:1, 3:3}

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
        
    def clear_cache(self):
        self._neigh_top_bot = None
        self._neigh_left = None
        self._neigh_right = None
        self.save()
        
        #clear cache for all child MajorTri
        for tri in self.majortri_set.all():
            tri.clear_cache()
        
    def neighbors(self,include_self=False):
        if not self._neigh_top_bot or not self._neigh_left or not self._neigh_right:
            r = self.ring
            i = self.ring_i
            self._neigh_top_bot = Face.objects.get(world=self.world, ring=r+1-2*(r%2), ring_i=i)
            self._neigh_left = Face.objects.get(world=self.world, ring=ADJ_RING[r], ring_i=i if r==2 else (i-1)%5)
            self._neigh_right = Face.objects.get(world=self.world, ring=ADJ_RING[r], ring_i=i if r==1 else (i+1)%5)
            self.save()
        neighbors = {'top_bot':self._neigh_top_bot, 'left':self._neigh_left, 'right':self._neigh_right}
        if include_self:
            neighbors['center'] = self
        return neighbors
        
    def neighbor_ids(self):
        return dict((k,v.pk) for k,v in self.neighbors().items())
        
    def majortris(self):
        return self.majortri_set.all().values('id', 'i', 'sea')

        

class MajorTri(models.Model):
    face = models.ForeignKey('Face', on_delete=models.CASCADE)
    i = models.PositiveSmallIntegerField() #index (in face)
    sea = models.BooleanField(default=True)
    
    #cached fields (neighbor names are accurate if current FACE points down)
    _neigh_top_bot = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, related_name='majortri_top_bot_set')
    _neigh_left = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, related_name='majortri_left_set')
    _neigh_right = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, related_name='majortri_right_set')
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
    def static_rci(i, n, tpd):
        ri = n-1-int((n*n-i-1)**0.5) if tpd else int((n*n-i-1)**0.5)
        ci = i-n*n+(n-ri)**2
        return ri,ci
        
    def rci(self): #row column index
        return self.static_rci(self.i, self.face.major_dim, self.face.tpd())
        
    def clear_cache(self):
        self._neigh_top_bot = None
        self._neigh_left = None
        self._neigh_right = None
        self._map = ''
        self.save()
        
    def neighbors(self):
        if not self._neigh_top_bot or not self._neigh_left or not self._neigh_right:
            n = self.face.world.major_dim
            r = self.major_row
            c = self.major_col
            fpd = self.face.points_down()
            nei_faces = self.face.neighbors()
            
            for dir in ('top_bot','left','right'):
                #generate naive neighbors
                nei_face = self.face
                if dir == 'top_bot':
                    nei_r,nei_c = (r+1,c-1) if c%2 else (r-1,c+1)
                if dir == 'left':
                    nei_r,nei_c = r, c-1 if fpd else c+1
                if dir == 'right':
                    nei_r,nei_c = r, c+1 if fpd else c-1
                
                #handle neighbors on adjacent faces
                if nei_r == -1:
                    nei_face,nei_r,nei_c = nei_faces['top_bot'], 0, 2*n-2-c
                if nei_c == -1:
                    nei_face = nei_faces['left'] if fpd else nei_faces['right']
                    dir_from_nei_face = [k for k,v in nei_face.neighbors().items() if v.id==self.face.id]
                    print(self.id,self.face.id,nei_face.id, dir_from_nei_face)
                    nei_face,nei_r,nei_c = nei_faces['left'], 0, 2*n-2-c
                if nei_c+2*nei_r>2*n-2:
                    nei_face,nei_r,nei_c = nei_faces['right'], n-1-r, 2*n-2-c
                    
                #update model
                setattr(self, '_neigh_{}'.format(dir), MajorTri.objects.get(face=nei_face, major_row=nei_r, major_col=nei_c))
            self.save()
        return {'top_bot':self._neigh_top_bot, 'left':self._neigh_left, 'right':self._neigh_right}
            
    def neighbor_ids(self):
        return dict((k,None if not v else v.pk) for k,v in self.neighbors().items())


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