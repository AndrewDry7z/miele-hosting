# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets
from .models import Catalog, Tag, File, Countries, Person
from .serializers import CatalogSerializer, TagSerializer, FilesSerializer, UserSerializer, CountrySerializer, PersonSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User


class CatalogViewSet(viewsets.ModelViewSet):
  serializer_class = CatalogSerializer
  queryset = Catalog.objects.all()
  authentication_classes = (TokenAuthentication, )


class UserViewSet(viewsets.ModelViewSet):
  serializer_class = UserSerializer
  queryset = User.objects.all()
  permission_classes = (AllowAny,)


class TagsViewSet(viewsets.ModelViewSet):
  serializer_class = TagSerializer
  queryset = Tag.objects.all()
  authentication_classes = (TokenAuthentication, )


class EmployeeViewSet(viewsets.ModelViewSet):
  serializer_class = PersonSerializer
  queryset = Person.objects.all()
  authentication_classes = (TokenAuthentication, )


class FilesViewSet(viewsets.ModelViewSet):
  serializer_class = FilesSerializer
  queryset = File.objects.all()
  authentication_classes = (TokenAuthentication,)


class CountryViewSet(viewsets.ModelViewSet):
  serializer_class = CountrySerializer
  queryset = Countries.objects.all()
  authentication_classes = (TokenAuthentication,)
