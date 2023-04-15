from django.urls import include, path
from . import views
from rest_framework import routers

urlpatterns = [
    path('post/', views.DonationPostView.as_view())
]