# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Catalog, Person, Tag, File, Countries
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
  list_display = ['title', 'article']
  search_fields = ['title']


admin.site.register(Tag)
admin.site.register(File)
admin.site.register(Countries)
admin.site.register(Person)

