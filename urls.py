"""restframework URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
try:
    from swagger_schema import get_swagger_view
except ImportError:
    from rest_framework_swagger.views import get_swagger_view


# url用于设置swagger上的所有接口的前缀 URL, 默认为空, 另外 BASE URL 显示不正常
#  schema_views = get_swagger_view(title='Shop API', url='/swagger/')
schema_views = get_swagger_view(title='Shop API')

urlpatterns = [
    # django 自带的用户管理后台
    url(r'^admin/', admin.site.urls),
    # REST Framework自带的API 后台
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # swagger
    url(r'^swagger/', schema_views),
    # 用户
    url(r'^', include('apps.user.urls')),
]
