from django.db import models
import json

ADJ_RING = {0:0, 1:2, 2:1, 3:3}

class World(models.Model):
    #dimensions should be multiples of 3 for evenly distributed start locations
    major_dim = models.PositiveSmallIntegerField(default=6, help_text="Number of major triangles per face edge.")
    minor_dim = models.PositiveSmallIntegerField(default=6, help_text="Number of minor triangles per major triangle edge.")
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
            self._neigh_right = Face.objects.get(world=self.world, face_ring=ADJ_RING[r], face_index=(i-1+2*(r%2))%5)
            self.save()
        return {'top':self._neigh_top, 'left':self._neigh_left, 'right':self._neigh_right}
            
    def neighbor_ids(self):
        return dict((k,v.pk) for k,v in self.neighbors().items())
        
    def map(self):
        if not self._map:
            n = self.world.major_dim
            tris = dict((k,v.majortri_set) for k,v in self.neighbors().items())
            tris['center'] = self.majortri_set
            
            map = []
            reverse_if_points_up = lambda x: x if self.points_down() else reversed(x)
            for ri in reverse_if_points_up(range(-n//3,n)):
                if ri<0:
                    row = list(reversed(tris['top'].filter(major_row=-1-ri)))
                else:
                    row = list(reversed(tris['left'].filter(major_row=n-1-ri, major_col__lt=n*2//3)))
                    row += list(tris['center'].filter(major_row=ri))
                    row += list(reversed(tris['right'].filter(major_row=n-1-ri, major_col__gt=2*(ri-n//3))))
                row = [tri.dict_for_static() for tri in reverse_if_points_up(row)]
                map.append(row)
                
            self._map = json.dumps(map)
            self.save()
        return json.loads(self._map)
        

class MajorTri(models.Model):
    face = models.ForeignKey('Face', on_delete=models.CASCADE)
    major_row = models.PositiveSmallIntegerField()
    major_col = models.PositiveSmallIntegerField()
    sea = models.BooleanField(default=True)
    
    serializer_fields = ('id', 'major_row', 'major_col', 'sea')
    serializer_method_fields = tuple()
    
    class Meta:
        ordering = ['face','major_row','major_col']
        unique_together = ['face','major_row','major_col']
        indexes = [
            models.Index(fields=['face','major_row','major_col']),
            models.Index(fields=['face']),
        ]
    
    def __str__(self):
        return '{} mj({},{})'.format(self.face, self.major_row, self.major_col)
    
    def points_down(self):
        return self.face.face_ring%2 != self.major_col%2
        
    def dict_for_static(self):
        return dict((k, getattr(self,k)() if k in self.serializer_method_fields else getattr(self,k)) for k in self.serializer_fields)
    

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