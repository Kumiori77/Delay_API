from django.db import models

# Create your models here.
class Delay(models.Model):
    title = models.CharField(max_length=100)
    start = models.DateField("date published")
    end = models.DateField("date published")
    number = models.CharField(max_length=50)
    text = models.CharField(max_length=500)
    link = models.CharField(max_length=200)