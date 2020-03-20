from django.db import models

# Create your models here.

class urls(models.Model):
    url = models.CharField(max_length=150)

class words_count(models.Model):
    fromurl = models.CharField(max_length=150)
    words = models.CharField(max_length=30)
    count = models.IntegerField()