from django.db import models

class Route(models.Model):
  first_city = models.CharField(max_length=200)
  second_city = models.CharField(max_length=200)
  path = models.JSONField()
