"""webskripsi.film URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, re_path

from . import views
app_name = 'film'

urlpatterns = [
	path('search/', views.carifilm, name="cari"),
    path('tfidf/', views.pptfidf, name="pptfidf"),
    path('history/', views.pptfidf, name="history"),
    re_path(r'^detail/(?P<sluginput>[\w-]+)/$', views.detailfilm, name="details"),
    path('', views.index, name="index"),
]
