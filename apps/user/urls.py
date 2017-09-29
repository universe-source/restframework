from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from .views import PersonViewSet, GroupViewSet


router = routers.DefaultRouter()
router.register(r'users', PersonViewSet)
router.register(r'groups', GroupViewSet)


urlpatterns = [
    url(r'^', include(router.urls), name='user'),
]
