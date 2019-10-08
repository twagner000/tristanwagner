from django.db import models
from django.db.models import F
import json

ADJ_RING = {0:0, 1:2, 2:1, 3:3}

class World(models.Model):
    #dimensions should be multiples of 3 for evenly distributed start locations
    major_dim = models.PositiveSmallIntegerField(default=6, help_text="Number of major triangles per face edge.")
    minor_dim = models.PositiveSmallIntegerField(default=9, help_text="Number of minor triangles per major triangle edge.")
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        ordering = ['-date_created']
        
    def __str__(self):
        return 'w{}'.format(self.pk)
        
        
class Face(models.Model):
    world = models.ForeignKey('World', on_delete=models.CASCADE)
    face_ring = models.PositiveSmallIntegerField()
    face_index = models.PositiveSmallIntegerField()
    
    #cached fields (neighbor names are accurate if current face points down)
    _neigh_top = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, related_name='face_top_set')
    _neigh_left = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, related_name='face_left_set')
    _neigh_right = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, related_name='face_right_set')
    _map = models.TextField(blank=True)
    
    class Meta:
        ordering = ['world','face_ring','face_index']
        unique_together = ['world','face_ring','face_index']
        indexes = [
            models.Index(fields=['world','face_ring','face_index']),
            models.Index(fields=['world']),
        ]
    
    def __str__(self):
        return '{} f({},{})'.format(self.world, self.face_ring, self.face_index)
        
    def points_down(self):
        return self.face_ring%2 > 0
        
    def neighbors(self):
        if not self._neigh_top or not self._neigh_left or not self._neigh_right:
            r = self.face_ring
            i = self.face_index
            self._neigh_top = Face.objects.get(world=self.world, face_ring=r+1-2*(r%2), face_index=i)
            self._neigh_left = Face.objects.get(world=self.world, face_ring=ADJ_RING[r], face_index=(i+1-2*(r%2))%5)
            self._neigh_right = Face.objects.get(world=self.world, face_ring=ADJ_RING[r], face_index=i if r%3 else (i-1+2*(r%2))%5)
            self.save()
        return {'top':self._neigh_top, 'left':self._neigh_left, 'right':self._neigh_right}
            
    def neighbor_ids(self):
        return dict((k,v.pk) for k,v in self.neighbors().items())
        
    def map(self):
        return None if not self._map else json.loads(self._map)
        
    def generate_map(self):
        n = self.world.major_dim
        tris = dict((k,v.majortri_set) for k,v in self.neighbors().items())
        tris['center'] = self.majortri_set
        if self.face_ring in (0,3): #polar
            tris['left'] = tris['left'].annotate(r2=F('major_col')/2, c2=2*F('major_row') + F('major_col')%2).order_by('r2','c2')
            tris['right'] = tris['right'].annotate(r2=F('major_row')+(F('major_col')+1)/2, c2=F('major_col')).order_by('r2','c2')
        else:
            tris['left'] = tris['left'].annotate(r2=F('major_row'), c2=F('major_col')).reverse()
            tris['right'] = tris['right'].annotate(r2=F('major_row'), c2=F('major_col')).reverse()
            
        if self.points_down():
            tris['top'] = tris['top'].reverse()
        else:
            tris['center'] = tris['center'].reverse()
            tris['left'] = tris['left'].reverse()
            tris['right'] = tris['right'].reverse()
        
        map = []
        reverse_if_points_up = lambda x: x if self.points_down() else reversed(x)
        for ri in reverse_if_points_up(range(-n//3,n)):
            if ri<0:
                row = list(tris['top'].filter(major_row=-1-ri))
            else:
                if self.face_ring == 0:
                    row = list(tris['right'].filter(r2=ri, c2__lt=n*2//3))
                    row += list(tris['center'].filter(major_row=ri))
                    row += list(tris['left'].filter(r2=n-1-ri, c2__gt=2*(ri-n//3)))
                elif self.face_ring == 1:
                    row = list(tris['left'].filter(r2=n-1-ri, c2__lt=n*2//3))
                    row += list(tris['center'].filter(major_row=ri))
                    row += list(tris['right'].filter(r2=n-1-ri, c2__gt=2*(ri-n//3)))
                elif self.face_ring == 2:
                    row = list(tris['right'].filter(r2=n-1-ri, c2__gt=2*(ri-n//3)))
                    row += list(tris['center'].filter(major_row=ri))
                    row += list(tris['left'].filter(r2=n-1-ri, c2__lt=n*2//3))
                elif self.face_ring == 3:
                    row = list(tris['left'].filter(r2=n-1-ri, c2__gt=2*(ri-n//3)))
                    row += list(tris['center'].filter(major_row=ri))
                    row += list(tris['right'].filter(r2=ri, c2__lt=n*2//3))
            map.append(row)
        
        return map
        

class MajorTri(models.Model):
    face = models.ForeignKey('Face', on_delete=models.CASCADE)
    major_row = models.PositiveSmallIntegerField()
    major_col = models.PositiveSmallIntegerField()
    sea = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['face','major_row','major_col']
        unique_together = ['face','major_row','major_col']
        indexes = [
            models.Index(fields=['face','major_row','major_col']),
            models.Index(fields=['face']),
        ]
    
    def __str__(self):
        return '{} mj({},{})'.format(self.face, self.major_row, self.major_col)
        
    def get_r2_left(self):
        return self.major_col//2
        
    def get_r2_right(self):
        return self.major_row + (self.major_col+1)//2


class MinorTri(models.Model):
    major_tri = models.ForeignKey('MajorTri', on_delete=models.CASCADE)
    minor_row = models.PositiveSmallIntegerField()
    minor_col = models.PositiveSmallIntegerField()
    #land_terrain
    #under_terrain
    
    def __str__(self):
        return '{} mn({},{})'.format(self.majortri, self.minor_row, self.minor_col)
    
    class Meta:
        ordering = ['major_tri','minor_row','minor_col']
        unique_together = ['major_tri','minor_row','minor_col']
        indexes = [
            models.Index(fields=['major_tri','minor_row','minor_col']),
            models.Index(fields=['major_tri']),
        ]