from django.conf.urls import url, include
from rest_framework import routers

from .apis import PersonViewSet, GroupViewSet


router = routers.DefaultRouter()
router.register(r'users', PersonViewSet)
router.register(r'groups', GroupViewSet)


urlpatterns = [
    url(r'^', include(router.urls), name='user'),
]
