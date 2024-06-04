from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.DonationPostListView.as_view()),
    path('all/', views.DonationPostView.as_view()),
    path('new/', views.DonationPostCreateView.as_view()),
    path('donate/', views.DonateView.as_view()),
    path('payment/success/', views.PaymentSuccessView.as_view(), name='success'),
    path('payment/cancel/', views.PaymentCancelView.as_view(), name='cancel'),
]