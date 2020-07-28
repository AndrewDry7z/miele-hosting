# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  phone = models.CharField(max_length=15, blank=True)
  skype = models.CharField(max_length=100, blank=True)
  photo = models.FileField(upload_to='media/users/', blank=False, default=None)


class Catalog(models.Model):
  title = models.CharField(max_length=200, unique=True)
  description = models.TextField(blank=True)
  article = models.CharField(max_length=40, blank=True)
  file = models.FileField(upload_to='media/%Y/%m/%d/', blank=False, default=None)
  owner = models.OneToOneField(Employee, blank=True, null=True, default=None, on_delete=models.SET('Removed User'))

  def __str__(self):
    return self.title


class Tag(models.Model):
  name = models.CharField(max_length=140)
  items = models.ManyToManyField(Catalog, related_name='tags')

  def __str__(self):
    return self.name
