from django.urls import include, path
from . import views
from rest_framework import routers

urlpatterns = [
    path('home-page/', views.HomePageLayoutView.as_view())
]