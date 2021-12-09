from django.db import models

class Route(models.Model):
  id = models.AutoField(primary_key=True)
  first_city = models.CharField(max_length=200)
  second_city = models.CharField(max_length=200)
  priority = models.CharField(max_length=200)
  path = models.JSONField()

class City(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=200)
  point_x = models.FloatField()
  point_y = models.FloatField()

class Relation(models.Model):
  id = models.AutoField(primary_key=True)
  first_city = models.ForeignKey(
    'City',
    on_delete=models.CASCADE,
    related_name='first_city'
  )
  second_city = models.ForeignKey(
    'City',
    on_delete=models.CASCADE,
    related_name='second_city'
  )

class PropsRelation(models.Model):
  id = models.AutoField(primary_key=True)
  relation_type = models.CharField(max_length=200)
  time = models.IntegerField()
  cost = models.FloatField()
  schedule = models.JSONField(default='null')
  relation = models.ForeignKey(
    'Relation',
    on_delete=models.CASCADE
  )


class RouteDebug(models.Model):
  id = models.AutoField(primary_key=True)
  first_city = models.CharField(max_length=200)
  second_city = models.CharField(max_length=200)
  path = models.JSONField()

class CityDebug(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=200)
  point_x = models.FloatField()
  point_y = models.FloatField()

class RelationDebug(models.Model):
  id = models.AutoField(primary_key=True)
  first_city = models.ForeignKey(
    'CityDebug',
    on_delete=models.CASCADE,
    related_name='first_city'
  )
  second_city = models.ForeignKey(
    'CityDebug',
    on_delete=models.CASCADE,
    related_name='second_city'
  )

class PropsRelationDebug(models.Model):
  id = models.AutoField(primary_key=True)
  relation_type = models.CharField(max_length=200)
  time = models.IntegerField()
  cost = models.FloatField()
  schedule = models.JSONField(default='null')
  relation = models.ForeignKey(
    'RelationDebug',
    on_delete=models.CASCADE
  )
