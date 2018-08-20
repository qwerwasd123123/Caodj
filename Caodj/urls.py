"""Caodj URL Configuration

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
from django.contrib import admin
from django.urls import path
from app01 import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index.html/',views.index),
    path('get_imgs.html/', views.get_imgs),
    path('blog/',views.blog.yy),
    path('login/',views.login),
    path('register/',views.register),
    # path('blog/login.html/',views.login),
    # path('blog/register.html/',views.register),
    # path('blog/home/',views.blog.home),
    # path('blog/new/',views.blog.new),
    # path('blog/good/',views.blog.good),
]
