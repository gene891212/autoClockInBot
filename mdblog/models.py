from django.db import models
from django.urls import reverse

# Create your models here.
class Disease(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    
    def get_absolute_url(self):
        return reverse('disease', args=[str(self.title)])

    def __str__(self):
        return self.title

