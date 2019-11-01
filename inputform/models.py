from django.db import models

# Create your models here.

class UserForm(models.Model):
    email = models.EmailField(max_length=40)
    file = models.FileField(upload_to='uploads/%Y/%m/%d/', null=True, blank=True)
    quarter = models.CharField(max_length=1)
    students_ids = models.CharField(max_length=100)
    students_names = models.CharField(max_length=100)
    subject = models.CharField(max_length=40)
    year = models.CharField(max_length=4)
