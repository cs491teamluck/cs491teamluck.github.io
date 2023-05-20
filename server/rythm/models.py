from django.db import models

# Create your models here.
class User(models.Model):
    userid = models.CharField(max_length=11, primary_key=True)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


