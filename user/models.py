from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

class College(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    ranking = models.IntegerField()
    tuition_fee = models.FloatField()
    programs = models.TextField()  # Comma-separated list of programs
    scholarships = models.BooleanField(default=False)
    link = models.URLField(null=True, blank=True)


    

    def __str__(self):
        return self.name
    
class blog(models.Model):
    title = models.CharField(max_length=100)
    detail = models.CharField(max_length=1000000000000)
    created_at = models.DateTimeField(default=datetime.now,blank=True)




