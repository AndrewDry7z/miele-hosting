# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Catalog, Employee, Tag
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
  list_display = ['title', 'article']
  search_fields = ['title']


class EmployeeInline(admin.StackedInline):
  model = Employee
  can_delete = False
  verbose_name_plural = 'employee'


class UserAdmin(BaseUserAdmin):
  inlines = (EmployeeInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Tag)

