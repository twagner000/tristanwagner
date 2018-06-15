from django.db import models
from django.utils import timezone
from django.template import Template, Context

class Puzzle(models.Model):
    def puzzle_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/puzzles/<slug>/<filename>
        return 'puzzles/{0}/{1}'.format(instance.slug, filename)
        
    author = models.ForeignKey('auth.User', models.PROTECT)
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    solution = models.CharField(max_length=50)
    puzzle_template = models.TextField()
    fail_template = models.TextField()
    success_template = models.TextField()
    puzzle_file = models.FileField(upload_to=puzzle_path, blank=True)
    success_image = models.ImageField(upload_to=puzzle_path, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    release_date = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.title
        
    def puzzle_html(self):
        return Template(self.puzzle_template).render(Context({'puzzle':self}))
        
    def fail_html(self):
        return Template(self.fail_template).render(Context({'puzzle':self}))
        
    def success_html(self):
        return Template(self.success_template).render(Context({'puzzle':self}))

    