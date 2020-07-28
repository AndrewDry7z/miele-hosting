# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets
from .models import Catalog, Tag, File
from .serializers import CatalogSerializer, TagSerializer, FilesSerializer, UserSerializer
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User


class CatalogViewSet(viewsets.ModelViewSet):
  serializer_class = CatalogSerializer
  queryset = Catalog.objects.all()
  authentication_classes = (TokenAuthentication, )


class UserViewSet(viewsets.ModelViewSet):
  serializer_class = UserSerializer
  queryset = User.objects.all()
  authentication_classes = (TokenAuthentication,)


class TagsViewSet(viewsets.ModelViewSet):
  serializer_class = TagSerializer
  queryset = Tag.objects.all()
  authentication_classes = (TokenAuthentication, )

class FilesViewSet(viewsets.ModelViewSet):
  serializer_class = FilesSerializer
  queryset = File.objects.all()
  authentication_classes = (TokenAuthentication,)
