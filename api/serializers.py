from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from .models import Catalog, Person, Tag, File, Countries
from django.contrib.auth.models import User


class TagSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tag
    fields = ['id', 'name', 'catalog_items']


class TagsCatalogSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tag
    fields = ['id', 'name']


class FilesSerializer(serializers.ModelSerializer):
  class Meta:
    model = File
    fields = ['id', 'name', 'file', 'catalog_item']


class CountrySerializer(serializers.ModelSerializer):
  class Meta:
    model = Countries
    fields = ['id', 'countryname', 'code', 'flag']


class PersonSerializer(serializers.ModelSerializer):
  class Meta:
    model = Person
    fields = ['phone', 'skype', 'photo', 'country']


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

  class Meta:
    model = Catalog
    fields = ['id', 'title', 'description', 'article', 'owner', 'tags', 'files']
