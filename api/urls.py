"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import CatalogViewSet, TagsViewSet, FilesViewSet, UserViewSet, CountryViewSet, PersonViewSet, PreviewsViewSet

router = routers.DefaultRouter()
router.register('catalog', CatalogViewSet)
router.register('tags', TagsViewSet)
router.register('previews', PreviewsViewSet)
router.register('files', FilesViewSet)
router.register('users', UserViewSet)
router.register('countries', CountryViewSet)
router.register('person', PersonViewSet)

urlpatterns = [
  path('', include(router.urls))
]
