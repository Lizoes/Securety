from django.db import models

# Create your models here.


class Loginer(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    create_time = models.DateTimeField(auto_now_add=True)

