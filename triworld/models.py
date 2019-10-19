from django.db import models
from django.db.models import F
import json
import random

from . import constants

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
            
    def add_continents(self):
        n = self.major_dim
        sn = self.minor_dim
        world_tris = MajorTri.objects.filter(face__world=self)
        
        #clear database
        world_tris.update(sea=True)
        
        #polar caps and home continent
        polar_cap = world_tris.filter(face__ring=0, ri__lt=n/3) | world_tris.filter(face__ring=3, ri__gte=n*2/3)
        home_continent = world_tris.filter(face__ring=1, face__ring_i=0).exclude(ci__lte=n*2/3-2-2*F('ri')).exclude(ci__gte=n*4/3).exclude(ri__gte=n*2/3)
        """(polar_cap | home_continent).update(sea=False)"""
        
        #establish opposite continents region
        #exclude left edges of polar portions to simplify zoomed in maps (only adjacent polar land major tris are polar caps)
        continent_region = world_tris.filter(face__ring__in=(1,2)).exclude(face__ring=1, face__ring_i=0).exclude(face__ring=2, face__ring_i__in=(0,4))
        continent_region = continent_region | world_tris.filter(face__ring=0, ri__gte=n*2/3).exclude(face__ring_i=0).exclude(ci=0)
        continent_region = continent_region | world_tris.filter(face__ring=3, ri__lt=n/3).exclude(face__ring_i=0).exclude(ci=0)
        
        #pick initial seeds
        seed_region = continent_region.filter(face__ring=1, face__ring_i__in=(2,3)) | continent_region.filter(face__ring=2, face__ring_i__in=(1,3)) #east to west: 2,1  1,2  1,3  2,3
        seeds = seed_region.filter(id__in=random.sample(list(seed_region.values_list('id',flat=True)),k=int(constants.CONTINENT_SEED_RATIO*n*n)))
        """seeds.update(sea=False)"""
        
        #find initial candidates
        candidates = set()
        land = list(seeds.values_list('id',flat=True))
        
        def land_candidates(tri):
            return [nei for nei in tri.neighbors().values() if nei and (nei.id not in land) and (nei in continent_region)]
        
        for t in seeds:
            candidates.update(land_candidates(t))
        
        #expand from seeds
        land_target = int(constants.CONTINENT_LAND_RATIO*n*n)
        while len(land) < land_target:
            new_land = random.choice(list(candidates))
            land.append(new_land.id)
            candidates.remove(new_land)
            candidates.update(land_candidates(new_land))
            
        #update database
        (polar_cap | home_continent | continent_region.filter(id__in=land)).update(sea=False)
        polar_cap.update(ice=True)
        
        #clear MinorTris ("small" tris)
        MinorTri.objects.filter(major_tri__face__world=self).delete()
        
        #add MinorTris
        rows = constants.row_lists(sn)
        for tri in home_continent:
            tpd = tri.tpd()
            MinorTri.objects.bulk_create(MinorTri(major_tri=tri,i=rows[tpd][ri]['r0']+ci,ri=ri,ci=ci) for ri in range(sn) for ci in range(rows[tpd][ri]['rn']))
            
        
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
        self._neigh_left = Face.objects.get(world=self.world, ring=constants.ADJ_RING[r], ring_i=i if r==2 else (i-1)%5)
        self._neigh_right = Face.objects.get(world=self.world, ring=constants.ADJ_RING[r], ring_i=i if r==1 else (i+1)%5)
        self.save()
        
        #update cache for children
        for tri in self.majortri_set.all():
            tri.update_cache()
            
    def neighbor(self,angle):
        if self.fpd():
            if angle==0:
                return self._neigh_top_bot
            if angle==120:
                return self._neigh_left
            if angle==240:
                return self._neigh_right
        else:
            if angle==180:
                return self._neigh_top_bot
            if angle==60:
                return self._neigh_left
            if angle==300:
                return self._neigh_right
        return None
            
    def neighbors(self):
        return {'top_bot':self._neigh_top_bot, 'left':self._neigh_left, 'right':self._neigh_right}
        
    def neighbor_ids(self):
        return dict((k,v.pk) for k,v in self.neighbors().items())

        

class MajorTri(models.Model):
    face = models.ForeignKey('Face', on_delete=models.CASCADE)
    i = models.PositiveSmallIntegerField() #index (in face)
    ri = models.PositiveSmallIntegerField() #row index
    ci = models.PositiveSmallIntegerField() #column index
    sea = models.BooleanField(default=True)
    ice = models.BooleanField(default=False)
    
    neighbors = models.ManyToManyField('self', through='MajorTriNeighbor')
    
    class Meta:
        ordering = ['face','i']
        unique_together = ['face','i']
        indexes = [
            models.Index(fields=['face','i']),
            models.Index(fields=['face']),
        ]
    
    def __str__(self):
        return '{} mj({})'.format(self.face, self.i)
        
    def tpd(self): #assuming fpd is accurate
        return self.face.fpd() != (self.ci%2>0)
            
    def update_cache(self):
        self.majortri_from_set.all().delete()
        
        n = self.face.world.major_dim
        ri,ci,tpd = self.ri, self.ci, self.tpd()
        rows = constants.row_lists(n)
        
        neighbors = []
        for angle in range(0,360,30):
            nei_tpd = tpd
            nei_face = self.face
            nei_ri, nei_ci = constants.MJTRI_NEIGHBORS[angle](ri,ci,tpd)
            if nei_ri < 0:
                nei_face = nei_face.neighbor(0)
                nei_ri += n
                nei_tpd = not nei_tpd
            if nei_ri >= n:
                nei_face = nei_face.neighbor(180)
                nei_ri -= n
                nei_tpd = not nei_tpd
            if nei_face and nei_ci < 0:
                nei_face = nei_face.neighbor(240 if nei_tpd else 300)
                if nei_face:
                    nei_ci += rows[nei_face.fpd()][nei_ri]['rn']
                nei_tpd = not nei_tpd
            if nei_face and nei_ci >= rows[nei_face.fpd()][nei_ri]['rn']:
                nei_ci -= rows[nei_face.fpd()][nei_ri]['rn'] #get tri in current row before updating face
                nei_face = nei_face.neighbor(120 if nei_tpd else 60)
                nei_tpd = not nei_tpd
            try:
                nei = MajorTriNeighbor(from_majortri=self, to_majortri=MajorTri.objects.get(face=nei_face, ri=nei_ri, ci=nei_ci), angle=angle)
                neighbors.append(nei)
            except:
                print('no neighbor for ',self.face,ri,ci,angle,'; tried',nei_face,nei_ri,nei_ci)
            
        MajorTriNeighbor.objects.bulk_create(neighbors)
                
        """
        for angle in range(0,360,30):
            setattr(self, '_neigh_{}'.format(angle), None)
        self._map = ''
        
        n = self.face.world.major_dim
        nei_faces = self.face.neighbors()
        fpd = self.face.fpd()
        tpd = self.tpd()
        ri = self.ri
        ci = self.ci
        
        #calculate neighbors
        for dir,dirdict in constants.TRI_NEIGHBORS.items():
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
            nei_i=constants.i_from_rci(nei_ri,nei_ci,n,nei_face.fpd())
            setattr(self, '_neigh_{}'.format(dirdict['angles'][int(tpd)]), MajorTri.objects.get(face=nei_face, i=nei_i))
            setattr(self, '_neigh_{}'.format(dirdict['angles'][1-int(tpd)]), None)

        self.save()
        """
        
    def neighbors(self):
        #return dict((angle,getattr(self, '_neigh_{}'.format(angle))) for angle in range(0,360,60))
        return dict((nei.angle,nei.to_majortri) for nei in self.majortri_from_set.all())
            
    def neighbor_ids(self):
        return dict((k,None if not v else v.pk) for k,v in self.neighbors().items())
        
        

class MajorTriNeighbor(models.Model):
    from_majortri = models.ForeignKey(MajorTri, on_delete=models.CASCADE, related_name='majortri_from_set')
    to_majortri = models.ForeignKey(MajorTri, on_delete=models.CASCADE, related_name='majortri_to_set')
    angle = models.PositiveSmallIntegerField()


class MinorTri(models.Model):
    major_tri = models.ForeignKey('MajorTri', on_delete=models.CASCADE)
    i = models.PositiveSmallIntegerField()
    ri = models.PositiveSmallIntegerField()
    ci = models.PositiveSmallIntegerField()
    #land_terrain
    #under_terrain
    
    def __str__(self):
        return '{} mn({})'.format(self.major_tri, self.i)
    
    class Meta:
        ordering = ['major_tri','i']
        unique_together = ['major_tri','i']
        indexes = [
            models.Index(fields=['major_tri','i']),
            models.Index(fields=['major_tri','ri','ci']),
            models.Index(fields=['major_tri']),
        ]