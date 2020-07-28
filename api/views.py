# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets
from .models import Catalog, Tag
from .serializers import CatalogSerializer, TagSerializer
from rest_framework.authentication import TokenAuthentication


class CatalogViewSet(viewsets.ModelViewSet):
  serializer_class = CatalogSerializer
  queryset = Catalog.objects.all()
  authentication_classes = (TokenAuthentication, )


class TagsViewSet(viewsets.ModelViewSet):
  serializer_class = TagSerializer
  queryset = Tag.objects.all()
  authentication_classes = (TokenAuthentication, )

