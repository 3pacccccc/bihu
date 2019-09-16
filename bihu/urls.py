"""bihu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve

from bihu.settings import MEDIA_ROOT, STATIC_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'accounts/', include('allauth.urls')),  # 第三方登陆url
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),  # 配置url里面文件的上传
    url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),  # 配置url里面文件的上传
    path('markdownx/', include('markdownx.urls')),

    # APP下的路由
    path('users/', include('users.urls', namespace='users')),
    path('news/', include('news.urls', namespace='news')),
    path('articles/', include('articles.urls', namespace='articles')),
]
