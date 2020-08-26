# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Catalog, Tag, File, Countries, Person, Preview
from .serializers import CatalogSerializer, TagSerializer, FilesSerializer, UserSerializer, CountrySerializer, \
  PreviewsSerializer, PersonSerializer

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.decorators import action


class CatalogViewSet(viewsets.ModelViewSet):
  serializer_class = CatalogSerializer
  queryset = Catalog.objects.all()
  authentication_classes = (TokenAuthentication,)


class UserViewSet(viewsets.ModelViewSet):
  serializer_class = UserSerializer
  queryset = User.objects.all()
  # permission_classes = (AllowAny,)
  authentication_classes = (TokenAuthentication,)


class TagsViewSet(viewsets.ModelViewSet):
  serializer_class = TagSerializer
  queryset = Tag.objects.all()
  authentication_classes = (TokenAuthentication,)


class PersonViewSet(viewsets.ModelViewSet):
  serializer_class = PersonSerializer
  queryset = Person.objects.all()
  authentication_classes = (TokenAuthentication,)

  @action(detail=True, methods=['put'])
  def person(self, request, pk=None):
    user = self.get_object()
    person = user.person
    serializer = UserSerializer(person, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FilesViewSet(viewsets.ModelViewSet):
  serializer_class = FilesSerializer
  queryset = File.objects.all()
  authentication_classes = (TokenAuthentication,)


class PreviewsViewSet(viewsets.ModelViewSet):
  serializer_class = PreviewsSerializer
  queryset = Preview.objects.all()
  authentication_classes = (TokenAuthentication,)


class CountryViewSet(viewsets.ModelViewSet):
  serializer_class = CountrySerializer
  queryset = Countries.objects.all()
  authentication_classes = (TokenAuthentication,)


class GetAuthToken(ObtainAuthToken):
  def post(self, request, *args, **kwargs):
    response = super(GetAuthToken, self).post(request, *args, **kwargs)
    token = Token.objects.get(key=response.data['token'])
    user = User.objects.get(id=token.user_id)
    user_serializer = UserSerializer(user, many=False)
    return Response({'token': token.key, 'user': user_serializer.data})
