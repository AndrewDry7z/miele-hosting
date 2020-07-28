from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Catalog, Employee, Tag, File
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


class EmployeeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Employee
    fields = ['id', 'user', 'phone', 'skype', 'photo']


class CatalogSerializer(serializers.ModelSerializer):
  owner = EmployeeSerializer(many=False)
  tags = TagsCatalogSerializer(many=True)
  files = FilesSerializer(many=True)

  class Meta:
    model = Catalog
    fields = ['id', 'title', 'description', 'article', 'owner', 'tags', 'files']


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username', 'password']
    extra_kwargs = {'password': {'write_only': True, 'required': True}}

  def create(self, validated_data):
    user = User.objects.create_user(**validated_data)
    Token.objects.create(user=user)
    return user
