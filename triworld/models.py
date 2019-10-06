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
            
            
class FaceExt(models.Model):
    face = models.OneToOneField('Face', primary_key=True, on_delete=models.CASCADE)
    points_down = models.BooleanField(default=None)
    
    #for json_data, use json.dumps(pyvar) or pyvar = json.loads(self.json_data)
    neighbor_ids = models.TextField(default='null')
    map = models.TextField(default='null')
    
    class Meta:
        ordering = ['face']
        indexes = [models.Index(fields=['face']),]
    
    def refresh(self):
        self.points_down = self.face.points_down()
    
        #populate neighbor_ids
        r = self.face.face_ring
        i = self.face.face_index
        horiz = Face.objects.get(world=self.face.world, face_ring=r+1-2*(r%2), face_index=i)
        horiz_counterclock = Face.objects.get(world=self.face.world, face_ring=ADJ_RING[r], face_index=(i+1-2*(r%2))%5)
        horiz_clockwise = Face.objects.get(world=self.face.world, face_ring=ADJ_RING[r], face_index=(i-1+2*(r%2))%5)
        if r%2:
            self.neighbor_ids = json.dumps([horiz.pk, None, horiz_clockwise.pk, None, horiz_counterclock.pk, None])
        else:
            self.neighbor_ids = json.dumps([None, horiz_counterclock.pk, None, horiz.pk, None, horiz_clockwise.pk])
            
        #populate map (tri names are accurate if center face points down)
        n = self.face.world.major_dim
        center_tri = self.face.majortri_set
        top_tri = horiz.majortri_set
        left_tri = horiz_counterclock.majortri_set
        right_tri = horiz_clockwise.majortri_set
        
        map = []
        reverse_if_points_up = lambda x: x if self.points_down else reversed(x)
        for ri in reverse_if_points_up(range(-n//3,n)):
            if ri<0:
                row = list(reversed(top_tri.filter(major_row=-1-ri)))
            else:
                row = list(reversed(left_tri.filter(major_row=n-1-ri, major_col__lt=n*2//3)))
                print(type(row))
                row += list(center_tri.filter(major_row=ri))
                row += list(reversed(right_tri.filter(major_row=n-1-ri, major_col__gt=2*(ri-n//3))))
            row = [tri.dict_for_static() for tri in reverse_if_points_up(row)]
            map.append(row)
            
        self.map = json.dumps(map)
        
        return self
        

class MajorTri(models.Model):
    face = models.ForeignKey('Face', on_delete=models.CASCADE)
    major_row = models.PositiveSmallIntegerField()
    major_col = models.PositiveSmallIntegerField()
    sea = models.BooleanField(default=True)
    
    serializer_fields = ('id', 'major_row', 'major_col', 'sea', 'points_down')
    serializer_method_fields = ('points_down', )
    
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