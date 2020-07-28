from rest_framework import serializers
from .models import Catalog, Employee, Tag


class TagSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tag
    fields = ['id', 'name', 'items']


class TagsCatalogSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tag
    fields = ['id', 'name']


class EmployeeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Employee
    fields = ['id', 'user', 'phone', 'skype', 'photo']


class CatalogSerializer(serializers.ModelSerializer):
  owner = EmployeeSerializer(many=False)
  tags = TagsCatalogSerializer(many=True)

  class Meta:
    model = Catalog
    fields = ['id', 'title', 'description', 'article', 'file', 'owner', 'tags']
