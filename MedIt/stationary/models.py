from django.db import models

class Stationary(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()