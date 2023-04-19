from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.DonationPostListView.as_view()),
    path('all/', views.DonationPostView.as_view()),
    path('new/', views.DonationPostCreateView.as_view()),
    path('donate/', views.DonateView.as_view())
]