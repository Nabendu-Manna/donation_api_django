from django.urls import include, path
from . import views
from rest_framework import routers

urlpatterns = [
    path('list/', views.DonationPostListView.as_view()),
    path('post/', views.DonationPostView.as_view()),
    path('post/new', views.DonationPostCreateView.as_view())
]