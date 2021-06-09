from django.urls import path

from . import views

urlpatterns = [
    path('', views.ads_list, name='ads_list')
]
