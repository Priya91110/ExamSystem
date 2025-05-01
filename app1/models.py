from django.db import models
# Create your models here.
# models.py
from django.db import models

class Student(models.Model):
    enrollment_number = models.CharField(max_length=15, unique=True)
    dob = models.DateField()
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
