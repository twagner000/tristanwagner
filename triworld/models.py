from django.db import models

class World(models.Model):
    major_dim = models.PositiveSmallIntegerField(default=6, editable=False, help_text="Number of major triangles per face edge.")
    minor_dim = models.PositiveSmallIntegerField(default=6, editable=False, help_text="Number of minor triangles per major triangle edge.")
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        ordering = ['-date_created']
        
        
class MajorTri(models.Model):
    world = models.ForeignKey('World', on_delete=models.CASCADE, editable=False)
    face_ring = models.PositiveSmallIntegerField(editable=False)
    face_index = models.PositiveSmallIntegerField(editable=False)
    major_row = models.PositiveSmallIntegerField(editable=False)
    major_col = models.PositiveSmallIntegerField(editable=False)
    sea = models.BooleanField(default=True, editable=False)
    
    def __str__(self):
        return 'w{} f{},{} mj({},{})'.format(self.world.pk, self.face_ring, self.face_index, self.major_row, self.major_col)
    
    class Meta:
        ordering = ['world','face_ring','face_index','major_row','major_col']
        unique_together = ['world','face_ring','face_index','major_row','major_col']
        indexes = [
            models.Index(fields=['world','face_ring','face_index','major_row','major_col']),
            models.Index(fields=['world','face_ring','face_index']),
            models.Index(fields=['world']),
        ]
    
    
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