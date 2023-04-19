from django.urls import include, path
from . import views
from rest_framework import routers

urlpatterns = [
    path('list/', views.DonationPostListView.as_view()),
    path('all/', views.DonationPostView.as_view()),
    path('new/', views.DonationPostCreateView.as_view())
]