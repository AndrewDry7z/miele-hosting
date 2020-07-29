# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from .validators import validate_svg


class Countries(models.Model):
  countryname = models.CharField(max_length=100)
  code = models.CharField(max_length=3)
  flag = models.FileField(upload_to='media/flags/', validators=[validate_svg])

  def __str__(self):
    return self.countryname


class Employee(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
  phone = models.CharField(max_length=15, blank=True)
  skype = models.CharField(max_length=100, blank=True)
  photo = models.FileField(upload_to='media/users/', blank=False, default=None)
  country = models.ForeignKey(Countries, default=None, on_delete=models.SET('DELETED'))

  def __str__(self):
    name = f"{self.user.first_name} {self.user.last_name}"
    return name

class Catalog(models.Model):
  title = models.CharField(max_length=200, unique=True)
  description = models.TextField(blank=True)
  article = models.CharField(max_length=40, blank=True)
  owner = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.SET('Removed User'))

  def __str__(self):
    return self.title


class Tag(models.Model):
  name = models.CharField(max_length=140)
  catalog_items = models.ManyToManyField(Catalog, related_name='tags')

  def __str__(self):
    return self.name


class File(models.Model):
  name = models.CharField(max_length=140)
  file = models.FileField(upload_to='media/%Y/%m/%d/', blank=False, default=None)
  catalog_item = models.ForeignKey(Catalog, related_name='files', on_delete=models.CASCADE)

  def __str__(self):
    return self.name
