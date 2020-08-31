from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from .models import Catalog, Person, Tag, File, Countries, Preview
from django.contrib.auth.models import User
import os
from core import settings



class TagSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tag
    fields = ['id', 'name', 'catalog_items']


class TagsCatalogSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tag
    fields = ['id', 'name']


class FilesSerializer(serializers.ModelSerializer):
  file_size = serializers.SerializerMethodField()
  title = serializers.SerializerMethodField()

  class Meta:
    model = File
    fields = ['id', 'name', 'title', 'file', 'file_size', 'catalog_item']

  def get_file_size(self, obj):
    return os.path.getsize(settings.BASE_DIR + obj.file.url)

  def get_title(self, obj):
    return os.path.basename(settings.BASE_DIR + obj.file.url)


class PreviewsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Preview
    fields = ['id', 'name', 'image', 'catalog_item']


class CountrySerializer(serializers.ModelSerializer):
  class Meta:
    model = Countries
    fields = ['id', 'countryname', 'code', 'flag']


class PersonSerializer(serializers.ModelSerializer):
  class Meta:
    model = Person
    fields = ['id', 'phone', 'skype', 'photo', 'country']


class UserSerializer(serializers.ModelSerializer):
  person = PersonSerializer(many=False)

  def create(self, validated_data):
    person_data = validated_data.pop('person')
    user = User.objects.create(
      **validated_data
    )
    user.set_password(user.password)
    user.save()
    Person.objects.create(user=user, **person_data)
    return user

  class Meta:
    model = User
    fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'person']
    extra_kwargs = {'password': {'write_only': True, 'required': True}}


class CatalogSerializer(serializers.ModelSerializer):
  owner = PersonSerializer(many=False)
  tags = TagsCatalogSerializer(many=True)
  files = FilesSerializer(many=True)
  previews = PreviewsSerializer(many=True)

  class Meta:
    model = Catalog
    fields = ['id', 'title', 'description', 'article', 'owner', 'tags', 'files', 'previews']
