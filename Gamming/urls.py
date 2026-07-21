"""
URL configuration for Gamming project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from Gamming import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('browse/',views.browse),
    path('details/',views.details),
    path('streams/',views.streams),
    path('profile/',views.profile),
    path('login/',views.login),
    path('registration/',views.sign,name='registration'),
    path('adminmain/',views.adminmain),
    path('user/',views.user),
    path('userlist/',views.list),
    path('trending/',views.trending),
    path('gamelist/',views.gamelist),
    path('addgame/',views.addgame),
    path('del/',views.delete),


]
