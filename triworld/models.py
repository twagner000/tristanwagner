from django.db import models

ADJ_RING = {0:0, 1:2, 2:1, 3:3}

class World(models.Model):
    #dimensions should be multiples of 3 for evenly distributed start locations
    major_dim = models.PositiveSmallIntegerField(default=6, editable=False, help_text="Number of major triangles per face edge.")
    minor_dim = models.PositiveSmallIntegerField(default=6, editable=False, help_text="Number of minor triangles per major triangle edge.")
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        ordering = ['-date_created']
        
    def __str__(self):
        return 'w{}'.format(self.pk)
        
        
class Face(models.Model):
    world = models.ForeignKey('World', on_delete=models.CASCADE, editable=False)
    face_ring = models.PositiveSmallIntegerField(editable=False)
    face_index = models.PositiveSmallIntegerField(editable=False)
    
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
        
    def adj_faces(self):
        r = self.face_ring
        i = self.face_index
        horiz = Face.objects.get(world=self.world, face_ring=r+1-2*(r%2), face_index=i)
        horiz_counterclock = Face.objects.get(world=self.world, face_ring=ADJ_RING[r], face_index=(i+1-2*(r%2))%5)
        horiz_clockwise = Face.objects.get(world=self.world, face_ring=ADJ_RING[r], face_index=(i-1+2*(r%2))%5)
        if r%2:
            return [horiz, None, horiz_clockwise, None, horiz_counterclock, None]
        else:
            return [None, horiz_counterclock, None, horiz, None, horiz_clockwise]
        

class MajorTri(models.Model):
    face = models.ForeignKey('Face', on_delete=models.CASCADE, editable=False)
    major_row = models.PositiveSmallIntegerField(editable=False)
    major_col = models.PositiveSmallIntegerField(editable=False)
    sea = models.BooleanField(default=True, editable=False)
    
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
    

class MinorTri(models.Model):
    major_tri = models.ForeignKey('MajorTri', on_delete=models.CASCADE)
    minor_row = models.PositiveSmallIntegerField(editable=False)
    minor_col = models.PositiveSmallIntegerField(editable=False)
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